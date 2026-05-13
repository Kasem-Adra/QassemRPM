import argparse
import sys
from pathlib import Path

from qassemrpm.builder import build_spec


def main() -> None:
    parser = argparse.ArgumentParser(
        description="QassemRPM: A modern RPM packaging tool for developers."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    build_parser = subparsers.add_parser(
        "build",
        help="Build an RPM from a SPEC file",
    )
    build_parser.add_argument(
        "spec",
        help="Path to the .spec file, for example: examples/hello.spec",
    )
    build_parser.add_argument(
        "--topdir",
        help="Custom RPM workspace directory (_topdir)",
        default=None,
    )

    args = parser.parse_args()

    if args.command == "build":
        spec_path = Path(args.spec)

        if not spec_path.exists():
            print(f"❌ Error: SPEC file not found: {spec_path}")
            sys.exit(1)

        print(f"🛠️  Building RPM from: {spec_path}")

        try:
            result = build_spec(spec_path, topdir=args.topdir)
        except RuntimeError as error:
            print(f"❌ {error}")
            sys.exit(1)

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print("✅ Build completed successfully!")
            sys.exit(0)

        print(f"🛑 Build failed with exit code {result.returncode}")
        sys.exit(result.returncode)

    parser.print_help()


if __name__ == "__main__":
    main()
