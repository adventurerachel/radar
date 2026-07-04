from abc import ABC, abstractmethod


class BaseMonitor(ABC):
    name: str

    @abstractmethod
    def collect(self) -> dict:
        pass