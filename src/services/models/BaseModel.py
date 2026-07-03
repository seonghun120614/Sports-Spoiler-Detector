from abc import ABC, abstractmethod
from typing import Any

"""
Abstract Class

for homogeneity about other feature extractors or detector
"""
class BaseModel(ABC):

    @abstractmethod
    def predict(self, arg: Any):
        """predicting label from target"""
        pass

    @abstractmethod
    def batch_predict(self, arg: Any):
        """predicting labels from target"""
        pass