"""Построение локальной value-сети MuZero (GMZ/SMZ) из remote_search_cfg + загрузка весов.

Используется и сервером (DRY), и env-воркером для реакций. Конструкция идентична серверной
(gmz_inference_server / smz_inference_server), чтобы веса грузились в совместимую форму.
"""
from __future__ import annotations


def _dims(search_cfg_payload: dict):
    obs_dim = int(search_cfg_payload.get("obs_dim", 0))
    action_sizes = [int(x) for x in search_cfg_payload.get("action_sizes", [])]
    if obs_dim <= 0 or not action_sizes:
        raise ValueError(
            "muzero_value_net_builder: пустой search_cfg (obs_dim<=0 или action_sizes=[]). "
            "Где: build_*_net_from_search_cfg. Что делать: дождаться публикации "
            "*_remote_search_cfg.json рядом с весами (actor_sync/SMB)."
        )
    rest = {
        "latent_dim": int(search_cfg_payload.get("latent_dim", 256)),
        "hidden_dim": int(search_cfg_payload.get("hidden_dim", 256)),
        "num_layers": int(search_cfg_payload.get("num_layers", 2)),
        "action_embed_dim": int(search_cfg_payload.get("action_embed_dim", 64)),
    }
    return obs_dim, action_sizes, rest


def build_gmz_net_from_search_cfg(search_cfg_payload: dict, *, device):
    from core.models.gumbel_muzero_model import GumbelMuZeroNet

    obs_dim, action_sizes, rest = _dims(search_cfg_payload)
    net = GumbelMuZeroNet(obs_dim=obs_dim, action_sizes=action_sizes, **rest).to(device)
    net.eval()
    return net


def build_smz_net_from_search_cfg(search_cfg_payload: dict, *, device):
    from core.models.sampled_muzero_model import make_sampled_muzero_net

    obs_dim, action_sizes, rest = _dims(search_cfg_payload)
    net = make_sampled_muzero_net(obs_dim=obs_dim, action_sizes=action_sizes, **rest).to(device)
    net.eval()
    return net


def load_value_net_weights(net, weights_path: str, *, device=None) -> bool:
    """Загрузить веса в сеть (strict=False). Нет файла/ошибка → False, без исключения."""
    import torch

    from core.models.utils import normalize_state_dict

    try:
        sd = torch.load(weights_path, map_location=device or torch.device("cpu"))
        net.load_state_dict(normalize_state_dict(sd), strict=False)
        return True
    except Exception:
        return False


def write_init_weights_from_cfg(search_cfg_path: str, out_path: str, *, algo: str = "gmz", device=None) -> str:
    """Bootstrap: построить сеть из search_cfg и сохранить СЛУЧАЙНО инициализированные веса.

    Позволяет поднять remote IS без предварительного обучения на ПК1 — сервер стартует с
    рандома, learner потом синканёт настоящие веса (формы совпадают, обе строятся из cfg).
    Возвращает out_path. Бросает с понятным сообщением, если cfg не читается/битый.
    """
    import json

    import torch

    dev = device or torch.device("cpu")
    try:
        with open(search_cfg_path, encoding="utf-8") as fh:
            payload = json.load(fh)
    except OSError as exc:
        raise OSError(
            f"write_init_weights_from_cfg: не удалось прочитать search_cfg {search_cfg_path}: {exc}. "
            f"Где: bootstrap весов. Что делать: укажи путь к *_remote_search_cfg.json (на шаре/actor_sync)."
        ) from exc
    net = build_smz_net_from_search_cfg(payload, device=dev) if str(algo).lower() == "smz" \
        else build_gmz_net_from_search_cfg(payload, device=dev)
    torch.save(net.state_dict(), out_path)
    return out_path
