import pytest
from rest_framework.exceptions import ValidationError

from ..extensions.format_validators import (
    EvenProjectNumberFormatValidator,
    IntegerListFormatValidator,
)


@pytest.mark.parametrize(
    "test_class,user_input,result",
    [
        (IntegerListFormatValidator, "1234, asdf", False),
        (IntegerListFormatValidator, "456456, 95174", True),
        (EvenProjectNumberFormatValidator, "AG-1234A", True),
        (EvenProjectNumberFormatValidator, "ZH-56789", True),
        (EvenProjectNumberFormatValidator, "AG1234A", False),
        (EvenProjectNumberFormatValidator, "AG-123", False),
        (EvenProjectNumberFormatValidator, "1234A-AG", False),
        (EvenProjectNumberFormatValidator, "AG-1234A,ZH-56789", True),
        (EvenProjectNumberFormatValidator, "AG-1234A, ZH-56789", True),
        (EvenProjectNumberFormatValidator, "AG-1234A,ZH-56789,BE-ABC12", True),
        (EvenProjectNumberFormatValidator, "AG-1234A, ZH-56789, BE-ABC12", True),
        (EvenProjectNumberFormatValidator, "AG-1234A,ZH-123", False),
        (EvenProjectNumberFormatValidator, "AG-1234A,,ZH-56789", False),
    ],
)
def test_format_validators(test_class, user_input, result):
    try:
        test_class().validate(user_input, None)
        assert result
    except ValidationError:
        assert not result
