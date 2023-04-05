import sys
import pygame
import timeit

from typing import List
from pygame import Surface, key
from pygame.sprite import Group, Sprite, AbstractGroup
from functions import draw_text
import config

class Entity(Sprite):
    def __init__(self, groups: Group | List[Group] = []):
        super().__init__(*groups if isinstance(groups, list) else [groups])
        self.name: str = "example_sprite"
        self.image = Surface((50, 50))
        self.rect = self.image.get_rect()
    
    def move(self, x:int = 0, y: int = 0):
        self.rect.move_ip(x, y)

class System(AbstractGroup):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
    
    @staticmethod
    def move(entity: Entity, x, y):
        entity.rect.move_ip(x, y)

def move(entity: Entity, x, y):
    entity.rect.move_ip(x, y)

pygame.init()
height = config.HEIGHT
width = config.WIDTH
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


system = System()
player = Entity(groups=system)
player.move(5, 5)

n_times = 100_000_000
    
while 1:
    # background
    screen.fill(config.BACKGROUND_COLOR)
    draw_text(screen, 'testsetsey', (330, 350))

    # get mouse position
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    keys = key.get_pressed()
    mov = [0, 0]
    if keys[pygame.K_RIGHT]:
        mov[0] += 1
    if keys[pygame.K_LEFT]:
        mov[0] += -1
    if keys[pygame.K_UP]:
        mov[1] += -1
    if keys[pygame.K_DOWN]:
        mov[1] += 1
    
    player.rect.center = 0, 0
    print('System::move', timeit.timeit(lambda: System.move(player, 1, 1), number=n_times))
    player.rect.center = 0, 0
    print('player::move', timeit.timeit(lambda: player.move(1, 1), number=n_times))
    player.rect.center = 0, 0
    print('func::move  ', timeit.timeit(lambda: player.move(1, 1), number=n_times))
    player.rect.center = 0, 0
    print('+'*50)

    System.move(player, *mov)
    system.draw(screen)
    system.update()

    pygame.display.flip()
    clock.tick(30)