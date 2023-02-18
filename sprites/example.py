from pygame import Surface
from pygame.sprite import Sprite


class Sprite(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Surface((50, 50))
        self.rect = self.image.get_rect()