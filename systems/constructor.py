import random
import sys
import pygame

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
    in_screen = Surface(screen.get_size())
    clock = Clock()

    _sys = system(in_screen).start()

    while True:
        in_screen.fill("darkgray")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        _sys.update()
        screen.blit(in_screen, (0,0))
        pygame.display.flip()
        clock.tick(15)
