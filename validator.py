from pathlib import Path


REQUIRED_TAGS = [
    "Name",
    "Version",
    "Release",
    "Summary",
    "License",
]

REQUIRED_SECTIONS = [
    "%description",
    "%prep",
    "%build",
    "%install",
    "%files",
]


def validate_spec(path: str):
    spec_path = Path(path)

    if not spec_path.exists():
        return False, f"SPEC file not found: {path}"

    content = spec_path.read_text()

    errors = []

    # Validate required tags
    for tag in REQUIRED_TAGS:
        if f"{tag}:" not in content:
            errors.append(f"Missing required tag: {tag}")

    # Validate required sections
    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"Missing required section: {section}")

    if errors:
        return False, "\n".join(errors)

    return True, "SPEC validation passed successfully."
