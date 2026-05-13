SECTION_NAMES = [
    "description",
    "prep",
    "build",
    "install",
    "files",
    "changelog",
]


def parse_spec_sections(path: str):
    with open(path, "r") as f:
        lines = f.readlines()

    sections = {}
    current_section = None
    buffer = []

    for line in lines:
        stripped = line.strip()

        # Detect section start
        if stripped.startswith("%"):
            section_name = stripped[1:].split()[0]

            if section_name in SECTION_NAMES:
                # Save previous section
                if current_section:
                    sections[current_section] = "".join(buffer).strip()

                current_section = section_name
                buffer = []
                continue

        # Append content
        if current_section:
            buffer.append(line)

    # Save last section
    if current_section:
        sections[current_section] = "".join(buffer).strip()

    return sections
