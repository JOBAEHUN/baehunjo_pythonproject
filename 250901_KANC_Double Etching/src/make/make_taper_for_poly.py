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
    bend_gc_right_arc, addpass_left_arc, addpass_right_arc, ring_cross_section_inner, new_straight_gc_right_arc, \
    bend_gc_arc_180
from .make_elements import grating_coupler_elliptical_arc, make_path
from .make_MZIMMI import make_1x2mmi_core
from gdsfactory.typings import AnyComponentFactory, ComponentSpec, CrossSectionSpec
from make import make_elements


## Modified by Taewon
## The R value need to be fixed. (set to inside edge of core now)

def taper(taper_length, taper_tip_width, propagtion_length, polymer_width, period, fill_factor):
    # parameters
    clad_w = 30
    core_w = 0.7
    layer_core = (34, 0)
    layer_clad = (34, 1)
    layer_polymer = (35, 0)

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

    ### left S-bend ~ Taper waveguide
    bus_connect = c << gf.components.taper(length=100, width1=16.7, width2=core_w + clad_w, with_two_ports=True,
                                           cross_section='strip', with_bbox=True, layer=layer_clad)
    bus_connect_right = c << gf.components.taper(length=100, width1=16.7, width2=core_w + clad_w, with_two_ports=True,
                                                 cross_section='strip', with_bbox=True, layer=layer_clad)
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
    bus_connect.connect("o2", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_connect_right.connect("o2", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    # Polymer part
    ## Coupling Area
    polymer = c << make_path([gf.path.straight(2 * taper_length + propagtion_length)], layer=layer_polymer,
                             width=polymer_width)
    polymer.connect("o1", bus_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    # Text
    Text = c << gf.components.text(
        text="Coupling Length = {0} \n Taper Tip Width ={1},Polymer Width = {2}".format(taper_length, taper_tip_width,
                                                                                        polymer_width), size=30,
        justify="left", layer=(34, 0))
    Text.move([0, 80])

    c.flatten()

    return c


def taper_only(taper_length, taper_tip_width):
    # parameters
    clad_w = 16
    core_w = 0.9
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


def taper_only2(taper_length, taper_tip_width):
    # parameters
    clad_w = 16
    core_w = 0.3
    period = 0.87
    fill_factor = 0.6
    layer_core = (36, 0)
    layer_clad = (36, 1)

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


def make_snake_bend_KANC(length1, radius, bend_num, layer, width, taper_length, taper_tip_width, period, fill_factor):
    # parameters
    clad_w = 30
    core_w = 0.7
    layer_core = (34, 0)
    layer_clad = (34, 1)
    layer_polymer = (35, 0)
    c = gf.Component()

    paths_list = [gf.path.straight(length1),
                  gf.path.arc(radius=radius, angle=-90)]
    angle_sequence = [90, 90, -90, -90]

    for i in range(bend_num):
        angle = angle_sequence[i % 4]
        paths_list.append(gf.path.arc(radius=radius, angle=angle))

    if bend_num % 4 == 0:
        paths_list.append(gf.path.straight(length1))
        paths_list.append(gf.path.arc(radius=radius, angle=-90))
        paths_list.append(gf.path.straight(length1))

    else:
        paths_list.append(gf.path.straight(length1))
        paths_list.append(gf.path.arc(radius=radius, angle=90))
        paths_list.append(gf.path.straight(length1))

    snake_wg = c << make_elements.make_path(paths_list, layer=layer, width=width)
    snake_wg = snake_wg.mirror_y()

    snake_wg_clad = c << make_elements.make_path(paths_list, layer=(34, 1), width=core_w + clad_w)
    snake_wg_clad = snake_wg_clad.mirror_y()

    # core part
    ## Grating_Coupler
    grating = grating_coupler_elliptical_arc(core_w, period, fill_factor)
    grating_mirror = grating_coupler_elliptical_arc(core_w, period, fill_factor)
    grat = c << grating
    grat_mirror = c << grating_mirror
    grat_mirror = grat_mirror.mirror_x()

    ## bus waveguide
    ### S-bend bus waveguide (left)
    bus_left = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=-90), gf.path.straight(100)], layer=layer_core, width=core_w)

    ### Straight bus waveguie (right)
    bus_right = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=90), gf.path.straight(100)], layer=layer_core, width=core_w)

    ## taper
    ### taper (left)
    taper_left = c << gf.components.taper(length=taper_length, width1=core_w, width2=taper_tip_width,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    ### taper (right)
    taper_right = c << gf.components.taper(length=taper_length, width1=taper_tip_width, width2=core_w,
                                           with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    taper_right.dxmin = taper_left.dxmax

    taper_left.connect("o2", snake_wg.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_right.connect("o1", snake_wg.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    bus_left.connect("o1", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_right.connect("o1", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat.connect("o1", bus_right["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat_mirror.connect("o1", bus_left["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat.move([10, 0])
    grat_mirror.move([-10, 0])

    # clad part

    ## bus waveguide
    ### S-bend bus waveguide (left)
    ### S-bend bus waveguide (left)
    bus_left = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=-90), gf.path.straight(100)], layer=layer_clad, width=16.7)

    ### Straight bus waveguie (right)
    bus_right = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=90), gf.path.straight(100)], layer=layer_clad, width=16.7)

    ### left S-bend ~ Taper waveguide
    bus_connect = c << gf.components.taper(length=100, width1=16.7, width2=core_w + clad_w, with_two_ports=True,
                                           cross_section='strip', with_bbox=True, layer=layer_clad)
    bus_connect_right = c << gf.components.taper(length=100, width1=16.7, width2=core_w + clad_w, with_two_ports=True,
                                                 cross_section='strip', with_bbox=True, layer=layer_clad)
    ## taper
    ### taper (left)
    taper_left = c << gf.components.taper(length=taper_length, width1=core_w + clad_w, width2=taper_tip_width + clad_w,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_clad)
    ### taper (right)
    taper_right = c << gf.components.taper(length=taper_length, width1=taper_tip_width + clad_w, width2=core_w + clad_w,
                                           with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_clad)
    taper_right.dxmin = taper_left.dxmax

    taper_left.connect("o2", snake_wg_clad.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_right.connect("o1", snake_wg_clad.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    bus_left.connect("o1", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_right.connect("o1", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)

    # taper_middle.connect("o1",bus_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    bus_connect.connect("o2", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_connect_right.connect("o2", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    # Polymer part
    ## Coupling Area
    polymer = c << make_path([gf.path.straight(taper_length)], layer=layer_polymer, width=width)
    polymer.connect("o1", bus_right.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    polymer = c << make_path([gf.path.straight(taper_length)], layer=layer_polymer, width=width)
    polymer.connect("o1", bus_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    # Text
    Text = c << gf.components.text(
        text="Radius = {0} Bend_num = {1} Coupling Length = {2} Taper Tip Width ={3} Polymer Width = {4}".format(radius,
                                                                                                                 bend_num,
                                                                                                                 taper_length,
                                                                                                                 taper_tip_width,
                                                                                                                 width),
        size=40, justify="left", layer=(34, 0))
    Text.move([-taper_length, 50])

    c.flatten()

    return c


def make_snake_bend(length1, radius, bend_num, layer, width, period, fill_factor):
    # parameters
    clad_w = 30
    core_w = 0.7
    layer_core = (34, 0)
    layer_clad = (34, 1)
    layer_polymer = (35, 0)
    taper_length = 5000
    taper_tip_width = 0.35
    c = gf.Component()

    paths_list = [gf.path.straight(length1),
                  gf.path.arc(radius=radius, angle=-90)]
    angle_sequence = [90, 90, -90, -90]

    for i in range(bend_num):
        angle = angle_sequence[i % 4]
        paths_list.append(gf.path.arc(radius=radius, angle=angle))

    if bend_num % 4 == 0:
        paths_list.append(gf.path.arc(radius=radius, angle=90))
        paths_list.append(gf.path.straight(length1))
    else:
        paths_list.append(gf.path.arc(radius=radius, angle=-90))
        paths_list.append(gf.path.straight(length1))

    snake_wg = c << make_elements.make_path(paths_list, layer=layer, width=width)
    snake_wg_clad = c << make_elements.make_path(paths_list, layer=(layer[0], layer[1] + 1), width=width + 16)

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
    bus_right = c << bend_gc_arc_180(length=100,
                                     layer=layer_core,
                                     width=core_w)

    ## taper
    ### taper (left)
    taper_left = c << gf.components.taper(length=taper_length, width1=core_w, width2=taper_tip_width,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    ### taper (right)
    taper_right = c << gf.components.taper(length=taper_length, width1=taper_tip_width, width2=core_w,
                                           with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    taper_right.dxmin = taper_left.dxmax

    taper_left.connect("o2", snake_wg.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_right.connect("o1", snake_wg.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    bus_left.connect("o1", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_right.connect("o1", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat.connect("o1", bus_right["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat_mirror.connect("o1", bus_left["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat.move([10, 0])
    grat_mirror.move([-10, 0])

    c.flatten()
    return c


def polymer_propagation_loss(taper_length, taper_tip_width, propagtion_length, polymer_width, period, fill_factor,
                             n_loop):
    # parameters
    clad_w = 30
    core_w = 0.7
    layer_core = (34, 0)
    layer_clad = (34, 1)
    layer_polymer = (35, 0)

    c = gf.Component()

    # propagatio nloss
    custom_xs = gf.cross_section.cross_section(width=polymer_width, layer=(35, 0))
    bend_euler_custom = gf.components.bend_euler(radius=200, cross_section=custom_xs)
    # n_loop = int(propagtion_length/2000)
    lt = int(propagtion_length / n_loop) - 400 * np.pi
    propa_loss = c << gf.components.spiral(length=lt, bend=bend_euler_custom, straight='straight',
                                           cross_section=custom_xs, spacing=20, n_loops=n_loop)
    # core part
    ## Grating_Coupler
    grating = grating_coupler_elliptical_arc(core_w, period, fill_factor)
    grating_mirror = grating_coupler_elliptical_arc(core_w, period, fill_factor)
    grat = c << grating
    grat_mirror = c << grating_mirror
    grat_mirror = grat_mirror.mirror_x()

    ## bus waveguide
    ### S-bend bus waveguide (left)
    bus_left = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=-90), gf.path.straight(100)], layer=layer_core, width=core_w)

    ### Straight bus waveguie (right)
    bus_right = c << make_elements.make_path(
        [gf.path.straight(300), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=90), gf.path.straight(100)], layer=layer_core, width=core_w)

    ## taper
    ### taper (left)
    taper_left = c << gf.components.taper(length=taper_length, width1=core_w, width2=taper_tip_width,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    ### taper (right)
    taper_right = c << gf.components.taper(length=taper_length, width1=taper_tip_width, width2=core_w,
                                           with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_core)
    taper_right.dxmin = taper_left.dxmax + propagtion_length

    taper_left.connect("o2", propa_loss.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_right.connect("o1", propa_loss.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    bus_left.connect("o1", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_right.connect("o1", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat.connect("o1", bus_right["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat_mirror.connect("o1", bus_left["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    grat.move([-10, 0])
    grat_mirror.move([10, 0])

    # clad part
    # propagatio nloss
    custom_xs = gf.cross_section.cross_section(width=core_w + clad_w, layer=layer_clad)
    bend_euler_custom = gf.components.bend_euler(radius=200, cross_section=custom_xs)
    # n_loop = int(propagtion_length/2000)
    lt = int(propagtion_length / n_loop) - 400 * np.pi
    propa_loss = c << gf.components.spiral(length=lt, bend=bend_euler_custom, straight='straight',
                                           cross_section=custom_xs, spacing=20, n_loops=n_loop)

    ## bus waveguide
    ### S-bend bus waveguide (left)
    bus_left = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=-90), gf.path.straight(100)], layer=layer_clad, width=16.7)

    ### Straight bus waveguie (right)
    bus_right = c << make_elements.make_path(
        [gf.path.straight(300), gf.path.arc(radius=100, angle=-90), gf.path.straight(100),
         gf.path.arc(radius=100, angle=90), gf.path.straight(100)], layer=layer_clad, width=16.7)

    ### left S-bend ~ Taper waveguide
    bus_connect = c << gf.components.taper(length=100, width1=16.7, width2=core_w + clad_w, with_two_ports=True,
                                           cross_section='strip', with_bbox=True, layer=layer_clad)
    bus_connect_right = c << gf.components.taper(length=100, width1=16.7, width2=core_w + clad_w, with_two_ports=True,
                                                 cross_section='strip', with_bbox=True, layer=layer_clad)
    ## taper
    ### taper (left)
    taper_left = c << gf.components.taper(length=taper_length, width1=core_w + clad_w, width2=taper_tip_width + clad_w,
                                          with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_clad)
    ### taper (right)
    taper_right = c << gf.components.taper(length=taper_length, width1=taper_tip_width + clad_w, width2=core_w + clad_w,
                                           with_two_ports=True, cross_section='strip', with_bbox=True, layer=layer_clad)
    taper_right.dxmin = taper_left.dxmax + propagtion_length

    taper_left.connect("o2", propa_loss.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_right.connect("o1", propa_loss.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    bus_left.connect("o1", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_right.connect("o1", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)

    # taper_middle.connect("o1",bus_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    bus_connect.connect("o2", taper_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    bus_connect_right.connect("o2", taper_right.ports["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    # Polymer part
    ## Coupling Area
    polymer = c << make_path([gf.path.straight(taper_length)], layer=layer_polymer, width=polymer_width)
    polymer.connect("o1", bus_right.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    polymer = c << make_path([gf.path.straight(taper_length)], layer=layer_polymer, width=polymer_width)
    polymer.connect("o1", bus_left.ports["o1"], allow_layer_mismatch=True, allow_width_mismatch=True)

    # Text
    Text = c << gf.components.text(
        text="Coupling Length = {0}\nTaper Tip Width ={1}\nPropagation Length = {2}\nPolymer Width = {3}".format(
            taper_length, taper_tip_width, propagtion_length, polymer_width), size=40, justify="left", layer=(34, 0))
    Text.move([0, 270])

    c.flatten()

    return c

