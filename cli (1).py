from pathlib import Path

from qassemrpm.spec import parse_spec, render_markdown_doc


def test_parse_example_spec():
    info = parse_spec(Path(__file__).parent.parent / "examples" / "hello.spec")
    assert info.name == "hello-qassem"
    assert info.version == "0.1.0"
    assert "python3" in info.requires
    assert "make" in info.build_requires


def test_render_markdown_doc():
    info = parse_spec(Path(__file__).parent.parent / "examples" / "hello.spec")
    doc = render_markdown_doc(info)
    assert "# hello-qassem" in doc
    assert "## Build Requirements" in doc
    assert "## Changelog" in doc
