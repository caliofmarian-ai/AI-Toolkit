from abc import ABC, abstractmethod

class Rule(ABC):

    NAME = "Unnamed Rule"

    @abstractmethod
    def evaluate(self, report):
        pass
