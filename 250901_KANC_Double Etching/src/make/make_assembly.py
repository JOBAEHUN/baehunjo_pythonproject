import numpy as np
from . import make_elements
import gdsfactory as gf
from gdsfactory.path import straight, arc

# 석현 파트
def Dicing_key(layer, width_dic, length_dic):
    c = gf.Component()

    top_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)
    mid_box = c << make_elements.make_box(layer, 50)
    r_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)

    top_box.connect('o1', mid_box.ports['o2'], allow_layer_mismatch=True)
    r_box.connect('o1', mid_box.ports['o3'], allow_layer_mismatch=True)

    return c


def Sbend_edge_coupler_In(layer_core,layer_clad, length, width, length_dic, struc_num, shape_num):
    c = gf.Component()

    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=20, angle=-90), gf.path.straight(25),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length)], layer=layer_core, width=width)
    dicing_wg = c << make_elements.make_path([straight(length_dic)], layer_core, width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=20, angle=-90), gf.path.straight(25),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length)], layer=layer_clad, width=width+10)
    dicing_wg_clad = c << make_elements.make_path([straight(length_dic)], layer_clad, width + 10)

    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
            # GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.5)
            # GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
            # GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)
            # GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
            # GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)
            # GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)


    GC1.mirror_x()
    S_wg.connect('o2', dicing_wg.ports['o1'], allow_layer_mismatch=True)
    S_wg_clad.connect('o2', dicing_wg_clad.ports['o1'],allow_layer_mismatch=True)
    GC1.connect('o1', S_wg.ports['o1'], allow_layer_mismatch=True)

    if shape_num ==1:
        GC1.move([10,0])
        # GC2.move([-10,0])

    return c


def Sbend_edge_coupler_Out(layer_core,layer_clad, length, width, length_dic, struc_num, shape_num):
    c = gf.Component()

    dicing_wg = c << make_elements.make_path([straight(length_dic)], layer_core, width)
    strip_wg = c << make_elements.make_path([straight(length)], layer_core, width)
    dicing_wg_clad = c << make_elements.make_path([straight(length_dic)], layer_clad, width + 10)
    strip_wg_clad = c << make_elements.make_path([straight(length)], layer_clad, width + 10)
    # GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, wavelength, grating_line_width)

    if struc_num == 0:
        if shape_num == 0:
            # GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
        else:
            # GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            # GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
        else:
            # GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)
    else:
        if shape_num == 0:
            # GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
        else:
            # GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)

    strip_wg.connect('o1', dicing_wg.ports['o2'], allow_layer_mismatch=True)
    strip_wg_clad.connect('o1', dicing_wg_clad.ports['o2'],allow_layer_mismatch=True)
    GC2.connect('o1', strip_wg.ports['o2'], allow_layer_mismatch=True)

    if shape_num ==1:
    #     # GC1.move([0,10])
        GC2.move([-10,0])

    return c


def inverse_taper_edge_coupler_In(layer_core, layer_clad, width, width_max, length_taper, length_dic,struc_num, shape_num):
    c = gf.Component()

    dicing_wg = c << make_elements.make_path([straight(length_dic)], layer_core, width_max)
    Sbend_wg = c << make_elements.make_path(
        [straight(100), arc(radius=20, angle=-90), straight(25),
         arc(radius=20, angle=90), straight((400-length_taper)+(125-length_dic))], layer=layer_core, width=width)
    inverse_taper_in = c << make_elements.make_taper(width, width_max, length_taper, layer_core)
    dicing_wg_clad = c << make_elements.make_path([straight(length_dic)], layer_clad, width_max + 10)
    Sbend_wg_clad = c << make_elements.make_path(
        [straight(100), arc(radius=20, angle=-90), straight(25),
         arc(radius=20, angle=90), straight((400-length_taper)+(125-length_dic))], layer=layer_clad, width=width+10)
    inverse_taper_in_clad = c << make_elements.make_taper(width + 10, width_max + 10, length_taper, layer_clad)

    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
            # GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.5)
            # GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
            # GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)
            # GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
            # GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)
            # GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)


    GC1.mirror_x()

    inverse_taper_in.connect('o2', dicing_wg.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Sbend_wg.connect('o2', inverse_taper_in.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    inverse_taper_in_clad.connect('o2', dicing_wg_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Sbend_wg_clad.connect('o2', inverse_taper_in_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC1.connect('o1', Sbend_wg.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    if shape_num ==1:
        GC1.move([10,0])
        # GC2.move([-10,0])

    return c


def inverse_taper_edge_coupler_Out(layer_core, layer_clad, width, width_max, length_taper, length_dic,struc_num, shape_num):
    c = gf.Component()

    strip_wg = c << make_elements.make_path([straight((400 - length_taper) + (125 - length_dic))], layer_core, width)
    dicing_wg = c << make_elements.make_path([straight(length_dic)], layer_core, width_max)
    inverse_taper_out = c << make_elements.make_taper(width_max, width, length_taper, layer_core)
    strip_wg_clad = c << make_elements.make_path([straight((400 - length_taper) + (125 - length_dic))], layer_clad, width + 10)
    dicing_wg_clad = c << make_elements.make_path([straight(length_dic)], layer_clad, width_max + 10)
    inverse_taper_out_clad = c << make_elements.make_taper(width + 10, width_max + 10, length_taper, layer_clad)

    if struc_num == 0:
        if shape_num == 0:
            # GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
        else:
            # GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            # GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
        else:
            # GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1, fill_factor=0.6)
    else:
        if shape_num == 0:
            # GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
        else:
            # GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)

    inverse_taper_out.connect('o1', dicing_wg.ports['o2'], allow_layer_mismatch=True)
    strip_wg.connect('o1', inverse_taper_out.ports['o2'], allow_layer_mismatch=True)
    inverse_taper_out_clad.connect('o2', dicing_wg_clad.ports['o2'], allow_layer_mismatch=True)
    strip_wg_clad.connect('o2', inverse_taper_out_clad.ports['o1'], allow_layer_mismatch=True)
    GC2.connect('o1', strip_wg.ports['o2'], allow_layer_mismatch=True)

    if shape_num ==1:
    #     # GC1.move([0,10])
        GC2.move([-10,0])

    return c


#유진스 파트

def make_oband_mmi(length_mmi, width_mmi, center_mmi, length_taper, width_start_taper,
                   width_end_taper, S_wg_length, layer, layer2,struc_num, shape_num):

    c = gf.Component()


    # Create MMI core with specified parameters
    MMIcore = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi, center=center_mmi, layer=layer)


    # Create Taper with specified parameters
    left_upper_Taper = c << make_elements.make_taper(left_width=width_start_taper, right_width=width_end_taper, length=length_taper, layer=layer)
    left_lower_Taper = c << make_elements.make_taper(left_width=width_start_taper, right_width=width_end_taper, length=length_taper, layer=layer)
    right_upper_Taper = c << make_elements.make_taper(left_width=width_end_taper, right_width=width_start_taper, length=length_taper, layer=layer)
    right_lower_Taper = c << make_elements.make_taper(left_width=width_end_taper, right_width=width_start_taper, length=length_taper, layer=layer)

    ##포트 붙이기
    # Connect Taper's output to MMI core's input
    left_upper_Taper.connect("o2", MMIcore.ports["coreinput1"], allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_Taper.connect("o2", MMIcore.ports["coreinput2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_upper_Taper.connect("o1", MMIcore.ports["coreoutput1"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_Taper.connect("o1", MMIcore.ports["coreoutput2"], allow_layer_mismatch=True,allow_width_mismatch=True)


    S_wg1 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)
    S_wg1.mirror()

    S_wg2 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)
    S_wg2.mirror()

    S_wg3 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)

    S_wg4 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)

    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.05, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.05, fill_factor=0.6)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.05, fill_factor=0.6)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.05, fill_factor=0.6)

    # 포트 설정
    c.add_port(name='o1', port=S_wg1.ports[0])
    c.add_port(name='o2', port=S_wg1.ports[1])
    c.add_port(name='o1', port=S_wg2.ports[0])
    c.add_port(name='o2', port=S_wg2.ports[1])
    c.add_port(name='o1', port=S_wg3.ports[0])
    c.add_port(name='o2', port=S_wg3.ports[1])
    c.add_port(name='o1', port=S_wg4.ports[0])
    c.add_port(name='o2', port=S_wg4.ports[1])

    S_wg1.connect('o1', left_upper_Taper.ports['o1'], allow_layer_mismatch=True, mirror=True,allow_width_mismatch=True)
    GC1.connect('o1', S_wg1.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg2.connect('o1', left_lower_Taper.ports['o1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    GC2.connect('o1', S_wg2.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg3.connect('o1', right_upper_Taper.ports['o2'], allow_layer_mismatch=True, mirror=True,allow_width_mismatch=True)
    GC3.connect('o1', S_wg3.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg4.connect('o1', right_lower_Taper.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    GC4.connect('o1', S_wg4.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    ##cladding
    MMIcore_cl = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi + 10, center=center_mmi, layer=layer2)

    # Create Taper with specified parameters
    left_upper_Taper_cl = c << make_elements.make_taper(left_width=width_start_taper + 10, right_width=width_end_taper + 10,
                                                        length=length_taper, layer=layer2)
    left_lower_Taper_cl = c << make_elements.make_taper(left_width=width_start_taper + 10, right_width=width_end_taper + 10,
                                                        length=length_taper, layer=layer2)
    right_upper_Taper_cl = c << make_elements.make_taper(left_width=width_end_taper + 10, right_width=width_start_taper + 10,
                                                         length=length_taper, layer=layer2)
    right_lower_Taper_cl = c << make_elements.make_taper(left_width=width_end_taper + 10, right_width=width_start_taper + 10,
                                                         length=length_taper, layer=layer2)

    S_wg1_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2, width=width_start_taper +10)
    S_wg1_cl.mirror()

    S_wg2_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2, width=width_start_taper+10)
    S_wg2_cl.mirror()

    S_wg3_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2, width=width_start_taper+10)

    S_wg4_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2, width=width_start_taper+10)

    ##cladding 포트 붙이기
    # Connect Taper's output to MMI core's input
    left_upper_Taper_cl.connect("o2", MMIcore_cl.ports["coreinput1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    left_lower_Taper_cl.connect("o2", MMIcore_cl.ports["coreinput2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    right_upper_Taper_cl.connect("o1", MMIcore_cl.ports["coreoutput1"], allow_layer_mismatch=True, allow_width_mismatch=True)
    right_lower_Taper_cl.connect("o1", MMIcore_cl.ports["coreoutput2"], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg1_cl.connect('o1', left_upper_Taper_cl.ports['o1'], allow_layer_mismatch=True, mirror=True, allow_width_mismatch=True)

    S_wg2_cl.connect('o1', left_lower_Taper_cl.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg3_cl.connect('o1', right_upper_Taper_cl.ports['o2'], allow_layer_mismatch=True, mirror=True,
                  allow_width_mismatch=True)

    S_wg4_cl.connect('o1', right_lower_Taper_cl.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    if shape_num == 1:
        GC1.move([10, 0])
        GC2.move([10, 0])
        GC3.move([-10, 0])
        GC4.move([-10, 0])

    return c

def make_oband_switch(sbend_radius,length_mmi, width_mmi, center_mmi, length_taper, width_start_taper,
                   width_end_taper, S_wg_length, flat_length, center_flat, layer,layer2,struc_num, shape_num):

    c = gf.Component()

    # Create MMI core with specified parameters
    MMIcore = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi, center=center_mmi, layer=layer)

    # Create Taper with specified parameters
    left_upper_Taper = c << make_elements.make_taper(left_width=width_start_taper, right_width=width_end_taper, length=length_taper, layer=layer)
    left_lower_Taper = c << make_elements.make_taper(left_width=width_start_taper, right_width=width_end_taper, length=length_taper, layer=layer)
    right_upper_Taper = c << make_elements.make_taper(left_width=width_end_taper, right_width=width_start_taper, length=length_taper, layer=layer)
    right_lower_Taper = c << make_elements.make_taper(left_width=width_end_taper, right_width=width_start_taper, length=length_taper, layer=layer)

    # taper, sbend 사이 left flat
    left_upper_flat = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper, layer=layer, center=center_flat)
    left_lower_flat = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper, layer=layer, center=center_flat)


    left_upper_sbend = c << make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper, layer=layer)
    left_lower_sbend = c.add_ref(make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper, layer=layer))
    left_lower_sbend.mirror()
    right_upper_sbend = c.add_ref(make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper, layer=layer))
    right_upper_sbend.mirror_x()
    ##x,y둘다 대칭은 port에서 mirror=true
    right_lower_sbend = c.add_ref(make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper, layer=layer))

    #높이
    S_wg_upper_left0 = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=0)], layer=layer, width=width_start_taper)

    S_wg_upper_right0 = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=30)], layer=layer, width=width_start_taper)

    S_wg_lower_left0 = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=0)], layer=layer, width=width_start_taper)

    S_wg_lower_right0 = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=30)], layer=layer, width=width_start_taper)
    S_wg_lower_right0.mirror()

    c.add_port(name='o1', port=S_wg_upper_left0.ports[0])
    c.add_port(name='o2', port=S_wg_upper_left0.ports[1])
    c.add_port(name='o1', port=S_wg_upper_right0.ports[0])
    c.add_port(name='o2', port=S_wg_upper_right0.ports[1])
    c.add_port(name='o1', port=S_wg_lower_left0.ports[0])
    c.add_port(name='o2', port=S_wg_lower_left0.ports[1])
    c.add_port(name='o1', port=S_wg_lower_right0.ports[0])
    c.add_port(name='o2', port=S_wg_lower_right0.ports[1])

    #중앙 반원 mzi
    ##안쪽 위
    S_wg_upper_left = c << make_elements.make_path(
        [gf.path.straight(30), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=0)], layer=layer, width=width_start_taper)

    S_wg_upper_right = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=530)], layer=layer, width=width_start_taper)

    ##안쪽 아래
    S_wg_lower_left = c << make_elements.make_path(
        [gf.path.straight(30), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=0)], layer=layer, width=width_start_taper)
    S_wg_lower_left.mirror()

    S_wg_lower_right = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=530)], layer=layer, width=width_start_taper)



    c.add_port(name='o1', port=S_wg_upper_left.ports[0])
    c.add_port(name='o2', port=S_wg_upper_left.ports[1])
    c.add_port(name='o1', port=S_wg_upper_right.ports[0])
    c.add_port(name='o2', port=S_wg_upper_right.ports[1])
    c.add_port(name='o1', port=S_wg_lower_left.ports[0])
    c.add_port(name='o2', port=S_wg_lower_left.ports[1])
    c.add_port(name='o1', port=S_wg_lower_right.ports[0])
    c.add_port(name='o2', port=S_wg_lower_right.ports[1])

    # taper, sbend 사이 right flat
    right_upper_flat = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper, layer=layer, center=center_flat)
    right_lower_flat = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper, layer=layer, center=center_flat)

    #2번째 mmi
    # Create MMI core with specified parameters
    MMIcore2 = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi, center=center_mmi, layer=layer)

    # Create Taper with specified parameters
    left_upper_Taper2 = c << make_elements.make_taper(left_width=width_start_taper,
                                                      right_width=width_end_taper, length=length_taper, layer=layer)
    left_lower_Taper2 = c << make_elements.make_taper(left_width=width_start_taper,
                                                      right_width=width_end_taper, length=length_taper, layer=layer)
    right_upper_Taper2 = c << make_elements.make_taper(left_width=width_end_taper,
                                                       right_width=width_start_taper, length=length_taper, layer=layer)
    right_lower_Taper2 = c << make_elements.make_taper(left_width=width_end_taper,
                                                       right_width=width_start_taper, length=length_taper, layer=layer)

    ##포트 붙이기
    # Connect Taper's output to MMI core's input
    left_upper_Taper.connect("o2", MMIcore.ports["coreinput1"], allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_Taper.connect("o2", MMIcore.ports["coreinput2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_upper_Taper.connect("o1", MMIcore.ports["coreoutput1"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_Taper.connect("o1", MMIcore.ports["coreoutput2"], allow_layer_mismatch=True,allow_width_mismatch=True)

    #MZI
    left_upper_flat.connect("input",right_upper_Taper["o2"],allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_flat.connect("input", right_lower_Taper["o2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    left_upper_sbend.connect("input",left_upper_flat["output"],allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_sbend.connect("input",left_lower_flat["output"],allow_layer_mismatch=True,allow_width_mismatch=True)

    #높이
    S_wg_upper_left0.connect("o1", left_upper_sbend["output"], allow_layer_mismatch=True, allow_width_mismatch=True,
                            mirror=True)
    S_wg_lower_left0.connect("o1", left_lower_sbend["output"], allow_layer_mismatch=True, allow_width_mismatch=True, mirror=True )

    S_wg_upper_left.connect("o1",S_wg_upper_left0["o2"],allow_layer_mismatch=True,allow_width_mismatch=True)
    S_wg_lower_left.connect("o1",S_wg_lower_left0["o2"],allow_layer_mismatch=True,allow_width_mismatch=True,mirror=True)
    S_wg_upper_right.connect("o1",S_wg_upper_left["o2"],allow_layer_mismatch=True,allow_width_mismatch=True,mirror=True)
    S_wg_lower_right.connect("o1",S_wg_lower_left["o2"],allow_layer_mismatch=True,allow_width_mismatch=True,mirror=True)

    # 높이
    S_wg_upper_right0.connect("o1", S_wg_upper_right["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_lower_right0.connect("o1", S_wg_lower_right["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,mirror=True)


    right_upper_sbend.connect("input",S_wg_upper_right0["o2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_sbend.connect("input",S_wg_lower_right0["o2"], allow_layer_mismatch=True,allow_width_mismatch=True, mirror=True)
    right_upper_flat.connect("input",right_upper_sbend["output"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_flat.connect("input", right_lower_sbend["output"], allow_layer_mismatch=True,allow_width_mismatch=True)

    # 2번째 mmi port
    left_upper_Taper2.connect("o1", right_upper_flat.ports["output"], allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_Taper2.connect("o1", right_lower_flat.ports["output"], allow_layer_mismatch=True,allow_width_mismatch=True)
    MMIcore2.connect("coreinput2", left_upper_Taper2.ports["o2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    MMIcore2.connect("coreinput1", left_lower_Taper2.ports["o2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_upper_Taper2.connect("o1", MMIcore2.ports["coreoutput1"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_Taper2.connect("o1", MMIcore2.ports["coreoutput2"], allow_layer_mismatch=True,allow_width_mismatch=True)


    S_wg1 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)
    S_wg1.mirror()

    S_wg2 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)
    S_wg2.mirror()

    S_wg3 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)

    S_wg4 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)

    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.05, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.05, fill_factor=0.6)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.05, fill_factor=0.6)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.05, fill_factor=0.6)

    # 포트 설정
    c.add_port(name='o1', port=S_wg1.ports[0])
    c.add_port(name='o2', port=S_wg1.ports[1])
    c.add_port(name='o1', port=S_wg2.ports[0])
    c.add_port(name='o2', port=S_wg2.ports[1])
    c.add_port(name='o1', port=S_wg3.ports[0])
    c.add_port(name='o2', port=S_wg3.ports[1])
    c.add_port(name='o1', port=S_wg4.ports[0])
    c.add_port(name='o2', port=S_wg4.ports[1])

    S_wg1.connect('o1', left_upper_Taper.ports['o1'], allow_layer_mismatch=True, mirror=True,allow_width_mismatch=True)
    GC1.connect('o1', S_wg1.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg2.connect('o1', left_lower_Taper.ports['o1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    GC2.connect('o1', S_wg2.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg3.connect('o1', right_upper_Taper2.ports['o2'], allow_layer_mismatch=True, mirror=True,allow_width_mismatch=True)
    GC3.connect('o1', S_wg3.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg4.connect('o1', right_lower_Taper2.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    GC4.connect('o1', S_wg4.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    ##cldding

    MMIcore_cl = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi + 10, center=center_mmi,
                                                 layer=layer2)

    # Create Taper with specified parameters
    left_upper_Taper_cl = c << make_elements.make_taper(left_width=width_start_taper + 10,
                                                        right_width=width_end_taper + 10, length=length_taper,
                                                        layer=layer2)
    left_lower_Taper_cl = c << make_elements.make_taper(left_width=width_start_taper + 10,
                                                        right_width=width_end_taper + 10, length=length_taper,
                                                        layer=layer2)
    right_upper_Taper_cl = c << make_elements.make_taper(left_width=width_end_taper + 10,
                                                         right_width=width_start_taper + 10, length=length_taper,
                                                         layer=layer2)
    right_lower_Taper_cl = c << make_elements.make_taper(left_width=width_end_taper + 10,
                                                         right_width=width_start_taper + 10, length=length_taper,
                                                         layer=layer2)

    # taper, sbend 사이 left flat
    left_upper_flat_cl = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper + 10, layer=layer2,
                                                         center=center_flat)
    left_lower_flat_cl = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper + 10, layer=layer2,
                                                         center=center_flat)

    left_upper_sbend_cl = c << make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper + 10, layer=layer2)
    left_lower_sbend_cl = c.add_ref(
        make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper + 10, layer=layer2))
    left_lower_sbend_cl.mirror()
    right_upper_sbend_cl = c.add_ref(
        make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper + 10, layer=layer2))
    right_upper_sbend_cl.mirror_x()
    ##x,y둘다 대칭은 port에서 mirror=true
    right_lower_sbend_cl = c.add_ref(
        make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper + 10, layer=layer2))

    # 높이
    S_wg_upper_left0_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=0)], layer=layer2, width=width_start_taper + 10)

    S_wg_upper_right0_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=30)], layer=layer2, width=width_start_taper + 10)

    S_wg_lower_left0_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=0)], layer=layer2, width=width_start_taper + 10)

    S_wg_lower_right0_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=30)], layer=layer2, width=width_start_taper + 10)
    S_wg_lower_right0_cl.mirror()

    c.add_port(name='o1', port=S_wg_upper_left0_cl.ports[0])
    c.add_port(name='o2', port=S_wg_upper_left0_cl.ports[1])
    c.add_port(name='o1', port=S_wg_upper_right0_cl.ports[0])
    c.add_port(name='o2', port=S_wg_upper_right0_cl.ports[1])
    c.add_port(name='o1', port=S_wg_lower_left0_cl.ports[0])
    c.add_port(name='o2', port=S_wg_lower_left0_cl.ports[1])
    c.add_port(name='o1', port=S_wg_lower_right0_cl.ports[0])
    c.add_port(name='o2', port=S_wg_lower_right0_cl.ports[1])

    # 중앙 반원 mzi
    ##안쪽 위
    S_wg_upper_left_cl = c << make_elements.make_path(
        [gf.path.straight(30), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=0)], layer=layer2, width=width_start_taper + 10)

    S_wg_upper_right_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=530)], layer=layer2, width=width_start_taper + 10)

    ##안쪽 아래
    S_wg_lower_left_cl = c << make_elements.make_path(
        [gf.path.straight(30), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=0)], layer=layer2, width=width_start_taper + 10)
    S_wg_lower_left_cl.mirror()

    S_wg_lower_right_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=530)], layer=layer2, width=width_start_taper + 10)

    c.add_port(name='o1', port=S_wg_upper_left_cl.ports[0])
    c.add_port(name='o2', port=S_wg_upper_left_cl.ports[1])
    c.add_port(name='o1', port=S_wg_upper_right_cl.ports[0])
    c.add_port(name='o2', port=S_wg_upper_right_cl.ports[1])
    c.add_port(name='o1', port=S_wg_lower_left_cl.ports[0])
    c.add_port(name='o2', port=S_wg_lower_left_cl.ports[1])
    c.add_port(name='o1', port=S_wg_lower_right_cl.ports[0])
    c.add_port(name='o2', port=S_wg_lower_right_cl.ports[1])

    # taper, sbend 사이 right flat
    right_upper_flat_cl = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper + 10,
                                                          layer=layer2, center=center_flat)
    right_lower_flat_cl = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper + 10,
                                                          layer=layer2, center=center_flat)

    # 2번째 mmi
    # Create MMI core with specified parameters
    MMIcore2_cl = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi + 10, center=center_mmi,
                                                  layer=layer2)

    # Create Taper with specified parameters
    left_upper_Taper2_cl = c << make_elements.make_taper(left_width=width_start_taper + 10,
                                                         right_width=width_end_taper + 10, length=length_taper,
                                                         layer=layer2)
    left_lower_Taper2_cl = c << make_elements.make_taper(left_width=width_start_taper + 10,
                                                         right_width=width_end_taper + 10, length=length_taper,
                                                         layer=layer2)
    right_upper_Taper2_cl = c << make_elements.make_taper(left_width=width_end_taper + 10,
                                                          right_width=width_start_taper + 10, length=length_taper,
                                                          layer=layer2)
    right_lower_Taper2_cl = c << make_elements.make_taper(left_width=width_end_taper + 10,
                                                          right_width=width_start_taper + 10, length=length_taper,
                                                          layer=layer2)

    ##포트 붙이기
    # Connect Taper's output to MMI core's input
    left_upper_Taper_cl.connect("o2", MMIcore_cl.ports["coreinput1"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)
    left_lower_Taper_cl.connect("o2", MMIcore_cl.ports["coreinput2"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)
    right_upper_Taper_cl.connect("o1", MMIcore_cl.ports["coreoutput1"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)
    right_lower_Taper_cl.connect("o1", MMIcore_cl.ports["coreoutput2"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)

    # MZI
    left_upper_flat_cl.connect("input", right_upper_Taper_cl["o2"], allow_layer_mismatch=True,
                               allow_width_mismatch=True)
    left_lower_flat_cl.connect("input", right_lower_Taper_cl["o2"], allow_layer_mismatch=True,
                               allow_width_mismatch=True)
    left_upper_sbend_cl.connect("input", left_upper_flat_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)
    left_lower_sbend_cl.connect("input", left_lower_flat_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)

    # 높이
    S_wg_upper_left0_cl.connect("o1", left_upper_sbend_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True,
                                mirror=True)
    S_wg_lower_left0_cl.connect("o1", left_lower_sbend_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True, mirror=True)

    S_wg_upper_left_cl.connect("o1", S_wg_upper_left0_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_lower_left_cl.connect("o1", S_wg_lower_left0_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,
                               mirror=True)
    S_wg_upper_right_cl.connect("o1", S_wg_upper_left_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,
                                mirror=True)
    S_wg_lower_right_cl.connect("o1", S_wg_lower_left_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,
                                mirror=True)

    # 높이
    S_wg_upper_right0_cl.connect("o1", S_wg_upper_right_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_lower_right0_cl.connect("o1", S_wg_lower_right_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,
                                 mirror=True)

    right_upper_sbend_cl.connect("input", S_wg_upper_right0_cl["o2"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)
    right_lower_sbend_cl.connect("input", S_wg_lower_right0_cl["o2"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True, mirror=True)
    right_upper_flat_cl.connect("input", right_upper_sbend_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)
    right_lower_flat_cl.connect("input", right_lower_sbend_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)

    # 2번째 mmi port
    left_upper_Taper2_cl.connect("o1", right_upper_flat_cl.ports["output"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)
    left_lower_Taper2_cl.connect("o1", right_lower_flat_cl.ports["output"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)
    MMIcore2_cl.connect("coreinput2", left_upper_Taper2_cl.ports["o2"], allow_layer_mismatch=True,
                        allow_width_mismatch=True)
    MMIcore2_cl.connect("coreinput1", left_lower_Taper2_cl.ports["o2"], allow_layer_mismatch=True,
                        allow_width_mismatch=True)
    right_upper_Taper2_cl.connect("o1", MMIcore2_cl.ports["coreoutput1"], allow_layer_mismatch=True,
                                  allow_width_mismatch=True)
    right_lower_Taper2_cl.connect("o1", MMIcore2_cl.ports["coreoutput2"], allow_layer_mismatch=True,
                                  allow_width_mismatch=True)

    S_wg1_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2,
        width=width_start_taper + 10)
    S_wg1_cl.mirror()

    S_wg2_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2,
        width=width_start_taper + 10)
    S_wg2_cl.mirror()

    S_wg3_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2,
        width=width_start_taper + 10)

    S_wg4_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2,
        width=width_start_taper + 10)

    # 포트 설정
    c.add_port(name='o1', port=S_wg1_cl.ports[0])
    c.add_port(name='o2', port=S_wg1_cl.ports[1])
    c.add_port(name='o1', port=S_wg2_cl.ports[0])
    c.add_port(name='o2', port=S_wg2_cl.ports[1])
    c.add_port(name='o1', port=S_wg3_cl.ports[0])
    c.add_port(name='o2', port=S_wg3_cl.ports[1])
    c.add_port(name='o1', port=S_wg4_cl.ports[0])
    c.add_port(name='o2', port=S_wg4_cl.ports[1])

    S_wg1_cl.connect('o1', left_upper_Taper_cl.ports['o1'], allow_layer_mismatch=True, mirror=True,
                     allow_width_mismatch=True)

    S_wg2_cl.connect('o1', left_lower_Taper_cl.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg3_cl.connect('o1', right_upper_Taper2_cl.ports['o2'], allow_layer_mismatch=True, mirror=True,
                     allow_width_mismatch=True)

    S_wg4_cl.connect('o1', right_lower_Taper2_cl.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    if shape_num == 1:
        GC1.move([10, 0])
        GC2.move([10, 0])
        GC3.move([-10, 0])
        GC4.move([-10, 0])

    return c

def make_oband_asymmetric_switch(sbend_radius,phase_shift_length,length_mmi, width_mmi, center_mmi, length_taper, width_start_taper,
                   width_end_taper, S_wg_length, flat_length, center_flat,
                       layer,layer2,struc_num, shape_num):

    c = gf.Component()

    # Create MMI core with specified parameters
    MMIcore = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi, center=center_mmi, layer=layer)

    # Create Taper with specified parameters
    left_upper_Taper = c << make_elements.make_taper(left_width=width_start_taper, right_width=width_end_taper, length=length_taper, layer=layer)
    left_lower_Taper = c << make_elements.make_taper(left_width=width_start_taper, right_width=width_end_taper, length=length_taper, layer=layer)
    right_upper_Taper = c << make_elements.make_taper(left_width=width_end_taper, right_width=width_start_taper, length=length_taper, layer=layer)
    right_lower_Taper = c << make_elements.make_taper(left_width=width_end_taper, right_width=width_start_taper, length=length_taper, layer=layer)

    # taper, sbend 사이 left flat
    left_upper_flat = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper, layer=layer, center=center_flat)
    left_lower_flat = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper, layer=layer, center=center_flat)


    left_upper_sbend = c << make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper, layer=layer)
    left_lower_sbend = c.add_ref(make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper, layer=layer))
    left_lower_sbend.mirror()
    right_upper_sbend = c.add_ref(make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper, layer=layer))
    right_upper_sbend.mirror_x()
    ##x,y둘다 대칭은 port에서 mirror=true
    right_lower_sbend = c.add_ref(make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper, layer=layer))

    #높이
    S_wg_upper_left0 = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=0)], layer=layer, width=width_start_taper)

    S_wg_upper_right0 = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=30)], layer=layer, width=width_start_taper)

    S_wg_lower_left0 = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=0)], layer=layer, width=width_start_taper)

    S_wg_lower_right0 = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=30)], layer=layer, width=width_start_taper)
    S_wg_lower_right0.mirror()

    c.add_port(name='o1', port=S_wg_upper_left0.ports[0])
    c.add_port(name='o2', port=S_wg_upper_left0.ports[1])
    c.add_port(name='o1', port=S_wg_upper_right0.ports[0])
    c.add_port(name='o2', port=S_wg_upper_right0.ports[1])
    c.add_port(name='o1', port=S_wg_lower_left0.ports[0])
    c.add_port(name='o2', port=S_wg_lower_left0.ports[1])
    c.add_port(name='o1', port=S_wg_lower_right0.ports[0])
    c.add_port(name='o2', port=S_wg_lower_right0.ports[1])

    #중앙 반원 mzi
    ##안쪽 위
    S_wg_upper_left = c << make_elements.make_path(
        [gf.path.straight(30), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(phase_shift_length),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=0)], layer=layer, width=width_start_taper)

    S_wg_upper_right = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(phase_shift_length),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=530)], layer=layer, width=width_start_taper)

    ##안쪽 아래
    S_wg_lower_left = c << make_elements.make_path(
        [gf.path.straight(30), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=0)], layer=layer, width=width_start_taper)
    S_wg_lower_left.mirror()

    S_wg_lower_right = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=530)], layer=layer, width=width_start_taper)



    c.add_port(name='o1', port=S_wg_upper_left.ports[0])
    c.add_port(name='o2', port=S_wg_upper_left.ports[1])
    c.add_port(name='o1', port=S_wg_upper_right.ports[0])
    c.add_port(name='o2', port=S_wg_upper_right.ports[1])
    c.add_port(name='o1', port=S_wg_lower_left.ports[0])
    c.add_port(name='o2', port=S_wg_lower_left.ports[1])
    c.add_port(name='o1', port=S_wg_lower_right.ports[0])
    c.add_port(name='o2', port=S_wg_lower_right.ports[1])

    # taper, sbend 사이 right flat
    right_upper_flat = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper, layer=layer, center=center_flat)
    right_lower_flat = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper, layer=layer, center=center_flat)

    #2번째 mmi
    # Create MMI core with specified parameters
    MMIcore2 = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi, center=center_mmi, layer=layer)

    # Create Taper with specified parameters
    left_upper_Taper2 = c << make_elements.make_taper(left_width=width_start_taper,
                                                      right_width=width_end_taper, length=length_taper, layer=layer)
    left_lower_Taper2 = c << make_elements.make_taper(left_width=width_start_taper,
                                                      right_width=width_end_taper, length=length_taper, layer=layer)
    right_upper_Taper2 = c << make_elements.make_taper(left_width=width_end_taper,
                                                       right_width=width_start_taper, length=length_taper, layer=layer)
    right_lower_Taper2 = c << make_elements.make_taper(left_width=width_end_taper,
                                                       right_width=width_start_taper, length=length_taper, layer=layer)

    ##포트 붙이기
    # Connect Taper's output to MMI core's input
    left_upper_Taper.connect("o2", MMIcore.ports["coreinput1"], allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_Taper.connect("o2", MMIcore.ports["coreinput2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_upper_Taper.connect("o1", MMIcore.ports["coreoutput1"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_Taper.connect("o1", MMIcore.ports["coreoutput2"], allow_layer_mismatch=True,allow_width_mismatch=True)

    #MZI
    left_upper_flat.connect("input",right_upper_Taper["o2"],allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_flat.connect("input", right_lower_Taper["o2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    left_upper_sbend.connect("input",left_upper_flat["output"],allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_sbend.connect("input",left_lower_flat["output"],allow_layer_mismatch=True,allow_width_mismatch=True)

    #높이
    S_wg_upper_left0.connect("o1", left_upper_sbend["output"], allow_layer_mismatch=True, allow_width_mismatch=True,
                            mirror=True)
    S_wg_lower_left0.connect("o1", left_lower_sbend["output"], allow_layer_mismatch=True, allow_width_mismatch=True, mirror=True )

    S_wg_upper_left.connect("o1",S_wg_upper_left0["o2"],allow_layer_mismatch=True,allow_width_mismatch=True)
    S_wg_lower_left.connect("o1",S_wg_lower_left0["o2"],allow_layer_mismatch=True,allow_width_mismatch=True,mirror=True)
    S_wg_upper_right.connect("o1",S_wg_upper_left["o2"],allow_layer_mismatch=True,allow_width_mismatch=True,mirror=True)
    S_wg_lower_right.connect("o1",S_wg_lower_left["o2"],allow_layer_mismatch=True,allow_width_mismatch=True,mirror=True)

    # 높이
    S_wg_upper_right0.connect("o1", S_wg_upper_right["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_lower_right0.connect("o1", S_wg_lower_right["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,mirror=True)


    right_upper_sbend.connect("input",S_wg_upper_right0["o2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_sbend.connect("input",S_wg_lower_right0["o2"], allow_layer_mismatch=True,allow_width_mismatch=True, mirror=True)
    right_upper_flat.connect("input",right_upper_sbend["output"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_flat.connect("input", right_lower_sbend["output"], allow_layer_mismatch=True,allow_width_mismatch=True)

    # 2번째 mmi port
    left_upper_Taper2.connect("o1", right_upper_flat.ports["output"], allow_layer_mismatch=True,allow_width_mismatch=True)
    left_lower_Taper2.connect("o1", right_lower_flat.ports["output"], allow_layer_mismatch=True,allow_width_mismatch=True)
    MMIcore2.connect("coreinput2", left_upper_Taper2.ports["o2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    MMIcore2.connect("coreinput1", left_lower_Taper2.ports["o2"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_upper_Taper2.connect("o1", MMIcore2.ports["coreoutput1"], allow_layer_mismatch=True,allow_width_mismatch=True)
    right_lower_Taper2.connect("o1", MMIcore2.ports["coreoutput2"], allow_layer_mismatch=True,allow_width_mismatch=True)


    S_wg1 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)
    S_wg1.mirror()

    S_wg2 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)
    S_wg2.mirror()

    S_wg3 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)

    S_wg4 = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer, width=width_start_taper)

    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, period=1.0, fill_factor=0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC3 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
            GC4 = c << make_elements.grating_coupler_elliptical_trenches(width_start_taper, 1.8397, 0.4269)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, 1.05, 0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, 1.05, 0.6)
            GC3 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, 1.05, 0.6)
            GC4 = c << make_elements.grating_coupler_elliptical_arc(width_start_taper, 1.05, 0.6)

    # 포트 설정
    c.add_port(name='o1', port=S_wg1.ports[0])
    c.add_port(name='o2', port=S_wg1.ports[1])
    c.add_port(name='o1', port=S_wg2.ports[0])
    c.add_port(name='o2', port=S_wg2.ports[1])
    c.add_port(name='o1', port=S_wg3.ports[0])
    c.add_port(name='o2', port=S_wg3.ports[1])
    c.add_port(name='o1', port=S_wg4.ports[0])
    c.add_port(name='o2', port=S_wg4.ports[1])

    S_wg1.connect('o1', left_upper_Taper.ports['o1'], allow_layer_mismatch=True, mirror=True,allow_width_mismatch=True)
    GC1.connect('o1', S_wg1.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg2.connect('o1', left_lower_Taper.ports['o1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    GC2.connect('o1', S_wg2.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg3.connect('o1', right_upper_Taper2.ports['o2'], allow_layer_mismatch=True, mirror=True,allow_width_mismatch=True)
    GC3.connect('o1', S_wg3.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    S_wg4.connect('o1', right_lower_Taper2.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    GC4.connect('o1', S_wg4.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    ##cldding

    MMIcore_cl = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi + 10, center=center_mmi,
                                                 layer=layer2)

    # Create Taper with specified parameters
    left_upper_Taper_cl = c << make_elements.make_taper(left_width=width_start_taper + 10,
                                                        right_width=width_end_taper + 10, length=length_taper,
                                                        layer=layer2)
    left_lower_Taper_cl = c << make_elements.make_taper(left_width=width_start_taper + 10,
                                                        right_width=width_end_taper + 10, length=length_taper,
                                                        layer=layer2)
    right_upper_Taper_cl = c << make_elements.make_taper(left_width=width_end_taper + 10,
                                                         right_width=width_start_taper + 10, length=length_taper,
                                                         layer=layer2)
    right_lower_Taper_cl = c << make_elements.make_taper(left_width=width_end_taper + 10,
                                                         right_width=width_start_taper + 10, length=length_taper,
                                                         layer=layer2)

    # taper, sbend 사이 left flat
    left_upper_flat_cl = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper + 10, layer=layer2,
                                                         center=center_flat)
    left_lower_flat_cl = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper + 10, layer=layer2,
                                                         center=center_flat)

    left_upper_sbend_cl = c << make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper + 10, layer=layer2)
    left_lower_sbend_cl = c.add_ref(
        make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper + 10, layer=layer2))
    left_lower_sbend_cl.mirror()
    right_upper_sbend_cl = c.add_ref(
        make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper + 10, layer=layer2))
    right_upper_sbend_cl.mirror_x()
    ##x,y둘다 대칭은 port에서 mirror=true
    right_lower_sbend_cl = c.add_ref(
        make_elements.make_MZI_Sbend_waveguide(width_um=width_start_taper + 10, layer=layer2))

    # 높이
    S_wg_upper_left0_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=0)], layer=layer2, width=width_start_taper + 10)

    S_wg_upper_right0_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=30)], layer=layer2, width=width_start_taper + 10)

    S_wg_lower_left0_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=0)], layer=layer2, width=width_start_taper + 10)

    S_wg_lower_right0_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=10, angle=-90), gf.path.straight(70),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length=30)], layer=layer2, width=width_start_taper + 10)
    S_wg_lower_right0_cl.mirror()

    c.add_port(name='o1', port=S_wg_upper_left0_cl.ports[0])
    c.add_port(name='o2', port=S_wg_upper_left0_cl.ports[1])
    c.add_port(name='o1', port=S_wg_upper_right0_cl.ports[0])
    c.add_port(name='o2', port=S_wg_upper_right0_cl.ports[1])
    c.add_port(name='o1', port=S_wg_lower_left0_cl.ports[0])
    c.add_port(name='o2', port=S_wg_lower_left0_cl.ports[1])
    c.add_port(name='o1', port=S_wg_lower_right0_cl.ports[0])
    c.add_port(name='o2', port=S_wg_lower_right0_cl.ports[1])

    # 중앙 반원 mzi
    ##안쪽 위
    S_wg_upper_left_cl = c << make_elements.make_path(
        [gf.path.straight(30), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(phase_shift_length),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=0)], layer=layer2, width=width_start_taper + 10)

    S_wg_upper_right_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(phase_shift_length),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=530)], layer=layer2, width=width_start_taper + 10)

    ##안쪽 아래
    S_wg_lower_left_cl = c << make_elements.make_path(
        [gf.path.straight(30), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=0)], layer=layer2, width=width_start_taper + 10)
    S_wg_lower_left_cl.mirror()

    S_wg_lower_right_cl = c << make_elements.make_path(
        [gf.path.straight(0), gf.path.arc(radius=sbend_radius, angle=-90), gf.path.straight(1),
         gf.path.arc(radius=sbend_radius, angle=90), gf.path.straight(length=530)], layer=layer2, width=width_start_taper + 10)

    c.add_port(name='o1', port=S_wg_upper_left_cl.ports[0])
    c.add_port(name='o2', port=S_wg_upper_left_cl.ports[1])
    c.add_port(name='o1', port=S_wg_upper_right_cl.ports[0])
    c.add_port(name='o2', port=S_wg_upper_right_cl.ports[1])
    c.add_port(name='o1', port=S_wg_lower_left_cl.ports[0])
    c.add_port(name='o2', port=S_wg_lower_left_cl.ports[1])
    c.add_port(name='o1', port=S_wg_lower_right_cl.ports[0])
    c.add_port(name='o2', port=S_wg_lower_right_cl.ports[1])

    # taper, sbend 사이 right flat
    right_upper_flat_cl = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper + 10,
                                                          layer=layer2, center=center_flat)
    right_lower_flat_cl = c << make_elements.make_mziflat(length=flat_length, width=width_start_taper + 10,
                                                          layer=layer2, center=center_flat)

    # 2번째 mmi
    # Create MMI core with specified parameters
    MMIcore2_cl = c << make_elements.make_mmicore(length=length_mmi, width=width_mmi + 10, center=center_mmi,
                                                  layer=layer2)

    # Create Taper with specified parameters
    left_upper_Taper2_cl = c << make_elements.make_taper(left_width=width_start_taper + 10,
                                                         right_width=width_end_taper + 10, length=length_taper,
                                                         layer=layer2)
    left_lower_Taper2_cl = c << make_elements.make_taper(left_width=width_start_taper + 10,
                                                         right_width=width_end_taper + 10, length=length_taper,
                                                         layer=layer2)
    right_upper_Taper2_cl = c << make_elements.make_taper(left_width=width_end_taper + 10,
                                                          right_width=width_start_taper + 10, length=length_taper,
                                                          layer=layer2)
    right_lower_Taper2_cl = c << make_elements.make_taper(left_width=width_end_taper + 10,
                                                          right_width=width_start_taper + 10, length=length_taper,
                                                          layer=layer2)

    ##포트 붙이기
    # Connect Taper's output to MMI core's input
    left_upper_Taper_cl.connect("o2", MMIcore_cl.ports["coreinput1"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)
    left_lower_Taper_cl.connect("o2", MMIcore_cl.ports["coreinput2"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)
    right_upper_Taper_cl.connect("o1", MMIcore_cl.ports["coreoutput1"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)
    right_lower_Taper_cl.connect("o1", MMIcore_cl.ports["coreoutput2"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)

    # MZI
    left_upper_flat_cl.connect("input", right_upper_Taper_cl["o2"], allow_layer_mismatch=True,
                               allow_width_mismatch=True)
    left_lower_flat_cl.connect("input", right_lower_Taper_cl["o2"], allow_layer_mismatch=True,
                               allow_width_mismatch=True)
    left_upper_sbend_cl.connect("input", left_upper_flat_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)
    left_lower_sbend_cl.connect("input", left_lower_flat_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)

    # 높이
    S_wg_upper_left0_cl.connect("o1", left_upper_sbend_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True,
                                mirror=True)
    S_wg_lower_left0_cl.connect("o1", left_lower_sbend_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True, mirror=True)

    S_wg_upper_left_cl.connect("o1", S_wg_upper_left0_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_lower_left_cl.connect("o1", S_wg_lower_left0_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,
                               mirror=True)
    S_wg_upper_right_cl.connect("o1", S_wg_upper_left_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,
                                mirror=True)
    S_wg_lower_right_cl.connect("o1", S_wg_lower_left_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,
                                mirror=True)

    # 높이
    S_wg_upper_right0_cl.connect("o1", S_wg_upper_right_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_lower_right0_cl.connect("o1", S_wg_lower_right_cl["o2"], allow_layer_mismatch=True, allow_width_mismatch=True,
                                 mirror=True)

    right_upper_sbend_cl.connect("input", S_wg_upper_right0_cl["o2"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)
    right_lower_sbend_cl.connect("input", S_wg_lower_right0_cl["o2"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True, mirror=True)
    right_upper_flat_cl.connect("input", right_upper_sbend_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)
    right_lower_flat_cl.connect("input", right_lower_sbend_cl["output"], allow_layer_mismatch=True,
                                allow_width_mismatch=True)

    # 2번째 mmi port
    left_upper_Taper2_cl.connect("o1", right_upper_flat_cl.ports["output"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)
    left_lower_Taper2_cl.connect("o1", right_lower_flat_cl.ports["output"], allow_layer_mismatch=True,
                                 allow_width_mismatch=True)
    MMIcore2_cl.connect("coreinput2", left_upper_Taper2_cl.ports["o2"], allow_layer_mismatch=True,
                        allow_width_mismatch=True)
    MMIcore2_cl.connect("coreinput1", left_lower_Taper2_cl.ports["o2"], allow_layer_mismatch=True,
                        allow_width_mismatch=True)
    right_upper_Taper2_cl.connect("o1", MMIcore2_cl.ports["coreoutput1"], allow_layer_mismatch=True,
                                  allow_width_mismatch=True)
    right_lower_Taper2_cl.connect("o1", MMIcore2_cl.ports["coreoutput2"], allow_layer_mismatch=True,
                                  allow_width_mismatch=True)

    S_wg1_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2,
        width=width_start_taper + 10)
    S_wg1_cl.mirror()

    S_wg2_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2,
        width=width_start_taper + 10)
    S_wg2_cl.mirror()

    S_wg3_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2,
        width=width_start_taper + 10)

    S_wg4_cl = c << make_elements.make_path(
        [gf.path.straight(6), gf.path.arc(radius=20, angle=-90), gf.path.straight(40),
         gf.path.arc(radius=20, angle=90), gf.path.straight(length=S_wg_length)], layer=layer2,
        width=width_start_taper + 10)

    # 포트 설정
    c.add_port(name='o1', port=S_wg1_cl.ports[0])
    c.add_port(name='o2', port=S_wg1_cl.ports[1])
    c.add_port(name='o1', port=S_wg2_cl.ports[0])
    c.add_port(name='o2', port=S_wg2_cl.ports[1])
    c.add_port(name='o1', port=S_wg3_cl.ports[0])
    c.add_port(name='o2', port=S_wg3_cl.ports[1])
    c.add_port(name='o1', port=S_wg4_cl.ports[0])
    c.add_port(name='o2', port=S_wg4_cl.ports[1])

    S_wg1_cl.connect('o1', left_upper_Taper_cl.ports['o1'], allow_layer_mismatch=True, mirror=True,
                     allow_width_mismatch=True)

    S_wg2_cl.connect('o1', left_lower_Taper_cl.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg3_cl.connect('o1', right_upper_Taper2_cl.ports['o2'], allow_layer_mismatch=True, mirror=True,
                     allow_width_mismatch=True)

    S_wg4_cl.connect('o1', right_lower_Taper2_cl.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    if shape_num == 1:
        GC1.move([10, 0])
        GC2.move([10, 0])
        GC3.move([-10, 0])
        GC4.move([-10, 0])

    return c

# 희윤 파트
def S_GC_trench(length1, length2, radius, layer, width, wavelength, grating_line_width):
    c = gf.Component()

    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=(layer[0], layer[1] + 1),
        width=10 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, wavelength, grating_line_width)
    GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, wavelength, grating_line_width)

    GC1.mirror_x()
    S_wg.mirror_x()
    S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    return c

def S_GC_arc(length1, length2, radius, layer, width, period, fill_factor):
    c = gf.Component()

    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=(layer[0], layer[1] + 1),
        width=10 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    GC1.mirror_x()
    S_wg.mirror_x()
    S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10,0])
    GC2.move([-10,0])
    return c

#경진 파트
def Sbend_waveguide_GC(length1, length2, radius, layer, width, struc_num, shape_num):
    c = gf.Component()

    # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=(layer[0],layer[1]+1), width=10 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.0, fill_factor=0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.0, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.0, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.0, fill_factor=0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
        else:
            # 24.07.14 Test, period 1.05 -> 1
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)

    GC1.mirror_x()
    S_wg.mirror_x()
    S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    if shape_num == 1:
        GC1.move([10, 0])
        GC2.move([-10, 0])
    return c


def make_snake_propagation(length1, length2, line_num, layer, width, struc_num, shape_num):
    c = gf.Component()

    angle_sequence = [90, -90, 90, -90]

    if line_num == 2:
        paths_list = [gf.path.straight(137.5),
                      gf.path.arc(radius=20, angle=90),
                      gf.path.straight(length1 + 80),
                      gf.path.arc(radius=20, angle=-90),
                      gf.path.straight(length2),
                      gf.path.arc(radius=20, angle=-90),
                      gf.path.straight(length1 + 80),
                      gf.path.arc(radius=20, angle=90),
                      gf.path.straight(187.5)]
    elif line_num == 4:
        paths_list = [gf.path.straight(100),
                      gf.path.arc(radius=20, angle=90),
                      gf.path.straight(length1 + 80),
                      gf.path.arc(radius=20, angle=-90),
                      gf.path.straight(length2),
                      gf.path.arc(radius=20, angle=-90)]
        for i in range(line_num - 2):
            angle = angle_sequence[i % 4]
            paths_list.append(gf.path.straight(length1))
            paths_list.append(gf.path.arc(radius=20, angle=angle))
            paths_list.append(gf.path.straight(length2))
            paths_list.append(gf.path.arc(radius=20, angle=angle))
        paths_list.append(gf.path.straight(length1 + 80))
        paths_list.append(gf.path.arc(radius=20, angle=90))
        paths_list.append(gf.path.straight(95))
    else:
        paths_list = [gf.path.straight(100),
                      gf.path.arc(radius=20, angle=90),
                      gf.path.straight(length1 + 80),
                      gf.path.arc(radius=20, angle=-90),
                      gf.path.straight(length2),
                      gf.path.arc(radius=20, angle=-90)]
        for i in range(line_num - 2):
            angle = angle_sequence[i % 4]
            paths_list.append(gf.path.straight(length1))
            paths_list.append(gf.path.arc(radius=20, angle=angle))
            paths_list.append(gf.path.straight(length2))
            paths_list.append(gf.path.arc(radius=20, angle=angle))
        paths_list.append(gf.path.straight(length1 + 40))
        paths_list.append(gf.path.arc(radius=20, angle=-90))
        paths_list.append(gf.path.straight(65 * line_num - 295))
        paths_list.append(gf.path.arc(radius=20, angle=90))
        paths_list.append(gf.path.arc(radius=20, angle=90))
        paths_list.append(gf.path.straight(100))

    snake_wg = c << make_elements.make_path(paths_list, layer=layer, width=width)
    snake_wg_clad = c << make_elements.make_path(paths_list, layer=(layer[0], layer[1] + 1), width=width + 10)

    # 포트 설정
    c.add_port(name='o1', port=snake_wg.ports[0])
    c.add_port(name='o2', port=snake_wg.ports[1])

    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 1.0, 0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 1.0, 0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 1.0, 0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 1.0, 0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 1.05, 0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 1.05, 0.6)

    GC1.mirror_x()
    GC1.mirror_y()
    snake_wg.mirror_x()
    snake_wg_clad.mirror_x()
    snake_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    snake_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', snake_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    if shape_num == 1:
        GC1.move([10, 0])
        GC2.move([-10, 0])
    return c

# 석영 파트
def make_snake_bend(length1, length2, bend_num,layer, width, struc_num, shape_num):
    c = gf.Component()

    paths_list = [gf.path.straight(length1),
                  gf.path.arc(radius=40, angle=-90),
                  gf.path.straight(length2)]
    angle_sequence = [-90, 90, 90, -90]

    for i in range(bend_num):
        angle = angle_sequence[i % 4]
        paths_list.append(gf.path.arc(radius=20, angle=angle))
        paths_list.append(gf.path.straight(length2))

    paths_list.append(gf.path.arc(radius=40, angle=90))
    paths_list.append(gf.path.arc(radius=40, angle=90))
    paths_list.append(gf.path.straight(25*(bend_num/2) + 20 * bend_num + 25))
    paths_list.append(gf.path.arc(radius=40, angle=-90))
    paths_list.append(gf.path.straight(135))

    snake_wg = c << make_elements.make_path(paths_list, layer=layer, width=width)
    snake_wg_clad = c << make_elements.make_path(paths_list, layer= (layer[0], layer[1] + 1), width=width + 10)

    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, 1, 0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, 1, 0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.0, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.0, fill_factor=0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(width, 1.8397, 0.4269)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period=1.05, fill_factor=0.6)

    GC1.mirror_x()
    GC1.mirror_y()

    snake_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True)
    snake_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', snake_wg.ports['o2'], allow_layer_mismatch=True)

    if shape_num == 1:
        GC1.move([10, 0])
        GC2.move([-10, 0])

    return c

# 강석 CROW 구조
def taper(width1, width2, length, layer):
    c = gf.Component()

    # Create a taper component
    taper = gf.components.taper(
        width1=width1,  # Start width in microns
        width2=width2,  # End width in microns
        length=length,  # Length of the taper in microns
        layer=layer
    )
    c.add_ref(taper)
    c.add_port(name='o1', center=[0,0], width=width1, orientation=180, layer=layer)
    c.add_port(name='o2', center=[length, 0], width=width2, orientation=0, layer=layer)

    return c

def GratingResonator(average_width, gap, period, Np):
    c = gf.Component()

    a = average_width - gap
    b = average_width + gap
    t = Np*period+period/2

    #points 모음
    #초기 points 설정: upper = 위의 점, lower = 아래 점
    #PS~ : Phase shifter 부분 upper, lower 점들

    points_upper = np.array([
        [0, a/2],
        [period/2, a/2],
        [period/2, b/2],
        [period, b/2]
    ])
    points_lower = np.array([
        [period, -b/2],
        [period/2, -b/2],
        [period/2, -a/2],
        [0, -a/2]
    ])

    PS_points_upper = np.array([
        [Np*period, b/2],
        [Np*period + period/2, b/2]
    ])
    PS_points_lower = np.array([
        [Np*period + period/2, -b/2],
        [Np*period, -b/2]
    ])

    # Grating Resonator에서 격자의 윗부분 점들의 집합 생성
    for i in range(1,Np):
        points_upper_1 = np.array([
            [i*period, a/2],
            [i*period + period/2, a/2],
            [i*period + period/2, b/2],
            [i*period + period, b/2]
        ])
        points_upper = np.concatenate((points_upper, points_upper_1), axis=0)
    points_upper = np.concatenate((points_upper, PS_points_upper), axis=0)
    for i in range(Np):
        points_upper_2 = np.array([
            [t + i*period, a/2],
            [t + i*period + period/2, a/2],
            [t + i*period + period/2, b/2],
            [t + i*period + period, b/2]
        ])
        points_upper = np.concatenate((points_upper, points_upper_2), axis=0)

    # Grating Resonator에서 격자의 아랫부분 점들의 집합 생성
    for i in range(1,Np):
        points_lower_1 = np.array([
            [i*period + period, -b/2],
            [i*period + period/2, -b/2],
            [i*period + period/2, -a/2],
            [i*period, -a/2]
        ])
        points_lower = np.concatenate((points_lower_1, points_lower), axis=0)
    points_lower = np.concatenate((PS_points_lower, points_lower), axis=0)
    for i in range(Np):
        points_lower_2 = np.array([
            [t + i*period + period, -b/2],
            [t + i*period + period/2, -b/2],
            [t + i*period + period/2, -a/2],
            [t + i*period, -a/2]
        ])
        points_lower = np.concatenate((points_lower_2, points_lower), axis=0)


    points = np.concatenate((points_upper, points_lower), axis=0)
    c.add_polygon(points, layer=(34,0))
    c.add_port(name='opt_1', center=[0, 0], width=average_width, orientation=180, layer=(34, 0))
    c.add_port(name='opt_2', center=[t + Np*period, 0], width=average_width, orientation=0, layer=(34, 0))
    c.add_port(name='opt_3', center=[0,0], width=average_width, orientation=0, layer=(34,0))

    return c


def CROW_Oband_Passive_Test(average_width, gap, period, Np, Nr, wg_width, struc_num, shape_num):
    c = gf.Component()

    #변수 할당
    crow_length = 2*Np*period + period/2
    total_length = Nr * crow_length

    #Input part
    line_input = c << make_elements.make_path([gf.path.straight(length=10)], width=average_width, layer=(34, 0))
    #Output Part
    line_output = c << make_elements.make_path([gf.path.straight(length=10)], width=average_width, layer=(34, 0))
    # Input part_clad
    line_input_clad = c << make_elements.make_path([gf.path.straight(length=10)], width=average_width + 10, layer=(34, 1))
    # Output Part_clad
    line_output_clad = c << make_elements.make_path([gf.path.straight(length=10)], width=average_width + 10, layer=(34, 1))
    #slab
    slab = c << make_elements.make_polygon(wg_width + 10, total_length, (34, 1))
    taper_slab_input = c << taper(wg_width+10, wg_width+10, 10, (34,1))
    taper_slab_output = c << taper(wg_width+10, wg_width+10, 10, (34,1))
    #taper
    taper_1 = c << taper(wg_width, average_width, 34, (34,0))
    taper_2 = c << taper(average_width, wg_width, 34, (34,0))
    #taper_clad
    taper_1_clad = c << taper(wg_width+10, average_width+10, 34, (34,1))
    taper_2_clad = c << taper(average_width+10, wg_width+10, 34, (34,1))
    #bend WG
    k = 400 - total_length - 20
    if k < 200:
        path_input = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=10, angle=-90), gf.path.straight(20), gf.path.arc(radius=10, angle=90), gf.path.straight(50)], width=wg_width, layer=(34, 0))
        path_output = c << make_elements.make_path([gf.path.straight(400 - total_length - 20)], width=wg_width, layer=(34, 0))
        path_input_clad = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=10, angle=-90), gf.path.straight(20), gf.path.arc(radius=10, angle=90), gf.path.straight(50)], width=wg_width + 10, layer=(34, 1))
        path_output_clad = c << make_elements.make_path([gf.path.straight(400 - total_length - 20)], width=wg_width + 10, layer=(34, 1))
    else:
        path_input = c << make_elements.make_path([gf.path.straight(50 + (k - 200)), gf.path.arc(radius=10, angle=-90), gf.path.straight(20), gf.path.arc(radius=10, angle=90), gf.path.straight(50)], width=wg_width, layer=(34, 0))
        path_output = c << make_elements.make_path([gf.path.straight(100)], width=wg_width, layer=(34, 0))
        path_input_clad = c << make_elements.make_path([gf.path.straight(50 + (k - 200)), gf.path.arc(radius=10, angle=-90), gf.path.straight(20), gf.path.arc(radius=10, angle=90), gf.path.straight(50)], width=wg_width + 10, layer=(34, 1))
        path_output_clad = c << make_elements.make_path([gf.path.straight(100)], width=wg_width + 10, layer=(34, 1))


    # #Grating Coupler
    if struc_num == 0:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(average_width, 1.76, 0.508)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(average_width, 1.76, 0.508)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(average_width, period=1.0, fill_factor=0.5)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(average_width, period=1.0, fill_factor=0.5)
    elif struc_num == 1:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(average_width, 1.76, 0.41)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(average_width, 1.76, 0.41)
        else:
            GC1 = c << make_elements.grating_coupler_elliptical_arc(average_width, period=1.0, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(average_width, period=1.0, fill_factor=0.6)
    else:
        if shape_num == 0:
            GC1 = c << make_elements.grating_coupler_elliptical_trenches(average_width, 1.8397, 0.4269)
            GC2 = c << make_elements.grating_coupler_elliptical_trenches(average_width, 1.8397, 0.4269)
        else:
            # 24.07.14 Test, period 1.05 -> 1
            GC1 = c << make_elements.grating_coupler_elliptical_arc(average_width, period=1.05, fill_factor=0.6)
            GC2 = c << make_elements.grating_coupler_elliptical_arc(average_width, period=1.05, fill_factor=0.6)

    # CROW 붙이기
    for i in range(1, Nr+1):
        globals()['Resonator_{}'.format(i)] = c << GratingResonator(average_width, gap, period, Np)
        if k-100 >= 0:
            globals()['Resonator_{}'.format(i)].movex(k-100)
    for i in range(2, Nr+1):
        globals()['Resonator_{}'.format(i)].connect('opt_1', globals()['Resonator_{}'.format(i-1)].ports['opt_2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    #input, output과 CROW 연결
    line_input.connect('o2', globals()['Resonator_{}'.format(1)].ports['opt_1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    taper_1.connect('o2', line_input.ports['o1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    path_input.connect('o1', taper_1.ports['o1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    GC1.connect('o1', path_input.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    line_output.connect('o1', globals()['Resonator_{}'.format(Nr)].ports['opt_2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    taper_2.connect('o1', line_output.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    path_output.connect('o1', taper_2.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    GC2.connect('o1', path_output.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    line_input_clad.connect('o2', globals()['Resonator_{}'.format(1)].ports['opt_1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    taper_1_clad.connect('o2', line_input_clad.ports['o1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    path_input_clad.connect('o1', taper_1_clad.ports['o1'], allow_layer_mismatch=True,allow_width_mismatch=True)
    line_output_clad.connect('o1', globals()['Resonator_{}'.format(Nr)].ports['opt_2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    taper_2_clad.connect('o1', line_output_clad.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)
    path_output_clad.connect('o1', taper_2_clad.ports['o2'], allow_layer_mismatch=True,allow_width_mismatch=True)

    #slab 연결
    taper_slab_input.connect('o1', taper_1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    slab.connect('o1', taper_slab_input.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_slab_output.connect('o2', slab.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    if shape_num == 1:
        GC1.move([10, 0])
        GC2.move([-10, 0])

    return c

## Modified by Taewon
## The R value need to be fixed. (set to inside edge of core now)

def ring_resonator(layer_core, layer_cladding, ring_rad, gap, struc_num, shape_num):
    c = gf.Component()
    # parameters

    clad_width = 5
    core_width = 0.7
    wavelength = 1.5
    grating_pitch = 0.6

    layer = (34, 0)

    width1 = 0.6
    width2 = 0.7
    width3 = 0.8
    width4 = 0.9

    bend_radius1 = 5
    bend_radius2 = 10
    bend_radius3 = 15
    bend_radius4 = 20
    bend_radius5 = 30

    bend_length1 = 25

    # 희윤 파라미터
    wavelength1 = 1.664
    grating_line_width1_1 = 0.3866
    grating_line_width1_2 = 0.4813
    grating_line_width1_3 = 0.5754

    wavelength2 = 1.76
    grating_line_width2_1 = 0.41
    grating_line_width2_2 = 0.508
    grating_line_width2_3 = 0.608

    wavelength3 = 1.8397
    grating_line_width3_1 = 0.4269
    grating_line_width3_2 = 0.5324
    grating_line_width3_3 = 0.636

    # a straight waveguide
    
    waveguide_core = Sbend_waveguide_GC(400, bend_length1, bend_radius2, layer=layer_core, width=core_width,struc_num=struc_num,shape_num=shape_num)

    c << waveguide_core

    # a core part of ring resonator
    R1 = c << gf.components.ring(radius=ring_rad, width=core_width, angle_resolution=2.5, layer=layer_core)
    R1.move([(100 + 400 + 10.7) / 2, ring_rad + bend_length1 + 20.7 + gap-90])

    # a clad part of ring resonator
    if (ring_rad <= 5.35):
        R2 = c << gf.components.circle(radius=5.35 + ring_rad, angle_resolution=2.5, layer=layer_cladding)
    else:
        R2 = c << gf.components.ring(radius=ring_rad, width=core_width + 2 * clad_width, angle_resolution=2.5,
                                     layer=layer_cladding)

    R2.move([(100 + 400 + 10.7) / 2, ring_rad + bend_length1 + 20.7 + gap-90])

    return c


def micro_disk(core_layer, clad_layer, core_width, gap,struc_num, shape_num):
    c = gf.Component()
    clad_width = 5
    core_area = 0.7
    wavelength = 1.5
    grating_pitch = 0.6
    layer = (34, 0)

    width1 = 0.6
    width2 = 0.7
    width3 = 0.8
    width4 = 0.9

    bend_radius1 = 5
    bend_radius2 = 10
    bend_radius3 = 15
    bend_radius4 = 20
    bend_radius5 = 30

    bend_length1 = 25

    # 희윤 파라미터
    wavelength1 = 1.664
    grating_line_width1_1 = 0.3866
    grating_line_width1_2 = 0.4813
    grating_line_width1_3 = 0.5754

    wavelength2 = 1.76
    grating_line_width2_1 = 0.41
    grating_line_width2_2 = 0.508
    grating_line_width2_3 = 0.608

    wavelength3 = 1.8397
    grating_line_width3_1 = 0.4269
    grating_line_width3_2 = 0.5324
    grating_line_width3_3 = 0.636

    # a straight waveguide
    waveguide_core = Sbend_waveguide_GC(400, bend_length1, bend_radius2, layer=core_layer, width=0.7,struc_num=struc_num, shape_num=shape_num)

    c << waveguide_core

    # a core part of microdisk

    R1 = c << gf.components.circle(radius=core_width, angle_resolution=2.5, layer=core_layer)
    R1.move([(100 + 400 + 10.7) / 2, core_width + bend_length1 + 20.35 + gap-90])
    # a clad part of microdisk

    R2 = c << gf.components.circle(radius=clad_width + core_width, angle_resolution=2.5, layer=clad_layer)
    R2.move([(100 + 400 + 10.7) / 2, core_width + bend_length1 + 20.35 + gap-90])

    return c

