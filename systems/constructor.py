from enum import Enum
import sys
import pygame

from config import WIDTH, HEIGHT, UPSCALE

from pygame import display, Surface, init
from pygame.time import Clock
from pygame.transform import scale


def wrap_grid_builder(system, width, height, upscale):
    init()
    width = width / upscale
    height = height / upscale

    screen = display.set_mode((width*upscale, height*upscale))
    down_scale_screen = Surface((width, height))
    clock = Clock()

    system = system(down_scale_screen).start()

    while True:
        down_scale_screen.fill("gray")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        system.update()

        scaled_win = scale(down_scale_screen, (width*upscale, height*upscale))
        screen.blit(scaled_win, (0, 0))
        pygame.display.flip()
        clock.tick(15)


def default_builder(system, width, height, upscale):
    init()
    width = width / upscale
    height = height / upscale

    screen = display.set_mode((width*upscale, height*upscale))
    clock = Clock()

    system = system(screen).start()

    while True:
        screen.fill("gray")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        system.update()

        pygame.display.flip()
        clock.tick(15)
