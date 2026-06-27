"""Task 2: eval.py резолвит phase_obs_features ДО постройки env.

Приоритет: контракт агента → hyperparams.json → env-var → 0.
"""

import json
import os
import tempfile
from unittest.mock import patch

import pytest

# Не импортируем eval.py напрямую (тяжёлый), выделяем тестируемые функции через exec.
# Вместо этого тестируем _resolve_phase_obs_for_agent через import из eval.py
# после патча log, чтобы не трогать файловую систему.


@pytest.fixture(autouse=True)
def _patch_log():
    """Патчим log() на no-op, чтобы не писать в runtime/logs."""
    with patch("eval.log"):
        yield


@pytest.fixture(autouse=True)
def _clean_env():
    """Сбрасываем env-переменные после каждого теста."""
    orig_phase = os.environ.pop("PHASE_OBS_FEATURES", None)
    orig_reaction = os.environ.pop("AZ_REACTION_VALUE_POLICY", None)
    yield
    if orig_phase is not None:
        os.environ["PHASE_OBS_FEATURES"] = orig_phase
    else:
        os.environ.pop("PHASE_OBS_FEATURES", None)
    if orig_reaction is not None:
        os.environ["AZ_REACTION_VALUE_POLICY"] = orig_reaction
    else:
        os.environ.pop("AZ_REACTION_VALUE_POLICY", None)


class TestResolvePhaseObsForAgent:
    def _call(self, agent_id: str, hyperparams: dict | None = None):
        """Помогает вызвать _resolve_phase_obs_for_agent с временным hyperparams.json."""
        from eval import _resolve_phase_obs_for_agent

        if hyperparams is not None:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False, encoding="utf-8"
            ) as f:
                json.dump(hyperparams, f)
                path = f.name
            try:
                with patch("eval.open", open) as _open_mock:
                    # Мы патчим open внутри eval.py — поскольку eval использует
                    # встроенный open, а не import open, лучше поменять cwd
                    # или использовать monkeypatch на os.path.abspath.
                    # Упрощение: просто положим hyperparams.json в текущую директорию.
                    pass
            finally:
                os.unlink(path)
        else:
            # Без hyperparams.json
            _resolve_phase_obs_for_agent(agent_id)

    def test_contract_extras_phase_1_sets_env(self, monkeypatch, tmp_path):
        """Контракт агента с extras.phase_obs_features=1 → PHASE_OBS_FEATURES=1."""
        from eval import _resolve_phase_obs_for_agent

        # Мокаем _load_agent_contract_extras
        monkeypatch.setattr(
            "eval._load_agent_contract_extras",
            lambda _aid: {"phase_obs_features": 1, "reaction_value_policy": 1},
        )
        # hyperparams.json не существует в cwd теста → open бросит FileNotFoundError,
        # обработчик внутри _resolve_phase_obs_for_agent проигнорирует его.
        monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
        monkeypatch.delenv("AZ_REACTION_VALUE_POLICY", raising=False)

        _resolve_phase_obs_for_agent("dummy_agent")

        assert os.environ["PHASE_OBS_FEATURES"] == "1"
        assert os.environ["AZ_REACTION_VALUE_POLICY"] == "1"

    def test_contract_extras_phase_0_sets_env(self, monkeypatch):
        """Контракт агента с extras.phase_obs_features=0 → PHASE_OBS_FEATURES=0."""
        from eval import _resolve_phase_obs_for_agent

        monkeypatch.setattr(
            "eval._load_agent_contract_extras",
            lambda _aid: {"phase_obs_features": 0, "reaction_value_policy": 0},
        )
        # hyperparams.json не существует → fallback на env-var (или 0).
        monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
        monkeypatch.setenv("AZ_REACTION_VALUE_POLICY", "1")

        _resolve_phase_obs_for_agent("dummy_agent")

        assert os.environ["PHASE_OBS_FEATURES"] == "0"
        assert os.environ["AZ_REACTION_VALUE_POLICY"] == "0"

    def test_log_opponent_contract_extras(self, monkeypatch):
        """Opponent extras должны быть видны в eval-логе, но не менять env-флаги learner."""
        import eval as eval_mod

        logs: list[str] = []
        monkeypatch.setattr(
            eval_mod,
            "_load_agent_contract_extras",
            lambda _aid: {"phase_obs_features": 1, "reaction_value_policy": 1, "train_algo": "ppo"},
        )
        monkeypatch.setattr(eval_mod, "log", logs.append)

        eval_mod._log_agent_contract_extras("opp-agent", role="opponent")

        assert logs
        assert "[RESOLVE][OPPONENT]" in logs[0]
        assert "agent_id=opp-agent" in logs[0]
        assert "phase_obs_features=1" in logs[0]
        assert "reaction_value_policy=1" in logs[0]
        assert "train_algo=ppo" in logs[0]

    def test_no_contract_extras_falls_back_to_hyperparams(self, monkeypatch, tmp_path):
        """Нет extras → берём из hyperparams.json."""
        from eval import _resolve_phase_obs_for_agent

        monkeypatch.setattr(
            "eval._load_agent_contract_extras",
            lambda _aid: {},
        )
        # Пишем временный hyperparams.json
        hp_file = tmp_path / "hyperparams.json"
        hp_file.write_text(
            json.dumps({"alphazero_tree": {"phase_obs_features": 1, "reaction_value_policy": 0}}),
            encoding="utf-8",
        )
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
        monkeypatch.delenv("AZ_REACTION_VALUE_POLICY", raising=False)

        _resolve_phase_obs_for_agent("dummy_agent")

        assert os.environ["PHASE_OBS_FEATURES"] == "1"
        assert os.environ["AZ_REACTION_VALUE_POLICY"] == "0"

    def test_no_contract_no_hyperparams_falls_back_to_env(self, monkeypatch, tmp_path):
        """Нет extras и нет hyperparams → берём из env-var."""
        from eval import _resolve_phase_obs_for_agent

        monkeypatch.setattr(
            "eval._load_agent_contract_extras",
            lambda _aid: {},
        )
        # Убедимся, что hyperparams.json не найден
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
        monkeypatch.setenv("AZ_REACTION_VALUE_POLICY", "0")

        _resolve_phase_obs_for_agent("dummy_agent")

        assert os.environ["PHASE_OBS_FEATURES"] == "1"
        assert os.environ["AZ_REACTION_VALUE_POLICY"] == "0"

    def test_no_contract_no_hyperparams_no_env_defaults_to_zero(self, monkeypatch, tmp_path):
        """Ничего нет → дефолт 0."""
        from eval import _resolve_phase_obs_for_agent

        monkeypatch.setattr(
            "eval._load_agent_contract_extras",
            lambda _aid: {},
        )
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
        monkeypatch.delenv("AZ_REACTION_VALUE_POLICY", raising=False)

        _resolve_phase_obs_for_agent("dummy_agent")

        assert os.environ["PHASE_OBS_FEATURES"] == "0"
        assert os.environ["AZ_REACTION_VALUE_POLICY"] == "0"

    def test_hyperparams_missing_section_defaults_to_zero(self, monkeypatch, tmp_path):
        """hyperparams.json есть, но нет alphazero_tree → 0."""
        from eval import _resolve_phase_obs_for_agent

        monkeypatch.setattr(
            "eval._load_agent_contract_extras",
            lambda _aid: {},
        )
        hp_file = tmp_path / "hyperparams.json"
        hp_file.write_text(json.dumps({"dqn": {"lr": 1e-3}}), encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
        monkeypatch.delenv("AZ_REACTION_VALUE_POLICY", raising=False)

        _resolve_phase_obs_for_agent("dummy_agent")

        assert os.environ["PHASE_OBS_FEATURES"] == "0"
        assert os.environ["AZ_REACTION_VALUE_POLICY"] == "0"


class TestResolveRulesetVersion:
    def test_defaults_to_selected_mission(self, monkeypatch):
        from eval import _resolve_ruleset_version

        monkeypatch.delenv("RULESET_VERSION", raising=False)
        monkeypatch.setenv("MISSION_NAME", "annihilation")

        assert _resolve_ruleset_version(None) == "annihilation_v2"
        assert _resolve_ruleset_version("annihilation") == "annihilation_v2"

    def test_explicit_env_has_priority(self, monkeypatch):
        from eval import _resolve_ruleset_version

        monkeypatch.setenv("MISSION_NAME", "annihilation")
        monkeypatch.setenv("RULESET_VERSION", "custom_ruleset_v9")

        assert _resolve_ruleset_version("annihilation") == "custom_ruleset_v9"


class TestResolveEnvMissionName:
    def test_prefers_canonical_mission_key(self, monkeypatch):
        from eval import _resolve_env_mission_name

        class Env:
            mission_key = "annihilation"
            mission_name = "Annihilation / Kill Points"

        monkeypatch.setenv("MISSION_NAME", "only_war")

        assert _resolve_env_mission_name(Env()) == "annihilation"

    def test_uses_env_fallback_when_key_missing(self, monkeypatch):
        from eval import _resolve_env_mission_name

        class Env:
            mission_name = "Only War"

        monkeypatch.setenv("MISSION_NAME", "annihilation")

        assert _resolve_env_mission_name(Env()) == "annihilation"


class TestReapplyResolvedPhaseObs:
    """Регресс: резолвленное значение должно пережить клоббер от `from train import`.

    train.py на import-time уходит в else-ветку (TRAIN_ALGO=dqn в процессе eval) и
    жёстко ставит PHASE_OBS_FEATURES="0", затирая то, что выставил резолвер. Постройка
    env (_build_env_from_train_roster) обязана переустановить резолвленное значение
    ПОСЛЕ импорта train и ДО gym.make.
    """

    def test_reapply_restores_after_clobber(self, monkeypatch):
        from eval import _reapply_resolved_phase_obs, _resolve_phase_obs_for_agent

        monkeypatch.setattr(
            "eval._load_agent_contract_extras",
            lambda _aid: {"phase_obs_features": 1, "reaction_value_policy": 1},
        )
        monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
        monkeypatch.delenv("AZ_REACTION_VALUE_POLICY", raising=False)

        _resolve_phase_obs_for_agent("dummy_agent")
        assert os.environ["PHASE_OBS_FEATURES"] == "1"

        # Имитируем клоббер от `from train import ...` (else-ветка train.py).
        os.environ["PHASE_OBS_FEATURES"] = "0"
        os.environ["AZ_REACTION_VALUE_POLICY"] = "0"

        _reapply_resolved_phase_obs()

        assert os.environ["PHASE_OBS_FEATURES"] == "1"
        assert os.environ["AZ_REACTION_VALUE_POLICY"] == "1"

    def test_reapply_noop_without_resolve(self, monkeypatch):
        """Без предшествующего резолва re-apply ничего не трогает."""
        import eval as eval_mod
        from eval import _reapply_resolved_phase_obs

        monkeypatch.setattr(eval_mod, "_PHASE_OBS_RESOLVED_ENV", {}, raising=False)
        monkeypatch.setenv("PHASE_OBS_FEATURES", "0")

        _reapply_resolved_phase_obs()

        assert os.environ["PHASE_OBS_FEATURES"] == "0"
