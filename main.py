import pygame

import esper

from components import KeyboardInput, Renderable, Velocity
from processors import EventProcessor, KeyboardInputProcessor, MovementProcessor, RenderProcessor


FPS = 60
RESOLUTION = 720, 480

def run():
    # Initialize Pygame stuff
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Esper Pygame example")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    # Initialize Esper world, and create a "player" Entity with a few Components.
    world = esper.World()
    player = world.create_entity()
    world.add_component(player, Velocity(x=0, y=0))
    world.add_component(player, Renderable(image=pygame.image.load("redsquare.png"), posx=100, posy=100))
    world.add_component(player, KeyboardInput())
    # Another motionless Entity:
    enemy = world.create_entity()
    world.add_component(enemy, Renderable(image=pygame.image.load("bluesquare.png"), posx=400, posy=250))
    world.add_component(enemy, Velocity(x=0, y=0))

    # Create some Processor instances, and asign them to be processed.
    render_processor = RenderProcessor(window=window)
    movement_processor = MovementProcessor(minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])
    event_processor = EventProcessor()
    keyboard_input_processor = KeyboardInputProcessor()
    world.add_processor(render_processor)
    world.add_processor(movement_processor)
    world.add_processor(event_processor)
    world.add_processor(keyboard_input_processor)

    running = True
    while running:
        world.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
