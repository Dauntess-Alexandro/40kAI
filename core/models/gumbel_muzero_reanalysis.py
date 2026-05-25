from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import torch


@dataclass
class GumbelMuZeroReanalysisConfig:
    """Configuration for GumbelMuZero reanalysis.

    MuZero / EfficientZero reanalysis: periodically re-compute policy targets
    for older transitions using the current (improved) network's search,
    rather than relying on the stale policy from self-play.
    """
    fast_sims: int = 16  # number of MCTS simulations for reanalysis (lighter than full search)
    batch_size: int = 64  # how many transitions to reanalysis per call


class GumbelMuZeroReanalyzer:
    """Reanalyzer that uses real search to update stale policy targets.

    Every fraction of training steps, this samples old transitions from the
    replay buffer and re-runs a lightweight search (fast_sims) on each state
    to produce higher-quality policy targets than the original self-play visit counts.
    """

    def __init__(
        self,
        config: Optional[GumbelMuZeroReanalysisConfig] = None,
        search: Optional["GumbelMuZeroSearch"] = None,
        device: Optional[torch.device] = None,
    ):
        self._cfg = config or GumbelMuZeroReanalysisConfig()
        self._search = search  # GumbelMuZeroSearch instance
        self._device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @property
    def config(self) -> GumbelMuZeroReanalysisConfig:
        return self._cfg

    def update_replay_with_reanalysis(self, replay, net) -> int:
        """Run reanalysis on a random sample of the replay buffer.

        Args:
            replay: GumbelMuZeroReplayBuffer instance
            net: current GMZ network (used as fallback when search is unavailable)

        Returns:
            Number of transitions updated.
        """
        if len(replay) == 0:
            return 0

        batch_size = max(1, int(self._cfg.batch_size))
        transitions = replay.sample(batch_size)

        n_updated = 0
        for tr in transitions:
            updated = self._update_one(tr, net)
            if updated:
                n_updated += 1

        return n_updated

    def _update_one(self, tr, net) -> bool:
        """Update policy targets for a single transition using real search.

        If self._search is available, runs a lightweight search using the stored
        legal_masks_by_head to produce fresh policy targets. Otherwise falls back
        to softmax(initial_inference logits).
        """
        # B2: Check for stored legal masks (needed for real search)
        legal_masks = getattr(tr, "legal_masks_by_head", None)
        obs_t = torch.as_tensor(
            np.asarray(tr.state, dtype=np.float32),
            device=self._device,
        ).unsqueeze(0)

        if legal_masks is not None and self._search is not None:
            # Real search path: use stored legal masks to run lightweight search
            try:
                obs_np = np.asarray(tr.state, dtype=np.float32)
                legal_masks_np = [np.asarray(m, dtype=bool) for m in legal_masks]
                pi_targets_new, _, _, _ = self._search.run(
                    obs=obs_np,
                    legal_masks_by_head=legal_masks_np,
                    deterministic=True,
                )
                # Update transition in-place
                tr.policy_targets = [np.asarray(p, dtype=np.float32) for p in pi_targets_new]
                return True
            except Exception:
                # Fallback on search error
                pass

        # Fallback: use initial inference softmax (original behavior)
        try:
            logits_list, _, _, _, _, _ = net.initial_inference(obs_t)
            new_policy_targets = []
            for head_logits in logits_list:
                probs = torch.softmax(head_logits.squeeze(0), dim=0).cpu().numpy().astype(np.float32)
                new_policy_targets.append(probs)
            tr.policy_targets = new_policy_targets
            return True
        except Exception:
            return False
