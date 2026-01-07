from pathlib import Path
import os
import numpy as np
from make import make_MMI
import gdsfactory as gf
from gdsfactory.technology import LayerViews
from gdsfactory.config import PATH
from gdsfactory.path import straight, euler, arc
#from make import make_assembly
from make import make_elements

def make_2x2_MMI(layout):

    wg_width = 0.7
    taper_length = 20
    layer = (34, 0)

    mmi_width = [4.2, 6.2, 8.2]
    mmi_length_2x2_1 = [48, 49, 50, 51]
    mmi_length_2x2_2 = [110, 111, 112, 113]
    mmi_length_2x2_3 = [194, 195, 196, 197]
    mmi_gap = [0.8, 0.8, 1.6]
    taper_width = [1.6, 2.4, 2.8]


    # # 2x2MMI 배치
    # for x in range(len(mmi_width_2x2)):
    #     if x == 0:
    #         for y in range(len(mmi_length_2x2_1)):
    #             mmi_2x2 = layout << make_MMI.make_2x2MMI(wg_width, taper_width_2x2[x], taper_length, mmi_length_2x2_1[y], mmi_width_2x2[x], mmi_gap_2x2[x],period = 0.87, fill_factor=0.5, layer=(34, 0))
    #             mmi_2x2.move([-9062,-900])


    mmi_2x2 = layout << make_MMI.make_2x2MMI(wg_width=0.7, taper_width= 1.6, taper_length = 20, mmi_length = 48, mmi_width = 4.2, mmi_gap = 0.8, period = 0.87, fill_factor=0.5, layer=(34, 0))
    #mmi_2x2.move([-9062,-900])

def make_4x4_MMI(layout):
    # 변수
    # wg_width = 0.7
    # taper_width = 2.6
    # taper_length = 100
    # mmi_length = 545
    # mmi_width = 20
    # mmi_gap = 5
    # layer = (34, 0)
    #
    # mmi_4x4 = layout << make_MMI.make_4x4MMI(wg_width, taper_width, taper_length, mmi_length, mmi_width, mmi_gap, period=0.87, fill_factor=0.5, layer=(34, 0))

############################################################
    wg_width = 0.7
    taper_length_4x4 = 100
    mmi_width_4x4 = [16,18,20,22]
    mmi_length_4x4 = [535,540,545,550]
    # mmi_length_2x2_2 = [48, 49, 50, 51]
    # mmi_length_2x2_3 = [110, 111, 112, 113]
    # mmi_length_2x2_4 = [194, 195, 196, 197]
    mmi_gap_4x4 = [4,4.5,5,5.5]
    taper_width_4x4 = [1.8,2.2,2.6,3]
    layer = (34, 0)

   # 4x4MMI 초기 위치
   #  x_position_4x4mmi = -135
   #  y_position_4x4mmi = -932
   #
   #  # 4x4MMI 간격
   #  x_pitch_4x4mmi = 150
   #  y_pitch_4x4mmi = 0
   #
   #  # 4x4MMI 텍스트 초기 위치
   #  x_position_4x4mmi_text = 0
   #  y_position_4x4mmi_text = 0
   #
   #  # 4x4MMI 텍스트 간격
   #  y_pitch_4x4mmi_text = 0



    # 4x4MMI 배치
    for x in range(len(mmi_width_4x4)):
        if x == 0:
            mmi_4x4 = layout << make_MMI.make_4x4MMI(wg_width, taper_width_4x4[x], taper_length_4x4, mmi_length_4x4[x],
                                                            mmi_width_4x4[x], mmi_gap_4x4[x], period = 0.87, fill_factor=0.5,layer=(34,0))
            mmi_4x4.move([-9386, -932])
        # elif x == 1:
        #     mmi_4x4 = layout << make_MMI.make_4x4MMI(wg_width, taper_width_4x4[x], taper_length_4x4, mmi_length_4x4[x],
        #                                              mmi_width_4x4[x], mmi_gap_4x4[x], period=0.87, fill_factor=0.5,
        #                                              layer=(34, 0))
        #     mmi_4x4.move([-9386 + 1643, -932])
        # elif x == 2:
        #     mmi_4x4 = layout << make_MMI.make_4x4MMI(wg_width, taper_width_4x4[x], taper_length_4x4, mmi_length_4x4[x],
        #                                              mmi_width_4x4[x], mmi_gap_4x4[x], period=0.87, fill_factor=0.5,
        #                                              layer=(34, 0))
        #     mmi_4x4.move([-9386 + 1643 * 2, -932])
        # elif x == 3:
        #     mmi_4x4 = layout << make_MMI.make_4x4MMI(wg_width, taper_width_4x4[x], taper_length_4x4, mmi_length_4x4[x],
        #                                              mmi_width_4x4[x], mmi_gap_4x4[x], period=0.87, fill_factor=0.5,
        #                                              layer=(34, 0))
        #     mmi_4x4.move([-9386 + 1643 * 3, -932])

def make_8x8_MMI(layout):
    # 변수
    wg_width = 0.7
    layer = (34, 0)
    taper_length = 200

    taper_width_8x8 = [1.8, 2.2, 2.6, 3, 3.4, 3.8]
    mmi_length_8x8 = [646, 666, 686, 706,726, 746]
    mmi_width_8x8 = [26, 29, 32, 36, 39, 42]
    mmi_gap_8x8 = [3.2, 3.6, 4, 4.4, 4.8, 5.2]

    # mmi_8x8 = layout << make_MMI.make_8x8MMI(wg_width, taper_width_8x8, taper_length_8x8, mmi_length_8x8, mmi_width_8x8, mmi_gap_8x8,
    #                                             period=0.87, fill_factor=0.5, layer=(34, 0))

   # 8x8MMI 배치
    for x in range(len(mmi_width_8x8)):
        if x == 0:
            mmi_8x8 = layout << make_MMI.make_8x8MMI(wg_width, taper_width_8x8[x], taper_length, mmi_length_8x8[x],
                                                            mmi_width_8x8[x], mmi_gap_8x8[x], period = 0.87, fill_factor=0.5,layer=(34,0))
            mmi_8x8.move([-9379, -1958])
        # elif x == 1:
        #     mmi_8x8 = layout << make_MMI.make_8x8MMI(wg_width, taper_width_8x8[x], taper_length, mmi_length_8x8[x],
        #                                              mmi_width_8x8[x], mmi_gap_8x8[x], period=0.87, fill_factor=0.5,
        #                                              layer=(34, 0))
        #     mmi_8x8.move([-9386 + 2000, -1958])
        # elif x == 2:
        #     mmi_8x8 = layout << make_MMI.make_8x8MMI(wg_width, taper_width_8x8[x], taper_length, mmi_length_8x8[x],
        #                                              mmi_width_8x8[x], mmi_gap_8x8[x], period=0.87, fill_factor=0.5,
        #                                              layer=(34, 0))
        #     mmi_8x8.move([-9386 + 4000, -1958])
        # elif x == 3:
        #     mmi_8x8 = layout << make_MMI.make_8x8MMI(wg_width, taper_width_8x8[x], taper_length, mmi_length_8x8[x],
        #                                              mmi_width_8x8[x], mmi_gap_8x8[x], period=0.87, fill_factor=0.5,
        #                                              layer=(34, 0))
        #     mmi_8x8.move([-9390, -4000])
        #
        # elif x == 4:
        #     mmi_8x8 = layout << make_MMI.make_8x8MMI(wg_width, taper_width_8x8[x], taper_length, mmi_length_8x8[x],
        #                                              mmi_width_8x8[x], mmi_gap_8x8[x], period=0.87, fill_factor=0.5,
        #                                              layer=(34, 0))
        #     mmi_8x8.move([-9390 + 2050, -4000])
        #
        # elif x == 5:
        #     mmi_8x8 = layout << make_MMI.make_8x8MMI(wg_width, taper_width_8x8[x], taper_length, mmi_length_8x8[x],
        #                                              mmi_width_8x8[x], mmi_gap_8x8[x], period=0.87, fill_factor=0.5,
        #                                              layer=(34, 0))
        #     mmi_8x8.move([-9390 + 4120, -4000])


#GC 늘린 버전의 8x8 MMI
def make_8x8_GC_MMI(layout):
    # 변수
    #고정 파라미터
    wg_width = 0.9
    layer = (34, 0)
    taper_length = 200

    #조정 파라미터
    taper_width_8x8 = 3.9
    mmi_length_8x8 = 689
    mmi_width_8x8 = 32
    mmi_gap_8x8 = 4

    # 8x8MMI 배치
    mmi_8x8 = layout << make_MMI.make_8x8MMI_GC(wg_width, taper_width_8x8, taper_length, mmi_length_8x8,
                                             mmi_width_8x8, mmi_gap_8x8, period=0.87, fill_factor=0.5,
                                             layer=(34, 0))
    mmi_8x8.move([-9390+ 423-250 + 400 -300-100+350,-2000+1000+125-120-4000])

    T_mmi_gap_8x8 = layout << gf.components.text(text=f"MMI_Gap: {mmi_gap_8x8}", size=20,
                                                 justify="left", layer=(34, 0))
    T_mmi_gap_8x8.move(
        [7754+10-12166 +8-3524+204-5-1+ 400-300-100+350, -6745-419+16+8576 +16 -3019+15 -2190+15+2159+16-4000-453])

    T_mmi_width_8x8 = layout << gf.components.text(text=f"MMI_Width: {mmi_width_8x8}", size=20,
                                                   justify="left", layer=(34, 0))
    T_mmi_width_8x8.move([7739-12166+8-3524+204-1+ 400-300-100+350, -6785-419+16+8576+16-3019+15-2190+15+2159+16-4000-453])

    T_mmi_length_8x8 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_8x8}", size=20,
                                                    justify="left", layer=(34, 0))
    T_mmi_length_8x8.move(
        [7720-12166+8-3524+204+ 400-300-100+350, -6825-419+16+8576+16-3019+15-2190+15+2159+16-4000-453])

    T_taper_width_8x8 = layout << gf.components.text(text=f"Taper_Width: {taper_width_8x8}", size=20,
                                                     justify="left", layer=(34, 0))
    T_taper_width_8x8.move(
        [7720-12166+8-3524+204+4+ 400-300-100+350, -6865-419+16+8576+16-3019+15-2190+15+2159+16-4000-453])

    T_taper_length_8x8 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=20,
                                                      justify="left", layer=(34, 0))
    T_taper_length_8x8.move([7705-12166+8-3524+204+ 400-300-100+350, -6901-419+16+8576+16-3019+15-2190+15+2159+16-4000-453])

    Hanyang_University_8x8 = layout << gf.components.text(text=f"Hanyang", size=40,
                                                          justify="left", layer=(34, 0))
    Hanyang_University_8x8.move([7727-12166+8-3524+204+ 400-300-100+350, -6703-419+16+8576+16-3019+15-2190+15+2159+16-4000-453])


#GC 늘린 버전의 4x4 MMI
def make_4x4_GC_MMI(layout):
    # 고정 변수
    wg_width = 0.9
    layer = (34, 0)
    taper_length = 100

    # 조정 변수
    taper_width_4x4_1 = 4.6
    mmi_length_4x4_1 = [540, 541]
    mmi_width_4x4_1 = 20
    mmi_gap_4x4_1 = 5

    # 4x4MMI 배치
    for x in range(len(mmi_length_4x4_1)):
        if x == 0:                #왼쪽
            mmi_4x4 = layout << make_MMI.make_4x4MMI_GC(wg_width, taper_width_4x4_1, taper_length, mmi_length_4x4_1[x],
                                                     mmi_width_4x4_1, mmi_gap_4x4_1, period=0.87, fill_factor=0.5,
                                                     layer=(34, 0))
            mmi_4x4.mirror_y()
            mmi_4x4.move([8182+20+100+50-100-30-13587-35+173-3400-140-445+ 400-300-100+350,-6783-756-50 -1230 + 60-690+10104+70+45-490-9300-50-140])
            T_mmi_gap_4x4 = layout << gf.components.text(text=f"MMI_Gap: {mmi_gap_4x4_1}", size=20,
                                                         justify="left", layer=(34, 0))
            T_mmi_gap_4x4.move(
                [7754 + 10 - 12070 - 97-3336-445-2.5+ 400-300-100+350, -6745 + 16 + 8595-900+16-9155-140])

            T_mmi_width_4x4 = layout << gf.components.text(text=f"MMI_Width: {mmi_width_4x4_1}", size=20,
                                                           justify="left", layer=(34, 0))
            T_mmi_width_4x4.move([7739 - 12070 - 97-3336-445+ 400-300-100+350, -6785 + 16 + 8595-900+16-9155-140])

            T_mmi_length_4x4 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_4x4_1[x]}", size=18,
                                                            justify="left", layer=(34, 0))
            T_mmi_length_4x4.move(
                [7720 - 12070 - 97+5-3336-445 + 4+ 400-300-100+350, -6825 + 16 + 8595-900+16-9155-140])

            T_taper_width_4x4 = layout << gf.components.text(text=f"Taper_Width: {taper_width_4x4_1}", size=20,
                                                             justify="left", layer=(34, 0))
            T_taper_width_4x4.move(
                [7720 - 12070 - 97-3336-445+ 400-300-100+350, -6865 + 16 + 8595-900+16-9155-140])

            T_taper_length_4x4 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=20,
                                                              justify="left", layer=(34, 0))
            T_taper_length_4x4.move([7705 - 12070 - 97-3336-445+ 400-300-100+350, -6901 + 16 + 8595-900+16-9155-140])

            Hanyang_University_4x4 = layout << gf.components.text(text=f"Hanyang", size=40,
                                                                  justify="left", layer=(34, 0))
            Hanyang_University_4x4.move([7727 - 12070 - 97-3336-445+ 400-300-100+350, -6703 + 16 + 8595-900+16-9155-140])

        elif x == 1:                #오른쪽
            mmi_4x4 = layout << make_MMI.make_4x4MMI_GC(wg_width, taper_width_4x4_1, taper_length, mmi_length_4x4_1[x],
                                                     mmi_width_4x4_1, mmi_gap_4x4_1, period=0.87, fill_factor=0.5,
                                                     layer=(34, 0))
            mmi_4x4.mirror_y()
            mmi_4x4.move([8182+20+100+50-100-30-13587-35+173-3400-140-445+2575+300+ 400-300-100+350,-6783-756-50 -1230 + 60-690+10104+70+45-490-9300-50-140])
            T_mmi_gap_4x4 = layout << gf.components.text(text=f"MMI_Gap: {mmi_gap_4x4_1}", size=20,
                                                         justify="left", layer=(34, 0))
            T_mmi_gap_4x4.move(
                [7754 + 10 - 12070 - 97-3336-445+2575+300-5+ 400-300-100+350, -6745 + 16 + 8595-900+16-9155-140])

            T_mmi_width_4x4 = layout << gf.components.text(text=f"MMI_Width: {mmi_width_4x4_1}", size=20,
                                                           justify="left", layer=(34, 0))
            T_mmi_width_4x4.move([7739 - 12070 - 97-3336-445+2575+300+ 400-300-100+350, -6785 + 16 + 8595-900+16-9155-140])

            T_mmi_length_4x4 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_4x4_1[x]}", size=18,
                                                            justify="left", layer=(34, 0))
            T_mmi_length_4x4.move(
                [7720 - 12070 - 97+5-3336-445+2575+300+ 4+4+ 400-300-100+350, -6825 + 16 + 8595-900+16-9155-140])

            T_taper_width_4x4 = layout << gf.components.text(text=f"Taper_Width: {taper_width_4x4_1}", size=20,
                                                             justify="left", layer=(34, 0))
            T_taper_width_4x4.move(
                [7720 - 12070 - 97-3336-445+2575+300+ 400-300-100+350, -6865 + 16 + 8595-900+16-9155-140])

            T_taper_length_4x4 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=20,
                                                              justify="left", layer=(34, 0))
            T_taper_length_4x4.move([7705 - 12070 - 97-3336-445+2575+300+ 400-300-100+350, -6901 + 16 + 8595-900+16-9155-140])

            Hanyang_University_4x4 = layout << gf.components.text(text=f"Hanyang", size=40,
                                                                  justify="left", layer=(34, 0))
            Hanyang_University_4x4.move([7727 - 12070 - 97-3336-445+2575+300+ 400-300-100+350, -6703 + 16 + 8595-900+16-9155-140])



def make_2x2_GC_MMI(layout):

    wg_width = 0.9
    taper_length = 20
    layer = (34, 0)

    mmi_length_1 = [43,44]
    mmi_gap = 0.2 #(구한 GAP 길이에서 TAPER WIDTH 길이를 뺌)
    taper_width = 1.8
    mmi_width = 4


    #2 X 2 MMI 배치
    for x in range(len(mmi_length_1)):
        if x == 0:                          #맨 상단 왼쪽에서 첫 번째
            mmi_2x2 = layout << make_MMI.make_2x2MMI_GC(wg_width, taper_width, taper_length, mmi_length_1[x],
                                                            mmi_width, mmi_gap, period = 0.87, fill_factor=0.5,layer=(34,0))
            mmi_2x2.move([400+4925+250+974+20+100-70 +100 + 60 -100+2377-450+200-13 + 20 -15132+10+355+173-100-2340-280+450-119+ 400-300-100+350,  100-756-6783+150 -500+8146+100-30-50-490-5000-180+175])

            T_mmi_gap_2x2 = layout << gf.components.text(text=f"MMI_Gap: {round(mmi_gap + taper_width, 2)}", size=17,
                                                         justify="left", layer=(34, 0))
            T_mmi_gap_2x2.move(
                [7754 + 10 - 12070 - 97-1226+204-2340-280+450-119+ 400-300-100+350, -6745 + 16 + 8595-900+16-1163+16-23-225+10-5000-180+175])

            T_mmi_width_2x2 = layout << gf.components.text(text=f"MMI_Width: {mmi_width}", size=17,
                                                           justify="left", layer=(34, 0))
            T_mmi_width_2x2.move([7739 - 12070 - 97-1225+15+204-2340-280+450-119+10+ 400-300-100+350, -6785 + 16 + 8595-900+16-1163+16-13-225+10-5000-180+175])

            T_mmi_length_2x2 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_1[x]}", size=16,
                                                            justify="left", layer=(34, 0))
            T_mmi_length_2x2.move(
                [7720 - 12070 - 97+5-1225+5+23+204-2340-280+450-119+ 400-300-100+350, -6825 + 16 + 8595-900+16-1163+16-225+10-5000-180+175])

            T_taper_width_2x2 = layout << gf.components.text(text=f"Taper_Width: {taper_width}", size=17,
                                                             justify="left", layer=(34, 0))
            T_taper_width_2x2.move(
                [7720 - 12070 - 97-1225+30-6-2+204-2340-280+450-119+ 400-300-100+350, -6865 + 16 + 8595-900+16-1163+16+30-17-225+10-5000-180+175])

            T_taper_length_2x2 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=17,
                                                              justify="left", layer=(34, 0))
            T_taper_length_2x2.move([7705 - 12070 - 97-1225+25+204-2340-280+450-119+ 400-300-100+350, -6901 + 16 + 8595-900+16-1163+16+22-225+10-5000-180+175])

            Hanyang_University_2x2 = layout << gf.components.text(text=f"Hanyang", size=30,
                                                                  justify="left", layer=(34, 0))
            Hanyang_University_2x2.move([7727 - 12070 - 97-1225+52-26+204-2340-280+450-119+ 400-300-100+350, -6703 + 16 + 8595-900+16-1163+16-30-225+10-5000-180+175])

        elif x == 1:                          #맨 상단 왼쪽에서 두 번째
            mmi_2x2 = layout << make_MMI.make_2x2MMI_GC(wg_width, taper_width, taper_length, mmi_length_1[x],
                                                            mmi_width, mmi_gap, period = 0.87, fill_factor=0.5,layer=(34,0))
            mmi_2x2.move([400+4925+250+974+20+100-70 +100 + 60 -100+2377-450+200-13 + 20 -15132+10+355+173-100-2340-280+450-119+ 400-300-100+350,  100-756-6783+150 -500+8146+100-30-50-490-5000-180+175-222-1105])

            T_mmi_gap_2x2 = layout << gf.components.text(text=f"MMI_Gap: {round(mmi_gap + taper_width, 2)}", size=17,
                                                         justify="left", layer=(34, 0))
            T_mmi_gap_2x2.move(
                [7754 + 10 - 12070 - 97-1226+204-2340-280+450-119+ 400-300-100+350, -6745 + 16 + 8595-900+16-1163+16-23-225+10-5000-180+175-222-1105])

            T_mmi_width_2x2 = layout << gf.components.text(text=f"MMI_Width: {mmi_width}", size=17,
                                                           justify="left", layer=(34, 0))
            T_mmi_width_2x2.move([7739 - 12070 - 97-1225+15+204-2340-280+450-119+10+ 400-300-100+350, -6785 + 16 + 8595-900+16-1163+16-13-225+10-5000-180+175-222-1105])

            T_mmi_length_2x2 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_1[x]}", size=16,
                                                            justify="left", layer=(34, 0))
            T_mmi_length_2x2.move(
                [7720 - 12070 - 97+5-1225+5+23+204-2340-280+450-119+ 400-300-100+350, -6825 + 16 + 8595-900+16-1163+16-225+10-5000-180+175-222-1105])

            T_taper_width_2x2 = layout << gf.components.text(text=f"Taper_Width: {taper_width}", size=17,
                                                             justify="left", layer=(34, 0))
            T_taper_width_2x2.move(
                [7720 - 12070 - 97-1225+30-6-2+204-2340-280+450-119+ 400-300-100+350, -6865 + 16 + 8595-900+16-1163+16+30-17-225+10-5000-180+175-222-1105])

            T_taper_length_2x2 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=17,
                                                              justify="left", layer=(34, 0))
            T_taper_length_2x2.move([7705 - 12070 - 97-1225+25+204-2340-280+450-119+ 400-300-100+350, -6901 + 16 + 8595-900+16-1163+16+22-225+10-5000-180+175-222-1105])

            Hanyang_University_2x2 = layout << gf.components.text(text=f"Hanyang", size=30,
                                                                  justify="left", layer=(34, 0))
            Hanyang_University_2x2.move([7727 - 12070 - 97-1225+52-26+204-2340-280+450-119+ 400-300-100+350, -6703 + 16 + 8595-900+16-1163+16-30-225+10-5000-180+175-222-1105])

    wg_width = 0.9
    taper_length = 20
    layer = (34, 0)

    mmi_length_2 = [43, 44]
    mmi_gap = 0.1 #(구한 GAP 길이에서 TAPER WIDTH 길이를 뺌)
    taper_width = 1.9
    mmi_width = 4

    for x in range(len(mmi_length_2)):
        if x == 0:                           #맨 상단 오른쪽에서 두 번째                    #맨 상단 오른쪽에서 두 번째
            mmi_2x2 = layout << make_MMI.make_2x2MMI_GC(wg_width, taper_width, taper_length, mmi_length_2[x],
                                                        mmi_width, mmi_gap, period=0.87, fill_factor=0.5, layer=(34, 0))
            mmi_2x2.move([
                             400 + 4925 + 250 + 974 + 20 + 100 - 70 + 100 + 60 - 100 + 2377 - 450 + 200 - 13 + 20 - 15132 + 10 + 355 + 173 - 100 - 2340 - 280 + 450 - 119 - 443 -25+2817 + 57.5+702 -123-207.5+ 400-300-100+350,
                             100 - 756 - 6783 + 150 - 500 + 8146 + 100 - 30 - 50 - 490 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236])

            T_mmi_gap_2x2 = layout << gf.components.text(text=f"MMI_Gap: {round(mmi_gap + taper_width, 2)}", size=17,
                                                         justify="left", layer=(34, 0))
            T_mmi_gap_2x2.move(
                [7754 + 10 - 12070 - 97 - 1226 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                 -6745 + 16 + 8595 - 900 + 16 - 1163 + 16 - 23 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236])

            T_mmi_width_2x2 = layout << gf.components.text(text=f"MMI_Width: {mmi_width}", size=17,
                                                           justify="left", layer=(34, 0))
            T_mmi_width_2x2.move([7739 - 12070 - 97 - 1225 + 15 + 204 - 2340 - 280 + 450 - 119 - 443-25 +11.5+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                                  -6785 + 16 + 8595 - 900 + 16 - 1163 + 16 - 13 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236])

            T_mmi_length_2x2 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_2[x]}", size=16,
                                                            justify="left", layer=(34, 0))
            T_mmi_length_2x2.move(
                [7720 - 12070 - 97 + 5 - 1225 + 5 + 23 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                 -6825 + 16 + 8595 - 900 + 16 - 1163 + 16 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236])

            T_taper_width_2x2 = layout << gf.components.text(text=f"Taper_Width: {taper_width}", size=17,
                                                             justify="left", layer=(34, 0))
            T_taper_width_2x2.move(
                [7720 - 12070 - 97 - 1225 + 30 - 6 - 2 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                 -6865 + 16 + 8595 - 900 + 16 - 1163 + 16 + 30 - 17 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236])

            T_taper_length_2x2 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=17,
                                                              justify="left", layer=(34, 0))
            T_taper_length_2x2.move([7705 - 12070 - 97 - 1225 + 25 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                                     -6901 + 16 + 8595 - 900 + 16 - 1163 + 16 + 22 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236])

            Hanyang_University_2x2 = layout << gf.components.text(text=f"Hanyang", size=30,
                                                                  justify="left", layer=(34, 0))
            Hanyang_University_2x2.move([7727 - 12070 - 97 - 1225 + 52 - 26 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123 -207.5+ 400-300-100+350,
                                         -6703 + 16 + 8595 - 900 + 16 - 1163 + 16 - 30 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949 + 93 +236])

        elif x == 1:                          #맨 상단 오른쪽에서 첫 번째
            mmi_2x2 = layout << make_MMI.make_2x2MMI_GC(wg_width, taper_width, taper_length, mmi_length_2[x],
                                                        mmi_width, mmi_gap, period=0.87, fill_factor=0.5, layer=(34, 0))
            mmi_2x2.move([
                             400 + 4925 + 250 + 974 + 20 + 100 - 70 + 100 + 60 - 100 + 2377 - 450 + 200 - 13 + 20 - 15132 + 10 + 355 + 173 - 100 - 2340 - 280 + 450 - 119 - 443 -25+2817 + 57.5+702 -123-207.5+ 400-300-100+350,
                             100 - 756 - 6783 + 150 - 500 + 8146 + 100 - 30 - 50 - 490 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236+1205])

            T_mmi_gap_2x2 = layout << gf.components.text(text=f"MMI_Gap: {round(mmi_gap + taper_width, 2)}", size=17,
                                                         justify="left", layer=(34, 0))
            T_mmi_gap_2x2.move(
                [7754 + 10 - 12070 - 97 - 1226 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                 -6745 + 16 + 8595 - 900 + 16 - 1163 + 16 - 23 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236 +1205])

            T_mmi_width_2x2 = layout << gf.components.text(text=f"MMI_Width: {mmi_width}", size=17,
                                                           justify="left", layer=(34, 0))
            T_mmi_width_2x2.move([7739 - 12070 - 97 - 1225 + 15 + 204 - 2340 - 280 + 450 - 119 - 443-25 +11.5+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                                  -6785 + 16 + 8595 - 900 + 16 - 1163 + 16 - 13 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236+1205])

            T_mmi_length_2x2 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_2[x]}", size=16,
                                                            justify="left", layer=(34, 0))
            T_mmi_length_2x2.move(
                [7720 - 12070 - 97 + 5 - 1225 + 5 + 23 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                 -6825 + 16 + 8595 - 900 + 16 - 1163 + 16 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236+1205])

            T_taper_width_2x2 = layout << gf.components.text(text=f"Taper_Width: {taper_width}", size=17,
                                                             justify="left", layer=(34, 0))
            T_taper_width_2x2.move(
                [7720 - 12070 - 97 - 1225 + 30 - 6 - 2 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                 -6865 + 16 + 8595 - 900 + 16 - 1163 + 16 + 30 - 17 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236+1205])

            T_taper_length_2x2 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=17,
                                                              justify="left", layer=(34, 0))
            T_taper_length_2x2.move([7705 - 12070 - 97 - 1225 + 25 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123-207.5+ 400-300-100+350,
                                     -6901 + 16 + 8595 - 900 + 16 - 1163 + 16 + 22 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949+ 93+236+1205])

            Hanyang_University_2x2 = layout << gf.components.text(text=f"Hanyang", size=30,
                                                                  justify="left", layer=(34, 0))
            Hanyang_University_2x2.move([7727 - 12070 - 97 - 1225 + 52 - 26 + 204 - 2340 - 280 + 450 - 119 - 443-25+2817+ 57.5+702-123 -207.5+ 400-300-100+350,
                                         -6703 + 16 + 8595 - 900 + 16 - 1163 + 16 - 30 - 225 + 10 - 5000 - 180 + 175 - 222 - 1105 - 997-1263+1949 + 93 +236+1205])

