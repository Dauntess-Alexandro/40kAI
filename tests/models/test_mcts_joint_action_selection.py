import numpy as np

from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig, MCTSNode
from core.models.alphazero_model import make_alphazero_net


def _mcts(*, enabled: bool) -> AlphaZeroFactorizedMCTS:
    return AlphaZeroFactorizedMCTS(
        make_alphazero_net(4, [2, 2, 2]),
        config=MCTSConfig(
            temperature_opening_moves=0,
            prior_weight_early=0.0,
            joint_action_from_best_child=enabled,
        ),
    )


def _root_with_children(children: list[tuple[tuple[int, ...], int]]) -> MCTSNode:
    root = MCTSNode(prior=1.0)
    for action_tuple, visits in children:
        child = MCTSNode(prior=0.5, parent=root, action_tuple=action_tuple)
        child.visit_count = int(visits)
        root.children[action_tuple] = child
    return root


def _uniform_inputs() -> tuple[list[np.ndarray], list[np.ndarray]]:
    priors = [
        np.array([0.5, 0.5], dtype=np.float32),
        np.array([0.5, 0.5], dtype=np.float32),
        np.array([0.5, 0.5], dtype=np.float32),
    ]
    legal = [np.array([1, 1], dtype=bool) for _ in priors]
    return priors, legal


def test_option_mode_executes_exact_best_child_but_keeps_marginal_targets():
    root = _root_with_children([
        ((0, 0, 0), 10),
        ((1, 1, 0), 9),
        ((1, 0, 1), 9),
    ])
    priors, legal = _uniform_inputs()

    policy_targets, selected = _mcts(enabled=True)._final_policy_from_visits(
        root,
        priors,
        legal,
        temperature=0.0,
        move_count=99,
        candidate_mode="option",
    )

    assert selected == [0, 0, 0]
    assert [int(np.argmax(pi)) for pi in policy_targets] == [1, 0, 0]


def test_option_mode_falls_back_when_most_visited_child_is_illegal(capsys):
    root = _root_with_children([
        ((1, 0, 0), 10),
        ((0, 1, 0), 8),
        ((0, 0, 1), 7),
    ])
    priors, legal = _uniform_inputs()
    legal[0] = np.array([1, 0], dtype=bool)

    _policy_targets, selected = _mcts(enabled=True)._final_policy_from_visits(
        root,
        priors,
        legal,
        temperature=0.0,
        move_count=99,
        candidate_mode="option",
    )

    assert selected == [0, 1, 0]
    captured = capsys.readouterr()
    assert "[AZ][MCTS][JOINT_FALLBACK]" in captured.err


def test_joint_mode_keeps_legacy_independent_head_selection():
    root = _root_with_children([
        ((0, 0, 0), 10),
        ((1, 1, 0), 9),
        ((1, 0, 1), 9),
    ])
    priors, legal = _uniform_inputs()

    _policy_targets, selected = _mcts(enabled=True)._final_policy_from_visits(
        root,
        priors,
        legal,
        temperature=0.0,
        move_count=99,
        candidate_mode="joint",
    )

    assert selected == [1, 0, 0]
