from . import make_elements
import gdsfactory as gf
from gdsfactory.path import straight



# 석현 파트
def Dicing_key(layer, width_dic, length_dic, type):
    c = gf.Component()

    if type == 1:
        top_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)
        mid_box = c << make_elements.make_box(layer, 50,1)
        r_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)
        # l_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)

        top_box.connect('o1', mid_box.ports['o2'], allow_layer_mismatch=True)
        r_box.connect('o1', mid_box.ports['o3'], allow_layer_mismatch=True)

        c.flatten()

        return c

    elif type == 2:
        top_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic+50)
        mid_box = c << make_elements.make_box(layer, 50,2)
        r_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)
        l_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)

        top_box.connect('o1', mid_box.ports['o2'], allow_layer_mismatch=True)
        r_box.connect('o1', mid_box.ports['o3'], allow_layer_mismatch=True)
        l_box.connect('o1',mid_box.ports['o1'], allow_layer_mismatch=True)

        c.flatten()

        return c

    else:
        top_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)
        bot_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)
        mid_box = c << make_elements.make_box(layer, 100, 3)
        r_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)
        l_box = c << make_elements.make_path([gf.path.straight(length_dic)], layer=layer, width=width_dic)

        top_box.connect('o1', mid_box.ports['o2'], allow_layer_mismatch=True)
        bot_box.connect('o1', mid_box.ports['o4'], allow_layer_mismatch=True)
        r_box.connect('o1', mid_box.ports['o3'], allow_layer_mismatch=True)
        l_box.connect('o1', mid_box.ports['o1'], allow_layer_mismatch=True)

        c.flatten()

        return c


def Ref_GC(layer_core,layer_clad, width, period, fill_factor, length1, length2, radius):
    c = gf.Component()

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
 # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(2*length1)], layer=layer_core, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(2*length1)], layer=(layer_clad[0], layer_clad[1]),
        width=16 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

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

def Taper_Coupler(layer_core,layer_clad, width, width_max, Taper_length, misalign, period, fill_factor, length1, length2, radius):
    c = gf.Component()

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
 # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer_core, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=(layer_clad[0], layer_clad[1]),
        width=16 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    taper_in = c << make_elements.make_taper_mis(width, width_max, Taper_length, layer_core, 0)
    taper_out = c << make_elements.make_taper_mis(width_max, width, Taper_length, layer_core, misalign)
    WG_out = c << make_elements.make_path([straight(400)], layer_core, width)

    taper_in_clad = c << make_elements.make_taper_mis(16 +width, 16 +width_max, Taper_length, layer_clad, 0)
    taper_out_clad = c << make_elements.make_taper_mis(16 +width_max, 16 +width, Taper_length, layer_clad, misalign)
    WG_out_clad = c << make_elements.make_path([straight(400)], layer_clad, 16 +width)

    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    GC1.mirror_x()
    # S_wg.mirror_x()
    # S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_in.connect('o1', S_wg['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_out.connect('o1', taper_in['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    WG_out.connect('o1', taper_out['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_in_clad.connect('o1', S_wg_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_out_clad.connect('o1', taper_in_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    WG_out_clad.connect('o1', taper_out_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.connect('o1', WG_out.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])
    GC2.move([-10, 0])

    c.flatten()

    return c

def Taper_strip_Coupler(layer_core,layer_clad, width, width_max, Taper_length, misalign, period, fill_factor, length1, length2, radius,strip_length):
    c = gf.Component()

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
 # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=layer_core, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(100), gf.path.arc(radius=radius, angle=-90), gf.path.straight(length2),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(length1)], layer=(layer_clad[0], layer_clad[1]),
        width=16 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    taper_in = c << make_elements.make_taper_mis(width, width_max, Taper_length, layer_core, 0)
    strip_in = c << make_elements.make_path([straight(strip_length)], layer_core, width_max)
    strip_out = c << make_elements.make_path_mis(width_max,strip_length,  layer_core, misalign)
    taper_out = c << make_elements.make_taper_mis(width_max, width, Taper_length, layer_core, misalign)
    WG_out = c << make_elements.make_path([straight(400)], layer_core, width)

    taper_in_clad = c << make_elements.make_taper_mis(16 +width, 16 +width_max, Taper_length, layer_clad, 0)
    strip_in_clad = c << make_elements.make_path([straight(strip_length)], layer_clad, 16+width_max)
    strip_out_clad = c << make_elements.make_path_mis(16 +width_max,strip_length, layer_clad, misalign)
    taper_out_clad = c << make_elements.make_taper_mis(16 +width_max, 16 +width, Taper_length, layer_clad, misalign)
    WG_out_clad = c << make_elements.make_path([straight(400)], layer_clad, 16 +width)

    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    GC1.mirror_x()
    # S_wg.mirror_x()
    # S_wg_clad.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_in.connect('o1', S_wg['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    strip_in.connect('o1', taper_in['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    strip_out.connect('o1', strip_in['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_out.connect('o1', strip_out['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    WG_out.connect('o1', taper_out['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_in_clad.connect('o1', S_wg_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    strip_in_clad.connect('o1', taper_in_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    strip_out_clad.connect('o1', strip_in_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_out_clad.connect('o1', strip_out_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    WG_out_clad.connect('o1', taper_out_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.connect('o1', WG_out.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])
    GC2.move([-10, 0])

    c.flatten()

    return c


def GC_single(layer_core, layer_clad, width, period, fill_factor):
    c = gf.Component()

    GC1 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)
    strip_wg = c << make_elements.make_path([straight(250)], layer_core, width)
    strip_wg_clad = c << make_elements.make_path([straight(250)], layer_clad, width+16)

    strip_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    strip_wg_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([-10, 0])

    c.flatten()

    return c
def Stitching_Ref_GC(layer_core,layer_clad, width, period, fill_factor, radius):
    c = gf.Component()


 # S-bend 경로 설정
    S_wg = c << make_elements.make_path(
        [gf.path.straight(250), gf.path.arc(radius=radius, angle=-90), gf.path.straight(200),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(250)], layer=layer_core, width=width)
    S_wg_clad = c << make_elements.make_path(
        [gf.path.straight(250), gf.path.arc(radius=radius, angle=-90), gf.path.straight(200),
         gf.path.arc(radius=radius, angle=90), gf.path.straight(250)], layer=(layer_clad[0], layer_clad[1]),
        width=16 + width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])

    GC2 = c << make_elements.grating_coupler_elliptical_arc(width, period, fill_factor)

    # S_wg.mirror_x()
    # S_wg_clad.mirror_x()
    S_wg.connect('o2', GC2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_clad.connect('o2', GC2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.connect('o1', S_wg.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([+10, 0])

    c.flatten()

    return c

def Stitching_wg(layer_core, layer_clad,width,radius):
    c = gf.Component()

    bend_wg = c << make_elements.make_path([gf.path.straight(250), gf.path.arc(radius=radius, angle=-90),
                                             gf.path.straight(200), gf.path.arc(radius=radius, angle=-90),
                                             gf.path.straight(250)], layer=layer_core, width=width)
    bend_wg_clad = c << make_elements.make_path([gf.path.straight(250), gf.path.arc(radius=radius, angle=-90),
                                             gf.path.straight(200), gf.path.arc(radius=radius, angle=-90),
                                             gf.path.straight(250)], layer=layer_clad, width=width+16)

    c.flatten()

    return c



def Edge_Coupler1(layer_core,layer_clad, width):
    c = gf.Component()

    WG_in = c << make_elements.make_path([straight(2000)], layer_core, 4)
    taper_in = c << make_elements.make_taper(4, width, 1000, layer_core)
    strip_wg = c << make_elements.make_path([straight(16000)], layer_core, width)
    taper_out = c << make_elements.make_taper(width, 4, 1000, layer_core)
    WG_out = c << make_elements.make_path([straight(2000)], layer_core, 4)

    WG_in_clad = c << make_elements.make_path([straight(2000)], layer_clad, 4 + 16)
    taper_in_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    strip_wg_clad = c << make_elements.make_path([straight(16000)], layer_clad, width + 16)
    taper_out_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    WG_out_clad = c << make_elements.make_path([straight(2000)], layer_clad, 4 + 16)

    taper_in.connect('o1', WG_in.ports['o2'], allow_layer_mismatch=True)
    strip_wg.connect('o1', taper_in.ports['o2'], allow_layer_mismatch=True)
    taper_out.connect('o1', strip_wg.ports['o2'], allow_layer_mismatch=True)
    WG_out.connect('o1', taper_out.ports['o2'], allow_layer_mismatch=True)

    taper_in_clad.connect('o1', WG_in_clad.ports['o2'], allow_layer_mismatch=True)
    strip_wg_clad.connect('o1', taper_in_clad.ports['o2'], allow_layer_mismatch=True)
    taper_out_clad.connect('o1', strip_wg_clad.ports['o2'], allow_layer_mismatch=True)
    WG_out_clad.connect('o1', taper_out_clad.ports['o2'], allow_layer_mismatch=True)

    c.flatten()

    return c


def Edge_Coupler2(layer_core,layer_clad, width):
    c = gf.Component()

    WG_in_l = c << make_elements.make_path([straight(2000)], layer_core, 4)
    taper_in_l = c << make_elements.make_taper(4, width, 1000, layer_core)
    strip_wg_l = c << make_elements.make_path([straight(6500)], layer_core, width)
    taper_out_l = c << make_elements.make_taper(width, 4, 1000, layer_core)
    WG_out_l = c << make_elements.make_path([straight(2000)], layer_core, 4)

    WG_in_r = c << make_elements.make_path([straight(2000)], layer_core, 4)
    taper_in_r = c << make_elements.make_taper(4, width, 1000, layer_core)
    strip_wg_r = c << make_elements.make_path([straight(6500)], layer_core, width)
    taper_out_r = c << make_elements.make_taper(width, 4, 1000, layer_core)
    WG_out_r = c << make_elements.make_path([straight(2000)], layer_core, 4)

    WG_in_l_clad = c << make_elements.make_path([straight(2000)], layer_clad, 4 + 16)
    taper_in_l_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    strip_wg_l_clad = c << make_elements.make_path([straight(6500)], layer_clad, width + 16)
    taper_out_l_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    WG_out_l_clad = c << make_elements.make_path([straight(2000)], layer_clad, 4 + 16)

    WG_in_r_clad = c << make_elements.make_path([straight(2000)], layer_clad, 4 + 16)
    taper_in_r_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    strip_wg_r_clad = c << make_elements.make_path([straight(6500)], layer_clad, width + 16)
    taper_out_r_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    WG_out_r_clad = c << make_elements.make_path([straight(2000)], layer_clad, 4 + 16)

    taper_in_l.connect('o1', WG_in_l.ports['o2'], allow_layer_mismatch=True)
    strip_wg_l.connect('o1', taper_in_l.ports['o2'], allow_layer_mismatch=True)
    taper_out_l.connect('o1', strip_wg_l.ports['o2'], allow_layer_mismatch=True)
    WG_out_l.connect('o1', taper_out_l.ports['o2'], allow_layer_mismatch=True)
    WG_in_r.connect('o1', WG_out_l.ports['o2'], allow_layer_mismatch=True)
    taper_in_r.connect('o1', WG_in_r.ports['o2'], allow_layer_mismatch=True)
    strip_wg_r.connect('o1', taper_in_r.ports['o2'], allow_layer_mismatch=True)
    taper_out_r.connect('o1', strip_wg_r.ports['o2'], allow_layer_mismatch=True)
    WG_out_r.connect('o1', taper_out_r.ports['o2'], allow_layer_mismatch=True)

    taper_in_l_clad.connect('o1', WG_in_l_clad.ports['o2'], allow_layer_mismatch=True)
    strip_wg_l_clad.connect('o1', taper_in_l_clad.ports['o2'], allow_layer_mismatch=True)
    taper_out_l_clad.connect('o1', strip_wg_l_clad.ports['o2'], allow_layer_mismatch=True)
    WG_out_l_clad.connect('o1', taper_out_l_clad.ports['o2'], allow_layer_mismatch=True)
    WG_in_r_clad.connect('o1', WG_out_l_clad.ports['o2'], allow_layer_mismatch=True)
    taper_in_r_clad.connect('o1', WG_in_r_clad.ports['o2'], allow_layer_mismatch=True)
    strip_wg_r_clad.connect('o1', taper_in_r_clad.ports['o2'], allow_layer_mismatch=True)
    taper_out_r_clad.connect('o1', strip_wg_r_clad.ports['o2'], allow_layer_mismatch=True)
    WG_out_r_clad.connect('o1', taper_out_r_clad.ports['o2'], allow_layer_mismatch=True)

    c.flatten()

    return c


def Edge_Coupler3(layer_core,layer_clad, width):
    c = gf.Component()

    WG_in_l = c << make_elements.make_path([straight(1000)], layer_core, 4)
    taper_in_l = c << make_elements.make_taper(4, width, 1000, layer_core)
    strip_wg_l = c << make_elements.make_path([straight(1000)], layer_core, width)
    taper_out_l = c << make_elements.make_taper(width, 4, 1000, layer_core)
    WG_out_l = c << make_elements.make_path([straight(1000)], layer_core, 4)

    WG_in_r = c << make_elements.make_path([straight(1000)], layer_core, 4)
    taper_in_r = c << make_elements.make_taper(4, width, 1000, layer_core)
    strip_wg_r = c << make_elements.make_path([straight(11000)], layer_core, width)
    taper_out_r = c << make_elements.make_taper(width, 4, 1000, layer_core)
    WG_out_r = c << make_elements.make_path([straight(1000)], layer_core, 4)

    WG_in_l_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
    taper_in_l_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    strip_wg_l_clad = c << make_elements.make_path([straight(1000)], layer_clad, width + 16)
    taper_out_l_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    WG_out_l_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)

    WG_in_r_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
    taper_in_r_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    strip_wg_r_clad = c << make_elements.make_path([straight(11000)], layer_clad, width + 16)
    taper_out_r_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    WG_out_r_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)

    taper_in_l.connect('o1', WG_in_l.ports['o2'], allow_layer_mismatch=True)
    strip_wg_l.connect('o1', taper_in_l.ports['o2'], allow_layer_mismatch=True)
    taper_out_l.connect('o1', strip_wg_l.ports['o2'], allow_layer_mismatch=True)
    WG_out_l.connect('o1', taper_out_l.ports['o2'], allow_layer_mismatch=True)
    WG_in_r.connect('o1', WG_out_l.ports['o2'], allow_layer_mismatch=True)
    taper_in_r.connect('o1', WG_in_r.ports['o2'], allow_layer_mismatch=True)
    strip_wg_r.connect('o1', taper_in_r.ports['o2'], allow_layer_mismatch=True)
    taper_out_r.connect('o1', strip_wg_r.ports['o2'], allow_layer_mismatch=True)
    WG_out_r.connect('o1', taper_out_r.ports['o2'], allow_layer_mismatch=True)

    taper_in_l_clad.connect('o1', WG_in_l_clad.ports['o2'], allow_layer_mismatch=True)
    strip_wg_l_clad.connect('o1', taper_in_l_clad.ports['o2'], allow_layer_mismatch=True)
    taper_out_l_clad.connect('o1', strip_wg_l_clad.ports['o2'], allow_layer_mismatch=True)
    WG_out_l_clad.connect('o1', taper_out_l_clad.ports['o2'], allow_layer_mismatch=True)
    WG_in_r_clad.connect('o1', WG_out_l_clad.ports['o2'], allow_layer_mismatch=True)
    taper_in_r_clad.connect('o1', WG_in_r_clad.ports['o2'], allow_layer_mismatch=True)
    strip_wg_r_clad.connect('o1', taper_in_r_clad.ports['o2'], allow_layer_mismatch=True)
    taper_out_r_clad.connect('o1', strip_wg_r_clad.ports['o2'], allow_layer_mismatch=True)
    WG_out_r_clad.connect('o1', taper_out_r_clad.ports['o2'], allow_layer_mismatch=True)

    c.flatten()

    return c

def Sbend_Edge_Coupler(layer_core,layer_clad, width,bend_radius,length):
    c = gf.Component()

    WG_in_l1 = c << make_elements.make_path([straight(1000)], layer_core, 4)
    taper_in_l1 = c << make_elements.make_taper(4, width, 1000, layer_core)
    S_wg_l1 = c << make_elements.make_path(
        [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(25),
         gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(length)], layer=layer_core, width=width)
    taper_out_l1 = c << make_elements.make_taper(width, 4, 1000, layer_core)
    WG_out_l1 = c << make_elements.make_path([straight(1000)], layer_core, 4)

    WG_in_l2 = c << make_elements.make_path([straight(1000)], layer_core, 4)
    taper_in_l2 = c << make_elements.make_taper(4, width, 1000, layer_core)
    S_wg_l2 = c << make_elements.make_path(
        [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(25),
         gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(length)], layer=layer_core, width=width)
    taper_out_l2 = c << make_elements.make_taper(width, 4, 1000, layer_core)
    WG_out_l2 = c << make_elements.make_path([straight(1000)], layer_core, 4)

    WG_in_l1_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
    taper_in_l1_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    S_wg_l1_clad = c << make_elements.make_path(
        [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(25),
         gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(length)], layer=layer_clad, width=width + 16)
    taper_out_l1_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    WG_out_l1_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)

    WG_in_l2_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
    taper_in_l2_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    S_wg_l2_clad = c << make_elements.make_path(
        [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(25),
         gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(length)], layer=layer_clad, width=width + 16)
    taper_out_l2_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    WG_out_l2_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
    #
    # WG_in_r1 = c << make_elements.make_path([straight(1000)], layer_core, 4)
    # taper_in_r1 = c << make_elements.make_taper(4, width, 1000, layer_core)
    # S_wg_r1 = c << make_elements.make_path(
    #     [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(25),
    #      gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(length)], layer=layer_core, width=width)
    # taper_out_r1 = c << make_elements.make_taper(width, 4, 1000, layer_core)
    # WG_out_r1 = c << make_elements.make_path([straight(1000)], layer_core, 4)
    #
    # WG_in_r2 = c << make_elements.make_path([straight(1000)], layer_core, 4)
    # taper_in_r2 = c << make_elements.make_taper(4, width, 1000, layer_core)
    # S_wg_r2 = c << make_elements.make_path(
    #     [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(25),
    #      gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(length)], layer=layer_core, width=width)
    # taper_out_r2 = c << make_elements.make_taper(width, 4, 1000, layer_core)
    # WG_out_r2 = c << make_elements.make_path([straight(1000)], layer_core, 4)
    #
    # WG_in_r1_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
    # taper_in_r1_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    # S_wg_r1_clad = c << make_elements.make_path(
    #     [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(25),
    #      gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(length)], layer=layer_clad, width=width + 16)
    # taper_out_r1_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    # WG_out_r1_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
    #
    # WG_in_r2_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
    # taper_in_r2_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
    # S_wg_r2_clad = c << make_elements.make_path(
    #     [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(25),
    #      gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(length)], layer=layer_clad, width=width + 16)
    # taper_out_r2_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
    # WG_out_r2_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)

    taper_in_l1.connect('o1', WG_in_l1.ports['o2'], allow_layer_mismatch=True)
    S_wg_l1.connect('o1', taper_in_l1.ports['o2'], allow_layer_mismatch=True)
    taper_out_l1.connect('o1', S_wg_l1.ports['o2'], allow_layer_mismatch=True)
    WG_out_l1.connect('o1', taper_out_l1.ports['o2'], allow_layer_mismatch=True)

    WG_in_l2.connect('o1', WG_out_l1.ports['o2'], allow_layer_mismatch=True)
    taper_in_l2.connect('o1', WG_in_l2.ports['o2'], allow_layer_mismatch=True)
    S_wg_l2.connect('o1', taper_in_l2.ports['o2'], allow_layer_mismatch=True)
    taper_out_l2.connect('o1', S_wg_l2.ports['o2'], allow_layer_mismatch=True)
    WG_out_l2.connect('o1', taper_out_l2.ports['o2'], allow_layer_mismatch=True)

    # WG_in_r1.connect('o1', WG_out_l2.ports['o2'], allow_layer_mismatch=True)
    # taper_in_r1.connect('o1', WG_in_r1.ports['o2'], allow_layer_mismatch=True)
    # S_wg_r1.connect('o1', taper_in_r1.ports['o2'], allow_layer_mismatch=True)
    # taper_out_r1.connect('o1', S_wg_r1.ports['o2'], allow_layer_mismatch=True)
    # WG_out_r1.connect('o1', taper_out_r1.ports['o2'], allow_layer_mismatch=True)
    #
    # WG_in_r2.connect('o1', WG_out_r1.ports['o2'], allow_layer_mismatch=True)
    # taper_in_r2.connect('o1', WG_in_r2.ports['o2'], allow_layer_mismatch=True)
    # S_wg_r2.connect('o1', taper_in_r2.ports['o2'], allow_layer_mismatch=True)
    # taper_out_r2.connect('o1', S_wg_r2.ports['o2'], allow_layer_mismatch=True)
    # WG_out_r2.connect('o1', taper_out_r2.ports['o2'], allow_layer_mismatch=True)


    taper_in_l1_clad.connect('o1', WG_in_l1_clad.ports['o2'], allow_layer_mismatch=True)
    S_wg_l1_clad.connect('o1', taper_in_l1_clad.ports['o2'], allow_layer_mismatch=True)
    taper_out_l1_clad.connect('o1', S_wg_l1_clad.ports['o2'], allow_layer_mismatch=True)
    WG_out_l1_clad.connect('o1', taper_out_l1_clad.ports['o2'], allow_layer_mismatch=True)

    WG_in_l2_clad.connect('o1', WG_out_l1_clad.ports['o2'], allow_layer_mismatch=True)
    taper_in_l2_clad.connect('o1', WG_in_l2_clad.ports['o2'], allow_layer_mismatch=True)
    S_wg_l2_clad.connect('o1', taper_in_l2_clad.ports['o2'], allow_layer_mismatch=True)
    taper_out_l2_clad.connect('o1', S_wg_l2_clad.ports['o2'], allow_layer_mismatch=True)
    WG_out_l2_clad.connect('o1', taper_out_l2_clad.ports['o2'], allow_layer_mismatch=True)

    # WG_in_r1_clad.connect('o1', WG_out_l2_clad.ports['o2'], allow_layer_mismatch=True)
    # taper_in_r1_clad.connect('o1', WG_in_r1_clad.ports['o2'], allow_layer_mismatch=True)
    # S_wg_r1_clad.connect('o1', taper_in_r1_clad.ports['o2'], allow_layer_mismatch=True)
    # taper_out_r1_clad.connect('o1', S_wg_r1_clad.ports['o2'], allow_layer_mismatch=True)
    # WG_out_r1_clad.connect('o1', taper_out_r1_clad.ports['o2'], allow_layer_mismatch=True)
    #
    # WG_in_r2_clad.connect('o1', WG_out_r1_clad.ports['o2'], allow_layer_mismatch=True)
    # taper_in_r2_clad.connect('o1', WG_in_r2_clad.ports['o2'], allow_layer_mismatch=True)
    # S_wg_r2_clad.connect('o1', taper_in_r2_clad.ports['o2'], allow_layer_mismatch=True)
    # taper_out_r2_clad.connect('o1', S_wg_r2_clad.ports['o2'], allow_layer_mismatch=True)
    # WG_out_r2_clad.connect('o1', taper_out_r2_clad.ports['o2'], allow_layer_mismatch=True)

    c.flatten()

    return c

#이전 버전
# def Sbend_Edge_Coupler(layer_core,layer_clad, width,bend_radius,length):
#     c = gf.Component()
#
#     WG_in_l1 = c << make_elements.make_path([straight(1000)], layer_core, 4)
#     taper_in_l1 = c << make_elements.make_taper(4, width, 1000, layer_core)
#     S_wg_l1 = c << make_elements.make_path(
#         [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(25),
#          gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(length)], layer=layer_core, width=width)
#     taper_out_l1 = c << make_elements.make_taper(width, 4, 1000, layer_core)
#     WG_out_l1 = c << make_elements.make_path([straight(1000)], layer_core, 4)
#
#     WG_in_l2 = c << make_elements.make_path([straight(1000)], layer_core, 4)
#     taper_in_l2 = c << make_elements.make_taper(4, width, 1000, layer_core)
#     S_wg_l2 = c << make_elements.make_path(
#         [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(25),
#          gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(length)], layer=layer_core, width=width)
#     taper_out_l2 = c << make_elements.make_taper(width, 4, 1000, layer_core)
#     WG_out_l2 = c << make_elements.make_path([straight(1000)], layer_core, 4)
#
#     WG_in_l1_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
#     taper_in_l1_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
#     S_wg_l1_clad = c << make_elements.make_path(
#         [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(25),
#          gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(length)], layer=layer_clad, width=width + 16)
#     taper_out_l1_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
#     WG_out_l1_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
#
#     WG_in_l2_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
#     taper_in_l2_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
#     S_wg_l2_clad = c << make_elements.make_path(
#         [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(25),
#          gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(length)], layer=layer_clad, width=width + 16)
#     taper_out_l2_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
#     WG_out_l2_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
#
#     WG_in_r1 = c << make_elements.make_path([straight(1000)], layer_core, 4)
#     taper_in_r1 = c << make_elements.make_taper(4, width, 1000, layer_core)
#     S_wg_r1 = c << make_elements.make_path(
#         [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(25),
#          gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(length)], layer=layer_core, width=width)
#     taper_out_r1 = c << make_elements.make_taper(width, 4, 1000, layer_core)
#     WG_out_r1 = c << make_elements.make_path([straight(1000)], layer_core, 4)
#
#     WG_in_r2 = c << make_elements.make_path([straight(1000)], layer_core, 4)
#     taper_in_r2 = c << make_elements.make_taper(4, width, 1000, layer_core)
#     S_wg_r2 = c << make_elements.make_path(
#         [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(25),
#          gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(length)], layer=layer_core, width=width)
#     taper_out_r2 = c << make_elements.make_taper(width, 4, 1000, layer_core)
#     WG_out_r2 = c << make_elements.make_path([straight(1000)], layer_core, 4)
#
#     WG_in_r1_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
#     taper_in_r1_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
#     S_wg_r1_clad = c << make_elements.make_path(
#         [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(25),
#          gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(length)], layer=layer_clad, width=width + 16)
#     taper_out_r1_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
#     WG_out_r1_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
#
#     WG_in_r2_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
#     taper_in_r2_clad = c << make_elements.make_taper(4 + 16, width + 16, 1000, layer_clad)
#     S_wg_r2_clad = c << make_elements.make_path(
#         [gf.path.straight(length), gf.path.arc(radius=bend_radius, angle=90), gf.path.straight(25),
#          gf.path.arc(radius=bend_radius, angle=-90), gf.path.straight(length)], layer=layer_clad, width=width + 16)
#     taper_out_r2_clad = c << make_elements.make_taper(width + 16, 4 + 16, 1000, layer_clad)
#     WG_out_r2_clad = c << make_elements.make_path([straight(1000)], layer_clad, 4 + 16)
#
#     taper_in_l1.connect('o1', WG_in_l1.ports['o2'], allow_layer_mismatch=True)
#     S_wg_l1.connect('o1', taper_in_l1.ports['o2'], allow_layer_mismatch=True)
#     taper_out_l1.connect('o1', S_wg_l1.ports['o2'], allow_layer_mismatch=True)
#     WG_out_l1.connect('o1', taper_out_l1.ports['o2'], allow_layer_mismatch=True)
#
#     WG_in_l2.connect('o1', WG_out_l1.ports['o2'], allow_layer_mismatch=True)
#     taper_in_l2.connect('o1', WG_in_l2.ports['o2'], allow_layer_mismatch=True)
#     S_wg_l2.connect('o1', taper_in_l2.ports['o2'], allow_layer_mismatch=True)
#     taper_out_l2.connect('o1', S_wg_l2.ports['o2'], allow_layer_mismatch=True)
#     WG_out_l2.connect('o1', taper_out_l2.ports['o2'], allow_layer_mismatch=True)
#
#     WG_in_r1.connect('o1', WG_out_l2.ports['o2'], allow_layer_mismatch=True)
#     taper_in_r1.connect('o1', WG_in_r1.ports['o2'], allow_layer_mismatch=True)
#     S_wg_r1.connect('o1', taper_in_r1.ports['o2'], allow_layer_mismatch=True)
#     taper_out_r1.connect('o1', S_wg_r1.ports['o2'], allow_layer_mismatch=True)
#     WG_out_r1.connect('o1', taper_out_r1.ports['o2'], allow_layer_mismatch=True)
#
#     WG_in_r2.connect('o1', WG_out_r1.ports['o2'], allow_layer_mismatch=True)
#     taper_in_r2.connect('o1', WG_in_r2.ports['o2'], allow_layer_mismatch=True)
#     S_wg_r2.connect('o1', taper_in_r2.ports['o2'], allow_layer_mismatch=True)
#     taper_out_r2.connect('o1', S_wg_r2.ports['o2'], allow_layer_mismatch=True)
#     WG_out_r2.connect('o1', taper_out_r2.ports['o2'], allow_layer_mismatch=True)
#
#
#     taper_in_l1_clad.connect('o1', WG_in_l1_clad.ports['o2'], allow_layer_mismatch=True)
#     S_wg_l1_clad.connect('o1', taper_in_l1_clad.ports['o2'], allow_layer_mismatch=True)
#     taper_out_l1_clad.connect('o1', S_wg_l1_clad.ports['o2'], allow_layer_mismatch=True)
#     WG_out_l1_clad.connect('o1', taper_out_l1_clad.ports['o2'], allow_layer_mismatch=True)
#
#     WG_in_l2_clad.connect('o1', WG_out_l1_clad.ports['o2'], allow_layer_mismatch=True)
#     taper_in_l2_clad.connect('o1', WG_in_l2_clad.ports['o2'], allow_layer_mismatch=True)
#     S_wg_l2_clad.connect('o1', taper_in_l2_clad.ports['o2'], allow_layer_mismatch=True)
#     taper_out_l2_clad.connect('o1', S_wg_l2_clad.ports['o2'], allow_layer_mismatch=True)
#     WG_out_l2_clad.connect('o1', taper_out_l2_clad.ports['o2'], allow_layer_mismatch=True)
#
#     WG_in_r1_clad.connect('o1', WG_out_l2_clad.ports['o2'], allow_layer_mismatch=True)
#     taper_in_r1_clad.connect('o1', WG_in_r1_clad.ports['o2'], allow_layer_mismatch=True)
#     S_wg_r1_clad.connect('o1', taper_in_r1_clad.ports['o2'], allow_layer_mismatch=True)
#     taper_out_r1_clad.connect('o1', S_wg_r1_clad.ports['o2'], allow_layer_mismatch=True)
#     WG_out_r1_clad.connect('o1', taper_out_r1_clad.ports['o2'], allow_layer_mismatch=True)
#
#     WG_in_r2_clad.connect('o1', WG_out_r1_clad.ports['o2'], allow_layer_mismatch=True)
#     taper_in_r2_clad.connect('o1', WG_in_r2_clad.ports['o2'], allow_layer_mismatch=True)
#     S_wg_r2_clad.connect('o1', taper_in_r2_clad.ports['o2'], allow_layer_mismatch=True)
#     taper_out_r2_clad.connect('o1', S_wg_r2_clad.ports['o2'], allow_layer_mismatch=True)
#     WG_out_r2_clad.connect('o1', taper_out_r2_clad.ports['o2'], allow_layer_mismatch=True)
#
#
#
#     return c
