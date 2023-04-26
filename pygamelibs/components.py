from typing import Callable
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
    def __init__(self, image: Surface, pos=None, depth=0, pos_type="center"):
        self.image = image
        self.rect = image.get_rect()
        self.depth: int = depth
        if pos:
            if pos_type == "center":
                self.rect.center = pos
            else:
                setattr(self.rect, pos_type, pos)

@dataclass
class ConstantVelocity:
    x: float = 1.0
    y: float = 1.0


class AnimatedRenderable:
    def __init__(self, images, pos=None, depth=0):
        self.images: Surface = images
        self.frame: int = 0
        self.last_update: int = 0
        self.depth: int = depth
        if pos:
            self.rect.center = pos


@dataclass
class Button:
    action: Callable
    state: str = "on"


@dataclass
class Enemy:
    name: str = "enemy"

@dataclass
class Player:
    pass


@dataclass
class Bullet:
    pass


@dataclass
class BackgroundObject:
    pass