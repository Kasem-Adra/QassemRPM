from qassemrpm.spec import parse_spec_sections


def test_parse_spec_sections():
    sections = parse_spec_sections("examples/hello.spec")

    assert isinstance(sections, dict)


def test_description_section_exists():
    sections = parse_spec_sections("examples/hello.spec")

    assert "description" in sections


def test_files_section_exists():
    sections = parse_spec_sections("examples/hello.spec")

    assert "files" in sections
