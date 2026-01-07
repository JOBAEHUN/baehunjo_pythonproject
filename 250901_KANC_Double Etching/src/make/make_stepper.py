import gdsfactory as gf

def add_stepper_rect_key(position, width, height, layer):

    c = gf.Component()
    c.add_polygon([
        (position[0] - width / 2, position[1] - height / 2),
        (position[0] + width / 2, position[1] - height / 2),
        (position[0] + width / 2, position[1] + height / 2),
        (position[0] - width / 2, position[1] + height / 2),
    ], layer=layer)
    return c