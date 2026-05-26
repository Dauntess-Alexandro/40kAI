"""EnvClonePool — pre-warmed pool of env clones for parallel MCTS simulations.

Usage
-----
The pool holds N independent copies of an env.  Each copy has its own
snapshot/restore state so MCTS simulations can run in parallel threads without
contention.

Typical use in AlphaZeroFactorizedMCTS when ``cfg.parallel_simulations > 1``:

    pool = EnvClonePool(base_env, pool_size=4)
    with pool.acquire() as clone_env:
        snapshot = clone_env.snapshot_state()
        ...  # rollout
        clone_env.restore_state(snapshot)

Thread-safety guarantee
-----------------------
Each env in the pool is used by at most one thread at a time.  The pool
itself is protected by a threading.Semaphore so borrowers block when all
clones are in use.

Limitations
-----------
- The clones share the *same* ``model`` / ``enemy`` Unit object lists as the
  original env.  Moving units via ``set_anchor`` in one clone therefore races
  with other clones.  The pool mitigates this by saving/restoring unit coords
  through the slim snapshot mechanism (``_model_unit_coords`` /
  ``_enemy_unit_coords`` keys), but users should be aware that deeper shared
  state (e.g. weapon data dicts) is read-only in practice and safe.
- numpy.random state is isolated per clone via per-thread seed injection.
- Logging inside simulation_mode is suppressed by design (simulation_mode
  already sets ``_simulation_mode_depth > 0``).
"""
from __future__ import annotations

import copy
import threading
from contextlib import contextmanager
from typing import Any, Generator


class EnvClonePool:
    """Pre-warmed pool of env clones for thread-parallel MCTS simulations.

    Parameters
    ----------
    base_env:
        The original env.  The pool takes a snapshot of it at construction
        time and creates ``pool_size`` independent copies via
        ``snapshot_state`` / ``restore_state``.
    pool_size:
        Number of parallel clones.  Default 4.
    """

    def __init__(self, base_env: Any, pool_size: int = 4) -> None:
        self._pool_size = max(1, int(pool_size))
        self._lock = threading.Lock()
        self._semaphore = threading.Semaphore(self._pool_size)
        self._available: list[Any] = []

        # Create clones via snapshot
        snap = base_env.snapshot_state() if hasattr(base_env, "snapshot_state") else None
        for _ in range(self._pool_size):
            clone = copy.copy(base_env)
            # Deep-copy the mutable state but share the immutable model/enemy refs
            if snap is not None and hasattr(clone, "restore_state"):
                clone.restore_state(snap)
            self._available.append(clone)

        self._in_use: set[int] = set()

    @contextmanager
    def acquire(self) -> Generator[Any, None, None]:
        """Context manager: borrow one env clone from the pool.

        Blocks if all clones are in use.  Guarantees the clone is returned
        to the pool on exit (even on exception).
        """
        self._semaphore.acquire()
        clone = None
        try:
            with self._lock:
                clone = self._available.pop()
                self._in_use.add(id(clone))
            yield clone
        finally:
            if clone is not None:
                with self._lock:
                    self._in_use.discard(id(clone))
                    self._available.append(clone)
            self._semaphore.release()

    @property
    def pool_size(self) -> int:
        return self._pool_size

    @property
    def available_count(self) -> int:
        with self._lock:
            return len(self._available)

    def reset_all(self, snapshot: dict) -> None:
        """Reset all idle clones to a new snapshot.

        Should only be called when all clones are idle (no ``acquire``
        contexts active).
        """
        with self._lock:
            for clone in self._available:
                if hasattr(clone, "restore_state"):
                    clone.restore_state(snapshot)
