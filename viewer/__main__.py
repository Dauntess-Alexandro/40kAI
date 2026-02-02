import argparse
import os
import torch

from viewer.app import launch


def main():
    parser = argparse.ArgumentParser(description="40kAI PySide6 Viewer")
    parser.add_argument(
        "--state",
        default=os.path.join(os.getcwd(), "gui", "state.json"),
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
