import argparse
import os

from app.run import run
from app.test import test

os.umask(0o022)

def main():
    parser = argparse.ArgumentParser(description="Hardware Monitor")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("run", help="Run collector")
    subparsers.add_parser("test", help="Run tests")

    args = parser.parse_args()

    if args.command == "test":
        test()
    else:
        run()

if __name__ == "__main__":
    main()