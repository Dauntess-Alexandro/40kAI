import torch


def test_model_wrapper_builds_net():
    from core.models.sampled_muzero_model import SampledMuZeroNet, make_sampled_muzero_net
    net = make_sampled_muzero_net(obs_dim=10, action_sizes=[3, 4], latent_dim=32,
                                  hidden_dim=32, num_layers=1, action_embed_dim=8)
    assert isinstance(net, SampledMuZeroNet)
    logits, value = net(torch.zeros(1, 10))
    assert len(logits) == 2 and value.shape[0] == 1


def test_trainer_wrapper_reexports():
    from core.models.sampled_muzero_trainer import (
        SampledMuZeroTrainConfig,
        train_sampled_muzero_step,
    )
    cfg = SampledMuZeroTrainConfig(batch_size=4, unroll_steps=2)
    assert cfg.batch_size == 4
    assert callable(train_sampled_muzero_step)


def test_selfplay_wrapper_reexports():
    from core.models.sampled_muzero_selfplay import (
        SampledSelfPlayConfig,
        play_episode_with_sampled_muzero,
    )
    cfg = SampledSelfPlayConfig()
    assert cfg.outcome_only is True
    assert callable(play_episode_with_sampled_muzero)
