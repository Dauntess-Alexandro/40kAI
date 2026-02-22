import os

import torch

from model.alphazero import AlphaZeroNet, load_alphazero_checkpoint, save_alphazero_checkpoint
from train_alphazero import EpisodeRecord, _write_metrics


def test_alphazero_checkpoint_roundtrip(tmp_path):
    net = AlphaZeroNet(8, [3, 2])
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    path = tmp_path / "alphazero_model-test.pth"

    save_alphazero_checkpoint(str(path), net, opt, epoch=3, step=42)
    loaded, meta = load_alphazero_checkpoint(str(path))

    assert isinstance(loaded, AlphaZeroNet)
    assert meta["agent_type"] == "alphazero"
    assert meta["epoch"] == 3
    assert meta["step"] == 42


def test_alphazero_metrics_written(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("models", exist_ok=True)
    episodes = [EpisodeRecord(1.0, 10, "win"), EpisodeRecord(-0.5, 8, "loss")]

    _write_metrics("unit", [0.1, 0.2], episodes)

    assert (tmp_path / "models" / "alphazero_data_unit.json").exists()
    assert (tmp_path / "metrics" / "reward_unit.png").exists()
    assert (tmp_path / "metrics" / "alphazero_stats_unit.csv").exists()
