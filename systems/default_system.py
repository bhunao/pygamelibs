import random
from enum import Enum

from pygame import K_UP, K_LEFT, K_DOWN, K_RIGHT, Vector2, K_w

from typing import Dict, Tuple

from pygame import Color, Surface
from pygame import Rect, draw
from pygame.key import get_pressed

from config import position
from systems.base_system import System


class Movement(Enum):
    UP = K_UP
    RIGHT = K_RIGHT
    DOWN = K_DOWN
    LEFT = K_LEFT

class ActionMovement(Enum):
    UP = K_UP
    RIGHT = K_RIGHT
    DOWN = K_DOWN
    LEFT = K_LEFT

valid_moves = [move for move in Movement]

class DefaultSystem(System):
    entities: Dict[Tuple[int, int], Color]
    surface: Surface

    def __init__(self, surface) -> None:
        self.surface = surface
        self.entities = dict()
    
    def keyboard_movement(self, rect: Rect):
        keys = get_pressed()
        add_to_pos = Vector2(0, 0)
        if keys[K_w]:
            print("asd")
            add_to_pos.y = 1
        if keys[K_RIGHT]:
            add_to_pos.x = 1
        if keys[K_DOWN]:
            add_to_pos.y = -1
        if keys[K_LEFT]:
            add_to_pos.x = -1
        
        pos = Vector2(rect.center)
        new_pos = pos + add_to_pos
        self.move(pos, (new_pos.x, new_pos.y), rect)


    def start(self):
        style = {
            "rect": Rect(0, 0, 50, 50),
            "color": "purple",
            "border_radius": 10
        }
        self.create(5, **style)
        return self

    def create(self, n=1, **style):
        max_x, max_y = self.surface.get_size()
        for _ in range(n):
            for __ in range(5):
                pos = random.randint(0, max_x), random.randint(0, max_y)
                if self.entities.get(pos) is None:
                    break  # retry 5 times
            style["rect"].center = pos
            self.entities[pos] =style

    def draw(self, **style) -> None:
        match style:
            case {"image": _ }:
                raise NotImplementedError
            case {"rect": _, "color": _, "border_radius": _ }:
                draw.rect(self.surface, **style)
            case _:
                raise NotImplementedError

    def move(self, pos: position, new_pos: position, rect: Rect) -> position:
        min_point = 0, 0
        max_point = self.surface.get_size()
        if self.entities.get(new_pos) is None:
            x, y = new_pos
            min_x, min_y = min_point
            max_x, max_y = max_point
            if x < min_x:
                x = max_x
            elif x > max_x:
                x = min_x
            if y < min_y:
                y = max_y
            elif y > max_y:
                y = min_y
            pos = x, y
        rect.center = pos
        return pos

    def update(self) -> None:
        new_dict = dict()
        for pos, style in self.entities.items():
            new_pos = pos[0] + \
                random.randint(-1, 1), pos[1] + random.randint(-1, 1)
            new_pos = pos
            pos = self.move(pos, new_pos, style["rect"])
            new_dict[pos] = style
            self.draw(**style)
        self.entities = new_dict