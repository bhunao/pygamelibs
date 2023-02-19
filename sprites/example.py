from typing import List, Tuple
from pygame import Color, Rect, Surface
from pygame.sprite import Sprite, Group
from pygame.math import Vector2
from pygame.draw import rect


class Sprite(Sprite):
    def __init__(self, groups: Group | List[Group] = []):
        super().__init__(*groups if isinstance(groups, list) else [groups])
        self.name: str = "example_sprite"
        self.image = Surface((50, 50))
        self.rect = self.image.get_rect()
    
    def move(self, x:int = 0, y: int = 0):
        self.rect.move_ip(x, y)


class GridSprite(Sprite):
    def __init__(self, size:Tuple[int, int] = (50, 50), color = (255, 0 ,0), border_color: Color | None = None, groups: Group | List[Group] = []):
        super().__init__(*groups if isinstance(groups, list) else [groups])

        self.name: str = "grid_sprite"
        self.size = Vector2(size)
        self.image = Surface(self.size)
        box = Rect(0, 0, self.size.x, self.size.y)
        rect(self.image, color, box)
        if border_color:
            rect(self.image, (255, 125, 125), box, 5)
        
        # self.image.fill(color)
        self.rect = self.image.get_rect()

    def move(self, x:int = 0, y: int = 0) -> None:
        self.rect.move_ip(x*self.size.x, y*self.size.y)

    def move_to_pos(self, x:int = 0, y: int = 0) -> None:
        self.rect.topleft = (x*self.size.x, y*self.size.y)
