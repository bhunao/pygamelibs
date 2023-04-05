import sys
import pygame

import config

from abc import ABC
from typing import List

from pygame import display, Surface, init
from pygame.time import Clock
from pygame.transform import scale


class Entity(ABC):
    pos: List[int] = [0, 0]

class System(ABC):
    _entities: List[Entity] = []
    surface: Surface

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

    def draw(self, entity: Entity) -> bool:
        print(entity.pos)
        self.surface.set_at(entity.pos, "red")
        return True

    @staticmethod
    def move(entity: Entity, pos: list[int]) -> bool:
        entity.pos[0] += pos[0]
        entity.pos[1] += pos[1]
        return True

def main():
    init()
    UPSCALE = 5
    WIDTH = config.WIDTH / UPSCALE
    HEIGHT = config.HEIGHT / UPSCALE

    screen = display.set_mode((WIDTH*UPSCALE, HEIGHT*UPSCALE))
    down_scale_screen = Surface((WIDTH, HEIGHT))
    clock = Clock()

    s = System(down_scale_screen)
    p = Entity()

    while 1:
        down_scale_screen.fill("gray")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        
        s.draw(p)
        print(p.pos)
        s.move(p, [1, 1])
        scaled_win = scale(down_scale_screen, (WIDTH*UPSCALE, HEIGHT*UPSCALE))
        screen.blit(scaled_win, (0, 0))
        pygame.display.flip()
        clock.tick(15)

main()