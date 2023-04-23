from pygame import Surface
from dataclasses import dataclass


@dataclass
class KeyboardInput:
    pass

@dataclass
class Velocity:
        x: float = 0.0
        y: float = 0.0


class Renderable:
    def __init__(self, image, posx, posy, depth=0):
        self.image: Surface = image
        self.depth: int = depth
        self.x: int = posx
        self.y: int = posy
        self.w: int = image.get_width()
        self.h: int = image.get_height()
