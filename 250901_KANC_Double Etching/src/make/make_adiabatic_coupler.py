from pathlib import Path
import os
import numpy as np
# from make import make_grating
# from make import make_propagationloss
import gdsfactory as gf
from gdsfactory.technology import LayerViews
from gdsfactory.config import PATH
from gdsfactory.path import straight, euler, arc
# from make import make_assembly
from make import make_elements
# import make_elements

def make_bottom_coupler(strip_input_length1, strip_input_length2, slab_length, strip_output_length, taper_length, width, tip, layer):
    c = gf.Component()

    # (INPUT) S-bend 경로 설정
    S_wg = c << make_elements.make_path([gf.path.straight(strip_input_length1), gf.path.arc(radius=200, angle=-90),
        gf.path.straight(25), gf.path.arc(radius=200, angle=90), gf.path.straight(strip_input_length2)], layer=layer, width=width)

    S_wg_clad = c << make_elements.make_path([gf.path.straight(strip_input_length1), gf.path.arc(radius=200, angle=-90),
        gf.path.straight(25), gf.path.arc(radius=200, angle=90), gf.path.straight(strip_input_length2)], layer=(layer[0], layer[1]+1),
        width=width+16)

    # 포트설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.5)

    GC1.mirror_x()
    # S_wg.mirror_x()
    # S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10,0])

    # INPUT TAPER 설정
    Input_taper = c << make_elements.make_taper(width, tip, taper_length, layer=layer)
    Input_taper_clad = c << make_elements.make_path([gf.path.straight(taper_length)], layer=(layer[0], layer[1] + 1), width=width+16)

    Input_taper.connect('o1', S_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_clad.connect('o1', S_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # Slab 영역 설정
    Slab_region = c << make_elements.make_path([gf.path.straight(slab_length)], layer=(layer[0], layer[1]+1), width=width+16)

    Slab_region.connect('o1', Input_taper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # OUTPUT 설정
    Output_taper = c << make_elements.make_taper(tip, width, taper_length, layer=layer)
    Output_taper_clad = c << make_elements.make_path([gf.path.straight(taper_length)], layer=(layer[0], layer[1] + 1), width=width+16)

    Output_taper.connect('o1', Slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_clad.connect('o1', Slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    Output_strip = c << make_elements.make_path([gf.path.straight(strip_output_length)], layer=layer, width=width)
    Output_strip_clad = c << make_elements.make_path([gf.path.straight(strip_output_length)], layer=(layer[0], layer[1] + 1), width=width+16)

    Output_strip.connect('o1', Output_taper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_strip_clad.connect('o1', Output_taper_clad.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.5)

    GC2.connect('o1', Output_strip.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([-10, 0])

    c.flatten()

    return c

def make_top_coupler(edge_slab_length, slab_length, taper_length, width, tip, layer):
    c = gf.Component()

    # Input slab 설정
    Input_slab_region = c << make_elements.make_path([gf.path.straight(edge_slab_length + 650)], layer=(layer[0], layer[1] + 1),
                                               width=width + 16)

    # INPUT TAPER 설정
    Input_taper = c << make_elements.make_taper(tip, width, taper_length, layer=layer)
    Input_taper_clad = c << make_elements.make_path([gf.path.straight(taper_length)], layer=(layer[0], layer[1] + 1), width=width+16)

    Input_taper.connect('o1', Input_slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True),
    Input_taper_clad.connect('o1', Input_slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # Strip + Slab 영역 설정
    Strip_wg = c << make_elements.make_path([gf.path.straight(slab_length)], layer=layer, width=width)
    Slab_region = c << make_elements.make_path([gf.path.straight(slab_length)], layer=(layer[0], layer[1] + 1),
                                               width=width + 16)

    Strip_wg.connect('o1', Input_taper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True),
    Slab_region.connect('o1', Input_taper_clad.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # OUTPUT 설정
    Output_taper = c << make_elements.make_taper(width, tip, taper_length, layer=layer)
    Output_taper_clad = c << make_elements.make_path([gf.path.straight(taper_length)], layer=(layer[0], layer[1] + 1), width=width+16)

    Output_taper.connect('o1', Slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_clad.connect('o1', Slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    Output_slab_region = c << make_elements.make_path([gf.path.straight(edge_slab_length)], layer=(layer[0], layer[1] + 1),
                                                     width=width + 16)

    Output_slab_region.connect('o1', Output_taper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    c.flatten()

    return c

def make_ref_bottom_coupler(strip_input_length1, strip_input_length2, slab_length, strip_output_length, taper_length,
                            width, layer):
    c = gf.Component()

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.5)
    GC1.mirror_x()

    S_wg = c << make_elements.make_path([gf.path.straight(strip_input_length1), gf.path.arc(radius=200, angle=-90),
                                             gf.path.straight(25), gf.path.arc(radius=200, angle=90),
                                             gf.path.straight(strip_input_length2), gf.path.straight(taper_length), gf.path.straight(slab_length), gf.path.straight(taper_length), gf.path.straight(strip_output_length)], layer=layer, width=width)

    S_wg_clad = c << make_elements.make_path(
            [gf.path.straight(strip_input_length1), gf.path.arc(radius=200, angle=-90),
                                             gf.path.straight(25), gf.path.arc(radius=200, angle=90),
                                             gf.path.straight(strip_input_length2), gf.path.straight(taper_length), gf.path.straight(slab_length), gf.path.straight(taper_length), gf.path.straight(strip_output_length)],
            layer=(layer[0], layer[1] + 1),
            width=width + 16)

    # 포트설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])

    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.5)

    GC2.connect('o1', S_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([-10, 0])

    c.flatten()

    return c

def make_ref_top_coupler(edge_slab_length, slab_length, taper_length, width, layer):
    c = gf.Component()

    # Input slab 설정
    Input_slab_region = c << make_elements.make_path([gf.path.straight(edge_slab_length + 650), gf.path.straight(taper_length), gf.path.straight(slab_length), gf.path.straight(taper_length), gf.path.straight(edge_slab_length)],
                                                         layer=(layer[0], layer[1] + 1),
                                                         width=width + 16)

    # # INPUT TAPER 설정
    # Input_taper = c << make_elements.make_taper(tip, width, taper_length, layer=layer)
    # Input_taper_clad = c << make_elements.make_taper(tip + 16, width + 16, taper_length,
    #                                                      layer=(layer[0], layer[1] + 1))
    #
    # Input_taper.connect('o1', Input_slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True),
    # Input_taper_clad.connect('o1', Input_slab_region.ports['o2'], allow_layer_mismatch=True,
    #                              allow_width_mismatch=True)
    #
    # # Strip + Slab 영역 설정
    # Strip_wg = c << make_elements.make_path([gf.path.straight(slab_length)], layer=layer, width=width)
    # Slab_region = c << make_elements.make_path([gf.path.straight(slab_length)], layer=(layer[0], layer[1] + 1),
    #                                                width=width + 16)
    #
    # Strip_wg.connect('o1', Input_taper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True),
    # Slab_region.connect('o1', Input_taper_clad.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    #
    # # OUTPUT 설정
    # Output_taper = c << make_elements.make_taper(width, tip, taper_length, layer=layer)
    # Output_taper_clad = c << make_elements.make_taper(width + 16, tip + 16, taper_length,
    #                                                       layer=(layer[0], layer[1] + 1))
    #
    # Output_taper.connect('o1', Slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # Output_taper_clad.connect('o1', Slab_region.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    #
    # Output_slab_region = c << make_elements.make_path([gf.path.straight(edge_slab_length)],
    #                                                       layer=(layer[0], layer[1] + 1),
    #                                                       width=width + 16)
    #
    # Output_slab_region.connect('o1', Output_taper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    c.flatten()

    return c

def add_cross_align_key(position, size=60, cross_width=20, layer=(34, 0)):
    """
    십자가 키를 추가하는 함수 (중앙에 작은 네모 포함).

    Args:
        layout: gdsfactory Component 객체
        position: 십자가 키의 중심 위치 (x, y)
        size: 십자가 키의 선 길이 (기본값: 100 µm)
        layer: GDS 레이어 정보
        center_square_size: 중앙 네모의 한 변 길이 (기본값: 10 µm)
    """
    c = gf.Component()
    # 수평 선 추가
    c.add_polygon([
        (position[0] - size / 2, position[1] - cross_width/2),
        (position[0] + size / 2, position[1] - cross_width/2),
        (position[0] + size / 2, position[1] + cross_width/2),
        (position[0] - size / 2, position[1] + cross_width/2),
        (position[0] - size / 2, position[1] - cross_width/2),
    ], layer=layer)

    # 수직 선 추가
    c.add_polygon([
        (position[0] - cross_width/2, position[1] - size / 2),
        (position[0] - cross_width/2, position[1] + size / 2),
        (position[0] + cross_width/2, position[1] + size / 2),
        (position[0] + cross_width/2, position[1] - size / 2),
        (position[0] - cross_width/2, position[1] - size / 2),
    ], layer=layer)

    # 클래딩 영역 추가 (타일링 방지)
    c.add_polygon([
        (position[0] - size/2 - 3, position[1] - size / 2 - 3),
        (position[0] - size/2 - 3, position[1] + size / 2 + 3),
        (position[0] + size/2 + 3, position[1] + size / 2 + 3),
        (position[0] + size/2 + 3, position[1] - size / 2 - 3),
        (position[0] - size/2 - 3, position[1] - size / 2 - 3),
    ], layer=(layer[0], layer[1] + 1))

    c.flatten()

    return c

def add_square_align_key(position, size=60, cross_width=20, layer=(34, 0)):
    c = gf.Component()

    # 왼쪽 상단 사각형 추가
    c.add_polygon([
        (position[0] - size / 2, position[1] + cross_width / 2),
        (position[0] - cross_width / 2, position[1] + cross_width / 2),
        (position[0] - cross_width / 2, position[1] + size / 2),
        (position[0] - size / 2, position[1] + size / 2)], layer=layer)

    # 오른쪽 상단 사각형 추가
    c.add_polygon([
        (position[0] + cross_width / 2, position[1] + cross_width / 2),
        (position[0] + size / 2, position[1] + cross_width / 2),
        (position[0] + size / 2, position[1] + size / 2),
        (position[0] + cross_width / 2, position[1] + size / 2)], layer=layer)

    # 왼쪽 하단 사각형 추가
    c.add_polygon([
        (position[0] - size / 2, position[1] - size / 2),
        (position[0] - cross_width / 2, position[1] - size / 2),
        (position[0] - cross_width / 2, position[1] - cross_width / 2),
        (position[0] - size / 2, position[1] - cross_width / 2)], layer=layer)

    # 오른쪽 하단 사각형 추가
    c.add_polygon([
        (position[0] + cross_width / 2, position[1] - size / 2),
        (position[0] + size / 2, position[1] - size / 2),
        (position[0] + size / 2, position[1] - cross_width / 2),
        (position[0] + cross_width / 2, position[1] - cross_width / 2)], layer=layer)

    # 클래딩 영역 추가 (타일링 방지)
    c.add_polygon([
        (position[0] - size/2 - 3, position[1] - size / 2 - 3),
        (position[0] - size/2 - 3, position[1] + size / 2 + 3),
        (position[0] + size/2 + 3, position[1] + size / 2 + 3),
        (position[0] + size/2 + 3, position[1] - size / 2 - 3),
        (position[0] - size/2 - 3, position[1] - size / 2 - 3),
    ], layer=(layer[0], layer[1] + 1))

    c.flatten()

    return c

# def make_oxide_etching(position, x_length, y_length, layer=(34, 0)):
#     c = gf.Component()
#
#     # SiO2 에칭/Cr 증착 패턴 (직사각형)
#     c.add_polygon([
#         (position[0] - x_length / 2, position[1] - y_length / 2),
#         (position[0] + x_length / 2, position[1] - y_length / 2),
#         (position[0] + x_length / 2, position[1] + y_length / 2),
#         (position[0] - x_length / 2, position[1] + y_length / 2)], layer=layer)
#
#     # c.flatten()
#
#     return c

def make_oxide_etching(x_length, y_length, layer=(34, 0)):
    c = gf.Component()

    # SiO2 에칭/Cr 증착 패턴 (직사각형)
    c.add_polygon([
        (- x_length / 2, - y_length / 2),
        (+ x_length / 2, - y_length / 2),
        (+ x_length / 2, + y_length / 2),
        (- x_length / 2, + y_length / 2)], layer=layer)

    c.flatten()

    return c

def make_indium_pillar(x_length, y_length, layer=(34, 0)):
    c = gf.Component()

    # 십자가 형태 (세로)
    c.add_polygon([
        (- x_length / 6, - y_length / 2),
        (+ x_length / 6, - y_length / 2),
        (+ x_length / 6, + y_length / 2),
        (- x_length / 6, + y_length / 2)], layer=layer)

    # 십자가 형태 (가로)
    c.add_polygon([
        (- x_length / 2, - y_length / 4),
        (+ x_length / 2, - y_length / 4),
        (+ x_length / 2, + y_length / 4),
        (- x_length / 2, + y_length / 4)], layer=layer)

    c.flatten()

    return c

def make_oxide_align_key(x_length, y_length, layer=(34, 0)):
    c = gf.Component()

    # SiO2 에칭/Cr 증착 패턴 (직사각형)
    c.add_polygon([
        (- x_length / 2, - y_length / 2),
        (+ x_length / 2, - y_length / 2),
        (+ x_length / 2, + y_length / 2),
        (- x_length / 2, + y_length / 2)], layer=layer)

    c.flatten()

    return c

def make_indium_align_key(x_distance, y_distance, x_length, y_length, layer=(34, 0)):
    c = gf.Component()

    # In 증착 패턴 (4방향 정사각형)
    c.add_polygon([
        (- x_length / 2, y_distance),
        (+ x_length / 2, y_distance),
        (+ x_length / 2, y_distance + y_length),
        (- x_length / 2, y_distance + y_length)], layer=layer)

    c.add_polygon([
        (- x_distance - x_length, - y_length / 2),
        (- x_distance, - y_length / 2),
        (- x_distance, y_length / 2),
        (- x_distance - x_length, y_length / 2)], layer=layer)

    c.add_polygon([
        (- x_length / 2, - y_distance - y_length),
        (+ x_length / 2, - y_distance - y_length),
        (+ x_length / 2, - y_distance),
        (- x_length / 2, - y_distance)], layer=layer)

    c.add_polygon([
        (x_distance, - y_length / 2),
        (x_distance + x_length, - y_length / 2),
        (x_distance + x_length, + y_length / 2),
        (x_distance, + y_length / 2)], layer=layer)

    c.flatten()

    return c

def add_cross_align_key2(position, size=60, cross_width=20, layer=(34, 0)):
    """
    십자가 키를 추가하는 함수 (중앙에 작은 네모 포함).

    Args:
        layout: gdsfactory Component 객체
        position: 십자가 키의 중심 위치 (x, y)
        size: 십자가 키의 선 길이 (기본값: 100 µm)
        layer: GDS 레이어 정보
        center_square_size: 중앙 네모의 한 변 길이 (기본값: 10 µm)
    """
    c = gf.Component()
    # 수평 선 추가
    c.add_polygon([
        (position[0] - size / 2, position[1] - cross_width/2),
        (position[0] + size / 2, position[1] - cross_width/2),
        (position[0] + size / 2, position[1] + cross_width/2),
        (position[0] - size / 2, position[1] + cross_width/2),
        (position[0] - size / 2, position[1] - cross_width/2),
    ], layer=layer)

    # 수직 선 추가
    c.add_polygon([
        (position[0] - cross_width/2, position[1] - size / 2),
        (position[0] - cross_width/2, position[1] + size / 2),
        (position[0] + cross_width/2, position[1] + size / 2),
        (position[0] + cross_width/2, position[1] - size / 2),
        (position[0] - cross_width/2, position[1] - size / 2),
    ], layer=layer)

    c.flatten()

    return c


def add_square_align_key2(position, size=60, cross_width=20, layer=(34, 0)):
    c = gf.Component()

    # 왼쪽 상단 사각형 추가
    c.add_polygon([
        (position[0] - size / 2-1, position[1] + cross_width / 2+1),
        (position[0] - cross_width / 2-1, position[1] + cross_width / 2+1),
        (position[0] - cross_width / 2-1, position[1] + size / 2+1),
        (position[0] - size / 2-1, position[1] + size / 2+1)], layer=layer)

    # 오른쪽 상단 사각형 추가
    c.add_polygon([
        (position[0] + cross_width / 2+1, position[1] + cross_width / 2+1),
        (position[0] + size / 2+1, position[1] + cross_width / 2+1),
        (position[0] + size / 2+1, position[1] + size / 2+1),
        (position[0] + cross_width / 2+1, position[1] + size / 2+1)], layer=layer)

    # 왼쪽 하단 사각형 추가
    c.add_polygon([
        (position[0] - size / 2-1, position[1] - size / 2-1),
        (position[0] - cross_width / 2-1, position[1] - size / 2-1),
        (position[0] - cross_width / 2-1, position[1] - cross_width / 2-1),
        (position[0] - size / 2-1, position[1] - cross_width / 2-1)], layer=layer)

    # 오른쪽 하단 사각형 추가
    c.add_polygon([
        (position[0] + cross_width / 2+1, position[1] - size / 2-1),
        (position[0] + size / 2+1, position[1] - size / 2-1),
        (position[0] + size / 2+1, position[1] - cross_width / 2-1),
        (position[0] + cross_width / 2+1, position[1] - cross_width / 2-1)], layer=layer)

    c.flatten()

    return c

# layout = gf.Component()
# paths_list = [gf.path.straight(25), gf.path.arc(radius=100, angle=-90)]
# wg = layout << make_elements.make_path(paths_list, layer=(34, 0), width=0.7)
# bottom_chip = layout << make_bottom_coupler(100, 100, 100, 100, 200, 0.7, 0.3, layer=(34, 0))
# top_chip = layout << make_top_coupler(100, 100, 200, 0.7, 0.3, layer=(34, 0))
# alignkey = layout << add_cross_align_key((0,0))
# alignkey = layout << add_square_align_key((0,0))
# etching = layout << make_oxide_etching(300, 150)
# indium = layout << make_indium_pillar(108, 36)
# layout.show()
