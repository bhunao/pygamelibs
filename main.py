from typing import Dict

import pygame
from pygame.locals import *
from pygame.sprite import Group, Sprite
from pygame.surface import Surface


def draw_text(_screen, text, pos, size=15, color=(255, 255, 255), bold=False):
    font = pygame.font.SysFont("Arial", size, bold)
    font.set_bold(True)
    text = font.render(str(text), True, color)
    text_rect = text.get_rect()
    text_rect.center = pos
    _screen.blit(text, text_rect)
    return text_rect


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 640))
        self.running = True
        self.groups: Dict[str, Group] = dict()

        # parts
        self.side = Side(self.groups)
        self.sprite_attributes = SpriteAttributes(GameSprite())

        # auto start
        self.create_sprites()
        self.run()

    def run(self):
        while self.running:
            self.event_manager()
            self.update_and_display()

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit()

    def update_and_display(self):
        self.screen.fill("#324572")
        self.update()
        pygame.display.flip()

    def quit(self):
        print(f"quiting... {self.running=}")
        pygame.quit()

    def update(self):
        for group in self.groups.values():
            group.draw(self.screen)
            group.update()

        self.side.update(self.screen)
        self.sprite_attributes.update(self.screen)

    def create_sprites(self):
        self.add_to_group(GameSprite(), "main")
        self.add_to_group(GameSprite(), "main")
        self.add_to_group(GameSprite(), "main")

    def add_to_group(self, sprite, group_name):
        group = self.groups.get(group_name, Group())
        group.add(sprite)
        self.groups[group_name] = group


class GameSprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = Surface((35, 35))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.center = 50, 50


class Side:
    def __init__(self, parent_groups):
        pygame.init()
        width = pygame.display.get_surface().get_width() * 0.4
        self.screen = Surface((width, 320))
        self.running = True
        self.groups: Dict[str, Group] = dict()
        self.parent_groups = parent_groups

    def list_parent_groups(self):
        for group_i, (group_name, group) in enumerate(self.parent_groups.items()):
            for spr_i, sprite in enumerate(group.sprites()):
                self.draw_list_item(group_i, group_name, group, spr_i, sprite)

    def update(self, screen: Surface):
        self.screen.fill("#394f7b")
        pos = screen.get_width() - self.screen.get_width(), 0
        self.list_parent_groups()
        screen.blit(self.screen, pos)

    def add_to_group(self, sprite, group_name):
        group = self.groups.get(group_name, Group())
        group.add(sprite)
        self.groups[group_name] = group

    def draw_list_item(self, group_i, group_name, group, spr_i, sprite):
        item_height = 40
        rect = Rect(0, spr_i*item_height, self.screen.get_width(), item_height-5)
        text = f"{sprite.__class__.__name__}, {sprite.rect.center}"
        pygame.draw.rect(self.screen, "darkblue", rect)
        draw_text(self.screen, text, rect.center)


class SpriteAttributes:
    def __init__(self, sprite):
        pygame.init()
        width = pygame.display.get_surface().get_width() * 0.4
        self.screen = Surface((width, 320))
        self.running = True
        self.sprite = sprite

    def update(self, screen: Surface):
        self.screen.fill("#3b8f9a")
        self.draw_attributes()
        pos = screen.get_width() - self.screen.get_width(), screen.get_height() - self.screen.get_height()
        screen.blit(self.screen, pos)

    def draw_attributes(self):
        item_height = 30
        for i, (key, value) in enumerate(self.sprite.__dict__.items()):
            text = f"{key}|{value} |"
            rect = Rect(0, i*item_height, self.screen.get_width(), item_height-5)
            pygame.draw.rect(self.screen, "black", rect)
            draw_text(self.screen, text, rect.center)


if __name__ == "__main__":
    App()
