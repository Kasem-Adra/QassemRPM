from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .builder import build_spec
from .spec import parse_spec, render_markdown_doc


def _cmd_info(args: argparse.Namespace) -> int:
    info = parse_spec(args.spec)
    print(f"Name: {info.name}")
    print(f"Version: {info.version}")
    print(f"Release: {info.release}")
    if info.summary:
        print(f"Summary: {info.summary}")
    if info.build_requires:
        print("BuildRequires:")
        for dep in info.build_requires:
            print(f"  - {dep}")
    return 0


def _cmd_doc(args: argparse.Namespace) -> int:
    info = parse_spec(args.spec)
    content = render_markdown_doc(info)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        print(f"Documentation written to {output}")
    else:
        print(content, end="")
    return 0


def _cmd_build(args: argparse.Namespace) -> int:
    result = build_spec(args.spec, topdir=args.topdir)
    print("$ " + " ".join(result.command))
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="qassemrpm", description="QassemRPM v0.1 - modern RPM packaging assistant")
    parser.add_argument("--version", action="version", version=f"QassemRPM {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    info = sub.add_parser("info", help="Read basic metadata from a SPEC file")
    info.add_argument("spec")
    info.set_defaults(func=_cmd_info)

    doc = sub.add_parser("doc", help="Generate Markdown documentation from a SPEC file")
    doc.add_argument("spec")
    doc.add_argument("-o", "--output")
    doc.set_defaults(func=_cmd_doc)

    build = sub.add_parser("build", help="Build an RPM using rpmbuild")
    build.add_argument("spec")
    build.add_argument("--topdir")
    build.set_defaults(func=_cmd_build)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
