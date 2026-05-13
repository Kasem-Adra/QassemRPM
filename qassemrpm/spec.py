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


@dataclass(slots=True)
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


def _read_spec(path: str | Path) -> tuple[Path, str]:
    spec_path = Path(path)
    if not spec_path.exists():
        raise FileNotFoundError(f"SPEC file not found: {path}")
    return spec_path, spec_path.read_text(encoding="utf-8")


def _get_tag(content: str, tag: str) -> str | None:
    match = re.search(rf"^{re.escape(tag)}:\s*(.+)$", content, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else None


def _split_dependencies(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in re.split(r",|\s+", value) if item.strip()]


def parse_spec(path: str | Path) -> SpecInfo:
    _, content = _read_spec(path)

    return SpecInfo(
        name=_get_tag(content, "Name"),
        version=_get_tag(content, "Version"),
        release=_get_tag(content, "Release"),
        summary=_get_tag(content, "Summary"),
        license=_get_tag(content, "License"),
        build_arch=_get_tag(content, "BuildArch"),
        requires=_split_dependencies(_get_tag(content, "Requires")),
        build_requires=_split_dependencies(_get_tag(content, "BuildRequires")),
        sections=parse_spec_sections(path),
    )


def render_markdown_doc(spec_data: SpecInfo | dict) -> str:
    if isinstance(spec_data, dict):
        spec_data = SpecInfo(**spec_data)

    lines = [
        f"# {spec_data.name or 'Unknown Package'}",
        "",
        "## Package Information",
        "",
        f"- Version: {spec_data.version or 'Unknown'}",
        f"- Release: {spec_data.release or 'Unknown'}",
        f"- Summary: {spec_data.summary or 'Unknown'}",
        f"- License: {spec_data.license or 'Unknown'}",
    ]

    if spec_data.requires:
        lines.extend(["", "## Runtime Requirements", ""])
        lines.extend(f"- {dep}" for dep in spec_data.requires)

    if spec_data.build_requires:
        lines.extend(["", "## Build Requirements", ""])
        lines.extend(f"- {dep}" for dep in spec_data.build_requires)

    for section in ["description", "prep", "build", "install", "files", "changelog"]:
        content = spec_data.sections.get(section)
        if content:
            title = section.replace("_", " ").title()
            lines.extend(["", f"## {title}", "", content])

    return "\n".join(lines).rstrip() + "\n"


def parse_spec_sections(path: str | Path) -> dict[str, str]:
    spec_path, _ = _read_spec(path)
    lines = spec_path.read_text(encoding="utf-8").splitlines(keepends=True)

    sections: dict[str, str] = {}
    current_section: str | None = None
    buffer: list[str] = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("%"):
            section_name = stripped[1:].split()[0]

            if section_name in SECTION_NAMES:
                if current_section:
                    sections[current_section] = "".join(buffer).strip()

                current_section = section_name
                buffer = []
                continue

        if current_section:
            buffer.append(line)

    if current_section:
        sections[current_section] = "".join(buffer).strip()

    return sections
