from typing import Tuple
from pygame import Surface
from pygame.sprite import Sprite
from pygame.math import Vector2


class Sprite(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.name: str = "example_sprite"
        self.image = Surface((50, 50))
        self.rect = self.image.get_rect()
    
    def move(self, x:int = 0, y: int = 0):
        self.rect.move_ip(x, y)


class GridSprite(Sprite):
    def __init__(self, size:Tuple[int, int] = (50, 50),  *groups):
        super().__init__(*groups)
        self.name: str = "grid_sprite"
        self.size = Vector2(size)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()

    def move(self, x:int = 0, y: int = 0) -> None:
        self.rect.move_ip(x*self.size.x, y*self.size.y)

    def move_to_pos(self, x:int = 0, y: int = 0) -> None:
        self.rect.topleft = (x*self.size.x, y*self.size.y)
