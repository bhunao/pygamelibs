from esper import Processor
from pygame import Surface, key, display, event, time
from pygame.locals import (
    K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE, QUIT, KEYDOWN, K_SPACE)

from functions import create_entity
from pygamelibs.components import (
    AnimatedRenderable, ConstantVelocity, KeyboardInput, Renderable, Velocity)


class MovementProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self._target = Velocity, Renderable

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, rend) in self.world.get_components(*self._target):
            # Update the Renderable Component's position by it's Velocity:
            rend.rect.x += vel.x
            rend.rect.y += vel.y

            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it tries to go outside:
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
            # self.window.blit(rend.image, (rend.x, rend.y))
        display.flip()


class KeyboardInputProcessor(Processor):
    def __init__(self):
        super().__init__()
        self._target = KeyboardInput, Velocity, Renderable

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
        # Clear the window:
        self.window.fill(self.clear_color)
        # This will iterate over every Entity that has this Component, and blit it:
        for ent, rend in self.world.get_component(AnimatedRenderable):
            self.window.blit(rend.images[rend.frame], (rend.x, rend.y))

        now = time.get_ticks()
        if now - rend.last_update > 250:
            rend.last_update = now
            old_frame = rend.frame
            rend.frame = rend.frame + 1 if old_frame < len(rend.images) else 0
        # Flip the framebuffers
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
                    self.time["space"] = now
                    create_entity(self.world,
                                  Renderable(image=self.bullet_sprite,
                                             posx=rend.rect.centerx, posy=rend.rect.centery),
                                  ConstantVelocity(x=0, y=-5)
                                  )


class CollisionProcessor(Processor):
    def __init__(self, type1, type2):
        super().__init__()
        self.type1 = type1
        self.type2 = type2

    def process(self):
        for ent, body in self.world.get_components(*self.type1, Velocity):
            for ent, body in self.world.get_components(*self.type2, Velocity):
                pass    # TODO: add collision process between types
