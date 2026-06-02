#!/usr/bin/env python
"""A/B бенч скорости/качества AZ tree: default vs A1/B1/B2, по N эпизодов с IS Local.

Гоняет конфиги ПО ОЧЕРЕДИ (каждый — отдельная тренировка с нуля), замеряет ep/h
по wall-time и парсит honest DET-eval winrate из лога прогона, затем пишет
сравнительную таблицу в runtime/logs/az_ab_bench_<дата>.md.

ВАЖНО:
- ep/h (скорость) при N=100 надёжна. winrate при N=100 — ШУМ (сеть едва обучена),
  для качества нужен длинный прогон или --resume с готового checkpoint.
- Требует CUDA (IS Local) и заполненный runtime/state/data.json (ростер из GUI).
- Закрой другие train/GUI перед запуском — иначе борьба за GPU исказит замеры.

Пример:
  python tools/az_ab_bench.py --episodes 100
  python tools/az_ab_bench.py --episodes 100 --only default,B2_noenemy
  python tools/az_ab_bench.py --episodes 5 --timeout 600     # калибровка
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]

# Базовое окружение: AZ tree + локальный inference server (вариант B-local)
BASE_ENV: dict[str, str] = {
    "TRAIN_ALGO": "alphazero_tree",
    "AZ_INFERENCE_SERVER": "1",
    "AZ_INFERENCE_SERVER_MODE": "local",
    "PRO_ACTOR_LEARNER": "1",
}

# Конфиги: имя -> переопределения env (всё остальное — из hyperparams.json)
CONFIGS: dict[str, dict[str, str]] = {
    "default": {},                              # как сейчас
    "A1_parallel1": {"AZ_MCTS_PARALLEL_SIMS": "1"},   # убрать передподписку потоков
    "B1_depth1": {"AZ_MCTS_MAX_DEPTH": "1"},          # глубина rollout 2->1
    "B2_noenemy": {"AZ_MCTS_SIMULATE_ENEMY": "0"},    # пропустить enemyTurn
}

_WR_RE = re.compile(r"\[AZ\]\[HONEST_EVAL\] done ep=(\d+) win_rate=([0-9.]+) n=(\d+)")
_EP_RE = re.compile(r"\bep=(\d+)/(\d+)")


def run_one(name: str, overrides: dict[str, str], episodes: int, timeout: float, logdir: Path) -> dict:
    env = os.environ.copy()
    env.update(BASE_ENV)
    env["TRAIN_EPISODES_OVERRIDE"] = str(int(episodes))
    env.update(overrides)

    log_path = logdir / f"bench_{name}.log"
    print(f"\n=== [{name}] start: episodes={episodes} overrides={overrides or '{}'} ===", flush=True)
    t0 = time.perf_counter()
    timed_out = False
    rc = 0
    try:
        with log_path.open("w", encoding="utf-8") as fh:
            proc = subprocess.run(
                [sys.executable, str(_REPO / "train.py")],
                env=env, stdout=fh, stderr=subprocess.STDOUT,
                cwd=str(_REPO), timeout=float(timeout),
            )
        rc = int(proc.returncode)
    except subprocess.TimeoutExpired:
        timed_out = True
    elapsed = time.perf_counter() - t0

    text = log_path.read_text(encoding="utf-8", errors="ignore")
    eps_done = 0
    for m in _EP_RE.finditer(text):
        eps_done = max(eps_done, int(m.group(1)))
    wr = n_eval = None
    for m in _WR_RE.finditer(text):
        wr = float(m.group(2))
        n_eval = int(m.group(3))
    eph = (eps_done / (elapsed / 3600.0)) if (elapsed > 0 and eps_done > 0) else 0.0
    sec_per_ep = (elapsed / eps_done) if eps_done > 0 else float("nan")

    res = {
        "name": name, "overrides": overrides, "elapsed_s": elapsed,
        "episodes": eps_done, "ep_per_h": eph, "sec_per_ep": sec_per_ep,
        "win_rate": wr, "eval_n": n_eval, "rc": rc, "timed_out": timed_out,
        "log": str(log_path),
    }
    print(
        f"=== [{name}] done: ep={eps_done} elapsed={elapsed:.0f}s "
        f"ep/h={eph:.1f} sec/ep={sec_per_ep:.1f} winrate={wr} "
        f"{'(TIMEOUT)' if timed_out else ''} rc={rc} ===",
        flush=True,
    )
    return res


def write_report(results: list[dict], episodes: int, report_path: Path) -> None:
    base = next((r for r in results if r["name"] == "default"), None)
    lines = [
        f"# AZ tree A/B бенч — {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Эпизодов на конфиг: **{episodes}** · режим: **IS Local** · по очереди, с нуля.",
        "",
        "⚠️ ep/h — надёжно. winrate при малом N — ШУМ (сеть едва обучена); "
        "для качества нужен длинный прогон или старт с checkpoint.",
        "",
        "| Конфиг | overrides | эп | сек/эп | ep/h | Δ скорости | winrate | n | статус |",
        "|--------|-----------|----|--------|------|-----------|---------|---|--------|",
    ]
    for r in results:
        delta = ""
        if base and base["ep_per_h"] > 0 and r["ep_per_h"] > 0:
            delta = f"{(r['ep_per_h'] / base['ep_per_h'] - 1.0) * 100:+.0f}%"
        ov = ", ".join(f"{k}={v}" for k, v in r["overrides"].items()) or "—"
        status = "TIMEOUT" if r["timed_out"] else (f"rc={r['rc']}" if r["rc"] else "ok")
        wr = "—" if r["win_rate"] is None else f"{r['win_rate']:.3f}"
        lines.append(
            f"| {r['name']} | {ov} | {r['episodes']} | {r['sec_per_ep']:.1f} | "
            f"{r['ep_per_h']:.1f} | {delta} | {wr} | {r['eval_n'] or '—'} | {status} |"
        )
    lines += ["", "Логи прогонов: " + ", ".join(f"`{Path(r['log']).name}`" for r in results), ""]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines), flush=True)
    print(f"\n[OK] отчёт: {report_path}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="AZ tree A/B speed/quality bench (IS Local)")
    ap.add_argument("--episodes", type=int, default=100)
    ap.add_argument("--timeout", type=float, default=86400.0, help="таймаут на конфиг, сек")
    ap.add_argument("--only", default="", help="список конфигов через запятую (default,A1_parallel1,...)")
    args = ap.parse_args()

    names = [s.strip() for s in args.only.split(",") if s.strip()] or list(CONFIGS.keys())
    unknown = [n for n in names if n not in CONFIGS]
    if unknown:
        print(f"[ERROR] неизвестные конфиги: {unknown}. Доступно: {list(CONFIGS)}", file=sys.stderr)
        return 2

    logdir = _REPO / "runtime" / "logs"
    logdir.mkdir(parents=True, exist_ok=True)
    results = [run_one(n, CONFIGS[n], args.episodes, args.timeout, logdir) for n in names]

    report = logdir / f"az_ab_bench_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    write_report(results, args.episodes, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
