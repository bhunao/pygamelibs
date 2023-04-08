from enum import Enum
from config import WIDTH, HEIGHT, UPSCALE
from systems.default_system import DefaultSystem
from systems.constructor import default_builder, wrap_grid_builder
from systems.wrap_grid import WrapGridSystem




class Builders(Enum):
    Default = default_builder, DefaultSystem
    WrapGrid = wrap_grid_builder, WrapGridSystem


def constructor(builder: Builders = Builders.Default, width=WIDTH, height=HEIGHT,
                upscale=UPSCALE):
    builder_func, system = builder.value
    return lambda: builder_func(system, width, height, upscale)
