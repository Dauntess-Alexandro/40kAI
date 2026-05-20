import argparse
import os
import sys

# До любого импорта Qt: иначе QQuickWidget фиксирует RHI=D3D11 и QOpenGLWidget не рисуется.
# Подробнее: app.viewer.app дублирует это перед import PySide6.
_v = os.environ.get("VIEWER_QSG_RHI_BACKEND", "").strip()
if _v:
    os.environ["QSG_RHI_BACKEND"] = _v
elif sys.platform == "win32":
    os.environ.setdefault("QSG_RHI_BACKEND", "opengl")

from app.viewer.app import launch
from project_paths import STATE_JSON_PATH


def main():
    parser = argparse.ArgumentParser(description="40kAI PySide6 Viewer")
    parser.add_argument(
        "--state",
        default=str(STATE_JSON_PATH),
        help="Path to state.json",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_PATH", "None"),
        help="Путь к pickle-модели или None для последней.",
    )
    args = parser.parse_args()
    launch(args.state, model_path=args.model)


if __name__ == "__main__":
    main()
