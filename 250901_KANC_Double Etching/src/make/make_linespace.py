from pathlib import Path
import os
import numpy as np
import gdsfactory as gf
from gdsfactory.technology import LayerViews
from gdsfactory.config import PATH
from gdsfactory.path import straight, euler, arc
from gdsfactory import Component

def line_space_pattern(width,line_width, space_width, num_lines, layer = (34,0)):
    pattern = gf.Component()
    for i in range(num_lines):
        line = pattern << gf.components.rectangle(size=(width, line_width), layer=layer)
        line.move([0,i*(line_width + space_width)])
    return pattern