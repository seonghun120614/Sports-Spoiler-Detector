from abc import ABC, abstractmethod
from typing import Any

"""
Abstract Class

for homogeneity about other feature extractors or detector
"""
class BaseModel(ABC):

    @abstractmethod
    def extract(self, arg: Any):
        """extracting labels from target"""
        pass