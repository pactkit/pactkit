"""PactKit CLI — Spec-driven agentic DevOps toolkit.

Usage:
    pactkit init                  # Deploy Expert mode (default)
    pactkit init --mode common    # Deploy lightweight Common mode
    pactkit init -t /tmp/preview  # Preview to custom directory
    pactkit update                # Re-deploy (same as init, idempotent)
    pactkit version               # Show version
"""
import argparse
import sys

from pactkit import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="pactkit",
        description="PactKit — Spec-driven agentic DevOps toolkit",
    )
    subparsers = parser.add_subparsers(dest="command")

    # pactkit init
    init_parser = subparsers.add_parser("init", help="Deploy PactKit configuration")
    init_parser.add_argument(
        "--mode",
        choices=["expert", "common"],
        default="expert",
        help="Deployment mode: expert (full, default) or common (lightweight)",
    )
    init_parser.add_argument(
        "-t", "--target",
        type=str,
        default=None,
        help="Custom target directory (default: ~/.claude)",
    )

    # pactkit update (alias for init)
    update_parser = subparsers.add_parser("update", help="Re-deploy PactKit configuration")
    update_parser.add_argument(
        "--mode",
        choices=["expert", "common"],
        default="expert",
        help="Deployment mode: expert (full, default) or common (lightweight)",
    )
    update_parser.add_argument(
        "-t", "--target",
        type=str,
        default=None,
        help="Custom target directory (default: ~/.claude)",
    )

    # pactkit version
    subparsers.add_parser("version", help="Show PactKit version")

    args = parser.parse_args()

    if args.command in ("init", "update"):
        if args.mode == "expert":
            from pactkit.generators.deployer import deploy
            deploy()
        else:
            from pactkit.common_user import main as common_main
            # Simulate CLI args for common_user
            sys.argv = ["pactkit"]
            if args.target:
                sys.argv.extend(["-t", args.target])
            common_main()

    elif args.command == "version":
        print(f"PactKit v{__version__}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
