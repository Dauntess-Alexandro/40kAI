from __future__ import annotations

from core.models.phoenix_dist import split_count_among_workers


def test_pc2_phoenix_launcher_import_and_context_env(monkeypatch):
    import tools.pc2_phoenix_actors as launcher

    seen: list[str] = []
    monkeypatch.delenv("MISSION_NAME", raising=False)
    monkeypatch.delenv("RULESET_VERSION", raising=False)
    launcher._apply_context_env(
        {"mission": "only_war", "ruleset_version": "only_war_v1"},
        log=seen.append,
    )

    assert callable(launcher.main)
    assert split_count_among_workers(total=5, num_workers=2) == [3, 2]
    assert "only_war" in seen[0]
