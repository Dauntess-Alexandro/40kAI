"""GUI contract for PHOENIX distributed actors wiring."""

from pathlib import Path


def test_gui_wires_phoenix_distributed_env_keys():
    source = Path("app/gui_qt/main.py").read_text(encoding="utf-8")
    for marker in (
        "PHOENIX_NUM_ACTORS",
        "PHOENIX_DISTRIBUTED_ACTORS",
        "PHOENIX_DIST_ROLLOUT_PORT",
        "PHOENIX_DIST_LOCAL_EPISODE_FRACTION",
        "PHOENIX_DIST_PC2_NUM_WORKERS",
        "PHOENIX_DIST_MAX_WINDOWS_PER_MSG",
        "resolve_phoenix_dist_episode_split",
    ):
        assert marker in source


def test_gui_counts_phoenix_topup_as_pc1_progress():
    source = Path("app/gui_qt/main.py").read_text(encoding="utf-8")
    start = source.index("def _record_dist_actor_episode(self, actor_idx: int) -> None:")
    end = source.index("def _update_dist_progress_display", start)
    body = source[start:end]
    assert "PHOENIX_DIST_TOPUP_ACTOR_IDX" in body
    assert "self._dist_pc1_ep_done += 1" in body


def test_phoenix_actor_emits_pc1_collection_marker():
    source = Path("train.py").read_text(encoding="utf-8")
    start = source.index("def _phoenix_actor_entry(")
    end = source.index("\ndef _main_actor_learner_phoenix_distributed", start)
    body = source[start:end]
    assert "[TRAIN][DIST][PC1] pc1_ep_collected actor=" in body
