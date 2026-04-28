import argparse
import os

from app.runner.run import run1, run2
from app.runner.test import test

os.umask(0o022)

def main():
    parser = argparse.ArgumentParser(description="Hardware Monitor")

    subparsers = parser.add_subparsers(dest="command")

    # 🔹 run
    run_parser = subparsers.add_parser("run", help="Run collector")
    run_sub = run_parser.add_subparsers(dest="run_mode")

    run_sub.add_parser("base", help="CPU/Disk/Battery")
    run_sub.add_parser("node", help="Network nodes")
    run_sub.add_parser("all", help="Run everything")

    # 🔹 test
    subparsers.add_parser("test", help="Run tests")

    args = parser.parse_args()

    if args.command == "test":
        test()

    elif args.command == "run":
        print(args.run_mode)
        # default → base
        if args.run_mode is None or args.run_mode == "base":
            run1()

        elif args.run_mode == "node":
            run2()

        elif args.run_mode == "all":
            run1()
            run2()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
