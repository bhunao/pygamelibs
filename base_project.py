import sys
import pygame

from sprites.example import Sprite, GridSprite
from config import configs


class Screen:
    def __init__(self) -> None:
        pygame.init()
        height = configs["screen"]["height"]
        width = configs["screen"]["width"]
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.group = pygame.sprite.Group()
        self.sprite = GridSprite(groups=self.group)
        self.sprite.move_to_pos(5, 5)
    
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

            self.group.draw(self.screen)
            self.group.update()

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    Screen().play()