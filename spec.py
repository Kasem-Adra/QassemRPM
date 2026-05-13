from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

SECTION_NAMES = [
    "description",
    "prep",
    "build",
    "install",
    "files",
    "changelog",
]


@dataclass
class SpecInfo:
    name: str | None = None
    version: str | None = None
    release: str | None = None
    summary: str | None = None
    license: str | None = None
    build_arch: str | None = None
    requires: list[str] = field(default_factory=list)
    build_requires: list[str] = field(default_factory=list)
    sections: dict[str, str] = field(default_factory=dict)


def _read_spec(path: str | Path) -> str:
    spec_path = Path(path)
    if not spec_path.exists():
        raise FileNotFoundError(f"SPEC file not found: {path}")
    return spec_path.read_text(encoding="utf-8")


def _tag_value(content: str, tag: str) -> str | None:
    match = re.search(rf"^{re.escape(tag)}:\s*(.+)$", content, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else None


def _split_dependencies(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in re.split(r",\s*", value) if item.strip()]


def parse_spec(path: str | Path) -> SpecInfo:
    """Parse basic RPM SPEC metadata and sections."""
    content = _read_spec(path)
    return SpecInfo(
        name=_tag_value(content, "Name"),
        version=_tag_value(content, "Version"),
        release=_tag_value(content, "Release"),
        summary=_tag_value(content, "Summary"),
        license=_tag_value(content, "License"),
        build_arch=_tag_value(content, "BuildArch"),
        requires=_split_dependencies(_tag_value(content, "Requires")),
        build_requires=_split_dependencies(_tag_value(content, "BuildRequires")),
        sections=parse_spec_sections(path),
    )


def parse_spec_sections(path: str | Path) -> dict[str, str]:
    """Parse known SPEC sections into a dictionary."""
    content = _read_spec(path)
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("%"):
            section_name = stripped[1:].split()[0]
            if section_name in SECTION_NAMES:
                current_section = section_name
                sections[current_section] = []
                continue

        if current_section:
            sections[current_section].append(line)

    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def render_markdown_doc(spec_data: SpecInfo | dict) -> str:
    """Render parsed SPEC information into Markdown documentation."""
    if isinstance(spec_data, dict):
        info = SpecInfo(
            name=spec_data.get("name"),
            version=spec_data.get("version"),
            release=spec_data.get("release"),
            summary=spec_data.get("summary"),
            license=spec_data.get("license"),
            requires=spec_data.get("requires", []),
            build_requires=spec_data.get("build_requires", []),
            sections=spec_data.get("sections", {}),
        )
    else:
        info = spec_data

    def bullet_list(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) if items else "- None"

    changelog = info.sections.get("changelog", "No changelog found.")

    return f"""# {info.name or 'Unknown Package'}

## Package Information

- Version: {info.version or 'Unknown'}
- Release: {info.release or 'Unknown'}
- Summary: {info.summary or 'Unknown'}
- License: {info.license or 'Unknown'}

## Runtime Requirements

{bullet_list(info.requires)}

## Build Requirements

{bullet_list(info.build_requires)}

## Changelog

{changelog}
"""
