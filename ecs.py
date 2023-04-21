import esper
import pygame

from pygame.image import load
from functions import draw_text

from pygamelibs.components import (
    Bullet, ConstantVelocity, Enemy, KeyboardInput, Player, Renderable, Velocity, Button)
from pygamelibs.processors import (
    ButtonProcessor, CollisionProcessor, ConstantMovementProcessor, EnemySpawnerProcessor, EventProcessor, KeyboardInputProcessor,
    MovementProcessor, RenderProcessor)


FPS = 60
RESOLUTION = 800, 600
spaceships = [load(f"assets/imgs/ships/ship_{n:04}.png") for n in range(23)]
bullets = [
    load("assets/imgs/effects/bullet_0000.png"),
    load("assets/imgs/effects/bullet_0002.png")
]


def run():
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
    world.add_component(player, Player())

    enemy = world.create_entity()
    world.add_component(enemy, Renderable(
        image=spaceships[14], posx=100, posy=100))
    world.add_component(enemy, Velocity(x=0, y=0))
    world.add_component(enemy, Enemy())

    world.create_entity(
                  Renderable(image=draw_text(
                      "alsdkja~slçkdjaçs~ldkj", (150, 150)), posx=300, posy=300),
                  )

    world.create_entity(world,
                  Velocity(x=0, y=0),
                  Renderable(image=spaceships[10], posx=137, posy=13),
                  )

    world.create_entity(world,
                  ConstantVelocity(),
                  Renderable(image=spaceships[8], posx=50, posy=13),
                  )

    world.create_entity(world,
                  Renderable(image=load("assets/imgs/ui/grey.png"),
                             posx=250, posy=250),
                  Button(lambda: print("button"), "on")
                  )

    render_processor = RenderProcessor(window=window)

    event_processor = EventProcessor()

    keyboard_input_processor = KeyboardInputProcessor(bullets[1])

    movement_processor = MovementProcessor(
        minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])

    constant_move_processor = ConstantMovementProcessor(
        minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])

    button_processor = ButtonProcessor()

    collision_processors = CollisionProcessor(type1=Bullet, type2=Enemy)

    enemy_spawner_processor = EnemySpawnerProcessor(Enemy, spaceships[14], RESOLUTION)

    world.add_processor(render_processor)
    world.add_processor(movement_processor)
    world.add_processor(event_processor)
    world.add_processor(keyboard_input_processor)
    world.add_processor(constant_move_processor)
    world.add_processor(button_processor)
    world.add_processor(collision_processors)
    world.add_processor(enemy_spawner_processor)


    running = True
    while running:
        window.fill("gray")
        world.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
