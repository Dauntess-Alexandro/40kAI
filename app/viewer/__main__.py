import argparse
import os

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
