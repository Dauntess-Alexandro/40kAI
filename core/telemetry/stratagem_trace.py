"""Журнал попыток/применения стратагем (eval + train verbose)."""
from __future__ import annotations

import os
from collections import Counter

# use_cp head → id стратагемы (см. warhamEnv action_space); fight — через fight_plan.
USE_CP_STRATAGEM_HEAD: dict[int, str] = {
    1: "insane_bravery",
    2: "overwatch",
    3: "smokescreen",
    4: "heroic_intervention",
}


def train_stratagem_trace_enabled() -> bool:
    """Включено при VERBOSE_LOGS=1 (или явно TRAIN_STRATAGEM_TRACE=1)."""
    return (
        os.getenv("VERBOSE_LOGS", "0") == "1"
        or os.getenv("TRAIN_STRATAGEM_TRACE", "0") == "1"
        or os.getenv("MANUAL_DICE", "0") == "1"
    )


def stratagem_trace_actor_ok(actor_idx: int) -> bool:
    """Ограничение шума: по умолчанию trace только actor 0 (-1 = eval/single)."""
    if not train_stratagem_trace_enabled():
        return False
    want = int(os.getenv("TRAIN_STRATAGEM_TRACE_ACTOR", "0") or "0")
    return int(actor_idx) in (-1, want)


def append_train_stratagem_log(line: str) -> None:
    import datetime

    from project_paths import AGENT_TRAIN_LOG_PATH, ensure_runtime_dirs

    ensure_runtime_dirs()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(AGENT_TRAIN_LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"{ts} | {line}\n")
    except Exception:
        return
    if os.getenv("TRAIN_LOG_TO_CONSOLE", "0") == "1":
        try:
            print(line, flush=True)
        except Exception:
            pass


def make_stratagem_tracer_for_train(
    log_fn=None,
    *,
    learner_side: str | None = None,
) -> StratagemEpisodeTracer | None:
    if not train_stratagem_trace_enabled():
        return None
    side = str(learner_side or os.getenv("LEARNER_SIDE", "P1") or "P1").strip().upper()
    if side not in {"P1", "P2"}:
        side = "P1"
    fn = log_fn or append_train_stratagem_log
    return StratagemEpisodeTracer(fn, learner_side=side, tag="TRAIN")


def stratagem_used_snapshot(env_unwrapped) -> tuple[tuple, ...]:
    """Снимок env.stratagem_used для diff после step."""
    raw = getattr(env_unwrapped, "stratagem_used", None) or []
    return tuple(tuple(x) for x in raw)


def new_stratagem_records(before: tuple[tuple, ...], after: tuple[tuple, ...]) -> list[tuple]:
    """Новые записи журнала стратагем (side, id, round, phase, unit_idx)."""
    if len(after) < len(before):
        return list(after)
    return list(after[len(before) :])


def stratagem_attempt_from_action(action_dict: dict) -> tuple[str | None, int | None]:
    """Попытка через flat use_cp/cp_on (command/reaction heads)."""
    use_cp = int(action_dict.get("use_cp", 0) or 0)
    sid = USE_CP_STRATAGEM_HEAD.get(use_cp)
    if not sid:
        return None, None
    return sid, int(action_dict.get("cp_on", 0) or 0)


def trace_side_label(env_side: str, learner_side: str) -> str:
    """env model/enemy → P1/P2 с учётом LEARNER_SIDE."""
    if env_side == "model":
        return str(learner_side)
    return "P2" if str(learner_side).upper() == "P1" else "P1"


# alias для eval
eval_side_label = trace_side_label


def cp_for_env_side(env_unwrapped, env_side: str) -> int:
    return int(env_unwrapped.modelCP if env_side == "model" else env_unwrapped.enemyCP)


def collect_stratagem_attempt_specs(
    action_dict: dict | None,
    fight_plan: dict | None = None,
) -> list[tuple[str, int | None, str]]:
    """Список попыток: (stratagem_id, unit_idx, source)."""
    specs: list[tuple[str, int | None, str]] = []
    if isinstance(action_dict, dict):
        sid, unit = stratagem_attempt_from_action(action_dict)
        if sid:
            specs.append((sid, unit, "use_cp"))
    for u_idx, fid in dict(fight_plan or {}).items():
        specs.append((str(fid), int(u_idx), "fight_plan"))
    return specs


def log_stratagem_attempts(
    trace_fn,
    *,
    step_no: int,
    env_side: str,
    learner_side: str,
    action_dict: dict | None,
    fight_plan: dict | None,
    ep_attempts: Counter,
    emit: bool = True,
    tag: str = "WH40K",
) -> list[tuple[str, int | None, str]]:
    specs = collect_stratagem_attempt_specs(action_dict, fight_plan)
    for sid, _unit, _source in specs:
        ep_attempts[sid] += 1
    if not emit:
        return specs
    side = trace_side_label(env_side, learner_side)
    for sid, unit, source in specs:
        if source == "use_cp" and isinstance(action_dict, dict):
            try:
                use_cp_v = int(action_dict.get("use_cp", 0) or 0)
            except (TypeError, ValueError):
                use_cp_v = 0
            try:
                cp_on_v = int(action_dict.get("cp_on", 0) or 0)
            except (TypeError, ValueError):
                cp_on_v = 0
            trace_fn(
                f"[{tag}][STRATAGEM][ATTEMPT] "
                f"step={step_no} side={side} env_side={env_side} stratagem={sid} unit={unit} "
                f"use_cp={use_cp_v} cp_on={cp_on_v}"
            )
        else:
            trace_fn(
                f"[{tag}][STRATAGEM][ATTEMPT] "
                f"step={step_no} side={side} env_side={env_side} stratagem={sid} unit={unit} "
                f"source={source}"
            )
    return specs


def log_stratagem_journal_diff(
    trace_fn,
    *,
    step_no: int,
    env_side_acting: str,
    learner_side: str,
    su_before: tuple[tuple, ...],
    su_after: tuple[tuple, ...],
    cp_model_before: int,
    cp_enemy_before: int,
    env_unwrapped,
    attempt_specs: list[tuple[str, int | None, str]],
    ep_applied: Counter,
    emit: bool = True,
    tag: str = "WH40K",
) -> list[tuple]:
    new_records = new_stratagem_records(su_before, su_after)
    if not emit:
        return new_records
    for rec in new_records:
        env_side = str(rec[0])
        sid = str(rec[1])
        rnd = int(rec[2])
        phase = str(rec[3] or "")
        unit = rec[4] if len(rec) > 4 else None
        cp_after = cp_for_env_side(env_unwrapped, env_side)
        cp_before = cp_model_before if env_side == "model" else cp_enemy_before
        ep_applied[sid] += 1
        trace_fn(
            f"[{tag}][STRATAGEM] "
            f"applied={sid} side={trace_side_label(env_side, learner_side)} env_side={env_side} "
            f"unit={unit} phase={phase} round={rnd} cp_before={cp_before} cp_after={cp_after}"
        )
    side = trace_side_label(env_side_acting, learner_side)
    for sid, unit, source in attempt_specs:
        applied = any(
            r[0] == env_side_acting
            and str(r[1]) == sid
            and (unit is None or r[4] == unit)
            for r in new_records
        )
        if applied:
            continue
        miss_tail = f"source={source} " if source != "use_cp" else ""
        trace_fn(
            f"[{tag}][STRATAGEM][MISS] "
            f"step={step_no} side={side} env_side={env_side_acting} attempted={sid} unit={unit} "
            f"{miss_tail}reason=no_journal_entry"
        )
    return new_records


class StratagemEpisodeTracer:
    """Trace стратагем за один train-эпизод (primary env)."""

    def __init__(self, log_fn, *, learner_side: str = "P1", tag: str = "TRAIN") -> None:
        self.log_fn = log_fn
        self.learner_side = learner_side
        self.tag = tag
        self.ep_attempts: Counter[str] = Counter()
        self.ep_applied: Counter[str] = Counter()

    def log_episode_summary(self, ep_label: str | int) -> None:
        if not self.ep_attempts and not self.ep_applied:
            return
        self.log_fn(
            f"[{self.tag}][STRATAGEM_SUMMARY] ep={ep_label} "
            f"attempts={dict(self.ep_attempts)} applied={dict(self.ep_applied)} "
            f"attempt_total={sum(self.ep_attempts.values())} "
            f"applied_total={sum(self.ep_applied.values())}"
        )
        self.ep_attempts.clear()
        self.ep_applied.clear()

    def run_enemy_turn(
        self,
        env_unwrapped,
        step_no: int,
        *,
        trunc: bool,
        policy_fn=None,
    ) -> None:
        enemy_specs: list[tuple[str, int | None, str]] = []
        su_before = stratagem_used_snapshot(env_unwrapped)
        cp_model_before = cp_for_env_side(env_unwrapped, "model")
        cp_enemy_before = cp_for_env_side(env_unwrapped, "enemy")

        if policy_fn is not None:
            def _wrapped(obs_any):
                action = policy_fn(obs_any)
                if isinstance(action, dict):
                    enemy_specs.extend(
                        log_stratagem_attempts(
                            self.log_fn,
                            step_no=step_no,
                            env_side="enemy",
                            learner_side=self.learner_side,
                            action_dict=action,
                            fight_plan=None,
                            ep_attempts=self.ep_attempts,
                            emit=True,
                            tag=self.tag,
                        )
                    )
                return action

            env_unwrapped.enemyTurn(trunc=trunc, policy_fn=_wrapped)
        else:
            env_unwrapped.enemyTurn(trunc=trunc)

        log_stratagem_journal_diff(
            self.log_fn,
            step_no=step_no,
            env_side_acting="enemy",
            learner_side=self.learner_side,
            su_before=su_before,
            su_after=stratagem_used_snapshot(env_unwrapped),
            cp_model_before=cp_model_before,
            cp_enemy_before=cp_enemy_before,
            env_unwrapped=env_unwrapped,
            attempt_specs=enemy_specs,
            ep_applied=self.ep_applied,
            emit=True,
            tag=self.tag,
        )

    def run_model_step(self, env, env_unwrapped, step_no: int, action_dict: dict):
        fight_plan = dict(getattr(env_unwrapped, "_pending_fight_stratagem_plan", None) or {})
        specs = log_stratagem_attempts(
            self.log_fn,
            step_no=step_no,
            env_side="model",
            learner_side=self.learner_side,
            action_dict=action_dict,
            fight_plan=fight_plan,
            ep_attempts=self.ep_attempts,
            emit=True,
            tag=self.tag,
        )
        su_before = stratagem_used_snapshot(env_unwrapped)
        cp_model_before = cp_for_env_side(env_unwrapped, "model")
        cp_enemy_before = cp_for_env_side(env_unwrapped, "enemy")
        try:
            result = env.step(action_dict)
        finally:
            try:
                from core.models.option_candidates import attach_fight_stratagem_plan

                attach_fight_stratagem_plan(env, None)
            except Exception:
                pass
        log_stratagem_journal_diff(
            self.log_fn,
            step_no=step_no,
            env_side_acting="model",
            learner_side=self.learner_side,
            su_before=su_before,
            su_after=stratagem_used_snapshot(env_unwrapped),
            cp_model_before=cp_model_before,
            cp_enemy_before=cp_enemy_before,
            env_unwrapped=env_unwrapped,
            attempt_specs=specs,
            ep_applied=self.ep_applied,
            emit=True,
            tag=self.tag,
        )
        return result
