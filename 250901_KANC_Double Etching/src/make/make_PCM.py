from make import make_grating
from make import make_propagationloss
from make import make_assembly
from make import make_elements
from pathlib import Path
from shapely.geometry import Polygon
from shapely.ops import unary_union
import os
import numpy as np
from . import make_grating
import gdsfactory as gf
from gdsfactory.technology import LayerViews
from gdsfactory.config import PATH
from gdsfactory.path import straight, euler, arc
from gdsfactory import Component
from gdsfactory.components.rings import ring_single_bend_coupler, ring_double_bend_coupler, coupler_ring_bend, \
    coupler_bend
from .make_grating import straight_gc_left_arc, straight_gc_right_arc, bend_gc_left_arc, ring_cross_section_outer, \
    bend_gc_right_arc, addpass_left_arc, addpass_right_arc, ring_cross_section_inner, new_straight_gc_right_arc
from .make_elements import grating_coupler_elliptical_arc, make_path
from .make_MZIMMI import make_1x2mmi_core
from gdsfactory.typings import AnyComponentFactory, ComponentSpec, CrossSectionSpec

from gdsfactory.path import straight, arc

# 석영 1x2, 2x2 MMI, MZI
def make_1x2mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer):
    c = gf.Component()

    # 직사각형을 추가합니다. 중심을 기준으로 너비와 높이의 절반만큼의 위치를 계산합니다.
    c.add_polygon([(-mmi_length / 2, -mmi_width / 2), (mmi_length / 2, -mmi_width / 2), (mmi_length / 2, mmi_width / 2),
            (-mmi_length / 2, mmi_width / 2)], layer=layer)

    # 주의: (0,0)은 중심임. y값 주의
    # 입력 포트 left upper
    c.add_port(name='coreinput1', center=(-mmi_length / 2, 0), width=taper_width, orientation=180, layer=layer)

    # 출력 포트 right upper
    c.add_port(name='coreoutput1', center=(mmi_length / 2, (taper_width + mmi_gap)/2), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right lower
    c.add_port(name='coreoutput2', center=(mmi_length / 2, -(taper_width + mmi_gap)/2), width=taper_width, orientation=0, layer=layer)

    Input_taper = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Output_taper_upper = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_lower = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)

    Input_taper.connect('o2', c.ports['coreinput1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_upper.connect('o1', c.ports['coreoutput1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_lower.connect('o1', c.ports['coreoutput2'], allow_layer_mismatch=True,
                               allow_width_mismatch=True)

    c.add_port(name='o1', port=Input_taper[0])
    c.add_port(name='o2', port=Output_taper_upper[1])
    c.add_port(name='o3', port=Output_taper_lower[1])

    c.flatten()

    return c

def make_2x2mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer):
    c = gf.Component()

    # 직사각형을 추가합니다. 중심을 기준으로 너비와 높이의 절반만큼의 위치를 계산합니다.
    c.add_polygon([(-mmi_length / 2, -mmi_width / 2), (mmi_length / 2, -mmi_width / 2), (mmi_length / 2, mmi_width / 2),
            (-mmi_length / 2, mmi_width / 2)], layer=layer)

    # 주의: (0,0)은 중심임. y값 주의
    # 입력 포트 left upper
    c.add_port(name='coreinput1', center=(-mmi_length / 2, (taper_width + mmi_gap)/2), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left lower
    c.add_port(name='coreinput2', center=(-mmi_length / 2, -(taper_width + mmi_gap)/2), width=2, orientation=180, layer=layer)

    # 출력 포트 right upper
    c.add_port(name='coreoutput1', center=(mmi_length / 2, (taper_width + mmi_gap)/2), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right lower
    c.add_port(name='coreoutput2', center=(mmi_length / 2, -(taper_width + mmi_gap)/2), width=taper_width, orientation=0, layer=layer)

    Input_taper_upper = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_lower = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Output_taper_upper = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_lower = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)

    Input_taper_upper.connect('o2', c.ports['coreinput1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_lower.connect('o2', c.ports['coreinput2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_upper.connect('o1', c.ports['coreoutput1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_lower.connect('o1', c.ports['coreoutput2'], allow_layer_mismatch=True,
                               allow_width_mismatch=True)

    c.add_port(name='o1', port=Input_taper_upper[0])
    c.add_port(name='o2', port=Input_taper_lower[0])
    c.add_port(name='o3', port=Output_taper_upper[1])
    c.add_port(name='o4', port=Output_taper_lower[1])
    c.add_port(name='o5', center=(-(mmi_length / 2) - taper_length, 0), width= taper_width, orientation=0, layer=layer)

    c.flatten()

    return c

def make_1x2MMI(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)

    GC1.mirror_x()

    S_wg_input = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                    gf.path.straight(25), gf.path.arc(radius=100, angle=90)
                                                    ], layer=(layer[0], layer[1] + 1),
                                                   width=wg_width + 16)

    Input_taper_clad = c << make_elements.make_taper(wg_width+ 16, mmi_width+ 16, 100, layer=(layer[0], layer[1] + 1))

    S_wg_input.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_clad.connect('o1', S_wg_input_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])

    MMI = c << make_1x2mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)
    MMI_clad = c << make_elements.make_path([gf.path.straight(2 * taper_length + mmi_length)], layer=(layer[0], layer[1] + 1), width=mmi_width + 16)

    MMI.connect('o1', S_wg_input.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    MMI_clad.connect('o1', S_wg_input.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # output 설정
    S_wg_output_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_upper_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                              gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                            gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                             width=wg_width + 16)
    Output_upper_clad = c << make_elements.make_taper(mmi_width + 12.8,  wg_width+ 16, 100, layer=(layer[0], layer[1] + 1))

    S_wg_output_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                               gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                               gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_lower_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                           gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                           gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)
    Output_lower_clad = c << make_elements.make_taper(mmi_width + 12.8,  wg_width+ 16, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_output_upper.connect('o1', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_upper_clad.connect('o1', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper_clad.connect('o1', Output_upper_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # S_wg_output_upper_clad.connect('o1', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_lower_clad.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower_clad.connect('o1', Output_lower_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # S_wg_output_lower_clad.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)

    GC2.connect('o1', S_wg_output_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([-10, 0])

    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)

    GC3.connect('o1', S_wg_output_lower.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC3.move([-10, 0])

    c.flatten()

    return c

def make_2x2MMI(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)

    GC1.mirror_x()
    GC2.mirror_x()

    S_wg_input_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_upper_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=90)
                                                          ], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)
    Input_upper_clad = c << make_elements.make_taper(wg_width + 16, mmi_width + 13.8, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_input_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_lower_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=-90)
                                                          ], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)
    Input_lower_clad = c << make_elements.make_taper(wg_width + 16, mmi_width + 13.8, 100,
                                                     layer=(layer[0], layer[1] + 1))

    S_wg_input_upper.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_upper_clad.connect('o1',S_wg_input_upper_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])

    # MMI 설정
    MMI = c << make_2x2mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)
    MMI_clad = c << make_elements.make_path([gf.path.straight(2 * taper_length + mmi_length)], layer=(layer[0], layer[1] + 1), width=mmi_width + 16)

    MMI.connect('o1', S_wg_input_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower.connect('o2', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_lower_clad.connect('o2', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower_clad.connect('o2', Input_lower_clad['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg_input_lower.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    MMI_clad.connect('o1', MMI.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([10, 0])

    # output 설정
    S_wg_output_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_upper_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                          gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)
    Output_upper_clad = c << make_elements.make_taper(mmi_width + 13.8, wg_width + 16, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_output_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_lower_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                           gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                           gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)
    Output_lower_clad = c << make_elements.make_taper(mmi_width + 13.8, wg_width + 16, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_output_upper.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_upper_clad.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper_clad.connect('o1', Output_upper_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower.connect('o1', MMI.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_lower_clad.connect('o1', MMI.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower_clad.connect('o1', Output_lower_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)


    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)
    GC4 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)

    GC3.connect('o1', S_wg_output_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC4.connect('o1', S_wg_output_lower.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC3.move([-10, 0])
    GC4.move([-10, 0])

    c.flatten()

    return c

def make_2x2_asymmetric_MZI(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, delta_length, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)

    GC1.mirror_x()
    GC2.mirror_x()

    S_wg_input_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_upper_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                              gf.path.straight(25), gf.path.arc(radius=100, angle=90)
                                              ], layer=(layer[0], layer[1] + 1),
                                             width=wg_width + 16)
    Input_upper_clad = c << make_elements.make_taper(wg_width + 16, mmi_width + 12.8, 100,
                                                     layer=(layer[0], layer[1] + 1))

    S_wg_input_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_lower_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=-90)
                                                          ], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)
    Input_lower_clad = c << make_elements.make_taper(wg_width + 16, mmi_width + 12.8, 100,
                                                     layer=(layer[0], layer[1] + 1))

    S_wg_input_upper.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_upper_clad.connect('o1', S_wg_input_upper_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])


    # S_wg_input_lower_clad.connect('o1', GC2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # 첫 번째 MMI 설정
    MMI = c << make_2x2mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)
    MMI_clad = c << make_elements.make_path([gf.path.straight(2 * taper_length + mmi_length)], layer=(layer[0], layer[1] + 1), width=mmi_width + 16)

    MMI.connect('o1', S_wg_input_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower.connect('o2', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_lower_clad.connect('o2', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower_clad.connect('o2', Input_lower_clad['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg_input_lower.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    MMI_clad.connect('o1', MMI.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([10, 0])

    # MZI 설정
    MZI_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=90), gf.path.straight(25),
                                         gf.path.arc(radius=100, angle=90), gf.path.straight(25),
                                         gf.path.arc(radius=100, angle=-90), gf.path.straight(400),
                                         gf.path.arc(radius=100, angle=-90), gf.path.straight(25),
                                        gf.path.arc(radius=100, angle=90), gf.path.straight(100)],
                                             layer=layer, width=wg_width)

    MZI_upper_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=90), gf.path.straight(25),
                                         gf.path.arc(radius=100, angle=90), gf.path.straight(25),
                                         gf.path.arc(radius=100, angle=-90), gf.path.straight(400),
                                         gf.path.arc(radius=100, angle=-90), gf.path.straight(25),
                                        gf.path.arc(radius=100, angle=90), gf.path.straight(100)],
                                                  layer=(layer[0], layer[1] + 1), width=wg_width + 16)

    MZI_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(400), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(25+delta_length/2), gf.path.arc(radius=100, angle=-90), gf.path.straight(25),
                                         gf.path.arc(radius=100, angle=-90), gf.path.straight(25+delta_length/2),
                                         gf.path.arc(radius=100, angle=90), gf.path.straight(100),
                                        gf.path.arc(radius=100, angle=90), gf.path.straight(25),
                                        gf.path.arc(radius=100, angle=-90), gf.path.straight(100)], layer=layer, width=wg_width)

    MZI_lower_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(400), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(25+delta_length/2), gf.path.arc(radius=100, angle=-90), gf.path.straight(25),
                                         gf.path.arc(radius=100, angle=-90), gf.path.straight(25+delta_length/2),
                                         gf.path.arc(radius=100, angle=90), gf.path.straight(100),
                                        gf.path.arc(radius=100, angle=90), gf.path.straight(25),
                                        gf.path.arc(radius=100, angle=-90), gf.path.straight(100)],
                                            layer=(layer[0], layer[1] + 1), width=wg_width + 16)

    MZI_upper.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    MZI_upper_clad.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)

    MZI_lower.connect('o1', MMI.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    MZI_lower_clad.connect('o1', MMI.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # 두 번째 MMI 설정
    MMI2 = c << make_2x2mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)
    MMI2_clad = c << make_elements.make_path([gf.path.straight(2 * taper_length + mmi_length)],
                                            layer=(layer[0], layer[1] + 1), width=mmi_width + 16)

    MMI2.connect('o1', MZI_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    MMI2_clad.connect('o1', MMI2.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # output 설정
    S_wg_output_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_upper_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                          gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)

    S_wg_output_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_lower_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                          gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)

    S_wg_output_upper.connect('o1', MMI2.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper_clad.connect('o1', MMI2.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower.connect('o1', MMI2.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower_clad.connect('o1', MMI2.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)
    GC4 = c << make_elements.grating_coupler_elliptical_arc(wg_width, 0.87, 0.6)

    GC3.connect('o1', S_wg_output_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC4.connect('o1', S_wg_output_lower.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC3.move([-10, 0])
    GC4.move([-10, 0])

    c.flatten()

    return c




## Modified by Taewon
## The R value need to be fixed. (set to inside edge of core now)

def taper(taper_length, taper_tip_width, propagtion_length):
    # parameters
    clad_w = 30
    core_w = 0.7
    period = 0.87
    fill_factor = 0.6
    layer_core = (34, 0)
    layer_clad = (34, 1)

    c = gf.Component()

    # core part
    ## Grating_Coupler
    grating = grating_coupler_elliptical_arc(core_w, period, fill_factor)
    grating_mirror = grating_coupler_elliptical_arc(core_w, period, fill_factor)
    grat = c << grating
    grat_mirror = c << grating_mirror
    grat_mirror = grat_mirror.mirror_x()

    ## bus waveguide
    ### S-bend bus waveguide (left)
    bus_left = c << bend_gc_left_arc(length=100,
                                     layer=layer_core,
                                     width=core_w)
    ### Straight bus waveguie (right)
    bus_right = c << straight_gc_right_arc(length=100,
                                           layer=layer_core,
                                           width=core_w)

    ## taper
    ### taper (left)
    taper_left = c << gf.components.taper(length=taper_length, width1=core_w, width2=taper_tip_width,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    ### taper (right)
    taper_right = c << gf.components.taper(length=taper_length, width1=taper_tip_width, width2=core_w,
                                           with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    taper_right.dxmin = taper_left.dxmax + propagtion_length

    bus_left.connect("o1", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_right.connect("o1", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat.connect("o1", bus_right["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat_mirror.connect("o1", bus_left["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat.move([-10, 0])
    grat_mirror.move([10, 0])

    # clad part
    ## bus waveguide
    ### S-bend bus waveguide (left)
    bus_left = c << bend_gc_left_arc(length=100,
                                     layer=layer_clad,
                                     width=16.7)
    ### Straight bus waveguie (right)
    bus_right = c << straight_gc_right_arc(length=100,
                                           layer=layer_clad,
                                           width=16.7)

    taper_middle = c << make_path([gf.path.straight(propagtion_length)], layer=layer_clad,
                                  width=taper_tip_width + clad_w)

    ## taper
    ### taper (left)
    taper_left = c << gf.components.taper(length=taper_length, width1=core_w + clad_w, width2=taper_tip_width + clad_w,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_clad)
    ### taper (right)
    taper_right = c << gf.components.taper(length=taper_length, width1=taper_tip_width + clad_w, width2=core_w + clad_w,
                                           with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_clad)
    taper_right.dxmin = taper_left.dxmax + propagtion_length

    bus_left.connect("o1", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_right.connect("o1", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_middle.connect("o2", taper_right.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    c.flatten()

    return c


def taper_only(taper_length, taper_tip_width):
    # parameters
    clad_w = 16
    core_w = 0.7
    period = 0.87
    fill_factor = 0.6
    layer_core = (34, 0)
    layer_clad = (34, 1)

    c = gf.Component()

    # core part

    ## taper
    ### taper core
    taper_core = c << gf.components.taper(length=taper_length, width1=core_w, width2=taper_tip_width,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    ### taper clad
    taper_clad = c << gf.components.taper(length=taper_length, width1=core_w + clad_w, width2=taper_tip_width + clad_w,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_clad)

    c.flatten()

    return c


def line_space_pattern(width,line_width, space_width, num_lines):
    pattern = gf.Component()
    for i in range(num_lines):
        line = pattern << gf.components.rectangle(size=(width, line_width), layer=(34,0))
        line.move([0,i*(line_width + space_width)])
    return pattern


#Propagation
def make_snake_propagation(length, radius, layer, width):
    c = gf.Component()

    paths_list = [gf.path.straight(length+100),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(120),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-200),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(100),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-220),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(80),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-240),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(60),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-260),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(40),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-280),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(20),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight((length-490)/2),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(10),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight((length-490)/2),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(20),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-280),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(40),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-260),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(60),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-240),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(80),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-220),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(100),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-200),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(120),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length+100)]


    snake_wg = c << make_elements.make_path(paths_list, layer=layer, width=width)
    snake_wg_clad = c << make_elements.make_path(paths_list, layer=(layer[0], layer[1] + 1), width=width + 16)

    # 포트 설정
    c.add_port(name='o1', port=snake_wg.ports[0])
    c.add_port(name='o2', port=snake_wg.ports[1])

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.6)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.6)

    GC1.mirror_x()
    GC1.mirror_y()
    snake_wg.mirror_x()
    snake_wg_clad.mirror_x()
    snake_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    snake_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', snake_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)


    GC1.move([10, 0])
    GC2.move([-10, 0])

    c.flatten()

    return c

def make_snake_propagation2(length, radius, layer, width):
    c = gf.Component()

    paths_list = [gf.path.straight(length+100),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(160),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-160),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(140),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-180),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(120),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-200),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(100),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-220),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(80),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-240),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(60),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-260),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(40),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(length-280),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(20),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight((length-490)/2),
                  gf.path.arc(radius=radius, angle=-90),
                  gf.path.straight(10),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight((length-490)/2),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(20),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-280),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(40),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-260),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(60),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-240),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(80),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-220),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(100),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length-200),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(120),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length - 180),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(140),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length - 160),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(160),
                  gf.path.arc(radius=radius, angle=90),
                  gf.path.straight(length+100)]


    snake_wg = c << make_elements.make_path(paths_list, layer=layer, width=width)
    snake_wg_clad = c << make_elements.make_path(paths_list, layer=(layer[0], layer[1] + 1), width=width + 16)

    # 포트 설정
    c.add_port(name='o1', port=snake_wg.ports[0])
    c.add_port(name='o2', port=snake_wg.ports[1])

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.6)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.6)

    GC1.mirror_x()
    GC1.mirror_y()
    snake_wg.mirror_x()
    snake_wg_clad.mirror_x()
    snake_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    snake_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', snake_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)


    GC1.move([10, 0])
    GC2.move([-10, 0])

    c.flatten()

    return c


def make_snake_bend(length1, radius, bend_num, layer, width):
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

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.6)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 0.87, 0.6)

    GC1.mirror_x()
    GC1.mirror_y()

    snake_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True)
    snake_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', snake_wg.ports['o2'], allow_layer_mismatch=True)

    GC1.move([10, 0])
    GC2.move([-10, 0])

    c.flatten()

    return c