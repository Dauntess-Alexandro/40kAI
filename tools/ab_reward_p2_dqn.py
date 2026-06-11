"""
A/B: P2 DQN, reward baseline (A) vs package A (B).

Оппонент: PPO snapshot или эвристика (SELF_PLAY_ENABLED=0).

Использование:
  python tools/ab_reward_p2_dqn.py --opponent heuristic --eval-games 0
  python tools/ab_reward_p2_dqn.py --episodes 1000 --eval-games 200 --opponent ppo
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAIN_LOG = ROOT / "runtime" / "logs" / "LOGS_FOR_AGENTS_TRAIN.md"
EVAL_LOG = ROOT / "runtime" / "logs" / "LOGS_FOR_AGENTS_EVAL.md"

OPPONENT_P1_PPO = "P1_Necrons_only_war_v1_final_ep3000_20260611_095847"

REWARD_B_OVERRIDES: dict[str, str] = {
    "RCFG_VP_OBJECTIVE_OC_MARGIN_SCALE": "0.06",
    "RCFG_VP_DIFF_REWARD_SCALE": "0.22",
    "RCFG_OBJECTIVE_PROGRESS_STEP_SCALE": "0.35",
    "RCFG_OBJECTIVE_PROGRESS_STEP_CAP": "0.50",
    "RCFG_SHOOT_REWARD_DAMAGE_SCALE": "0.45",
    "RCFG_DAMAGE_TAKEN_SCALE": "0.38",
    "RCFG_TURN_LIMIT_DRAW_PENALTY": "4.5",
    "RCFG_MISSION_NO_CONTEST_PENALTY": "0.35",
    "RCFG_VP_STALL_PENALTY": "0.12",
    "RCFG_REWARD_PROGRESS_EARLY_MULT": "1.35",
    "RCFG_REWARD_HOLD_LATE_MULT": "1.15",
}

_RE_LEAGUE_SAVE = re.compile(r"\[LEAGUE\]\[SAVE\] agent_id=(\S+)")
_RE_TRAIN_EVAL = re.compile(
    r"\[ACTOR_LEARNER\]\[EVAL\].*?"
    r"win_rate=([\d.]+).*?"
    r"draw_rate=([\d.]+).*?"
    r"turn_limit_rate=([\d.]+).*?"
    r"vp_diff_mean=([-\d.]+)"
)
_RE_TRAIN_SUMMARY = re.compile(
    r"\[TRAIN\]\[SUMMARY\] episodes=\d+ "
    r"win_rate=([\d.]+) draw_rate=([\d.]+) loss_rate=([\d.]+) "
    r"reward_mean=([-\d.]+) vp_diff_mean=([-\d.]+)"
)
_RE_SUMMARY_V2 = re.compile(r"\[SUMMARY_V2\]\s+(.+)")


def _base_env(*, opponent: str) -> dict[str, str]:
    env = {
        "PYTHONPATH": f"{ROOT / 'core'};{os.environ.get('PYTHONPATH', '')}".strip(";"),
        "TRAIN_ALGO": "dqn",
        "LEARNER_SIDE": "P2",
        "LEARNER_FACTION": "Necrons",
        "DQN_DISTRIBUTED_ACTORS": "0",
        "ADAPTIVE_TURN_LIMIT_CURRICULUM": "0",
        "REWARD_SCHEDULE_ENABLED": "0",
        "PRO_ACTOR_LEARNER": "1",
        "NUM_ACTORS": os.environ.get("NUM_ACTORS", "8"),
        "USE_AMP": os.environ.get("USE_AMP", "1"),
        "USE_COMPILE": os.environ.get("USE_COMPILE", "1"),
        "PREFETCH": os.environ.get("PREFETCH", "1"),
        "PIN_MEMORY": os.environ.get("PIN_MEMORY", "1"),
    }
    if opponent == "heuristic":
        env["SELF_PLAY_ENABLED"] = "0"
        env.pop("OPPONENT_AGENT_ID", None)
    else:
        env["SELF_PLAY_ENABLED"] = "1"
        env["SELF_PLAY_OPPONENT_MODE"] = "snapshot"
        env["OPPONENT_AGENT_ID"] = OPPONENT_P1_PPO
    return env


def _reward_env_for_variant(variant: str) -> dict[str, str]:
    if variant.upper() == "B":
        return dict(REWARD_B_OVERRIDES)
    return {}


def _strip_reward_overrides(env: dict[str, str]) -> None:
    for key in REWARD_B_OVERRIDES:
        env.pop(key, None)


def _run(cmd: list[str], env: dict[str, str], label: str, log_path: Path | None = None) -> int:
    print(f"\n=== {label} ===", flush=True)
    print(" ".join(cmd), flush=True)
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8") as fh:
            proc = subprocess.run(
                cmd,
                cwd=str(ROOT),
                env=env,
                check=False,
                stdout=fh,
                stderr=subprocess.STDOUT,
                text=True,
            )
        return int(proc.returncode)
    proc = subprocess.run(cmd, cwd=str(ROOT), env=env, check=False)
    if proc.returncode != 0:
        print(f"[AB][ERROR] {label} завершился с кодом {proc.returncode}", flush=True)
    return int(proc.returncode)


def _read_text(path: Path, max_bytes: int = 2_000_000) -> str:
    if not path.is_file():
        return ""
    data = path.read_bytes()
    if len(data) > max_bytes:
        data = data[-max_bytes:]
    return data.decode("utf-8", errors="replace")


def _parse_from_text(text: str) -> tuple[str | None, dict | None, dict | None]:
    agent_ids = _RE_LEAGUE_SAVE.findall(text)
    agent_id = agent_ids[-1] if agent_ids else None

    train_window = None
    for line in reversed(text.splitlines()):
        m = _RE_TRAIN_EVAL.search(line)
        if m:
            train_window = {
                "win_rate": float(m.group(1)),
                "draw_rate": float(m.group(2)),
                "turn_limit_rate": float(m.group(3)),
                "vp_diff_mean": float(m.group(4)),
            }
            break

    train_summary = None
    for line in reversed(text.splitlines()):
        m = _RE_TRAIN_SUMMARY.search(line)
        if m:
            train_summary = {
                "win_rate": float(m.group(1)),
                "draw_rate": float(m.group(2)),
                "loss_rate": float(m.group(3)),
                "reward_mean": float(m.group(4)),
                "vp_diff_mean": float(m.group(5)),
            }
            break

    return agent_id, train_window, train_summary


def _parse_eval_summary(since_marker: str) -> dict[str, str] | None:
    text = _read_text(EVAL_LOG)
    idx = text.rfind(since_marker)
    chunk = text[idx:] if idx >= 0 else text
    for line in reversed(chunk.splitlines()):
        m = _RE_SUMMARY_V2.search(line)
        if m:
            raw = m.group(1).strip()
            out: dict[str, str] = {}
            for part in raw.split():
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                out[k] = v
            return out
    return None


def _run_variant(
    variant: str,
    *,
    episodes: int,
    eval_games: int,
    opponent: str,
    out_dir: Path,
) -> dict:
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    marker = f"[AB][{variant}] start {stamp}"
    print(marker, flush=True)

    env = os.environ.copy()
    _strip_reward_overrides(env)
    env.update(_base_env(opponent=opponent))
    env.update(_reward_env_for_variant(variant))
    env["TRAIN_EPISODES_OVERRIDE"] = str(int(episodes))
    env["AB_VARIANT"] = variant.upper()

    train_log = out_dir / f"train_{variant.upper()}.log"
    py = sys.executable
    rc = _run([py, "-u", "train.py"], env, f"train {variant}", log_path=train_log)
    train_text = _read_text(train_log)
    agent_id, train_window, train_summary = _parse_from_text(train_text)

    result: dict = {
        "variant": variant.upper(),
        "opponent": opponent,
        "episodes": int(episodes),
        "train_exit_code": rc,
        "train_marker": marker,
        "train_log": str(train_log),
        "reward_overrides": dict(REWARD_B_OVERRIDES) if variant.upper() == "B" else {},
        "agent_id": agent_id,
        "train_window": train_window,
        "train_summary": train_summary,
    }

    if rc != 0:
        (out_dir / f"variant_{variant.upper()}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return result

    if not agent_id:
        print(f"[AB][WARN] {variant}: agent_id не найден в {train_log}", flush=True)

    if eval_games > 0 and agent_id:
        eval_marker = f"[AB][{variant}] eval {stamp}"
        print(eval_marker, flush=True)
        eval_env = env.copy()
        eval_env["EVAL_EPSILON"] = "0"
        eval_env["FORCE_GREEDY"] = "1"
        eval_cmd = [
            py,
            "-u",
            "eval.py",
            "--games",
            str(int(eval_games)),
            "--learner-agent-id",
            agent_id,
        ]
        if opponent == "ppo":
            eval_cmd.extend(["--opponent-agent-id", OPPONENT_P1_PPO])
        eval_rc = _run(eval_cmd, eval_env, f"eval {variant}")
        result["eval_exit_code"] = eval_rc
        result["eval_games"] = int(eval_games)
        result["eval_marker"] = eval_marker
        result["eval_summary"] = _parse_eval_summary(eval_marker)
    else:
        result["eval_games"] = 0

    (out_dir / f"variant_{variant.upper()}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return result


def _write_comparison(out_dir: Path, results: list[dict], *, opponent: str) -> None:
    opp_label = "эвристика" if opponent == "heuristic" else f"`{OPPONENT_P1_PPO}`"
    eval_games = results[0].get("eval_games", 0) if results else 0

    lines = [
        "# A/B reward: P2 DQN",
        "",
        f"- Opponent: {opp_label}",
        f"- Episodes train: {results[0].get('episodes', '?') if results else '?'}",
        f"- Eval games: {eval_games}",
        "- Dist: off, adaptive curriculum: off",
        "",
        "## Agent IDs",
        "",
    ]
    for r in results:
        lines.append(f"- **{r.get('variant', '?')}**: `{r.get('agent_id', '-')}`")
    lines.extend(["", "## Train summary", ""])

    if eval_games > 0:
        lines.extend(
            [
                "| Variant | agent_id | train win% | train draw% | eval P2 win% | stay@move | model_ctrl0 |",
                "|---------|----------|------------|-------------|--------------|-----------|-------------|",
            ]
        )
        for r in results:
            ts = r.get("train_summary") or r.get("train_window") or {}
            es = r.get("eval_summary") or {}
            lines.append(
                "| {variant} | `{agent}` | {tw_win} | {tw_draw} | {p2_wr} | {stay} | {ctrl0} |".format(
                    variant=r.get("variant", "?"),
                    agent=r.get("agent_id", "-"),
                    tw_win=f"{ts.get('win_rate', 0):.3f}" if ts else "-",
                    tw_draw=f"{ts.get('draw_rate', 0):.3f}" if ts else "-",
                    p2_wr=es.get("winrate_p2_all", "-"),
                    stay=es.get("stay_rate_when_move_options", "-"),
                    ctrl0=es.get("model_ctrl_zero_rate", "-"),
                )
            )
    else:
        lines.extend(
            [
                "| Variant | agent_id | win% | draw% | loss% | reward_mean | vp_diff |",
                "|---------|----------|------|-------|-------|-------------|---------|",
            ]
        )
        for r in results:
            ts = r.get("train_summary") or {}
            lines.append(
                "| {variant} | `{agent}` | {win} | {draw} | {loss} | {rew} | {vp} |".format(
                    variant=r.get("variant", "?"),
                    agent=r.get("agent_id", "-"),
                    win=f"{ts.get('win_rate', 0):.3f}" if ts else "-",
                    draw=f"{ts.get('draw_rate', 0):.3f}" if ts else "-",
                    loss=f"{ts.get('loss_rate', 0):.3f}" if ts else "-",
                    rew=f"{ts.get('reward_mean', 0):.3f}" if ts else "-",
                    vp=f"{ts.get('vp_diff_mean', 0):.3f}" if ts else "-",
                )
            )

    lines.append("")
    (out_dir / "comparison.md").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "comparison.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    agents_lines = [
        f"# P2 DQN agents ({opponent}, {results[0].get('episodes', '?')} ep)" if results else "# P2 DQN agents",
        "",
    ]
    for r in results:
        agents_lines.append(f"{r.get('variant', '?')}: {r.get('agent_id', '-')}")
    (out_dir / "agents.txt").write_text("\n".join(agents_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="A/B reward P2 DQN")
    parser.add_argument("--episodes", type=int, default=1000)
    parser.add_argument("--eval-games", type=int, default=200, help="0 = без eval")
    parser.add_argument("--opponent", choices=("heuristic", "ppo"), default="ppo")
    parser.add_argument(
        "--variants",
        type=str,
        default="A,B",
        help="Список веток через запятую: A, B или A,B",
    )
    args = parser.parse_args()

    run_id = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = ROOT / "artifacts" / "results" / "ab_reward" / f"{run_id}_{args.opponent}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[AB] opponent={args.opponent} output_dir={out_dir}", flush=True)

    variants = [v.strip().upper() for v in str(args.variants).split(",") if v.strip()]
    results: list[dict] = []
    for variant in variants:
        if variant not in {"A", "B"}:
            print(f"[AB][WARN] пропуск неизвестной ветки: {variant}", flush=True)
            continue
        res = _run_variant(
            variant,
            episodes=int(args.episodes),
            eval_games=int(args.eval_games),
            opponent=str(args.opponent),
            out_dir=out_dir,
        )
        results.append(res)
        if res.get("train_exit_code", 0) != 0:
            break

    _write_comparison(out_dir, results, opponent=str(args.opponent))
    print(f"\n[AB] готово: {out_dir / 'comparison.md'}", flush=True)
    for r in results:
        print(f"[AB] {r.get('variant')}: agent_id={r.get('agent_id')}", flush=True)
    return 0 if results and all(r.get("train_exit_code", 1) == 0 for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
