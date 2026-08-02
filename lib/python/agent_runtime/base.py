from abc import ABC, abstractmethod


class BaseAgent(ABC):

    NAME = "base"

    @abstractmethod
    def run(self, context):
        pass
