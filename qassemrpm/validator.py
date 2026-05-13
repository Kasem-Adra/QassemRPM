from __future__ import annotations

from pathlib import Path
import re

MANDATORY_TAGS = ["Name", "Version", "Release", "Summary", "License", "URL"]


def validate_spec(spec_path: str | Path) -> tuple[bool, str]:
    path = Path(spec_path)
    if not path.exists():
        return False, f"File not found: {path}"

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return False, f"Error reading file: {exc}"

    missing: list[str] = []
    for tag in MANDATORY_TAGS:
        match = re.search(rf"^{re.escape(tag)}:\s*(.+)$", content, re.MULTILINE)
        if not match or not match.group(1).strip():
            missing.append(tag)

    if missing:
        return False, f"Missing mandatory tags: {', '.join(missing)}"

    return True, "SPEC file is valid."
