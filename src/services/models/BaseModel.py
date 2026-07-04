from abc import ABC, abstractmethod
from typing import Any

from src.services.domains.SpoilerInformation import SpoilerElement

"""
Abstract Class

for homogeneity about other feature extractors or detector
"""
class BaseModel(ABC):

    @abstractmethod
    def predict(self, *arg: Any) -> Any:
        """predicting label from target"""
        pass