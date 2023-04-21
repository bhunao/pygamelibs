from typing import Callable, List
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
    def __init__(self, image: Surface, posx, posy, depth=0):
        self.image = image
        self.rect = image.get_rect()
        self.depth: int = depth
        self.rect.center = posx, posy
        self.w: int = image.get_width()
        self.h: int = image.get_height()


@dataclass
class ConstantVelocity:
    x: float = 1.0
    y: float = 1.0


class AnimatedRenderable:
    def __init__(self, images, posx, posy, depth=0):
        self.images: Surface = images
        self.frame: int = 0
        self.last_update: int = 0
        self.depth: int = depth
        self.x: int = posx
        self.y: int = posy
        self.w: int = images[0].get_width()
        self.h: int = images[0].get_height()


@dataclass
class Button:
    action: Callable
    state: str = "on"
