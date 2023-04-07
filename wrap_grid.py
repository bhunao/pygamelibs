import random

from typing import Dict, Tuple

from pygame import Color, Surface

from constructor import constructor

position = Tuple[int, int]


class System:
    entities: Dict[Tuple[int], Color] = dict()
    surface: Surface

    def start(self):
        self.create('red', 5)
        return self

    def __init__(self, surface) -> None:
        self.surface = surface

    def create(self, entity, n=1):
        max_x, max_y = self.surface.get_size()
        for _ in range(n):
            for __ in range(5):
                pos = random.randint(0, max_x), random.randint(0, max_y)
                if self.entities.get(pos) is None:
                    break  # retry 5 times
            self.entities[pos] = entity

    def draw(self, pos, color) -> None:
        self.surface.set_at(pos, color)

    def move(self, pos: position, new_pos: position) -> position:
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
            return x, y
        return pos

    def update(self) -> None:
        new_dict = dict()
        for pos, entity in self.entities.items():
            new_pos = pos[0] + \
                random.randint(-1, 1), pos[1] + random.randint(-1, 1)
            pos = self.move(pos, new_pos)
            new_dict[pos] = entity
            self.draw(pos, entity)
        self.entities = new_dict


if __name__ == '__main__':
    constructor(System)()
