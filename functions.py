from pygame.font import SysFont
from pygame import Surface


def draw_text(_screen: Surface, text: str | int, pos, size=15, color=(255, 255, 255), bold: bool = False):
    font = SysFont("Arial", size, bold)
    font.set_bold(True)
    text = font.render(str(text), True, color)
    text_rect = text.get_rect()
    text_rect.center = pos
    _screen.blit(text, text_rect)
    return text_rect
