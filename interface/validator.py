from abc import ABC, abstractmethod
from typing import Any


class ValidatorInterface(ABC):

    @staticmethod
    @abstractmethod
    def validate(value: Any) -> bool:
        pass