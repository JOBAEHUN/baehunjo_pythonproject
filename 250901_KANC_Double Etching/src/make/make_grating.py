from pathlib import Path
import os
import numpy as np

from . import make_elements
import gdsfactory as gf
from gdsfactory.technology import LayerViews
from gdsfactory.config import PATH
from gdsfactory.path import straight, euler, arc
from gdsfactory import Component

# 희윤 파트
def Straight_GC_arc(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.straight(length2), gf.path.straight(length1)], layer=layer, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.straight(length2), gf.path.straight(length1)], layer=(layer[0], layer[1] + 1),
        width=16 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    GC1.mirror_x()
    # S_wg.mirror_x()
    # S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])
    GC2.move([-10, 0])
    c.flatten()
    return c


def Bend_GC_arc(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=(layer[0], layer[1] + 1),
        width=16 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    GC1.mirror_x()
    # S_wg.mirror_x()
    # S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])
    GC2.move([-10, 0])
    c.flatten()
    return c


def bend_gc_left_arc(length, layer, width):
    c = gf.Component()
    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(length), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=90), gf.path.straight(100)], layer=layer, width=width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    c.flatten()
    return c

def bend_gc_arc_180(length, layer, width):
    c = gf.Component()
    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(length), gf.path.arc(radius=100, angle=90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=90), gf.path.straight(100)], layer=layer, width=width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    c.flatten()
    return c

def bend_gc_right_arc(length,layer, width):
    c = gf.Component()
    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(length), gf.path.arc(radius=100, angle=90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=-90), gf.path.straight(100)], layer=layer, width=width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    c.flatten()
    return c


def addpass_left_arc(length, layer, width):
    c = gf.Component()
    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=100, angle=-90), gf.path.straight(200),
         gf.path.arc(radius=100, angle=-90), gf.path.straight(length + 100)], layer=layer, width=width)


    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])


    return c

def addpass_right_arc(length, layer, width):
    c = gf.Component()
    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=100, angle=-90), gf.path.straight(200),
         gf.path.arc(radius=100, angle=-90), gf.path.straight(length+100)], layer=layer, width=width)


    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

def straight_gc_left_arc(length,layer, width):
    c = gf.Component()

    # Clad 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(length)], layer=layer, width=width)
    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    c.flatten()
    return c


def straight_gc_right_arc(length, layer, width):
    c = gf.Component()

    # Clad 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(length)], layer=layer, width=width)

    S_wg_mirror = S_wg.mirror_x()
    # 포트 설정
    c.add_port(name='o1', port=S_wg_mirror.ports[0])
    c.add_port(name='o2', port=S_wg_mirror.ports[1])

    c.flatten()
    return c

def new_straight_gc_right_arc(length, layer, width):
    c = gf.Component()

    # Clad 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(length)], layer=layer, width=width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    c.flatten()
    return c


# def ring_cross_section_outer(r, layer, ang, width):
#     c = gf.Component()
#     # cross_section 경로 설정
#     if ang != 0:
#         cross_section = c << make_elements.make_path(
#             [gf.path.arc(radius=100, angle=ang), gf.path.arc(radius=r, angle=-2 * ang),
#              gf.path.arc(radius=100, angle=ang)], layer=layer, width=width)

def ring_cross_section_outer(r,layer,ang,width):
    c = gf.Component()
    # cross_section 경로 설정
    if ang != 0 :
        cross_section = c << make_elements.make_path(
            [gf.path.arc(radius=100,angle=ang),gf.path.arc(radius=r,angle=-2*ang),gf.path.arc(radius=100,angle=ang)], layer=layer, width=width)
    else:
        cross_section = c << make_elements.make_path(
            [gf.path.straight(0)], layer=layer, width=width)

    # 포트 설정
    c.add_port(name='o1', port=cross_section.ports[0])
    c.add_port(name='o2', port=cross_section.ports[1])

    c.flatten()
    return c


# def ring_cross_section_inner(r, layer, ang, width):
#     c = gf.Component()
#     # cross_section 경로 설정
#     if ang != 0:
#         cross_section = c << make_elements.make_path(
#             [gf.path.straight(100), gf.path.arc(radius=100, angle=90), gf.path.straight(100),
#              gf.path.arc(radius=100, angle=-180),
#              gf.path.straight(100), gf.path.arc(radius=100, angle=90), gf.path.straight(100),
#              gf.path.straight(100), gf.path.arc(radius=100, angle=90), gf.path.straight(100),
#              gf.path.arc(radius=100, angle=-90), gf.path.straight(100), ], layer=layer, width=width)

def ring_cross_section_inner(r,layer,ang,width):
    c = gf.Component()
    # cross_section 경로 설정
    if ang != 0 :
        cross_section = c << make_elements.make_path(
            [gf.path.straight(100),gf.path.arc(radius=100,angle=90),gf.path.straight(100),
             gf.path.arc(radius=100,angle=-180),
             gf.path.straight(100),gf.path.arc(radius=100,angle=90),gf.path.straight(100),
             gf.path.straight(100),gf.path.arc(radius=100,angle=90),gf.path.straight(100),
             gf.path.arc(radius=100,angle=-90),gf.path.straight(100),], layer=layer, width=width)
    else:
        cross_section = c << make_elements.make_path(
            [gf.path.straight(0)], layer=layer, width=width)

    # 포트 설정
    c.add_port(name='o1', port=cross_section.ports[0])
    c.add_port(name='o2', port=cross_section.ports[1])

    c.flatten()
    return c

# JHY - Rib GC 소자 측정
def Full_Bend_GC_arc(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    fixed_clad_width = 16.7

    # 초반 40μm 직선 (폭 width)
    S_wg_40 = c << make_elements.make_path([gf.path.straight(40)], layer=layer, width=width)
    S_wg_40_clad = c << make_elements.make_path([gf.path.straight(40)], layer=(layer[0], layer[1] + 1), width=fixed_clad_width)

    # 40μm → 100μm까지 테이퍼 (폭 width → 7)
    taper_to_rib = c << make_elements.make_taper(left_width=width, right_width=7, length=60, layer=layer)
    taper_to_rib_clad = c << make_elements.make_taper(left_width=fixed_clad_width, right_width=fixed_clad_width, length=60, layer=(layer[0], layer[1] + 1))

    # 벤딩 + 직선 + 벤딩 (Rib 유지)
    S_wg_bend = c << make_elements.make_path(
        [gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90)], layer=layer, width=7
    )
    S_wg_bend_clad = c << make_elements.make_path(
        [gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90)], layer=(layer[0], layer[1] + 1), width=fixed_clad_width
    )

    # 300μm 직선 (폭 7 유지)
    S_wg_300 = c << make_elements.make_path([gf.path.straight(300)], layer=layer, width=7)
    S_wg_300_clad = c << make_elements.make_path([gf.path.straight(300)], layer=(layer[0], layer[1] + 1), width=fixed_clad_width)

    # 60μm 테이퍼 (폭 7 → width)
    taper_to_strip = c << make_elements.make_taper(left_width=7, right_width=width, length=60, layer=layer)
    taper_to_strip_clad = c << make_elements.make_taper(left_width=fixed_clad_width, right_width=fixed_clad_width, length=60, layer=(layer[0], layer[1] + 1))

    # 40μm 직선 (폭 width)
    S_wg_last_40 = c << make_elements.make_path([gf.path.straight(40)], layer=layer, width=width)
    S_wg_last_40_clad = c << make_elements.make_path([gf.path.straight(40)], layer=(layer[0], layer[1] + 1), width=fixed_clad_width)

    # GC 연결 추가
    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    # 요소 연결
    taper_to_rib.connect("o1", S_wg_40.ports["o2"])
    taper_to_rib_clad.connect("o1", S_wg_40_clad.ports["o2"])

    S_wg_bend.connect("o1", taper_to_rib.ports["o2"])
    S_wg_bend_clad.connect("o1", taper_to_rib_clad.ports["o2"])

    S_wg_300.connect("o1", S_wg_bend.ports["o2"])
    S_wg_300_clad.connect("o1", S_wg_bend_clad.ports["o2"])

    taper_to_strip.connect("o1", S_wg_300.ports["o2"])
    taper_to_strip_clad.connect("o1", S_wg_300_clad.ports["o2"])

    S_wg_last_40.connect("o1", taper_to_strip.ports["o2"])
    S_wg_last_40_clad.connect("o1", taper_to_strip_clad.ports["o2"])

    # GC 연결
    GC1.connect("o1", S_wg_40.ports["o1"], allow_layer_mismatch=True)
    GC2.connect("o1", S_wg_last_40.ports["o2"], allow_layer_mismatch=True)

    # 위치 조정
    GC1.move([10, 0])
    GC2.move([-10, 0])

    # 포트 설정
    c.add_port(name="o1", port=GC1.ports["o1"])
    c.add_port(name="o2", port=GC2.ports["o1"])

    c.flatten()
    return c

# JHY - Rib GC 소자 측정
def Shallow_Bend_GC_arc(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer, width=width
    )

    # GC 연결 추가
    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor, layer=layer)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor, layer=layer)

    GC1.mirror_x()
    GC1.connect("o1", S_wg.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect("o1", S_wg.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)

    # 위치 조정
    GC1.move([10, 0])
    GC2.move([-10, 0])

    # 포트 설정
    c.add_port(name="o1", port=GC1.ports["o1"])
    c.add_port(name="o2", port=GC2.ports["o1"])

    c.flatten()
    return c

# JHY - IMEC GC 소자 측정
def Bend_GC_standard_arc(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    S_path = [
        gf.path.straight(100),
        gf.path.arc(radius=radius, angle=-90),
        gf.path.straight(length2),
        gf.path.arc(radius=radius, angle=90),
        gf.path.straight(length1),
    ]

    # 메인 웨이브가이드 & 클래딩
    S_wg = c << make_elements.make_path(S_path, layer=layer, width=width)
    clad_layer = (layer[0], layer[1] + 1)
    S_wg_clad = c << make_elements.make_path(S_path, layer=clad_layer, width=width + 16)

    # 포트 정의
    c.add_port(name="o1", port=S_wg.ports[0])
    c.add_port(name="o2", port=S_wg.ports[1])

    # GC 추가
    GC1 = c << make_elements.grating_coupler_standard(
        taper_tip_width=width,
        period=period,
        fill_factor=fill_factor,
        port_width_o1=width + 16,
    )
    GC2 = c << make_elements.grating_coupler_standard(
        taper_tip_width=width,
        period=period,
        fill_factor=fill_factor,
        port_width_o1=width,
    )

    # 연결
    S_wg.connect("o1", GC1.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect("o1", GC1.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect("o1", S_wg.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)

    c.flatten()
    return c

# PSW - G2G 소자 측정
def Straight_GC_standard_arc(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    S_path = [
        gf.path.straight(100),
        gf.path.straight(length2),
        gf.path.straight(length1),
    ]

    # 메인 웨이브가이드 & 클래딩
    S_wg = c << make_elements.make_path(S_path, layer=layer, width=width)
    clad_layer = (layer[0], layer[1] + 1)
    S_wg_clad = c << make_elements.make_path(S_path, layer=clad_layer, width=width + 16)

    # 포트 정의
    c.add_port(name="o1", port=S_wg.ports[0])
    c.add_port(name="o2", port=S_wg.ports[1])

    # GC 추가
    GC1 = c << make_elements.grating_coupler_standard(
        taper_tip_width=width,
        period=period,
        fill_factor=fill_factor,
        port_width_o1=width + 16,
    )
    GC2 = c << make_elements.grating_coupler_standard(
        taper_tip_width=width,
        period=period,
        fill_factor=fill_factor,
        port_width_o1=width,
    )

    # 연결
    S_wg.connect("o1", GC1.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect("o1", GC1.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect("o1", S_wg.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)

    c.flatten()
    return c
