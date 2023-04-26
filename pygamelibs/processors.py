from random import randint
from esper import Processor
from pygame import Surface, key, display, event, time, mouse
from pygame.locals import (
    K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE, QUIT, KEYDOWN, K_SPACE,
    K_w, K_a, K_s, K_d)

from pygamelibs.components import (
    AnimatedRenderable, BackgroundObject, Bullet, ConstantVelocity, KeyboardInput,
    Renderable, Velocity, Button
)


class MovementProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self._target = Velocity, Renderable

    def process(self):
        for ent, (vel, rend) in self.world.get_components(*self._target):
            rend.rect.x += vel.x
            rend.rect.y += vel.y

            rend.rect.x = max(self.minx, rend.rect.x)
            rend.rect.y = max(self.miny, rend.rect.y)
            rend.rect.x = min(self.maxx - rend.rect.w, rend.rect.x)
            rend.rect.y = min(self.maxy - rend.rect.h, rend.rect.y)


class RenderProcessor(Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        for ent, rend in self.world.get_component(Renderable):
            self.window.blit(rend.image, rend.rect.topleft)
        display.flip()


class KeyboardInputProcessor(Processor):
    def __init__(self):
        super().__init__()
        self._target = KeyboardInput, Velocity, Renderable

    def process(self):
        keys = key.get_pressed()
        for ent, (k_input, vel, rend) in self.world.get_components(*self._target):
            if keys[K_a]:
                vel.x = -3
            elif keys[K_d]:
                vel.x = 3
            else:
                vel.x = 0
            if keys[K_w]:
                vel.y = -3
            elif keys[K_s]:
                vel.y = 3
            else:
                vel.y = 0


class EventProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for _event in event.get():
            if _event.type == QUIT:
                exit()
            elif _event.type == KEYDOWN:
                if _event.key == K_ESCAPE:
                    exit()


class AnimatedRenderProcessor(Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        self.window.fill(self.clear_color)
        for ent, rend in self.world.get_component(AnimatedRenderable):
            self.window.blit(rend.images[rend.frame], (rend.x, rend.y))

        now = time.get_ticks()
        if now - rend.last_update > 250:
            rend.last_update = now
            old_frame = rend.frame
            rend.frame = rend.frame + 1 if old_frame < len(rend.images) else 0
        display.flip()


class ConstantMovementProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self._target = ConstantVelocity, Renderable

    def process(self):
        for ent, (vel, rend) in self.world.get_components(*self._target):
            rend.rect.x += vel.x
            rend.rect.y += vel.y

            if self.miny > rend.rect.y or self.maxy < rend.rect.y:
                self.world.delete_entity(ent)
            if self.minx > rend.rect.x or self.maxx < rend.rect.x:
                self.world.delete_entity(ent)


class KeyboardInputProcessor(Processor):
    def __init__(self, bullet_sprite=Surface((50, 50))):
        super().__init__()
        self._target = KeyboardInput, Velocity, Renderable
        tick = time.get_ticks()
        self.time = {
            "space": tick
        }
        self.bullet_sprite = bullet_sprite

    def process(self):
        keys = key.get_pressed()
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
                now = time.get_ticks()
                teck = self.time.get("space", now)
                if now - teck > 200:
                    pos = rend.rect.center
                    self.time["space"] = now
                    self.world.create_entity(
                        Renderable(image=self.bullet_sprite,
                                   pos=pos),
                        ConstantVelocity(x=3, y=0),
                        Bullet()
                    )


class CollisionProcessor(Processor):
    def __init__(self, type1, type2):
        super().__init__()
        self.type1 = type1
        self.type2 = type2

    def process(self):
        for ent1, (type1, rend1) in self.world.get_components(self.type1, Renderable):
            for ent2, (type2, rend2) in self.world.get_components(self.type2, Renderable):
                if rend1.rect.colliderect(rend2.rect):
                    self.world.delete_entity(ent1)
                    self.world.delete_entity(ent2)
                    return


class ButtonProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()
        self._target = Renderable, Button

    def process(self, *args, **kwargs):
        mouse_pos = mouse.get_pos()
        mouse_buttons = mouse.get_pressed()
        for ent, (rend, button) in self.world.get_components(*self._target):
            if rend.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
                button.action()


class EnemySpawnerProcessor(Processor):
    def __init__(self, enemy, image, window_size, max_enemies=10) -> None:
        super().__init__()
        self.EnemyComponent = enemy
        self.image = image
        self.window_size = window_size
        self.max_enemies = max_enemies

    def process(self, *args, **kwargs):
        n_enemies = len(self.world.get_components(self.EnemyComponent))
        if n_enemies <= self.max_enemies:
            self.world.create_entity(
                self.EnemyComponent(),
                Renderable(self.image,
                           pos=(randint(0, self.window_size[0]),
                                randint(0, self.window_size[1]))),
                Velocity(randint(-2, 2), randint(1, 2)))


class BackgroundProcessor(Processor):
    def __init__(self, window_size) -> None:
        super().__init__()
        self.window_size = window_size

    def process(self, *args, **kwargs):
        for ent, (rend, bg_obj) in self.world.get_components(Renderable, BackgroundObject):
            if rend.rect.x < 5:
                rend.rect.x = self.window_size[0] - 10
