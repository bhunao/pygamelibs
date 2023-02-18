from typing import Tuple
from pygame import Surface
from pygame.sprite import Sprite


class Sprite(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = Surface((50, 50))
        self.rect = self.image.get_rect()
    
    def move(self, x:int = 0, y: int = 0):
        self.rect.move_ip(x, y)


class GridSprite(Sprite):
    def __init__(self, size:Tuple[int, int] = (50, 50),  *groups):
        super().__init__(*groups)
        print(size)
        self.size = size
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()

    def move(self, x:int = 0, y: int = 0):
        self.rect.move_ip(x*self.rect.width, y*self.rect.height)