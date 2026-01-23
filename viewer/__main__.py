import argparse
import os

from viewer.app import launch


def main():
    parser = argparse.ArgumentParser(description="40kAI PySide6 Viewer")
    parser.add_argument(
        "--state",
        default=os.path.join(os.getcwd(), "gui", "state.json"),
        help="Path to state.json",
    )
    args = parser.parse_args()
    launch(args.state)


if __name__ == "__main__":
    main()
