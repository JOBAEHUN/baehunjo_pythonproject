import numpy as np
import gdsfactory as gf
from make import make_elements
from make import make_grating


def Bend_leftGC_arc0(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    # TotalGC_S_wg = ([])
    # TotalGC_S_wg_clad = ([])

    for i in range(1,4):
        # S-bend 경로 설정
        S_wg = c << make_elements.make_path(
            [  gf.path.straight(length2),
             gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer, width=width)
        S_wg_clad = c << make_elements.make_path(
            [  gf.path.straight(length2),
             gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=(layer[0], layer[1] + 1),
            width=16 + width)
        # S_wg.rotate(90)
        # S_wg_clad.rotate(90)

        # TotalGC_S_wg.append(S_wg)
        # TotalGC_S_wg_clad.append(S_wg_clad)

    # for gc in TotalGC_S_wg:
    #     gc.rotate(90)
    #
    # for gc in TotalGC_S_wg_clad:
    #     gc.rotate(90)


        # 포트 설정
        c.add_port(name='o1', port=S_wg.ports[0])
        c.add_port(name='o2', port=S_wg.ports[1])

        GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

        GC1.mirror_x()
        # S_wg.mirror_x()
        # S_wg_clad.mirror_x()
        S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
        S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)


        GC1.move([10, 0])
 #       GC1.rotate(90)
        c.flatten()
        return c



def Bend_leftGC_arc(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2) ], layer=layer, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2)], layer=(layer[0], layer[1] + 1),
        width=16 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    GC1.mirror_x()
    # S_wg.mirror_x()
    # S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)


    GC1.move([10, 0])
    c.flatten()
    return c


def Bend_leftGC_arc1(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    # TotalGC_S_wg = ([])
    # TotalGC_S_wg_clad = ([])

    for i in range(1,4):
        # S-bend 경로 설정
        S_wg = c << make_elements.make_path(
            [  gf.path.straight(length2),
             gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer, width=width)
        S_wg_clad = c << make_elements.make_path(
            [  gf.path.straight(length2),
             gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=(layer[0], layer[1] + 1),
            width=16 + width)
        # S_wg.rotate(90)
        # S_wg_clad.rotate(90)

        # TotalGC_S_wg.append(S_wg)
        # TotalGC_S_wg_clad.append(S_wg_clad)

    # for gc in TotalGC_S_wg:
    #     gc.rotate(90)
    #
    # for gc in TotalGC_S_wg_clad:
    #     gc.rotate(90)


        # 포트 설정
        c.add_port(name='o1', port=S_wg.ports[0])
        c.add_port(name='o2', port=S_wg.ports[1])

        GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

        GC1.mirror_x()
        # S_wg.mirror_x()
        # S_wg_clad.mirror_x()
        S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
        S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)


        GC1.move([10, 0])
 #       GC1.rotate(90)
        c.flatten()
        return c