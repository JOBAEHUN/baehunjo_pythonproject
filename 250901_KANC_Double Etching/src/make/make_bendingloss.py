from pathlib import Path
import os
import numpy as np
from make import make_grating
from make import make_propagationloss
import gdsfactory as gf
from gdsfactory.technology import LayerViews
from gdsfactory.config import PATH
from gdsfactory.path import straight, euler, arc
from make import make_assembly
from make import make_elements

def make_snake_bend(length1, radius, bend_num, layer, width, period, fill_factor):
    c = gf.Component()

    paths_list = [gf.path.straight(length1),
                  gf.path.arc(radius=radius, angle=-90)]
    angle_sequence = [90, 90, -90, -90]

    for i in range(bend_num):
        angle = angle_sequence[i % 4]
        paths_list.append(gf.path.arc(radius=radius, angle=angle))

    if  bend_num % 4 == 0:
        paths_list.append(gf.path.arc(radius=radius, angle=90))
        paths_list.append(gf.path.straight(length1))
    else:
        paths_list.append(gf.path.arc(radius=radius, angle=-90))
        paths_list.append(gf.path.straight(length1))

    snake_wg = c << make_elements.make_path(paths_list, layer=layer, width=width)
    snake_wg_clad = c << make_elements.make_path(paths_list, layer= (layer[0], layer[1] + 1), width=width + 16)

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    GC1.mirror_x()
    GC1.mirror_y()

    snake_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True)
    snake_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', snake_wg.ports['o2'], allow_layer_mismatch=True)

    GC1.move([10, 0])
    GC2.move([-10, 0])

    c.flatten()

    return c

def make_full_snake_bend(length1, radius, bend_num, layer, width, period, fill_factor):
    c = gf.Component()

    width_rib = 7                # Rib waveguide 폭
    fixed_clad_width = 16.7      # 클래딩 폭 고정

    # ▽ Strip 시작부 (40 μm)
    S_strip = c << make_elements.make_path([straight(40)], layer=layer, width=width)
    S_strip_clad = c << make_elements.make_path([straight(40)], layer=(layer[0], layer[1] + 1), width=fixed_clad_width)

    # ▽ Taper: Strip → Rib (60 μm)
    taper_in = c << make_elements.make_taper(left_width=width, right_width=width_rib, length=60, layer=layer)
    taper_in_clad = c << make_elements.make_taper(left_width=fixed_clad_width, right_width=fixed_clad_width, length=60, layer=(layer[0], layer[1] + 1))

    # ▽ Rib 경로 구성
    rib_start = [straight(length1 - 100), arc(radius=radius, angle=-90)]
    angle_sequence = [90, 90, -90, -90]

    for i in range(bend_num):
        rib_start.append(arc(radius=radius, angle=angle_sequence[i % 4]))

    final_arc = arc(radius=radius, angle=90 if bend_num % 4 == 0 else -90)
    rib_end = [final_arc, straight(length1 - 100)]
    rib_paths = rib_start + rib_end

    core = c << make_elements.make_path(rib_paths, layer=layer, width=width_rib)
    core_clad = c << make_elements.make_path(rib_paths, layer=(layer[0], layer[1] + 1), width=fixed_clad_width)

    # ▽ Rib → Strip으로 복원
    taper_out = c << make_elements.make_taper(left_width=width_rib, right_width=width, length=60, layer=layer)
    taper_out_clad = c << make_elements.make_taper(left_width=fixed_clad_width, right_width=fixed_clad_width, length=60, layer=(layer[0], layer[1] + 1))

    S_out = c << make_elements.make_path([straight(40)], layer=layer, width=width)
    S_out_clad = c << make_elements.make_path([straight(40)], layer=(layer[0], layer[1] + 1), width=fixed_clad_width)

    # 연결
    taper_in.connect("o1", S_strip.ports["o2"])
    taper_in_clad.connect("o1", S_strip_clad.ports["o2"])
    core.connect("o1", taper_in.ports["o2"])
    core_clad.connect("o1", taper_in_clad.ports["o2"])
    taper_out.connect("o1", core.ports["o2"])
    taper_out_clad.connect("o1", core_clad.ports["o2"])
    S_out.connect("o1", taper_out.ports["o2"])
    S_out_clad.connect("o1", taper_out_clad.ports["o2"])

    # GC 연결
    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    GC1.connect("o1", S_strip.ports["o1"], allow_layer_mismatch=True)
    GC2.connect("o1", S_out.ports["o2"], allow_layer_mismatch=True)
    GC1.move([10, 0])
    GC2.move([-10, 0])

    # 포트 등록
    c.add_port("o1", GC1.ports["o1"])
    c.add_port("o2", GC2.ports["o1"])

    c.flatten()
    return c

def make_shallow_snake_bend(length1, radius, bend_num, layer, width, period, fill_factor):
    c = gf.Component()

    # ▽ 경로 구성 (Full 구조와 동일하게)
    rib_start = [straight(length1 - 0), arc(radius=radius, angle=-90)]
    angle_sequence = [90, 90, -90, -90]

    for i in range(bend_num):
        rib_start.append(arc(radius=radius, angle=angle_sequence[i % 4]))

    final_arc = arc(radius=radius, angle=90 if bend_num % 4 == 0 else -90)
    rib_end = [final_arc, straight(length1 - 0)]
    rib_paths = rib_start + rib_end

    # ▽ Snake waveguide 생성 (shallow etch)
    snake_wg = c << make_elements.make_path(rib_paths, layer=layer, width=width)

    # ▽ GC 생성
    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor, layer=layer)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor, layer=layer)

    # ▽ 연결
    GC1.connect("o1", snake_wg.ports["o1"], allow_width_mismatch=True)
    GC2.connect("o1", snake_wg.ports["o2"], allow_width_mismatch=True)
    GC1.move([10, 0])
    GC2.move([-10, 0])

    # ▽ 포트 지정
    c.add_port("o1", GC1.ports["o1"])
    c.add_port("o2", GC2.ports["o1"])

    c.flatten()
    return c