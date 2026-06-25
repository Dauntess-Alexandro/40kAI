"""Журнал попыток/применения стратагем (eval + train verbose)."""
from __future__ import annotations

import os
from collections import Counter


def episode_stratagem_summary_line(
    source,
    *,
    ep_label: str | int = "",
    tag: str = "TRAIN",
) -> str | None:
    """Per-episode сводка стратагем из журнала env + счётчиков реролла.

    *source* — либо unwrapped env (с атрибутами stratagem_used,
    _cmd_reroll_fired), либо dict-payload от актора
    (ключи _strat_applied, _strat_applied_total, _cmd_reroll_fired).
    cmd_reroll_wasted считается арифметикой: max(0, applied['command_reroll'] − fired).
    После реактивного гейта это диагностика armed-not-fired, CP не потрачен;
    это не штрафуемый waste. Строка лога сохранена для back-compat парсеров.
    Возвращает None если данных нет / всё нулевое.
    """
    if isinstance(source, dict):
        # payload-словарь от актора
        applied: dict[str, int] = dict(source.get("_strat_applied") or {})
        applied_total = int(source.get("_strat_applied_total") or 0)
        fired = int(source.get("_cmd_reroll_fired") or 0)
    else:
        # unwrapped env
        used = list(getattr(source, "stratagem_used", None) or [])
        counts: Counter[str] = Counter(str(rec[1]) for rec in used if len(rec) > 1)
        applied = dict(counts)
        applied_total = sum(counts.values())
        fired = int(getattr(source, "_cmd_reroll_fired", 0) or 0)

    applied_cr = int(applied.get("command_reroll", 0))
    wasted = max(0, applied_cr - fired)

    if not applied and not fired and not wasted:
        return None
    return (
        f"[{tag}][STRATAGEM_SUMMARY] ep={ep_label} "
        f"applied={applied} applied_total={applied_total} "
        f"cmd_reroll_fired={fired} cmd_reroll_wasted={wasted}"
    )


def emit_episode_stratagem_log(source, *, ep_label="", tag: str = "TRAIN") -> str | None:
    """Залогировать per-episode сводку стратагем, если включён debug-трейс (VERBOSE_LOGS=1).

    Для путей без собственного трейсера (GMZ/SMZ): берёт env/payload, строит строку и пишет
    в train-лог. Выключено без трейса; пустые данные → ничего. Возвращает записанную строку (или None).
    """
    if not train_stratagem_trace_enabled():
        return None
    line = episode_stratagem_summary_line(source, ep_label=ep_label, tag=tag)
    if line:
        append_train_stratagem_log(line)
    return line


def collect_ep_stratagem_payload(env_unwrapped) -> dict:
    """Сериализация стратагемных данных env в dict для payload актора.

    Вызывать в конце эпизода из actor-процесса; результат мержить в ep-payload
    для передачи learner'у через data_q.
    """
    used = list(getattr(env_unwrapped, "stratagem_used", None) or [])
    counts: Counter[str] = Counter(str(rec[1]) for rec in used if len(rec) > 1)
    fired = int(getattr(env_unwrapped, "_cmd_reroll_fired", 0) or 0)
    if not counts and not fired:
        return {}
    return {
        "_strat_applied": dict(counts),
        "_strat_applied_total": int(sum(counts.values())),
        "_cmd_reroll_fired": fired,
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
    """Попытка через strat_command-голову (контракт use_cp/cp_on удалён в task-4).

    Функция сохранена для обратной совместимости трейса; всегда возвращает (None, None)
    т.к. ключи use_cp/cp_on более не присутствуют в action_dict.
    """
    return None, None


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
    """Список попыток: (stratagem_id, unit_idx, source).

    use_cp/cp_on-ветка удалена (task-4): стратагемы теперь только через fight_plan
    и strat_command-голову (журнал stratagem_used).
    """
    specs: list[tuple[str, int | None, str]] = []
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
        trace_fn(
            f"[{tag}][STRATAGEM][MISS] "
            f"step={step_no} side={side} env_side={env_side_acting} attempted={sid} unit={unit} "
            f"source={source} reason=no_journal_entry"
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

    def log_episode_summary(self, ep_label: str | int, *, env_unwrapped=None) -> None:
        if not self.ep_attempts and not self.ep_applied:
            return
        reroll_suffix = ""
        if env_unwrapped is not None:
            fired = int(getattr(env_unwrapped, "_cmd_reroll_fired", 0) or 0)
            applied_cr = int(self.ep_applied.get("command_reroll", 0))
            # cmd_reroll_wasted = armed-not-fired, CP не потрачен; диагностика,
            # не штрафуемый waste. Имя поля в логе сохраняем для парсеров.
            wasted = max(0, applied_cr - fired)
            reroll_suffix = f" cmd_reroll_fired={fired} cmd_reroll_wasted={wasted}"
        self.log_fn(
            f"[{self.tag}][STRATAGEM_SUMMARY] ep={ep_label} "
            f"attempts={dict(self.ep_attempts)} applied={dict(self.ep_applied)} "
            f"attempt_total={sum(self.ep_attempts.values())} "
            f"applied_total={sum(self.ep_applied.values())}"
            f"{reroll_suffix}"
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
        specs = log_stratagem_attempts(
            self.log_fn,
            step_no=step_no,
            env_side="model",
            learner_side=self.learner_side,
            action_dict=action_dict,
            fight_plan={},
            ep_attempts=self.ep_attempts,
            emit=True,
            tag=self.tag,
        )
        su_before = stratagem_used_snapshot(env_unwrapped)
        cp_model_before = cp_for_env_side(env_unwrapped, "model")
        cp_enemy_before = cp_for_env_side(env_unwrapped, "enemy")
        result = env.step(action_dict)
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
