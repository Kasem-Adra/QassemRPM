from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable

_FIELD_RE = re.compile(r"^(?P<key>[A-Za-z][A-Za-z0-9_]*):\s*(?P<value>.*)$")
_SECTION_RE = re.compile(r"^%(?P<section>[a-zA-Z][\w-]*)\b(?P<rest>.*)$")

@dataclass(slots=True)
class SpecInfo:
    path: Path
    fields: dict[str, str] = field(default_factory=dict)
    sections: dict[str, list[str]] = field(default_factory=dict)
    build_requires: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.fields.get("Name", self.path.stem)

    @property
    def version(self) -> str:
        return self.fields.get("Version", "unknown")

    @property
    def release(self) -> str:
        return self.fields.get("Release", "unknown")

    @property
    def summary(self) -> str:
        return self.fields.get("Summary", "")


def _split_dependency_value(value: str) -> list[str]:
    parts: list[str] = []
    for item in value.split(","):
        clean = item.strip()
        if clean:
            parts.append(clean)
    return parts


def parse_spec(path: str | Path) -> SpecInfo:
    spec_path = Path(path)
    if not spec_path.exists():
        raise FileNotFoundError(f"SPEC file not found: {spec_path}")

    info = SpecInfo(path=spec_path)
    current_section: str | None = None

    for raw_line in spec_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.rstrip()
        section_match = _SECTION_RE.match(line.strip())
        if section_match:
            current_section = section_match.group("section").lower()
            info.sections.setdefault(current_section, [])
            rest = section_match.group("rest").strip()
            if rest:
                info.sections[current_section].append(rest)
            continue

        if current_section:
            info.sections.setdefault(current_section, []).append(line)
            continue

        field_match = _FIELD_RE.match(line)
        if not field_match:
            continue

        key = field_match.group("key")
        value = field_match.group("value").strip()
        info.fields[key] = value

        if key == "BuildRequires":
            info.build_requires.extend(_split_dependency_value(value))
        elif key == "Requires":
            info.requires.extend(_split_dependency_value(value))

    return info


def render_markdown_doc(info: SpecInfo) -> str:
    lines = [
        f"# {info.name}",
        "",
        f"**Version:** {info.version}",
        f"**Release:** {info.release}",
        "",
    ]
    if info.summary:
        lines += ["## Summary", "", info.summary, ""]

    if info.build_requires:
        lines += ["## Build Requirements", ""]
        lines += [f"- `{dep}`" for dep in info.build_requires]
        lines.append("")

    if info.requires:
        lines += ["## Runtime Requirements", ""]
        lines += [f"- `{dep}`" for dep in info.requires]
        lines.append("")

    if "description" in info.sections:
        description = "\n".join(info.sections["description"]).strip()
        if description:
            lines += ["## Description", "", description, ""]

    if "changelog" in info.sections:
        changelog = "\n".join(info.sections["changelog"]).strip()
        if changelog:
            lines += ["## Changelog", "", "```text", changelog, "```", ""]

    return "\n".join(lines).rstrip() + "\n"
