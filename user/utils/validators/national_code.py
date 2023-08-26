from typing import Any

from interface import ValidatorInterface


class NationalCodeValidator(ValidatorInterface):

    """
    this class validates if  a particular value is a valid iranian natinoal code or not.
    """

    NATIONAL_CODE_LENGTH = 10

    def validate(value: Any) -> bool:
        if (
            isinstance(value, str)
            and value.isdigit()
            and  len(value) == NationalCodeValidator.NATIONAL_CODE_LENGTH
        ):
            return True
        return False # TODO  we can use more detailed and accurate validations here
