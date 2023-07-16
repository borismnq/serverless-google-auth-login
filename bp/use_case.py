from abc import ABC
from abc import abstractmethod


class UseCase(ABC):
    @abstractmethod
    def run_use_case(self, params):
        pass
