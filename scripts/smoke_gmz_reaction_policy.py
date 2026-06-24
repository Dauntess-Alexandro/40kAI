"""Smoke: реальный короткий GMZ-selfplay локально — проверка install умных реакций.

Task 4 плана 2026-06-24-muzero-smart-stratagem-reactions.md.

Прогоняет play_episode_with_gumbel_muzero с настоящим env (gym.make 40kAI-v0) и настоящей
сетью GumbelMuZeroNet + GumbelMuZeroSearch (локально, без remote-IS). Перехватывает лог
install и проверяет:
  1) флаг ВКЛ (дефолт) → в логе есть "[GMZ][REACTION] reaction_value_policy=ON", эпизод без падений;
  2) флаг ВЫКЛ (GMZ_REACTION_VALUE_POLICY=0) → строки =ON нет, эпизод проходит (legacy-реакции).

Запуск:
  python scripts/smoke_gmz_reaction_policy.py
"""
from __future__ import annotations

import io
import os
import sys
from contextlib import redirect_stdout

# Локальный режим: remote-IS точно выключен.
os.environ.pop("GMZ_INFERENCE_SERVER", None)

import core.envs  # noqa: E402, F401 — регистрация '40kAI-v0'
import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

from core.engine.mission import deploy_for_mission, post_deploy_setup  # noqa: E402
from core.envs.warhamEnv import roll_off_attacker_defender  # noqa: E402
from core.models.gumbel_muzero_model import GumbelMuZeroNet  # noqa: E402
from core.models.gumbel_muzero_search import (  # noqa: E402
    GumbelMuZeroSearch,
    GumbelMuZeroSearchConfig,
)
from core.models.gumbel_muzero_selfplay import (  # noqa: E402
    GumbelSelfPlayConfig,
    play_episode_with_gumbel_muzero,
)
from train import (  # noqa: E402
    DEFAULT_MISSION_NAME,
    _build_units_from_config,
    _load_roster_config,
    action_sizes_from_env,
    normalize_mission_name,
)


def _build_env_and_search():
    """Собрать минимальный env + net + search (как actor-entry в train.py)."""
    roster = _load_roster_config()
    b_len = int(roster["b_len"])
    b_hei = int(roster["b_hei"])
    enemy, model = _build_units_from_config(roster, b_len, b_hei)
    mission_name = normalize_mission_name(roster.get("mission", DEFAULT_MISSION_NAME))

    env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
    env_u = env.unwrapped

    # deploy (как в actor-entry)
    attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
    deploy_for_mission(
        mission_name,
        model_units=model,
        enemy_units=enemy,
        b_len=b_len,
        b_hei=b_hei,
        attacker_side=attacker_side,
        log_fn=None,
    )
    post_deploy_setup(log_fn=None)
    env_u.attacker_side = attacker_side
    env_u.defender_side = defender_side

    # размеры
    state0, _ = env.reset(options={"m": model, "e": enemy, "trunc": True})
    if isinstance(state0, dict):
        n_obs = len(list(state0.values()))
    else:
        n_obs = int(__import__("numpy").array(state0).shape[0])
    len_model = int(len(model))
    n_actions = action_sizes_from_env(env, len_model)

    # маленькая сеть + минимум симуляций для скорости
    net = GumbelMuZeroNet(
        obs_dim=int(n_obs),
        action_sizes=[int(x) for x in n_actions],
        latent_dim=64,
        hidden_dim=64,
        num_layers=2,
        action_embed_dim=16,
    )
    net.eval()
    search = GumbelMuZeroSearch(
        net,
        config=GumbelMuZeroSearchConfig(
            num_simulations=4,
            root_top_k=4,
            discount=0.997,
            temperature=0.5,
            gumbel_scale=1.0,
            prior_weight=0.25,
            batch_recurrent=False,
            tree_reuse=False,
        ),
        device=torch.device("cpu"),
    )
    sp_cfg = GumbelSelfPlayConfig(
        temperature_opening_moves=2,
        temperature_opening_value=1.0,
        temperature_late_value=0.5,
    )
    return env, search, len_model, sp_cfg


def _run_episode(capture: io.StringIO) -> tuple[int, str]:
    """Прогнать один эпизод, вернуть (число переходов, перехваченный лог)."""
    env, search, len_model, sp_cfg = _build_env_and_search()
    with redirect_stdout(capture):
        transitions, info = play_episode_with_gumbel_muzero(
            env=env,
            search=search,
            inference_fn=None,
            len_model=len_model,
            config=sp_cfg,
            policy_version=0,
            episode_id=0,
        )
    return len(transitions), capture.getvalue()


def main() -> int:
    failures: list[str] = []

    # --- Случай 1: флаг ВКЛ (дефолт) ---
    os.environ.pop("GMZ_REACTION_VALUE_POLICY", None)
    cap1 = io.StringIO()
    try:
        n1, log1 = _run_episode(cap1)
    except Exception as exc:  # noqa: BLE001
        failures.append(f"[ON] эпизод упал с исключением: {exc!r}")
        log1 = cap1.getvalue()
        n1 = -1

    on_ok = "reaction_value_policy=ON" in log1
    print("=" * 70)
    print("СЛУЧАЙ 1: GMZ_REACTION_VALUE_POLICY дефолт (ВКЛ)")
    print(f"  эпизод завершён, переходов: {n1}")
    print(f"  лог содержит 'reaction_value_policy=ON': {on_ok}")
    for line in log1.splitlines():
        if "[GMZ][REACTION]" in line:
            print(f"  >> {line.strip()}")
    if not on_ok:
        failures.append("[ON] в логе нет 'reaction_value_policy=ON'")
    if n1 < 0:
        failures.append("[ON] эпизод не завершился нормально")

    # --- Случай 2: флаг ВЫКЛ ---
    os.environ["GMZ_REACTION_VALUE_POLICY"] = "0"
    cap2 = io.StringIO()
    try:
        n2, log2 = _run_episode(cap2)
    except Exception as exc:  # noqa: BLE001
        failures.append(f"[OFF] эпизод упал с исключением: {exc!r}")
        log2 = cap2.getvalue()
        n2 = -1
    os.environ.pop("GMZ_REACTION_VALUE_POLICY", None)

    off_ok = "reaction_value_policy=ON" not in log2
    print("=" * 70)
    print("СЛУЧАЙ 2: GMZ_REACTION_VALUE_POLICY=0 (ВЫКЛ)")
    print(f"  эпизод завершён, переходов: {n2}")
    print(f"  лог НЕ содержит 'reaction_value_policy=ON': {off_ok}")
    for line in log2.splitlines():
        if "[GMZ][REACTION]" in line:
            print(f"  >> {line.strip()}")
    if not off_ok:
        failures.append("[OFF] в логе неожиданно есть 'reaction_value_policy=ON'")
    if n2 < 0:
        failures.append("[OFF] эпизод не завершился нормально")

    print("=" * 70)
    if failures:
        print("SMOKE FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("SMOKE OK: install umnyh reakcij rabotaet (VKL -> =ON, VYKL -> net =ON), bez padenij.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
