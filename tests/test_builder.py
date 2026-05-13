from pathlib import Path

from qassemrpm.builder import create_workspace


def test_create_workspace(tmp_path: Path):
    create_workspace(tmp_path)

    for directory in [
        "BUILD",
        "BUILDROOT",
        "RPMS",
        "SOURCES",
        "SPECS",
        "SRPMS",
        "logs",
    ]:
        assert (tmp_path / directory).exists()
