import pytest

from requests.utils import from_key_val_list, parse_list_header


# Test cases
@pytest.mark.parametrize(
    'value, expected',
    [
        (None, None), # branch L326
        ([('key1', 'value1'), ('key2', 'value2')], {'key1': 'value1', 'key2': 'value2'}), # nominal case
        ([], {}), # limit case
        # unsupported types (branch L329)
        ('str', ValueError),
        (b'bytes', ValueError),
        (True, ValueError),
        (0, ValueError),
    ],
)
def test_from_key_val_list(value, expected):
    """Tests from_key_val_list will return a dictionary from a list of
    key-value pairs."""
    # If expected is an exception, test that it is raised
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            from_key_val_list(value)
    else:
        assert from_key_val_list(value) == expected


# Test cases
@pytest.mark.parametrize(
    'value, expected',
    [
        ('', []), # limit case
         # simple nominal cases
        ('token', ['token']),
        ('token, value', ['token', 'value']),
         # nominal cases with quoted values
        ('"token", value', ['token', 'value']),
        ('token, "quoted value"', ['token', 'quoted value']),
        # nominal case with quoted values containing commas
        ('token, "quoted value, with comma"', ['token', 'quoted value, with comma']),
    ],
)
def test_parse_list_header(value, expected):
    """Tests parse_list_header will return a list of values from a
    comma-separated string."""
    assert parse_list_header(value) == expected
