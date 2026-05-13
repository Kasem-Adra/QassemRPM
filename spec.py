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


def parse_spec(path: str):
    """
    Parse basic SPEC metadata.
    """
    spec_path = Path(path)

    if not spec_path.exists():
        raise FileNotFoundError(f"SPEC file not found: {path}")

    content = spec_path.read_text()

    data = {}

    patterns = {
        "name": r"^Name:\s*(.+)$",
        "version": r"^Version:\s*(.+)$",
        "release": r"^Release:\s*(.+)$",
        "summary": r"^Summary:\s*(.+)$",
        "license": r"^License:\s*(.+)$",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.MULTILINE)
        data[key] = match.group(1).strip() if match else None

    return data


def render_markdown_doc(spec_data: dict):
    """
    Render SPEC metadata into markdown.
    """
    return f"""# {spec_data.get('name', 'Unknown Package')}

## Package Information

- Version: {spec_data.get('version')}
- Release: {spec_data.get('release')}
- Summary: {spec_data.get('summary')}
- License: {spec_data.get('license')}
"""


def parse_spec_sections(path: str):
    """
    Parse SPEC sections into a dictionary.
    """
    with open(path, "r") as f:
        lines = f.readlines()

    sections = {}
    current_section = None
    buffer = []

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
