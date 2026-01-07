import numpy as np
from make import make_elements
import gdsfactory as gf
from gdsfactory.path import straight, arc

#석영님 2x2 mmi
def make_2x2mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer):
    c = gf.Component()

    # 직사각형을 추가합니다. 중심을 기준으로 너비와 높이의 절반만큼의 위치를 계산합니다.
    c.add_polygon([(-mmi_length / 2, -mmi_width / 2), (mmi_length / 2, -mmi_width / 2), (mmi_length / 2, mmi_width / 2),
            (-mmi_length / 2, mmi_width / 2)], layer=layer)

    # 주의: (0,0)은 중심임. y값 주의
    # 입력 포트 left upper
    c.add_port(name='coreinput1', center=(-mmi_length / 2, (taper_width + mmi_gap)/2), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left lower
    c.add_port(name='coreinput2', center=(-mmi_length / 2, -(taper_width + mmi_gap)/2), width=taper_width, orientation=180, layer=layer)

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

def make_2x2MMI(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, period, fill_factor, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC1.mirror_x()
    GC2.mirror_x()

    S_wg_input_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                         gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                         gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_upper_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=90)
                                                          ], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)
    Input_upper_clad = c << make_elements.make_taper(wg_width + 16, mmi_width +16 - taper_width - mmi_gap, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_input_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_lower_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                          gf.path.straight(25), gf.path.arc(radius=100, angle=-90)
                                                          ], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)

    Input_lower_clad = c << make_elements.make_taper(wg_width + 16, mmi_width + 16 - taper_width - mmi_gap, 100,
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
    Output_upper_clad = c << make_elements.make_taper(mmi_width + 16 - taper_width - mmi_gap, wg_width + 16, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_output_lower = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_lower_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                           gf.path.straight(25), gf.path.arc(radius=100, angle=90),
                                                           gf.path.straight(100)], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)
    Output_lower_clad = c << make_elements.make_taper(mmi_width + 16 - taper_width - mmi_gap, wg_width + 16, 100,
                                                      layer=(layer[0], layer[1] + 1))

    S_wg_output_upper.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_upper_clad.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper_clad.connect('o1', Output_upper_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower.connect('o1', MMI.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_lower_clad.connect('o1', MMI.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower_clad.connect('o1', Output_lower_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC4 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC3.connect('o1', S_wg_output_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC4.connect('o1', S_wg_output_lower.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC3.move([-10, 0])
    GC4.move([-10, 0])

    c.flatten()

    return c


# 지현 4X4, 8X8 MMI

def make_4x4mmi_core(wg_width, taper_width, taper_length,mmi_length, mmi_width, mmi_gap, layer):

    # 새로운 컴포넌트 생성
    c = gf.Component()

    # 직사각형을 추가합니다. 중심을 기준으로 너비와 높이의 절반만큼의 위치를 계산합니다.
    c.add_polygon([(-mmi_length / 2, -mmi_width / 2),
            (mmi_length / 2, -mmi_width / 2),
            (mmi_length / 2, mmi_width / 2),
            (-mmi_length / 2, mmi_width / 2),],
        layer=layer)

    # 주의: (0,0)은 중심임. y값 주의
    # 입력 포트 left upper 1
    c.add_port(name='coreinput1', center=(-mmi_length / 2, mmi_gap/2 + mmi_gap), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left upper 2
    c.add_port(name='coreinput2', center=(-mmi_length / 2, mmi_gap/2), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left lower 3
    c.add_port(name='coreinput3', center=(-mmi_length / 2, -mmi_gap/2), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left lower 4
    c.add_port(name='coreinput4', center=(-mmi_length / 2, -mmi_gap/2 - mmi_gap), width=taper_width, orientation=180, layer=layer)

    # 출력 포트 right upper1
    c.add_port(name='coreoutput1', center=(mmi_length / 2, mmi_gap/2 + mmi_gap), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right upper2
    c.add_port(name='coreoutput2', center=(mmi_length / 2, mmi_gap/2), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right lower1
    c.add_port(name='coreoutput3', center=(mmi_length / 2, -mmi_gap/2), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right lower2
    c.add_port(name='coreoutput4', center=(mmi_length / 2, -mmi_gap/2 - mmi_gap), width=taper_width, orientation=0, layer=layer)

    Input_taper_upper1 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_upper2 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_lower1 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_lower2 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)

    Output_taper_upper1 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_upper2 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_lower1 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_lower2 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)

    Input_taper_upper1.connect('o2', c.ports['coreinput1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_upper2.connect('o2', c.ports['coreinput2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_lower1.connect('o2', c.ports['coreinput3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_lower2.connect('o2', c.ports['coreinput4'], allow_layer_mismatch=True, allow_width_mismatch=True)

    Output_taper_upper1.connect('o1', c.ports['coreoutput1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_upper2.connect('o1', c.ports['coreoutput2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_lower1.connect('o1', c.ports['coreoutput3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_lower2.connect('o1', c.ports['coreoutput4'], allow_layer_mismatch=True, allow_width_mismatch=True)

    c.add_port(name='o1', port=Input_taper_upper1[0])
    c.add_port(name='o2', port=Input_taper_upper2[0])
    c.add_port(name='o3', port=Input_taper_lower1[0])
    c.add_port(name='o4', port=Input_taper_lower2[0])

    c.add_port(name='o5', port=Output_taper_upper1[1])
    c.add_port(name='o6', port=Output_taper_upper2[1])
    c.add_port(name='o7', port=Output_taper_lower1[1])
    c.add_port(name='o8', port=Output_taper_lower2[1])
    c.add_port(name='o9', center=(-(mmi_length / 2) - taper_length, 0), width=taper_width, orientation=0, layer=layer)
    c.add_port(name='o10', center=(0, 0), width=taper_width, orientation=0, layer=layer)

    c.flatten()

    return c

def make_4x4MMI(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, period, fill_factor, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC4 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)


    GC1.mirror_x()
    GC2.mirror_x()
    GC3.mirror_x()
    GC4.mirror_x()

#첫번째 Input포트 넣기
    S_wg_input_upper1 = c << make_elements.make_path([gf.path.straight(50),gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(300), gf.path.arc(radius=100, angle=90)], layer=layer, width=wg_width)
    S_wg_input_upper1_clad = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=-90),
                                                          gf.path.straight(300), gf.path.arc(radius=100, angle=90)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

# 두번째 Input포트 넣기
    S_wg_input_upper2 = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(50), gf.path.arc(radius=100, angle=90),gf.path.straight(50)], layer=layer, width=wg_width)
    S_wg_input_upper2_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(50), gf.path.arc(radius=100, angle=90),gf.path.straight(50)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

# 세번째 Input포트 넣기
    S_wg_input_lower1 = c << make_elements.make_path([gf.path.straight(250)], layer=layer, width=wg_width)
    S_wg_input_lower1_clad = c << make_elements.make_path([gf.path.straight(250)], layer=(layer[0], layer[1] + 1),width=wg_width + 16 )

#네번째 Input포트 넣기
    S_wg_input_lower2 = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(50), gf.path.arc(radius=100, angle=-90),gf.path.straight(50)], layer=layer, width=wg_width)
    S_wg_input_lower2_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(50), gf.path.arc(radius=100, angle=-90),gf.path.straight(50)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)



    # MMI 설정
    MMI_core = c << make_4x4mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)
    # MMI_core_clad_input_upper = c << make_elements.make_taper(wg_width + 16, mmi_width +24 - 3* mmi_gap, taper_length + mmi_length/2,
    #                                             layer=(layer[0], layer[1] + 1))
    # MMI_core_clad_input_lower = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))
    # MMI_core_clad_input_middel = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))
    #
    # MMI_core_clad_output_middel = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap,wg_width + 16,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))

    # 첫 번째 Input 포트 연결
    S_wg_input_upper1.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC1.connect('o1', S_wg_input_upper1_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])

    # 첫 번째 Input 포트 MMI에 연결
    MMI_core.connect('o1', S_wg_input_upper1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # MMI_core_clad_input_upper.connect('o1', S_wg_input_upper1_clad.ports['o2'], allow_layer_mismatch=True,
    #                                   allow_width_mismatch=True)

    #두 번째 Input 포트 연결 및 MMI에 연결
    S_wg_input_upper2.connect('o2', MMI_core.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg_input_upper2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper2_clad.connect('o2', MMI_core.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([10, 0])

    #세 번째 Input 포트 연결 및 MMI에 연결
    S_wg_input_lower1.connect('o2', MMI_core.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC3.connect('o1', S_wg_input_lower1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower1_clad.connect('o2', MMI_core.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC3.move([10, 0])

    #네 번째 Input 포트 연결 및 MMI에 연결, MMI_core_clad_input_lower 연결
    S_wg_input_lower2.connect('o2', MMI_core.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC4.connect('o1', S_wg_input_lower2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower2_clad.connect('o2', MMI_core.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # MMI_core_clad_input_lower.connect('o1', S_wg_input_lower2_clad.ports['o2'], allow_layer_mismatch=True,
    #                                   allow_width_mismatch=True)
    GC4.move([10, 0])


    # output 설정
    GC5 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC6 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC7 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC8 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC5.mirror_x()
    GC6.mirror_x()
    GC7.mirror_x()
    GC8.mirror_x()

    # 첫번째 output 포트 넣기
    S_wg_output_upper1 = c << make_elements.make_path([ gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(300), gf.path.arc(radius=100, angle=-90)],
                                                     layer=layer, width=wg_width)
    S_wg_output_upper1_clad = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                           gf.path.straight(300), gf.path.arc(radius=100, angle=-90)],
                                                          layer=(layer[0], layer[1] + 1), width=wg_width + 16)

    # 두번째 output 포트 넣기
    S_wg_output_upper2 = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(50), gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(50)], layer=layer, width=wg_width)
    S_wg_output_upper2_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                           gf.path.straight(50), gf.path.arc(radius=100, angle=-90),
                                                           gf.path.straight(50)], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)

    # 세번째 output포트 넣기
    S_wg_output_lower1 = c << make_elements.make_path([gf.path.straight(250)], layer=layer, width=wg_width)
    S_wg_output_lower1_clad = c << make_elements.make_path([gf.path.straight(250)], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)

    # 네번째 output 포트 넣기
    S_wg_output_lower2 = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(50)], layer=layer, width=wg_width)
    S_wg_output_lower2_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                           gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                           gf.path.straight(50)], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)

    # # Output MMI clad 설정
    # MMI_core_clad_output_upper = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))
    # MMI_core_clad_output_lower = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))

    # MMI에 첫 번째 output 포트 연결 및 MMI에 연결
    S_wg_output_upper1.connect('o2', MMI_core.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper1_clad.connect('o2', MMI_core.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC5.connect('o1', S_wg_output_upper1_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC5.move([-10, 0])

    # MMI에 두 번째 output 포트 연결 및 MMI에 연결
    S_wg_output_upper2.connect('o2', MMI_core.ports['o6'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper2_clad.connect('o2', MMI_core.ports['o6'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC6.connect('o1', S_wg_output_upper2_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC6.move([-10, 0])

    # MMI에 세 번째 output 포트 연결 및 MMI에 연결
    S_wg_output_lower1.connect('o2', MMI_core.ports['o7'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower1_clad.connect('o2', MMI_core.ports['o7'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC7.connect('o1', S_wg_output_lower1_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC7.move([-10, 0])

    # MMI에 네 번째 output 포트 연결 및 MMI에 연결
    S_wg_output_lower2.connect('o2', MMI_core.ports['o8'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower2_clad.connect('o2', MMI_core.ports['o8'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC8.connect('o1', S_wg_output_lower2_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC8.move([-10, 0])


    # Input MMI clad 설정
    MMI_core_clad_input_upper = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_lower = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_middle = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
                                                               taper_length + mmi_length / 2,
                                                               layer=(layer[0], layer[1] + 1))


    # Output MMI clad 설정
    MMI_core_clad_output_upper = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_output_lower = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))

    MMI_core_clad_output_middle = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
                                                                taper_length + mmi_length / 2,
                                                                layer=(layer[0], layer[1] + 1))

    #Input MMI core clad 연결
    MMI_core_clad_input_upper.connect('o1', S_wg_input_upper1_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_input_lower.connect('o1', S_wg_input_lower2_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)

    MMI_core_clad_input_middle.connect('o2', MMI_core.ports['o9'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)

    #Output MMI core clad 연결

    MMI_core_clad_output_upper.connect('o2', S_wg_output_upper1_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_output_lower.connect('o2', S_wg_output_lower2_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_output_middle.connect('o1', MMI_core.ports['o10'], allow_layer_mismatch=True,
                                       allow_width_mismatch=True)

    c.flatten()

    return c

def make_8x8mmi_core(wg_width, taper_width, taper_length,mmi_length, mmi_width, mmi_gap, layer):

    # 새로운 컴포넌트 생성
    c = gf.Component()

    # 직사각형을 추가합니다. 중심을 기준으로 너비와 높이의 절반만큼의 위치를 계산합니다.
    c.add_polygon([(-mmi_length / 2, -mmi_width / 2),
            (mmi_length / 2, -mmi_width / 2),
            (mmi_length / 2, mmi_width / 2),
            (-mmi_length / 2, mmi_width / 2),],
        layer=layer)


    # 주의: (0,0)은 중심임. y값 주의
    # 입력 포트 left upper 1
    c.add_port(name='coreinput1', center=(-mmi_length / 2, mmi_gap/2 + 3 * mmi_gap), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left upper 2
    c.add_port(name='coreinput2', center=(-mmi_length / 2, mmi_gap/2 + 2 * mmi_gap), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left upper 3
    c.add_port(name='coreinput3', center=(-mmi_length / 2, mmi_gap/2 + mmi_gap), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left upper 4
    c.add_port(name='coreinput4', center=(-mmi_length / 2, mmi_gap/2 ), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left lower 5
    c.add_port(name='coreinput5', center=(-mmi_length / 2, -mmi_gap/2 ), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left lower 6
    c.add_port(name='coreinput6', center=(-mmi_length / 2, -mmi_gap/2 - mmi_gap), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left lower 7
    c.add_port(name='coreinput7', center=(-mmi_length / 2, -mmi_gap/2 - 2 * mmi_gap), width=taper_width, orientation=180, layer=layer)
    # 입력 포트 left lower 8
    c.add_port(name='coreinput8', center=(-mmi_length / 2, -mmi_gap/2 - 3 * mmi_gap), width=taper_width, orientation=180, layer=layer)


    # 출력 포트 right upper1
    c.add_port(name='coreoutput1', center=(mmi_length / 2, mmi_gap/2 + 3 * mmi_gap), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right upper2
    c.add_port(name='coreoutput2', center=(mmi_length / 2, mmi_gap/2 + 2 * mmi_gap), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right upper3
    c.add_port(name='coreoutput3', center=(mmi_length / 2, mmi_gap / 2 + mmi_gap), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right upper4
    c.add_port(name='coreoutput4', center=(mmi_length / 2, mmi_gap / 2), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right lower1
    c.add_port(name='coreoutput5', center=(mmi_length / 2, -mmi_gap/2), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right lower2
    c.add_port(name='coreoutput6', center=(mmi_length / 2, -mmi_gap/2 - mmi_gap), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right lower3
    c.add_port(name='coreoutput7', center=(mmi_length / 2, -mmi_gap/2 - 2 * mmi_gap), width=taper_width, orientation=0, layer=layer)
    # 출력 포트 right lower4
    c.add_port(name='coreoutput8', center=(mmi_length / 2, -mmi_gap/2 - 3 * mmi_gap), width=taper_width, orientation=0, layer=layer)

    Input_taper_upper1 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_upper2 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_upper3 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_upper4 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_lower1 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_lower2 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_lower3 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)
    Input_taper_lower4 = c << make_elements.make_taper(wg_width, taper_width, taper_length, layer=layer)



    Output_taper_upper1 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_upper2 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_upper3 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_upper4 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_lower1 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_lower2 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_lower3 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)
    Output_taper_lower4 = c << make_elements.make_taper(taper_width, wg_width, taper_length, layer=layer)

    Input_taper_upper1.connect('o2', c.ports['coreinput1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_upper2.connect('o2', c.ports['coreinput2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_upper3.connect('o2', c.ports['coreinput3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_upper4.connect('o2', c.ports['coreinput4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_lower1.connect('o2', c.ports['coreinput5'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_lower2.connect('o2', c.ports['coreinput6'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_lower3.connect('o2', c.ports['coreinput7'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Input_taper_lower4.connect('o2', c.ports['coreinput8'], allow_layer_mismatch=True, allow_width_mismatch=True)

    Output_taper_upper1.connect('o1', c.ports['coreoutput1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_upper2.connect('o1', c.ports['coreoutput2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_upper3.connect('o1', c.ports['coreoutput3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_upper4.connect('o1', c.ports['coreoutput4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_lower1.connect('o1', c.ports['coreoutput5'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_lower2.connect('o1', c.ports['coreoutput6'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_lower3.connect('o1', c.ports['coreoutput7'], allow_layer_mismatch=True, allow_width_mismatch=True)
    Output_taper_lower4.connect('o1', c.ports['coreoutput8'], allow_layer_mismatch=True, allow_width_mismatch=True)

    c.add_port(name='o1', port=Input_taper_upper1[0])
    c.add_port(name='o2', port=Input_taper_upper2[0])
    c.add_port(name='o3', port=Input_taper_upper3[0])
    c.add_port(name='o4', port=Input_taper_upper4[0])
    c.add_port(name='o5', port=Input_taper_lower1[0])
    c.add_port(name='o6', port=Input_taper_lower2[0])
    c.add_port(name='o7', port=Input_taper_lower3[0])
    c.add_port(name='o8', port=Input_taper_lower4[0])


    c.add_port(name='o9', port=Output_taper_upper1[1])
    c.add_port(name='o10', port=Output_taper_upper2[1])
    c.add_port(name='o11', port=Output_taper_upper3[1])
    c.add_port(name='o12', port=Output_taper_upper4[1])
    c.add_port(name='o13', port=Output_taper_lower1[1])
    c.add_port(name='o14', port=Output_taper_lower2[1])
    c.add_port(name='o15', port=Output_taper_lower3[1])
    c.add_port(name='o16', port=Output_taper_lower4[1])
    c.add_port(name='o17', center=(-(mmi_length / 2) - taper_length, 0 ), width=taper_width, orientation=0, layer=layer)
    c.add_port(name='o18', center=(0, 0), width=taper_width, orientation=0, layer=layer)
    #c.add_port(name='o18', center=((mmi_length / 2) + taper_length, 0 ), width=taper_width, orientation=0, layer=layer)
    c.add_port(name='o19', center=(-(mmi_length / 2) - taper_length, (mmi_gap / 2) + mmi_gap + (mmi_gap / 2) ), width=taper_width, orientation=0, layer=layer)
    c.add_port(name='o20', center=(-(mmi_length / 2) - taper_length, -(mmi_gap / 2) - mmi_gap - (mmi_gap / 2)), width=taper_width, orientation=0, layer=layer)

    c.flatten()

    return c

def make_8x8MMI(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, period, fill_factor, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC4 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC5 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC6 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC7 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC8 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)


    GC1.mirror_x()
    GC2.mirror_x()
    GC3.mirror_x()
    GC4.mirror_x()
    GC5.mirror_x()
    GC6.mirror_x()
    GC7.mirror_x()
    GC8.mirror_x()

    #첫번째~여덟번째 Input Waveguide 넣기
    S_wg_input_upper1 = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(550), gf.path.arc(radius=100, angle=90)], layer=layer, width=wg_width)

    S_wg_input_upper2 = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(300), gf.path.arc(radius=100, angle=90),gf.path.straight(50)], layer=layer, width=wg_width)

    S_wg_input_upper3 = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(50), gf.path.arc(radius=100, angle=90),gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_input_upper4 = c << make_elements.make_path([gf.path.straight(300)], layer=layer, width=wg_width)

    S_wg_input_lower1 = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(50), gf.path.arc(radius=100, angle=-90),gf.path.straight(100)], layer=layer, width=wg_width)
    S_wg_input_lower2 = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(300), gf.path.arc(radius=100, angle=-90),gf.path.straight(50)], layer=layer, width=wg_width)
    S_wg_input_lower3 = c << make_elements.make_path([gf.path.straight(75),gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(550), gf.path.arc(radius=100, angle=-90),gf.path.straight(25)], layer=layer, width=wg_width)
    S_wg_input_lower4 = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(800), gf.path.arc(radius=100, angle=-90)], layer=layer, width=wg_width)



    #첫번째~여덟번째 Input clad 넣기
    S_wg_input_upper1_clad = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=100, angle=-90),
                                                     gf.path.straight(550), gf.path.arc(radius=100, angle=90)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_input_upper2_clad = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(300), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(50)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_input_upper3_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(100)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_input_upper4_clad = c << make_elements.make_path([gf.path.straight(300)],layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_input_lower1_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(50), gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(100)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_input_lower2_clad = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(300), gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(50)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_input_lower3_clad = c << make_elements.make_path([gf.path.straight(75), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(550), gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(25)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_input_lower4_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(800), gf.path.arc(radius=100, angle=-90)],
                                                     layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    #MMI 설정
    MMI_core = c << make_8x8mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)



    #첫 번째 Input 포트 연결
    GC1.connect('o1', S_wg_input_upper1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])

    # 첫 번째 input 포트를 MMI에 연결
    MMI_core.connect('o1', S_wg_input_upper1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # MMI_core_clad_input_upper.connect('o1', S_wg_input_upper1_clad.ports['o2'], allow_layer_mismatch=True,
    #                                    allow_width_mismatch=True)

    #두 번째 Input 포트 MMI에 연결
    S_wg_input_upper2.connect('o2', MMI_core.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg_input_upper2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper2_clad.connect('o2', MMI_core.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.move([10, 0])

    #나머지 Input 포트 MMI에 연결, 마지막 input lower4 clad 포트에 MMI_core_clad_input_lower 연결
    S_wg_input_upper3.connect('o2', MMI_core.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC3.connect('o1', S_wg_input_upper3.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper3_clad.connect('o2', MMI_core.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_upper4.connect('o2', MMI_core.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC4.connect('o1', S_wg_input_upper4.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper4_clad.connect('o2', MMI_core.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower1.connect('o2', MMI_core.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC5.connect('o1', S_wg_input_lower1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower1_clad.connect('o2', MMI_core.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower2.connect('o2', MMI_core.ports['o6'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC6.connect('o1', S_wg_input_lower2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower2_clad.connect('o2', MMI_core.ports['o6'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower3.connect('o2', MMI_core.ports['o7'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC7.connect('o1', S_wg_input_lower3.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower3_clad.connect('o2', MMI_core.ports['o7'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower4.connect('o2', MMI_core.ports['o8'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC8.connect('o1', S_wg_input_lower4.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower4_clad.connect('o2', MMI_core.ports['o8'], allow_layer_mismatch=True, allow_width_mismatch=True)


    GC3.move([10, 0])
    GC4.move([10, 0])
    GC5.move([10, 0])
    GC6.move([10, 0])
    GC7.move([10, 0])
    GC8.move([10, 0])

    # output 설정
    GC9 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC10 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC11 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC12 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC13 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC14 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC15 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC16 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC9.mirror_x()
    GC10.mirror_x()
    GC11.mirror_x()
    GC12.mirror_x()
    GC13.mirror_x()
    GC14.mirror_x()
    GC15.mirror_x()
    GC16.mirror_x()

    # 첫번째~여덟번째 output Waveguide 넣기
    S_wg_output_upper1 = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(550), gf.path.arc(radius=100, angle=-90),gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_upper2 = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(300), gf.path.arc(radius=100, angle=-90),gf.path.straight(50)], layer=layer, width=wg_width)

    S_wg_output_upper3 = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                     gf.path.straight(50), gf.path.arc(radius=100, angle=-90)], layer=layer, width=wg_width)

    S_wg_output_upper4 = c << make_elements.make_path([gf.path.straight(300)], layer=layer, width=wg_width)

    S_wg_output_lower1 = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(50), gf.path.arc(radius=100, angle=90)], layer=layer, width=wg_width)
    S_wg_output_lower2 = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(300), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(50)], layer=layer, width=wg_width)
    S_wg_output_lower3 = c << make_elements.make_path([gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(550), gf.path.arc(radius=100, angle=90),
                                                      gf.path.straight(75)], layer=layer, width=wg_width)
    S_wg_output_lower4 = c << make_elements.make_path([ gf.path.arc(radius=100, angle=-90),
                                                      gf.path.straight(800), gf.path.arc(radius=100, angle=90),gf.path.straight(100)],
                                                     layer=layer, width=wg_width)

    # 첫번째~여덟번째 output clad 넣기
    S_wg_output_upper1_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=90),
                                                       gf.path.straight(550), gf.path.arc(radius=100, angle=-90),
                                                       gf.path.straight(100)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_output_upper2_clad = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=90),
                                                       gf.path.straight(300), gf.path.arc(radius=100, angle=-90),
                                                       gf.path.straight(50)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_output_upper3_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=90),
                                                       gf.path.straight(50), gf.path.arc(radius=100, angle=-90)],
                                                      layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_output_upper4_clad = c << make_elements.make_path([gf.path.straight(300)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_output_lower1_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=100, angle=-90),
                                                       gf.path.straight(50), gf.path.arc(radius=100, angle=90)],
                                                      layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_output_lower2_clad = c << make_elements.make_path([gf.path.straight(50), gf.path.arc(radius=100, angle=-90),
                                                       gf.path.straight(300), gf.path.arc(radius=100, angle=90),
                                                       gf.path.straight(50)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_output_lower3_clad = c << make_elements.make_path([gf.path.straight(25), gf.path.arc(radius=100, angle=-90),
                                                       gf.path.straight(550), gf.path.arc(radius=100, angle=90),
                                                       gf.path.straight(75)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_output_lower4_clad = c << make_elements.make_path([gf.path.arc(radius=100, angle=-90),
                                                       gf.path.straight(800), gf.path.arc(radius=100, angle=90),
                                                       gf.path.straight(100)],
                                                      layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    #첫번째~여덟번째 output 포트를 MMI에 연결
    S_wg_output_upper1.connect('o1', MMI_core.ports['o9'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC9.connect('o1', S_wg_output_upper1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper1_clad.connect('o1', MMI_core.ports['o9'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_upper2.connect('o1', MMI_core.ports['o10'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC10.connect('o1', S_wg_output_upper2.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper2_clad.connect('o1', MMI_core.ports['o10'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_upper3.connect('o1', MMI_core.ports['o11'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC11.connect('o1', S_wg_output_upper3.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper3_clad.connect('o1', MMI_core.ports['o11'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_upper4.connect('o1', MMI_core.ports['o12'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC12.connect('o1', S_wg_output_upper4.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper4_clad.connect('o1', MMI_core.ports['o12'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower1.connect('o1', MMI_core.ports['o13'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC13.connect('o1', S_wg_output_lower1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower1_clad.connect('o1', MMI_core.ports['o13'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower2.connect('o1', MMI_core.ports['o14'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC14.connect('o1', S_wg_output_lower2.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower2_clad.connect('o1', MMI_core.ports['o14'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower3.connect('o1', MMI_core.ports['o15'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC15.connect('o1', S_wg_output_lower3.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower3_clad.connect('o1', MMI_core.ports['o15'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower4.connect('o1', MMI_core.ports['o16'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC16.connect('o1', S_wg_output_lower4.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower4_clad.connect('o1', MMI_core.ports['o16'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC9.move([-10, 0])
    GC10.move([-10, 0])
    GC11.move([-10, 0])
    GC12.move([-10, 0])
    GC13.move([-10, 0])
    GC14.move([-10, 0])
    GC15.move([-10, 0])
    GC16.move([-10, 0])

    #Input MMI Core clad 설정
    MMI_core_clad_input_upper = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 7 * mmi_gap,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_lower = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 7 * mmi_gap,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_middle = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 ,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))

    # output MMI Core clad 설정
    MMI_core_clad_output_upper = c << make_elements.make_taper( mmi_width + 24 - 7 * mmi_gap,wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_output_lower = c << make_elements.make_taper(mmi_width + 24 - 7 * mmi_gap,wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))

    MMI_core_clad_output_middle = c << make_elements.make_taper(mmi_width + 24 , wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))


    #MMI CORE CLAD 연결
    MMI_core_clad_input_upper.connect('o1', S_wg_input_upper1_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_input_lower.connect('o1', S_wg_input_lower4_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_input_middle.connect('o1', MMI_core.ports['o17'], allow_layer_mismatch=True, allow_width_mismatch=True)


    MMI_core_clad_output_upper.connect('o2', S_wg_output_upper1_clad.ports['o1'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_output_lower.connect('o2', S_wg_output_lower4_clad.ports['o1'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)

    MMI_core_clad_output_middle.connect('o1', MMI_core.ports['o18'], allow_layer_mismatch=True,
                                       allow_width_mismatch=True)

    c.flatten()

    return c

#GC 늘린 버전의 8X8 MMI
def make_8x8MMI_GC(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, period, fill_factor, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC4 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC5 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC6 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC7 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC8 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)


    GC1.mirror_x()
    GC2.mirror_x()
    GC3.mirror_x()
    GC4.mirror_x()
    GC5.mirror_x()
    GC6.mirror_x()
    GC7.mirror_x()
    GC8.mirror_x()

    #첫번째~여덟번째 Input Waveguide 넣기
    S_wg_input_upper1 = c << make_elements.make_path([ gf.path.straight(175), gf.path.arc(radius=200, angle=-90),
                                                     gf.path.straight(800), gf.path.arc(radius=200, angle=90),gf.path.straight(450)], layer=layer, width=wg_width)

    S_wg_input_upper2 = c << make_elements.make_path([gf.path.straight(150), gf.path.arc(radius=200, angle=-90),
                                                     gf.path.straight(550), gf.path.arc(radius=200, angle=90),gf.path.straight(475)], layer=layer, width=wg_width)

    S_wg_input_upper3 = c << make_elements.make_path([gf.path.straight(125),gf.path.arc(radius=200, angle=-90),
                                                     gf.path.straight(300), gf.path.arc(radius=200, angle=90),gf.path.straight(500)], layer=layer, width=wg_width)

    S_wg_input_upper4 = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=-90),
                                                     gf.path.straight(50), gf.path.arc(radius=200, angle=90),gf.path.straight(525)], layer=layer, width=wg_width)

    S_wg_input_lower1 = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=90),
                                                     gf.path.straight(50), gf.path.arc(radius=200, angle=-90),gf.path.straight(525)], layer=layer, width=wg_width)
    S_wg_input_lower2 = c << make_elements.make_path([gf.path.straight(125), gf.path.arc(radius=200, angle=90),
                                                     gf.path.straight(300), gf.path.arc(radius=200, angle=-90),gf.path.straight(500)], layer=layer, width=wg_width)
    S_wg_input_lower3 = c << make_elements.make_path([gf.path.straight(150),gf.path.arc(radius=200, angle=90),
                                                     gf.path.straight(550), gf.path.arc(radius=200, angle=-90),gf.path.straight(475)], layer=layer, width=wg_width)
    S_wg_input_lower4 = c << make_elements.make_path([gf.path.straight(175),gf.path.arc(radius=200, angle=90),
                                                     gf.path.straight(800), gf.path.arc(radius=200, angle=-90),gf.path.straight(450)], layer=layer, width=wg_width)



    #첫번째~여덟번째 Input clad 넣기
    S_wg_input_upper1_clad = c << make_elements.make_path([gf.path.straight(175),gf.path.arc(radius=200, angle=-90),
                                                     gf.path.straight(800), gf.path.arc(radius=200, angle=90), gf.path.straight(450)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_input_upper2_clad = c << make_elements.make_path([gf.path.straight(150), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(550), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(475)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_input_upper3_clad = c << make_elements.make_path([gf.path.straight(125), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(300), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(500)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_input_upper4_clad = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(50), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(525)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_input_lower1_clad = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(50), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(525)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_input_lower2_clad = c << make_elements.make_path([gf.path.straight(125), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(300), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(500)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_input_lower3_clad = c << make_elements.make_path([gf.path.straight(150), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(550), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(475)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_input_lower4_clad = c << make_elements.make_path([gf.path.straight(175), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(800), gf.path.arc(radius=200, angle=-90),gf.path.straight(450)],
                                                     layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    #MMI 설정
    MMI_core = c << make_8x8mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)



    #첫 번째 Input 포트 연결
    GC1.connect('o1', S_wg_input_upper1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])

    # 첫 번째 input 포트를 MMI에 연결
    MMI_core.connect('o1', S_wg_input_upper1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # MMI_core_clad_input_upper.connect('o1', S_wg_input_upper1_clad.ports['o2'], allow_layer_mismatch=True,
    #                                    allow_width_mismatch=True)

    #두 번째 Input 포트 MMI에 연결
    S_wg_input_upper2.connect('o2', MMI_core.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg_input_upper2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper2_clad.connect('o2', MMI_core.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.move([10, 0])

    #나머지 Input 포트 MMI에 연결, 마지막 input lower4 clad 포트에 MMI_core_clad_input_lower 연결
    S_wg_input_upper3.connect('o2', MMI_core.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC3.connect('o1', S_wg_input_upper3.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper3_clad.connect('o2', MMI_core.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_upper4.connect('o2', MMI_core.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC4.connect('o1', S_wg_input_upper4.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper4_clad.connect('o2', MMI_core.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower1.connect('o2', MMI_core.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC5.connect('o1', S_wg_input_lower1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower1_clad.connect('o2', MMI_core.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower2.connect('o2', MMI_core.ports['o6'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC6.connect('o1', S_wg_input_lower2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower2_clad.connect('o2', MMI_core.ports['o6'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower3.connect('o2', MMI_core.ports['o7'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC7.connect('o1', S_wg_input_lower3.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower3_clad.connect('o2', MMI_core.ports['o7'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower4.connect('o2', MMI_core.ports['o8'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC8.connect('o1', S_wg_input_lower4.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower4_clad.connect('o2', MMI_core.ports['o8'], allow_layer_mismatch=True, allow_width_mismatch=True)


    GC3.move([10, 0])
    GC4.move([10, 0])
    GC5.move([10, 0])
    GC6.move([10, 0])
    GC7.move([10, 0])
    GC8.move([10, 0])

    # output 설정
    GC9 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC10 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC11 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC12 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC13 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC14 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC15 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC16 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC9.mirror_x()
    GC10.mirror_x()
    GC11.mirror_x()
    GC12.mirror_x()
    GC13.mirror_x()
    GC14.mirror_x()
    GC15.mirror_x()
    GC16.mirror_x()

    # 첫번째~여덟번째 output Waveguide 넣기
    S_wg_output_upper1 = c << make_elements.make_path([gf.path.straight(450),gf.path.arc(radius=200, angle=90),
                                                     gf.path.straight(800), gf.path.arc(radius=200, angle=-90),gf.path.straight(175)], layer=layer, width=wg_width)

    S_wg_output_upper2 = c << make_elements.make_path([gf.path.straight(475), gf.path.arc(radius=200, angle=90),
                                                     gf.path.straight(550), gf.path.arc(radius=200, angle=-90),gf.path.straight(150)], layer=layer, width=wg_width)

    S_wg_output_upper3 = c << make_elements.make_path([gf.path.straight(500), gf.path.arc(radius=200, angle=90),
                                                     gf.path.straight(300), gf.path.arc(radius=200, angle=-90),gf.path.straight(125)], layer=layer, width=wg_width)

    S_wg_output_upper4 = c << make_elements.make_path([gf.path.straight(525), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(50), gf.path.arc(radius=200, angle=-90),gf.path.straight(100)], layer=layer, width=wg_width)

    S_wg_output_lower1 = c << make_elements.make_path([gf.path.straight(525), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(50), gf.path.arc(radius=200, angle=90),gf.path.straight(100)], layer=layer, width=wg_width)
    S_wg_output_lower2 = c << make_elements.make_path([gf.path.straight(500), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(300), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(125)], layer=layer, width=wg_width)
    S_wg_output_lower3 = c << make_elements.make_path([gf.path.straight(475), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(550), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(150)], layer=layer, width=wg_width)
    S_wg_output_lower4 = c << make_elements.make_path([ gf.path.straight(450),gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(800), gf.path.arc(radius=200, angle=90),gf.path.straight(175)],
                                                     layer=layer, width=wg_width)

    # 첫번째~여덟번째 output clad 넣기
    S_wg_output_upper1_clad = c << make_elements.make_path([ gf.path.straight(450), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(800), gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(175)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_output_upper2_clad = c << make_elements.make_path([gf.path.straight(475), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(550), gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(150)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_output_upper3_clad = c << make_elements.make_path([gf.path.straight(500), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(300), gf.path.arc(radius=200, angle=-90),gf.path.straight(125)],
                                                      layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_output_upper4_clad = c << make_elements.make_path([gf.path.straight(525), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(50), gf.path.arc(radius=200, angle=-90),gf.path.straight(100)],
                                                      layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    S_wg_output_lower1_clad = c << make_elements.make_path([gf.path.straight(525), gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(50), gf.path.arc(radius=200, angle=90),gf.path.straight(100)],
                                                      layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_output_lower2_clad = c << make_elements.make_path([gf.path.straight(500), gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(300), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(125)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_output_lower3_clad = c << make_elements.make_path([gf.path.straight(475), gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(550), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(150)], layer=(layer[0], layer[1] + 1),width=wg_width + 16)
    S_wg_output_lower4_clad = c << make_elements.make_path([gf.path.straight(450),gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(800), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(175)],
                                                      layer=(layer[0], layer[1] + 1),width=wg_width + 16)

    #첫번째~여덟번째 output 포트를 MMI에 연결
    S_wg_output_upper1.connect('o1', MMI_core.ports['o9'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC9.connect('o1', S_wg_output_upper1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper1_clad.connect('o1', MMI_core.ports['o9'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_upper2.connect('o1', MMI_core.ports['o10'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC10.connect('o1', S_wg_output_upper2.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper2_clad.connect('o1', MMI_core.ports['o10'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_upper3.connect('o1', MMI_core.ports['o11'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC11.connect('o1', S_wg_output_upper3.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper3_clad.connect('o1', MMI_core.ports['o11'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_upper4.connect('o1', MMI_core.ports['o12'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC12.connect('o1', S_wg_output_upper4.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper4_clad.connect('o1', MMI_core.ports['o12'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower1.connect('o1', MMI_core.ports['o13'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC13.connect('o1', S_wg_output_lower1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower1_clad.connect('o1', MMI_core.ports['o13'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower2.connect('o1', MMI_core.ports['o14'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC14.connect('o1', S_wg_output_lower2.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower2_clad.connect('o1', MMI_core.ports['o14'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower3.connect('o1', MMI_core.ports['o15'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC15.connect('o1', S_wg_output_lower3.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower3_clad.connect('o1', MMI_core.ports['o15'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_output_lower4.connect('o1', MMI_core.ports['o16'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC16.connect('o1', S_wg_output_lower4.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower4_clad.connect('o1', MMI_core.ports['o16'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC9.move([-10, 0])
    GC10.move([-10, 0])
    GC11.move([-10, 0])
    GC12.move([-10, 0])
    GC13.move([-10, 0])
    GC14.move([-10, 0])
    GC15.move([-10, 0])
    GC16.move([-10, 0])

    #Input MMI Core clad 설정
    MMI_core_clad_input_upper = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 7 * mmi_gap,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_lower = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 7 * mmi_gap,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    # MMI_core_clad_input_upper_middle = c << make_elements.make_taper(wg_width + 16, mmi_width + 16 - (mmi_gap) - 2*(mmi_gap) -(mmi_gap) ,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))
    # MMI_core_clad_input_lower_middle = c << make_elements.make_taper(wg_width + 16, mmi_width + 16 + (mmi_gap) + 2*(mmi_gap) +(mmi_gap)  ,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_middle = c << make_elements.make_taper(wg_width + 30, mmi_width + 16 ,
                                                               taper_length + mmi_length / 2,
                                                               layer=(layer[0], layer[1] + 1))


    # output MMI Core clad 설정
    MMI_core_clad_output_upper = c << make_elements.make_taper( mmi_width + 24 - 7 * mmi_gap,wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_output_lower = c << make_elements.make_taper(mmi_width + 24 - 7* mmi_gap,wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))

    MMI_core_clad_output_middle = c << make_elements.make_taper(mmi_width + 16 , wg_width + 30,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))


    #Input MMI core clad 연결
    MMI_core_clad_input_upper.connect('o1', S_wg_input_upper1_clad.ports['o2'], allow_layer_mismatch=True,
                                     allow_width_mismatch=True)
    MMI_core_clad_input_lower.connect('o1', S_wg_input_lower4_clad.ports['o2'], allow_layer_mismatch=True,
                                     allow_width_mismatch=True)
    MMI_core_clad_input_middle.connect('o1', MMI_core.ports['o17'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # Output MMI core clad 연결
    MMI_core_clad_output_upper.connect('o2', S_wg_output_upper1_clad.ports['o1'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_output_lower.connect('o2', S_wg_output_lower4_clad.ports['o1'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)

    MMI_core_clad_output_middle.connect('o1', MMI_core.ports['o18'], allow_layer_mismatch=True,
                                        allow_width_mismatch=True)

    c.flatten()

    return c

#GC늘린버전의 4X4 MMI
def make_4x4MMI_GC(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, period, fill_factor, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC4 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC1.mirror_x()
    GC2.mirror_x()
    GC3.mirror_x()
    GC4.mirror_x()

    # 첫번째 Input포트 넣기
    S_wg_input_upper1 = c << make_elements.make_path([ gf.path.straight(125),gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(300), gf.path.arc(radius=200, angle=90),gf.path.straight(200)],
                                                     layer=layer, width=wg_width)
    S_wg_input_upper1_clad = c << make_elements.make_path([ gf.path.straight(125),gf.path.arc(radius=200, angle=-90),
                                                           gf.path.straight(300), gf.path.arc(radius=200, angle=90),gf.path.straight(200)],
                                                          layer=(layer[0], layer[1] + 1), width=wg_width + 16)

    # 두번째 Input포트 넣기
    S_wg_input_upper2 = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(50), gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(225)], layer=layer, width=wg_width)
    S_wg_input_upper2_clad = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=-90),
                                                           gf.path.straight(50), gf.path.arc(radius=200, angle=90),
                                                           gf.path.straight(225)], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)

    # 세번째 Input포트 넣기
    S_wg_input_lower1 = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(50), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(225)], layer=layer, width=wg_width)
    S_wg_input_lower1_clad = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(50), gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(225)],  layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)

    # 네번째 Input포트 넣기
    S_wg_input_lower2 = c << make_elements.make_path([gf.path.straight(125),gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(300), gf.path.arc(radius=200, angle=-90), gf.path.straight(200)
                                                      ], layer=layer, width=wg_width)
    S_wg_input_lower2_clad = c << make_elements.make_path([gf.path.straight(125),gf.path.arc(radius=200, angle=90),
                                                           gf.path.straight(300), gf.path.arc(radius=200, angle=-90), gf.path.straight(200)
                                                           ], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)

    # MMI 설정
    MMI_core = c << make_4x4mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)
    # MMI_core_clad_input_upper = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))
    # MMI_core_clad_input_lower = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
    #                                                           taper_length + mmi_length / 2,
    #                                                           layer=(layer[0], layer[1] + 1))

    # 첫 번째 Input 포트 연결
    S_wg_input_upper1.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC1.connect('o1', S_wg_input_upper1_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])

    # 첫 번째 Input 포트 MMI에 연결
    MMI_core.connect('o1', S_wg_input_upper1.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # MMI_core_clad_input_upper.connect('o1', S_wg_input_upper1_clad.ports['o2'], allow_layer_mismatch=True,
    #                                   allow_width_mismatch=True)

    # 두 번째 Input 포트 연결 및 MMI에 연결
    S_wg_input_upper2.connect('o2', MMI_core.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg_input_upper2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper2_clad.connect('o2', MMI_core.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([10, 0])

    # 세 번째 Input 포트 연결 및 MMI에 연결
    S_wg_input_lower1.connect('o2', MMI_core.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC3.connect('o1', S_wg_input_lower1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower1_clad.connect('o2', MMI_core.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC3.move([10, 0])

    # 네 번째 Input 포트 연결 및 MMI에 연결, MMI_core_clad_input_lower 연결
    S_wg_input_lower2.connect('o2', MMI_core.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC4.connect('o1', S_wg_input_lower2.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower2_clad.connect('o2', MMI_core.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # MMI_core_clad_input_lower.connect('o1', S_wg_input_lower2_clad.ports['o2'], allow_layer_mismatch=True,
    #                                   allow_width_mismatch=True)
    GC4.move([10, 0])

    # output 설정
    GC5 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC6 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC7 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC8 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC5.mirror_x()
    GC6.mirror_x()
    GC7.mirror_x()
    GC8.mirror_x()

    # 첫번째 output 포트 넣기
    S_wg_output_upper1 = c << make_elements.make_path([ gf.path.straight(125), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(300), gf.path.arc(radius=200, angle=-90),gf.path.straight(200)],
                                                      layer=layer, width=wg_width)
    S_wg_output_upper1_clad = c << make_elements.make_path([gf.path.straight(125), gf.path.arc(radius=200, angle=90),
                                                            gf.path.straight(300), gf.path.arc(radius=200, angle=-90),gf.path.straight(200)],
                                                           layer=(layer[0], layer[1] + 1), width=wg_width + 16)

    # 두번째 output 포트 넣기
    S_wg_output_upper2 = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(50), gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(225)], layer=layer, width=wg_width)
    S_wg_output_upper2_clad = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=90),
                                                            gf.path.straight(50), gf.path.arc(radius=200, angle=-90),
                                                            gf.path.straight(225)], layer=(layer[0], layer[1] + 1),
                                                           width=wg_width + 16)

    # 세번째 output포트 넣기
    S_wg_output_lower1 = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(50), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(225)], layer=layer, width=wg_width)
    S_wg_output_lower1_clad = c << make_elements.make_path([gf.path.straight(100),gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(50), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(225)],layer=(layer[0], layer[1] + 1),
                                                           width=wg_width + 16)

    # 네번째 output 포트 넣기
    S_wg_output_lower2 = c << make_elements.make_path([gf.path.straight(125), gf.path.arc(radius=200, angle=-90),
                                                       gf.path.straight(300), gf.path.arc(radius=200, angle=90),
                                                       gf.path.straight(200)], layer=layer, width=wg_width)
    S_wg_output_lower2_clad = c << make_elements.make_path([gf.path.straight(125),gf.path.arc(radius=200, angle=-90),
                                                            gf.path.straight(300), gf.path.arc(radius=200, angle=90),
                                                            gf.path.straight(200)], layer=(layer[0], layer[1] + 1),
                                                           width=wg_width + 16)

    # # Output MMI clad 설정
    # MMI_core_clad_output_upper = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
    #                                                            taper_length + mmi_length / 2,
    #                                                            layer=(layer[0], layer[1] + 1))
    # MMI_core_clad_output_lower = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
    #                                                            taper_length + mmi_length / 2,
    #                                                            layer=(layer[0], layer[1] + 1))

    # MMI에 첫 번째 output 포트 연결 및 MMI에 연결
    S_wg_output_upper1.connect('o2', MMI_core.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper1_clad.connect('o2', MMI_core.ports['o5'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC5.connect('o1', S_wg_output_upper1_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC5.move([-10, 0])

    # MMI에 두 번째 output 포트 연결 및 MMI에 연결
    S_wg_output_upper2.connect('o2', MMI_core.ports['o6'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper2_clad.connect('o2', MMI_core.ports['o6'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC6.connect('o1', S_wg_output_upper2_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC6.move([-10, 0])

    # MMI에 세 번째 output 포트 연결 및 MMI에 연결
    S_wg_output_lower1.connect('o2', MMI_core.ports['o7'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower1_clad.connect('o2', MMI_core.ports['o7'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC7.connect('o1', S_wg_output_lower1_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC7.move([-10, 0])

    # MMI에 네 번째 output 포트 연결 및 MMI에 연결
    S_wg_output_lower2.connect('o2', MMI_core.ports['o8'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower2_clad.connect('o2', MMI_core.ports['o8'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC8.connect('o1', S_wg_output_lower2_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC8.move([-10, 0])


    # Input MMI clad 설정
    MMI_core_clad_input_upper = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_lower = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_middle = c << make_elements.make_taper(wg_width + 16, mmi_width + 24 - 3 * mmi_gap,
                                                               taper_length + mmi_length / 2,
                                                               layer=(layer[0], layer[1] + 1))

    # Output MMI clad 설정
    MMI_core_clad_output_upper = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
                                                               taper_length + mmi_length / 2,
                                                               layer=(layer[0], layer[1] + 1))
    MMI_core_clad_output_lower = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
                                                               taper_length + mmi_length / 2,
                                                               layer=(layer[0], layer[1] + 1))
    MMI_core_clad_output_middle = c << make_elements.make_taper(mmi_width + 24 - 3 * mmi_gap, wg_width + 16,
                                                                taper_length + mmi_length / 2,
                                                                layer=(layer[0], layer[1] + 1))

    # Input MMI core clad 연결
    MMI_core_clad_input_upper.connect('o1', S_wg_input_upper1_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_input_lower.connect('o1', S_wg_input_lower2_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_input_middle.connect('o2', MMI_core.ports['o9'], allow_layer_mismatch=True,
                                       allow_width_mismatch=True)

    # Output MMI core clad 연결
    MMI_core_clad_output_upper.connect('o2', S_wg_output_upper1_clad.ports['o2'], allow_layer_mismatch=True,
                                       allow_width_mismatch=True)
    MMI_core_clad_output_lower.connect('o2', S_wg_output_lower2_clad.ports['o2'], allow_layer_mismatch=True,
                                       allow_width_mismatch=True)
    MMI_core_clad_output_middle.connect('o1', MMI_core.ports['o10'], allow_layer_mismatch=True,
                                        allow_width_mismatch=True)

    c.flatten()

    return c


#GC늘린버전의 2X2 MMI
def make_2x2MMI_GC(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, period, fill_factor, layer):
    c = gf.Component()

    # input 설정
    GC1 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC1.mirror_x()
    GC2.mirror_x()

    S_wg_input_upper = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=200, angle=-90),
                                                     gf.path.straight(25), gf.path.arc(radius=200, angle=90)
                                                     ], layer=layer, width=wg_width)

    S_wg_input_upper_clad = c << make_elements.make_path([ gf.path.straight(100), gf.path.arc(radius=200, angle=-90),
                                                          gf.path.straight(25), gf.path.arc(radius=200, angle=90)
                                                          ], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)
    # Input_upper_clad = c << make_elements.make_taper(wg_width + 16, mmi_width + 16 - taper_width - mmi_gap, 100,
    #                                                  layer=(layer[0], layer[1] + 1))

    S_wg_input_lower = c << make_elements.make_path([ gf.path.arc(radius=200, angle=90),
                                                     gf.path.straight(25), gf.path.arc(radius=200, angle=-90),gf.path.straight(100)
                                                     ], layer=layer, width=wg_width)

    S_wg_input_lower_clad = c << make_elements.make_path([gf.path.straight(100), gf.path.arc(radius=200, angle=90),
                                                          gf.path.straight(25), gf.path.arc(radius=200, angle=-90)
                                                          ], layer=(layer[0], layer[1] + 1),
                                                         width=wg_width + 16)


    S_wg_input_upper.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_upper_clad.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # Input_upper_clad.connect('o1', S_wg_input_upper_clad['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1.move([10, 0])

    # MMI 설정
    MMI = c << make_2x2mmi_core(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, layer)

    MMI.connect('o1', S_wg_input_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    S_wg_input_lower.connect('o1', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_input_lower_clad.connect('o2', MMI.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', S_wg_input_lower.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC2.move([10, 0])

    # output 설정
    S_wg_output_upper = c << make_elements.make_path([ gf.path.arc(radius=200, angle=90),
                                                      gf.path.straight(25), gf.path.arc(radius=200, angle=-90),gf.path.straight(100)],
                                                     layer=layer, width=wg_width)

    S_wg_output_upper_clad = c << make_elements.make_path([gf.path.arc(radius=200, angle=90),
                                                           gf.path.straight(25), gf.path.arc(radius=200, angle=-90),gf.path.straight(100)
                                                           ], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)

    S_wg_output_lower = c << make_elements.make_path([gf.path.arc(radius=200, angle=-90),
                                                      gf.path.straight(25), gf.path.arc(radius=200, angle=90),gf.path.straight(100)
                                                      ], layer=layer, width=wg_width)

    S_wg_output_lower_clad = c << make_elements.make_path([gf.path.arc(radius=200, angle=-90),
                                                           gf.path.straight(25), gf.path.arc(radius=200, angle=90),gf.path.straight(100)
                                                           ], layer=(layer[0], layer[1] + 1),
                                                          width=wg_width + 16)

    S_wg_output_upper.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_upper_clad.connect('o1', MMI.ports['o3'], allow_layer_mismatch=True, allow_width_mismatch=True)


    S_wg_output_lower.connect('o1', MMI.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)
    S_wg_output_lower_clad.connect('o1', MMI.ports['o4'], allow_layer_mismatch=True, allow_width_mismatch=True)


    GC3 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)
    GC4 = c << make_elements.grating_coupler_elliptical_arc(wg_width, period, fill_factor)

    GC3.connect('o1', S_wg_output_upper.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC4.connect('o1', S_wg_output_lower.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC3.move([-10, 0])
    GC4.move([-10, 0])

    #Input MMI Core clad 설정
    MMI_core_clad_input_upper = c << make_elements.make_taper(wg_width + 16, mmi_width +16 -  mmi_gap -taper_width,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_input_lower = c << make_elements.make_taper( wg_width + 16,mmi_width +16 -  mmi_gap -taper_width,
                                                               taper_length + mmi_length / 2,
                                                               layer=(layer[0], layer[1] + 1))

    # Output MMI Core clad 설정
    MMI_core_clad_output_upper = c << make_elements.make_taper(mmi_width + 16 - mmi_gap - taper_width,wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))
    MMI_core_clad_output_lower = c << make_elements.make_taper(mmi_width + 16 - mmi_gap - taper_width, wg_width + 16,
                                                              taper_length + mmi_length / 2,
                                                              layer=(layer[0], layer[1] + 1))

    #MMI CORE CLAD 연결
    MMI_core_clad_input_upper.connect('o1', S_wg_input_upper_clad.ports['o2'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_input_lower.connect('o1', S_wg_input_lower_clad.ports['o2'], allow_layer_mismatch=True,
                                        allow_width_mismatch=True)
    MMI_core_clad_output_upper.connect('o2', S_wg_output_upper_clad.ports['o1'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)
    MMI_core_clad_output_lower.connect('o2', S_wg_output_lower_clad.ports['o1'], allow_layer_mismatch=True,
                                      allow_width_mismatch=True)



    c.flatten()

    return c















