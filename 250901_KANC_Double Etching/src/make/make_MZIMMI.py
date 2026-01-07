import numpy as np
from make import make_elements
import gdsfactory as gf
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
    #특별 출연(석현)
    MMI_out_clad = c << make_elements.make_taper(mmi_width + 16, wg_width + 16, 100,
                                                      layer=(layer[0], layer[1] + 1))
    MMI_out_clad.connect('o1', MMI_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

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
    Input_upper_clad = c << make_elements.make_taper(wg_width + 16, mmi_width, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_input_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_lower_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=-90)
                                                          ], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)
    Input_lower_clad = c << make_elements.make_taper(wg_width + 16, mmi_width, 100,
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

    MMI_in_clad = c << make_elements.make_taper(wg_width+ 16, mmi_width + 16, 100,
                                                layer=(layer[0], layer[1] + 1))
    MMI_in_clad.connect('o2', MMI_clad['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([10, 0])

    # output 설정
    S_wg_output_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_upper_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                          gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)
    Output_upper_clad = c << make_elements.make_taper(mmi_width, wg_width + 16, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_output_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_lower_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                           gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                           gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)
    Output_lower_clad = c << make_elements.make_taper(mmi_width, wg_width + 16, 100,
                                                      layer=(layer[0], layer[1] + 1))

    # 특별 출연(석현)
    MMI_out_clad = c << make_elements.make_taper(mmi_width + 16, wg_width + 18, 100,
                                                 layer=(layer[0], layer[1] + 1))
    MMI_out_clad.connect('o1', MMI_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

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
