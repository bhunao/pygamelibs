from pygame.font import SysFont


def draw_text(text: str | int, pos, size=15, color=(255, 255, 255), bold: bool = False):
    font = SysFont("Arial", size, bold)
    font.set_bold(True)
    text = font.render(str(text), True, color)
    text_rect = text.get_rect()
    text_rect.center = pos
    return text

def create_entity(world, *components):
    entity = world.create_entity()
    for component in components:
        world.add_component(entity, component)
    