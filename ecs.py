import esper
import pygame

from pygame.image import load
from functions import create_entity, draw_text

from pygamelibs.components import ConstantVelocity, KeyboardInput, Renderable, Velocity
from pygamelibs.processors import (
    ConstantMovementProcessor, EventProcessor, KeyboardInputProcessor,
    MovementProcessor, RenderProcessor)


FPS = 60
RESOLUTION = 800, 600
spaceships = [load(f"assets/imgs/ships/ship_{n:04}.png") for n in range(23)]
bullets = [
    load("assets/imgs/effects/bullet_0000.png"),
    load("assets/imgs/effects/bullet_0002.png")
]


def run():
    # Initialize Pygame stuff
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("mini-space")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    world = esper.World()
    player = world.create_entity()
    world.add_component(player, Velocity(x=0, y=0))
    world.add_component(player, Renderable(
        image=spaceships[3], posx=100, posy=100))
    world.add_component(player, KeyboardInput())

    enemy = world.create_entity()
    world.add_component(enemy, Renderable(
        image=spaceships[14], posx=400, posy=250))
    world.add_component(enemy, Velocity(x=0, y=0))

    create_entity(world,
                  Renderable(image=draw_text(
                      "alsdkja~slçkdjaçs~ldkj", (150, 150)), posx=300, posy=300),
                  )

    create_entity(world,
                  Velocity(x=0, y=0),
                  Renderable(image=spaceships[10], posx=137, posy=13),
                  )

    create_entity(world,
                  ConstantVelocity(),
                  Renderable(image=spaceships[8], posx=137, posy=13),
                  )

    # Create some Processor instances, and asign them to be processed.
    render_processor = RenderProcessor(window=window)

    event_processor = EventProcessor()

    keyboard_input_processor = KeyboardInputProcessor(bullets[1])

    movement_processor = MovementProcessor(
        minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])

    constant_move_processor = ConstantMovementProcessor(
        minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])

    world.add_processor(render_processor)
    world.add_processor(movement_processor)
    world.add_processor(event_processor)
    world.add_processor(keyboard_input_processor)
    world.add_processor(constant_move_processor)
    world.add_processor(RenderProcessor(window=window))

    running = True
    while running:
        window.fill("gray")
        world.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
