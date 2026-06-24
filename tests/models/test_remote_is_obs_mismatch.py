import json

from core.models.remote_is_search_cfg_common import (
    RemoteIsSmbPaths,
    ensure_remote_search_cfg,
)


def _setup(tmp_path, cfg_obs):
    cfgp = tmp_path / "gmz_remote_search_cfg.json"
    cfgp.write_text(json.dumps({"obs_dim": cfg_obs, "action_sizes": [3, 2]}), encoding="utf-8")
    wp = tmp_path / "latest_gmz_policy.pth"
    wp.write_text("dummy", encoding="utf-8")
    paths = RemoteIsSmbPaths(
        actor_sync_dir=str(tmp_path),
        search_cfg_path=str(cfgp),
        weights_path=str(wp),
    )
    return cfgp, wp, paths


def test_republish_on_obs_mismatch(tmp_path):
    cfgp, wp, paths = _setup(tmp_path, 17)
    called = {"n": 0}

    def fake_publish(**kw):
        called["n"] += 1
        cfgp.write_text(json.dumps({"obs_dim": 41, "action_sizes": [3, 2]}), encoding="utf-8")
        return [str(cfgp)]

    res = ensure_remote_search_cfg(
        "share",
        search_cfg_name="gmz_remote_search_cfg.json",
        publish_from_repo=fake_publish,
        resolve_paths=lambda s: paths,
        local_targets=lambda **k: [],
        current_obs_dim_fn=lambda: 41,
    )
    assert called["n"] == 1
    assert res.action == "generated"
    assert not wp.exists()  # устаревшие веса удалены


def test_found_when_obs_matches(tmp_path):
    cfgp, wp, paths = _setup(tmp_path, 41)
    called = {"n": 0}

    def fake_publish(**kw):
        called["n"] += 1
        return []

    res = ensure_remote_search_cfg(
        "share",
        search_cfg_name="x",
        publish_from_repo=fake_publish,
        resolve_paths=lambda s: paths,
        local_targets=lambda **k: [],
        current_obs_dim_fn=lambda: 41,
    )
    assert called["n"] == 0
    assert res.action == "found"
    assert wp.exists()


def test_found_when_fn_none(tmp_path):
    cfgp, wp, paths = _setup(tmp_path, 17)
    res = ensure_remote_search_cfg(
        "share",
        search_cfg_name="x",
        publish_from_repo=lambda **k: [],
        resolve_paths=lambda s: paths,
        local_targets=lambda **k: [],
    )
    assert res.action == "found"
    assert wp.exists()
