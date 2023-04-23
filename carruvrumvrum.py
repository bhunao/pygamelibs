from random import choice, randint
from os import listdir
from os.path import join
import esper
import pygame

from pygame.image import load
from pygame.transform import flip, rotate, scale2x
from functions import draw_text

from pygamelibs.components import (
        BackgroundObject, Bullet, Enemy, KeyboardInput, Player,
        Renderable, UIComponent, Velocity, Button)
from pygamelibs.processors import (
        BackgroundProcessor, ButtonProcessor, CollisionProcessor,
        ConstantMovementProcessor, EnemySpawnerProcessor, EventProcessor,
        KeyboardInputProcessor, MovementProcessor, RenderProcessor, UIProcessor)


def load_scale(path: str):
    return scale2x(load(path))

FPS = 60
RESOLUTION = 800, 400
spaceships = [load_scale(f"assets/imgs/ships/ship_{n:04}.png") for n in range(23)]
bullets = [
        rotate(load_scale("assets/imgs/effects/bullet_0000.png"), 90),
        rotate(load_scale("assets/imgs/effects/bullet_0002.png"), 90)
        ]
LANE_SIZE = RESOLUTION[1] / 5
lanes = []
for lane in range(int(RESOLUTION[1]/LANE_SIZE)):
    lane_points = lane * LANE_SIZE, lane * LANE_SIZE + LANE_SIZE - 1
    lanes.append(lane_points)


spawn_points = [x + LANE_SIZE/2 for x, _ in lanes[1:4]]

car_assets = "car_assets/Cars"
car_sprites = [load_scale(join(car_assets, f)) for f in listdir(car_assets)]
index = randint(0, len(car_sprites)-1)
enemy_sprite = flip(car_sprites[index], True, False)
lane_colors = [
        "darkgreen",
        "gray",
        "darkgray",
        "gray",
        "darkgreen"
        ]

class CarEnemySpawnerProcessor(EnemySpawnerProcessor):
    def process(self, *args, **kwargs):
        n_enemies = len(self.world.get_components(self.EnemyComponent))
        if n_enemies <= 3:
            self.world.create_entity(
                    self.EnemyComponent(),
                    Renderable(
                        image=self.image,
                        pos=(RESOLUTION[0], choice(spawn_points))
                        ),
                    Velocity(-1, 0))


def run():
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("car-vrum-vrum")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    world = esper.World()

    # cars
    for pos, color in zip(lanes, lane_colors):
        image = pygame.Surface((RESOLUTION[0], LANE_SIZE))
        # color = randint(0, 255), randint(0, 255), randint(0, 255), 
        image.fill(color)
        world.create_entity(
                Renderable(
                    image=image,
                    pos=(0, pos[0]),
                    pos_type="topleft"
                    )
                )

    world.create_entity(
            Player(),
            Velocity(x=0, y=0),
            Renderable(
                image=car_sprites[15],
                pos=(RESOLUTION[0]/2, RESOLUTION[1] - 100),
                ),
            KeyboardInput())

    world.create_entity(
            Renderable(image=draw_text(
                "car vrum vrum", (150, 150)), pos=(300, 300)),
            )

    world.create_entity(
            Renderable(image=load("assets/imgs/ui/grey.png"),
                       pos=(250, 250),
                       pos_type="bottomleft"),
            Button(lambda: print("button clicked"))
            )

    n_posts = 8
    teko = RESOLUTION[0] / n_posts
    for i in range(n_posts):
        world.create_entity(
                Renderable(
                    load_scale("car_assets/Props/light_double.png"),
                    pos=(teko * i, lanes[0][1]),
                    pos_type="bottomleft"
                    ),
                Velocity(-1, 0),
                BackgroundObject()
                )
        world.create_entity(
                Renderable(
                    load_scale("car_assets/Props/light_double.png"),
                    pos=(teko * i , lanes[3][1]),
                    pos_type="bottomleft"
                    ),
                Velocity(-1, 0),
                BackgroundObject()
                )

    world.create_entity(UIComponent())

    render_processor = RenderProcessor(window=window)

    event_processor = EventProcessor()

    keyboard_input_processor = KeyboardInputProcessor(bullets[1])

    movement_processor = MovementProcessor(
            minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])

    constant_move_processor = ConstantMovementProcessor(
            minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])

    button_processor = ButtonProcessor()

    collision_processors = CollisionProcessor(type1=Bullet, type2=Enemy)

    enemy_spawner_processor = CarEnemySpawnerProcessor(
            Enemy,
            enemy_sprite,
            RESOLUTION,
            spawn_points
            )

    ui_processor = UIProcessor()

    background_processor = BackgroundProcessor(RESOLUTION)

    world.add_processor(render_processor)
    world.add_processor(movement_processor)
    world.add_processor(event_processor)
    world.add_processor(keyboard_input_processor)
    world.add_processor(constant_move_processor)
    world.add_processor(button_processor)
    world.add_processor(collision_processors)
    world.add_processor(enemy_spawner_processor)
    world.add_processor(ui_processor)
    world.add_processor(background_processor)

    running = True
    while running:
        window.fill("gray")
        world.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
