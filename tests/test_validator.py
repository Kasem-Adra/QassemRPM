from qassemrpm.validator import validate_spec


def test_valid_spec_file():
    success, message = validate_spec("examples/hello.spec")

    assert success is True


def test_validator_returns_message():
    success, message = validate_spec("examples/hello.spec")

    assert isinstance(message, str)


# validator tests
