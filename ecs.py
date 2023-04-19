from dataclasses import dataclass
import itertools
import pygame
from pygame.locals import *

from pygame.image import load

import esper

from pygamelibs.components import KeyboardInput, Renderable, Velocity
from pygamelibs.processors import ConstantMovementProcessor, EventProcessor, MovementProcessor, RenderProcessor


def create_entity(world, *components):
    entity = world.create_entity()
    for component in components:
        world.add_component(entity, component)
    
def img_yielder(image_list):
    for image in itertools.cycle(image_list):
        yield image

class KeyboardInputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._target = KeyboardInput, Velocity, Renderable
        tick = pygame.time.get_ticks()
        self.time = {
            "space": tick
        }

    def process(self):
        keys = pygame.key.get_pressed()
        for ent, (k_input, vel, rend) in self.world.get_components(*self._target):
            if keys[K_LEFT]:
                vel.x = -3
            elif keys[K_RIGHT]:
                vel.x = 3
            else:
                vel.x = 0

            if keys[K_UP]:
                vel.y = -3
            elif keys[K_DOWN]:
                vel.y = 3
            else:
                vel.y = 0

            if keys[K_SPACE]:
                now = pygame.time.get_ticks()
                teck = self.time.get("space", now)
                if now - teck > 200:
                    self.time["space"] = now
                    create_entity(self.world,
                                Renderable(image=bullets[0], posx=rend.x, posy=rend.y),
                                ConstantVelocity(x=0, y=-5)
                                )

class CollisionProcessor(esper.Processor):
    def __init__(self, type1, type2):
        super().__init__()
        self.type1 = type1
        self.type2 = type2
    
    def process(self):
        pass


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
    world.add_component(player, Renderable(image=spaceships[3], posx=100, posy=100))
    world.add_component(player, KeyboardInput())

    enemy = world.create_entity()
    world.add_component(enemy, Renderable(image=spaceships[14], posx=400, posy=250))
    world.add_component(enemy, Velocity(x=0, y=0))

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
    movement_processor = MovementProcessor(minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])
    event_processor = EventProcessor()
    keyboard_input_processor = KeyboardInputProcessor()
    world.add_processor(render_processor)
    world.add_processor(movement_processor)
    world.add_processor(event_processor)
    world.add_processor(keyboard_input_processor)
    world.add_processor(ConstantMovementProcessor(minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1], out_of_window=True))
    world.add_processor(RenderProcessor(window=window))

    running = True
    while running:
        window.fill("gray")
        world.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()

