from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess


@dataclass(slots=True)
class BuildResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


def create_workspace(topdir: Path) -> None:
    for directory in [
        "BUILD",
        "BUILDROOT",
        "RPMS",
        "SOURCES",
        "SPECS",
        "SRPMS",
        "logs",
    ]:
        (topdir / directory).mkdir(parents=True, exist_ok=True)


def build_spec(spec_path: str | Path, topdir: str | Path | None = None) -> BuildResult:
    spec = Path(spec_path)

    if not spec.exists():
        raise FileNotFoundError(f"SPEC file not found: {spec}")

    if shutil.which("rpmbuild") is None:
        raise RuntimeError(
            "rpmbuild was not found. Install rpm-build or use the container command later."
        )

    command = ["rpmbuild", "-ba", str(spec)]

    if topdir:
        topdir_path = Path(topdir)
        create_workspace(topdir_path)
        command[1:1] = ["--define", f"_topdir {topdir_path.resolve()}"]

    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )

    return BuildResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
