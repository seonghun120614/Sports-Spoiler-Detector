from abc import ABC, abstractmethod
from typing import Any

from src.domains.SpoilerInformation import SpoilerElement

"""
Abstract Class

for homogeneity about other feature extractors or detector
"""
class BaseModel(ABC):

    @abstractmethod
    def predict(self, *arg: Any) -> list[list[SpoilerElement]]:
        """predicting label from target"""
        pass