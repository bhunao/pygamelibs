import sys
import pygame

from sprites.example import Sprite, GridSprite
from config import configs


class Screen:
    def __init__(self) -> None:
        pygame.init()
        height = configs["screen"]["width"]
        width = configs["screen"]["height"]
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.group = pygame.sprite.Group()
        # self.sprite = Sprite(self.group)
        self.sprite = GridSprite()
        self.sprite.add(self.group)
    
    def play(self):
        while 1:
            # background
            self.screen.fill(configs["screen"]["background-color"])

            # get mouse position
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            self.sprite.move(x=1)

            self.group.draw(self.screen)
            self.group.update()

            pygame.display.flip()
            self.clock.tick(10)

if __name__ == "__main__":
    Screen().play()