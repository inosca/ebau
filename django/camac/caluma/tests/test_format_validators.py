import pytest
from rest_framework.exceptions import ValidationError

from ..extensions.format_validators import IntegerListFormatValidator


@pytest.mark.parametrize(
    "test_class,user_input,result",
    [
        (IntegerListFormatValidator, "1234, asdf", False),
        (IntegerListFormatValidator, "456456, 95174", True),
    ],
)
def test_format_validators(test_class, user_input, result):
    try:
        test_class().validate(user_input, None)
        assert result
    except ValidationError:
        assert not result
