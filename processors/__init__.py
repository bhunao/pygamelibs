from esper import Processor

import pygame

from components import KeyboardInput, Renderable, Velocity

class MovementProcessor(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
            # Update the Renderable Component's position by it's Velocity:
            rend.x += vel.x
            rend.y += vel.y
            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it tries to go outside:
            rend.x = max(self.minx, rend.x)
            rend.y = max(self.miny, rend.y)
            rend.x = min(self.maxx - rend.w, rend.x)
            rend.y = min(self.maxy - rend.h, rend.y)


class RenderProcessor(Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)
        # This will iterate over every Entity that has this Component, and blit it:
        for ent, rend in self.world.get_component(Renderable):
            self.window.blit(rend.image, (rend.x, rend.y))
        # Flip the framebuffers
        pygame.display.flip()


class KeyboardInputProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        keys = pygame.key.get_pressed()
        for ent, (k_input, vel, rend) in self.world.get_components(KeyboardInput, Velocity, Renderable):
            if keys[pygame.K_LEFT]:
                print("left")
                vel.x = -3
            elif keys[pygame.K_RIGHT]:
                print("right")
                vel.x = 3
            else:
                vel.x = 0
            if keys[pygame.K_UP]:
                print("up")
                vel.y = -3
            elif keys[pygame.K_DOWN]:
                print("down")
                vel.y = 3
            else:
                vel.y = 0

class EventProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        # This will iterate over every Entity that has BOTH of these components:
        # Update the Renderable Component's position by it's Velocity:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
