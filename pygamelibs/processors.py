import enum
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE, QUIT, KEYDOWN, KEYUP
from pygame import key, display, event, time
from esper import Processor

from pygamelibs.components import AnimatedRenderable, ConstantVelocity, KeyboardInput, Renderable, Velocity



class OutOfBounds(enum):
    DELETE = enum.auto()
    KEEP_INSIDE = enum.auto()

class MovementProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy, outofbound: OutOfBounds = None):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self._target = Velocity, Renderable
        self.outofbound = outofbound

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, rend) in self.world.get_components(*self._target):
            # Update the Renderable Component's position by it's Velocity:
            rend.x += vel.x
            rend.y += vel.y

            match OutOfBounds(self.outofbound):
                case OutOfBounds.KEEP_INSIDE:
                    # An example of keeping the sprite inside screen boundaries. Basically,
                    # adjust the position back inside screen boundaries if it tries to go outside:
                    rend.x = max(self.minx, rend.x)
                    rend.y = max(self.miny, rend.y)
                    rend.x = min(self.maxx - rend.w, rend.x)
                    rend.y = min(self.maxy - rend.h, rend.y)
                case OutOfBounds.DELETE:
                    if self.miny > rend.y or self.maxy < rend.y:
                        self.world.delete_entity(ent)
                    if self.minx > rend.x or self.maxx < rend.x:
                        self.world.delete_entity(ent)



class RenderProcessor(Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        # Clear the window:
        # self.window.fill(self.clear_color)
        # This will iterate over every Entity that has this Component, and blit it:
        for ent, rend in self.world.get_component(Renderable):
            self.window.blit(rend.image, (rend.x, rend.y))
        # Flip the framebuffers
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
    def __init__(self, minx, maxx, miny, maxy, out_of_window=False):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self._target = ConstantVelocity, Renderable
        self.out_of_window = out_of_window

    def process(self):
        for ent, (vel, rend) in self.world.get_components(*self._target):
            rend.x += vel.x
            rend.y += vel.y

            if self.out_of_window:
                if self.miny > rend.y or self.maxy < rend.y:
                    self.world.delete_entity(ent)
                if self.minx > rend.x or self.maxx < rend.x:
                    self.world.delete_entity(ent)
