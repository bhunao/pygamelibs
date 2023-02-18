import sys
import pygame

from sprites.example import Sprite
from config import configs


pygame.init()
height = configs["screen"]["width"]
width = configs["screen"]["height"]
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

group = pygame.sprite.Group()
sprite = Sprite(group)

while 1:
    # background
    screen.fill("gray")

    # get mouse position
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    group.draw(screen)
    group.update()

    pygame.display.flip()
    clock.tick(60)
