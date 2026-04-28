import argparse
import os

from app.config import load_config, run_from_config
from app.runner.test import test

os.umask(0o022)

config = load_config()

def main():
    parser = argparse.ArgumentParser(description="Hardware Monitor")

    subparsers = parser.add_subparsers(dest="command")

    # 🔹 run
    run_parser = subparsers.add_parser("run", help="Run collector")
    run_sub = run_parser.add_subparsers(dest="run_mode")

    for run_name, run_cfg in config.get("runs", {}).items():
        help_text = run_cfg.get("description", f"Run {run_name}")
        run_sub.add_parser(run_name, help=help_text)

    # 🔹 test
    subparsers.add_parser("test", help="Run tests")

    args = parser.parse_args()

    if args.command == "test":
        test()

    elif args.command == "run":
        mode = args.run_mode or "base"
        run_from_config(mode, config)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
