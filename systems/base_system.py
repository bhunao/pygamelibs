from abc import ABC, abstractmethod
from typing import Dict, Tuple

from pygame import Color, Surface
from config import position


class System(ABC):
    entities: Dict[Tuple[int], Color]
    surface: Surface

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def create(self, entity, n=1):
        pass

    @abstractmethod
    def draw(self, pos, color) -> None:
        pass

    @abstractmethod
    def move(self, pos: position, new_pos: position) -> position:
        pass

    @abstractmethod
    def update(self) -> None:
        pass