import numpy as np
import pytest

from core.models.phoenix_dist import PhoenixSequenceAssembler, PhoenixWindowMeta, pack_phoenix_batch, unpack_phoenix_batch


def test_sequence_assembler_emits_contiguous_windows():
    asm = PhoenixSequenceAssembler(window=2)
    out = []
    for t in range(4):
        out.extend(asm.append([t, t], [t], [True], reward=float(t), done=False))
    assert len(out) == 2
    win, meta = out[0]
    assert isinstance(meta, PhoenixWindowMeta)
    assert meta.start_step == 0
    assert win.obs.shape == (3, 2)
    assert win.actions.shape == (3, 1)
    assert win.dones.tolist() == [0.0, 0.0, 0.0]
    assert win.obs[:, 0].tolist() == [0.0, 1.0, 2.0]


def test_sequence_assembler_pads_terminal_tail():
    asm = PhoenixSequenceAssembler(window=2)
    out = []
    out.extend(asm.append([0, 0], [0], [True], reward=1.0, done=False))
    out.extend(asm.append([1, 1], [1], [True], reward=2.0, done=True))
    assert len(out) == 2
    first, _ = out[0]
    second, _ = out[1]
    assert first.dones.tolist() == [0.0, 0.0, 1.0]
    assert second.dones.tolist() == [0.0, 1.0, 1.0]
    assert np.allclose(first.obs[1], first.obs[2])


def test_pack_unpack_phoenix_batch_roundtrip():
    asm = PhoenixSequenceAssembler(window=2)
    emitted = []
    for t in range(3):
        emitted.extend(asm.append([t, t], [0], [True], reward=float(t), done=(t == 2)))
    windows = [w for w, _m in emitted]
    metas = [m for _w, m in emitted]
    payload = pack_phoenix_batch(windows, worker_id=7, env_contract_hash="H", metas=metas, priorities=[1.0] * len(windows))
    got, pri = unpack_phoenix_batch(payload)
    assert len(got) == len(windows)
    assert payload["worker_id"] == 7
    assert payload["env_contract_hash"] == "H"
    assert pri is not None and pri.shape == (len(windows),)
    assert np.allclose(got[0].obs, windows[0].obs)


def test_unpack_rejects_bad_batch_rank():
    with pytest.raises(ValueError, match="ранги"):
        unpack_phoenix_batch({"obs": np.zeros((3,), dtype=np.float32), "actions": [], "active_masks": []})
