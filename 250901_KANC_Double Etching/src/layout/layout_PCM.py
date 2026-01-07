from pathlib import Path
import os
import numpy as np
from make import make_grating
from make import make_propagationloss
from make import make_bendingloss
from make import make_assembly
from make import make_elements
from make import make_linespace
from make import make_taper_for_poly
from make import make_MZIMMI
from make import make_MMI
import gdsfactory as gf
from gdsfactory.technology import LayerViews
from gdsfactory.config import PATH
from gdsfactory.path import straight, euler, arc

def PCM_Strip(layout):
    Full_etching_test_layer = (34,0)
    Shallow_etching_test_layer = (36, 0)

    # Etching Test - Full
    pattern_x = -7550
    pattern_y = 8900

    x_position_full_etching_text = -8350
    y_position_full_etching_text = 9580

    # Etching Test - 패턴 생성 및 이동
    pattern = layout << make_linespace.line_space_pattern(550, 100, 100, 6, Full_etching_test_layer)
    pattern.rotate(90)
    pattern.move([pattern_x, pattern_y])

    # Etching Test - 영역 생성 (Etching Test 패턴 기준)
    polygon_points = [
        (pattern_x - 1200, pattern_y - 100),  # 좌하단
        (pattern_x + 100, pattern_y - 100),  # 우하단
        (pattern_x + 100, pattern_y + 650),  # 우상단
        (pattern_x - 1200, pattern_y + 650),  # 좌상단
    ]
    layout.add_polygon(polygon_points, layer=(34, 1))

    T_full_etching_test = layout << gf.components.text(text="Full Etching Test", size=40, justify="left", layer=(34, 0))
    T_full_etching_test.move([x_position_full_etching_text, y_position_full_etching_text])

    # Etching Test - Shallow
    pattern_x = -6150
    pattern_y = 8900

    x_position_shallow_etching_text_clad = -6720
    y_position_shallow_etching_text_clad = 9610

    x_position_shallow_etching_text = -7000
    y_position_shallow_etching_text = 9580

    # Etching Test - 패턴 생성 및 이동
    pattern = layout << make_linespace.line_space_pattern(550, 100, 100, 6, Shallow_etching_test_layer)
    pattern.rotate(90)
    pattern.move([pattern_x, pattern_y])

    # Etching Test - 영역 생성 (Etching Test 패턴 기준)
    polygon_points = [
        (pattern_x - 1200, pattern_y - 100),  # 좌하단
        (pattern_x + 100, pattern_y - 100),  # 우하단
        (pattern_x + 100, pattern_y + 650),  # 우상단
        (pattern_x - 1200, pattern_y + 650),  # 좌상단
    ]
    layout.add_polygon(polygon_points, layer=(36, 1))

    # Shallow Etching Test 텍스트 영역
    polygon_points = [
        (x_position_shallow_etching_text_clad - 310, y_position_shallow_etching_text_clad - 44),  # 좌하단
        (x_position_shallow_etching_text_clad + 310, y_position_shallow_etching_text_clad - 44),  # 우하단
        (x_position_shallow_etching_text_clad + 310, y_position_shallow_etching_text_clad + 30),  # 우상단
        (x_position_shallow_etching_text_clad - 310, y_position_shallow_etching_text_clad + 30),  # 좌상단
    ]
    layout.add_polygon(polygon_points, layer=(36, 1))

    T_shallow_etching_test = layout << gf.components.text(text="Shallow Etching Test", size=40, justify="left", layer=(36, 0))
    T_shallow_etching_test.move([x_position_shallow_etching_text, y_position_shallow_etching_text])

    # Line space (Full)
    Line_width = [0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]
    Space_width = [0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]

    for i in range(0, len(Line_width)):
        if i <= 4:
            for j in range(0, len(Space_width)):
                pattern = layout << make_linespace.line_space_pattern(1500, Line_width[i], Space_width[j], 4, layer=(34, 0))
                pattern.move([-5850, 8800 + 6 * j + 75 * i])
        else:
            for j in range(0, len(Space_width)):
                pattern = layout << make_linespace.line_space_pattern(1500, Line_width[i], Space_width[j], 4, layer=(34, 0))
                pattern.move([-5850, 8800 + 420 + 6 * j + 75 * (i - 5)])

    for i in range(0, len(Line_width)):
        if i <= 4:
            T_MD_col = layout << gf.components.text(
                text="(Full) & (Line Width = %s) & (Space Width = 0.55, 0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.1, 0.05)" %
                     Line_width[i], size=10, justify="left", layer=(34, 0))
            T_MD_col.move([-5850, 8800 + 62 + 75 * i])
        else:
            T_MD_col = layout << gf.components.text(
                text="(Full) & (Line Width = %s) & (Space Width = 0.55, 0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.1, 0.05)" %
                     Line_width[i], size=10, justify="left", layer=(34, 0))
            T_MD_col.move([-5850, 8800 + 420 + 62 + 75 * (i - 5)])

    # Taper 형성 확인
    taper_only_width = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]

    for j in range(len(taper_only_width)):
        taper500 = layout << make_taper_for_poly.taper_only(500, taper_only_width[j])
        taper500.move([-2300, 9575 - 5 * j])
        taper500_text = layout << gf.components.text(text="500", size=20, justify="left", layer=(34, 0))
        taper500_text.move([-2300, 9595])

        taper1000_1 = layout << make_taper_for_poly.taper_only(1000, taper_only_width[j])
        taper1000_1.move([1700, 9575 - 5 * j])
        taper1000_1_text = layout << gf.components.text(text="1000", size=20, justify="left", layer=(34, 0))
        taper1000_1_text.move([1700, 9595])

        taper1000_2 = layout << make_taper_for_poly.taper_only(1000, taper_only_width[j])
        taper1000_2.move([200, 9575 - 5 * j])
        taper1000_2_text = layout << gf.components.text(text="1000", size=20, justify="left", layer=(34, 0))
        taper1000_2_text.move([200, 9595])

        taper1000_3 = layout << make_taper_for_poly.taper_only(1000, taper_only_width[j])
        taper1000_3.move([-1300, 9575 - 5 * j])
        taper1000_3_text = layout << gf.components.text(text="1000", size=20, justify="left", layer=(34, 0))
        taper1000_3_text.move([-1300, 9595])

        taper1500_1 = layout << make_taper_for_poly.taper_only(1500, taper_only_width[j])
        taper1500_1.move([1200, 9350 - 5 * j])
        taper1500_1_text = layout << gf.components.text(text="1500", size=20, justify="left", layer=(34, 0))
        taper1500_1_text.move([1200, 9370])

        taper1500_2 = layout << make_taper_for_poly.taper_only(1500, taper_only_width[j])
        taper1500_2.move([-550, 9350 - 5 * j])
        taper1500_2_text = layout << gf.components.text(text="1500", size=20, justify="left", layer=(34, 0))
        taper1500_2_text.move([-550, 9370])

        taper1500_3 = layout << make_taper_for_poly.taper_only(1500, taper_only_width[j])
        taper1500_3.move([-2300, 9350 - 5 * j])
        taper1500_3_text = layout << gf.components.text(text="1500", size=20, justify="left", layer=(34, 0))
        taper1500_3_text.move([-2300, 9370])

        taper2000 = layout << make_taper_for_poly.taper_only(2000, taper_only_width[j])
        taper2000.move([700, 9125 - 5 * j])
        taper2000_text = layout << gf.components.text(text="2000", size=20, justify="left", layer=(34, 0))
        taper2000_text.move([700, 9145])

        taper2500 = layout << make_taper_for_poly.taper_only(2500, taper_only_width[j])
        taper2500.move([-2300, 9125 - 5 * j])
        taper2500_text = layout << gf.components.text(text="2500", size=20, justify="left", layer=(34, 0))
        taper2500_text.move([-2300, 9145])

        taper5000 = layout << make_taper_for_poly.taper_only(5000, taper_only_width[j])
        taper5000.move([-2300, 8900 - 5 * j])
        taper5000_text = layout << gf.components.text(text="5000", size=20, justify="left", layer=(34, 0))
        taper5000_text.move([-2300, 8920])

    # Grating Coupler - Strip
    pitch = 0.87
    duty_cycle = 0.5
    fill_factor = 1 - duty_cycle
    width_strip = 0.9
    bend_radius = 200
    bend_length = 25

    x_gc_base = 2950
    y_gc = 9400

    for i in range(2):
        x_pos = x_gc_base + i * 1100

        gc = layout << make_grating.Bend_GC_arc(
            400, bend_length, bend_radius, (34, 0), width_strip,
            period=pitch, fill_factor=fill_factor
        )
        gc.move((x_pos, y_gc))

        txt_P = layout << gf.components.text(text=f"P = {pitch}", size=50, justify="left", layer=(34, 0))
        txt_P.move((x_pos - 50, y_gc - 140))

        txt_D = layout << gf.components.text(text=f"D = {duty_cycle}", size=50, justify="left", layer=(34, 0))
        txt_D.move((x_pos - 50, y_gc - 230))

        txt_W = layout << gf.components.text(text=f"W = {width_strip}", size=50, justify="left", layer=(34, 0))
        txt_W.move((x_pos - 50, y_gc - 320))

        txt_Uni = layout << gf.components.text(text="Hanyang", size=60, justify="left", layer=(34, 0))
        txt_Uni.move((x_pos + 450, y_gc - 120))

        txt_ASDL = layout << gf.components.text(text="ASDL", size=60, justify="left", layer=(34, 0))
        txt_ASDL.move((x_pos + 520, y_gc - 230))

        txt_WG = layout << gf.components.text(text="Strip-1310", size=60, justify="left", layer=(34, 0))
        txt_WG.move((x_pos + 420, y_gc - 330))

    # Grating Coupler - Version2
    pitch = 0.87
    duty_cycle = 0.5
    fill_factor = 1 - duty_cycle
    width_strip = 0.9
    bend_radius = 200
    bend_length = 25
    layer_strip = (34, 0)

    x_gc_base = 5100
    y_gc = 9400

    for i in range(2):
        x_pos = x_gc_base + i * 1100

        gc = layout << make_grating.Bend_GC_standard_arc(
            400, bend_length, bend_radius, layer_strip, width_strip,
            period=pitch, fill_factor=fill_factor
        )
        gc.move((x_pos, y_gc))

        txt_P = layout << gf.components.text(text=f"P = {pitch}", size=50, justify="left", layer=(34, 0))
        txt_P.move((x_pos - 10, y_gc - 140))

        txt_D = layout << gf.components.text(text=f"D = {duty_cycle}", size=50, justify="left", layer=(34, 0))
        txt_D.move((x_pos - 10, y_gc - 230))

        txt_W = layout << gf.components.text(text=f"W = {width_strip}", size=50, justify="left", layer=(34, 0))
        txt_W.move((x_pos - 10, y_gc - 320))

        txt_Uni = layout << gf.components.text(text="Hanyang", size=60, justify="left", layer=(34, 0))
        txt_Uni.move((x_pos + 480, y_gc - 100))

        txt_ASDL = layout << gf.components.text(text="ASDL", size=60, justify="left", layer=(34, 0))
        txt_ASDL.move((x_pos + 560, y_gc - 220))

        txt_WG = layout << gf.components.text(text="Version-2", size=60, justify="left", layer=(34, 0))
        txt_WG.move((x_pos + 450, y_gc - 340))

    # Bending Loss - Strip -0.9
    # Radius = 200 um & Number = 50
    snake = layout << make_bendingloss.make_snake_bend(135, 200, 50, (34, 0), 0.9, 0.87, 0.5)
    snake.move([-9520, 8600])
    txt1_In = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_In.move([-9520, 8600 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([-9520 - 30, 8600 - 240])
    txt3_In = layout << gf.components.text(text="N = 50", size=60, justify="left", layer=(34, 0))
    txt3_In.move([-9520 - 30, 8600 - 340])
    txt1_Out = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([900 + 30, 8600 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([900, 8600 - 240])
    txt3_Out = layout << gf.components.text(text="N = 50", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([900, 8600 - 340])

    # Radius = 200 um & Number = 40
    snake = layout << make_bendingloss.make_snake_bend(135, 200, 40, (34, 0), 0.9, 0.87, 0.5)
    snake.move([-9520, 8000])
    txt1_In = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_In.move([-9520, 8000 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([-9520 - 30, 8000 - 240])
    txt3_In = layout << gf.components.text(text="N = 40", size=60, justify="left", layer=(34, 0))
    txt3_In.move([-9520 - 30, 8000 - 340])
    txt1_Out = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([-1100 + 30, 8000 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([-1100, 8000 - 240])
    txt3_Out = layout << gf.components.text(text="N = 40", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([-1100, 8000 - 340])

    # Radius = 200 um & Number = 30
    snake = layout << make_bendingloss.make_snake_bend(135, 200, 30, (34, 0), 0.9, 0.87, 0.5)
    snake.move([1480, 8600])
    txt1_In = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_In.move([1480, 8600 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([1480 - 30, 8600 - 240])
    txt3_In = layout << gf.components.text(text="N = 30", size=60, justify="left", layer=(34, 0))
    txt3_In.move([1480 - 30, 8600 - 340])
    txt1_Out = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([7880 + 30, 8600 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([7880, 8600 - 240])
    txt3_Out = layout << gf.components.text(text="N = 30", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([7880, 8600 - 340])

    # Radius = 200 um & Number = 20
    snake = layout << make_bendingloss.make_snake_bend(135, 200, 20, (34, 0), 0.9, 0.87, 0.5)
    snake.move([190, 8000])
    txt1_In = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_In.move([190, 8000 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([190 - 30, 8000 - 240])
    txt3_In = layout << gf.components.text(text="N = 20", size=60, justify="left", layer=(34, 0))
    txt3_In.move([190 - 30, 8000 - 340])
    txt1_Out = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([4640 + 30, 8000 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([4640, 8000 - 240])
    txt3_Out = layout << gf.components.text(text="N = 20", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([4640, 8000 - 340])

    # Radius = 200 um & Number = 10
    snake = layout << make_bendingloss.make_snake_bend(135, 200, 10, (34, 0), 0.9, 0.87, 0.5)
    snake.move([5480, 8000])
    txt1_In = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_In.move([5480, 8000 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([5480 - 30, 8000 - 240])
    txt3_In = layout << gf.components.text(text="N = 10", size=60, justify="left", layer=(34, 0))
    txt3_In.move([5480 - 30, 8000 - 340])
    txt1_Out = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([7900 + 30, 8000 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([7900, 8000 - 240])
    txt3_Out = layout << gf.components.text(text="N = 10", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([7900, 8000 - 340])

    # Propagation Loss - Strip - 0.9
    rounds = [1, 4, 8, 12, 16, 20]
    lengths = [0.422, 0.847, 1.481, 2.191, 2.979, 3.843]

    # 공통 설정
    base_x = -10420
    base_y = 5600
    spacing_x = 1300
    spacing_y = -16
    text_base_x = -9000
    text_base_y = 5700
    text_spacing_x = 1350

    for i in range(len(rounds)):
        propa_loss = layout << make_propagationloss.make_simple_propagation(
            loops=rounds[i], bend_radius=200, core_width=0.9, rotate_up=True
        )
        propa_loss.move([base_x + spacing_x * (i + 1), base_y + spacing_y * i])

        text_x = text_base_x + text_spacing_x * i

        # X offset 조정 (긴 텍스트일수록 왼쪽으로 이동)
        x_adjustments = [-30, -30, -30, -50, -80, -80, -80]
        x_offset = x_adjustments[i]

        # 텍스트 생성
        txt_wg = layout << gf.components.text(text="Strip", size=60, justify="left", layer=(34, 0))
        txt_wg.move((text_x, text_base_y))

        txt_w = layout << gf.components.text(text="W=0.9", size=60, justify="left", layer=(34, 0))
        txt_w.move((text_x + x_offset, text_base_y - 100))

        txt_l = layout << gf.components.text(text=f"L={lengths[i]}", size=60, justify="left", layer=(34, 0))
        txt_l.move((text_x + x_offset, text_base_y - 200))

    # (1) 2 X 2 MMI 파라미터 설정
    wg_width = 0.9
    taper_length = 20
    layer = (34, 0)

    mmi_length_3 = 43
    mmi_gap = 0.4 #(구한 GAP 길이에서 TAPER WIDTH 길이를 뺌)
    taper_width = 1.6
    mmi_width = 4

    # (1) 2 X 2 MMI 배치 (왼쪽)
    mmi_2x2 = layout << make_MMI.make_2x2MMI_GC(wg_width, taper_width, taper_length, mmi_length_3,
                                                    mmi_width, mmi_gap, period = 0.87, fill_factor=0.5,layer=(34,0))
    mmi_2x2.move([400+4925+250+974+20+100-70 +100 + 60 -100+2377-450+200-13 + 20 -15132+10+355+173-100-2340-280+450-119+14889+77,  100-756-6783+150 -500+8146+100-30-50-490-5000-180+175-222-1105+12484-107.5])

    T_mmi_gap_2x2 = layout << gf.components.text(text=f"MMI_Gap: {round(mmi_gap + taper_width, 2)}", size=17,
                                                 justify="left", layer=(34, 0))
    T_mmi_gap_2x2.move(
        [7754 + 10 - 12070 - 97-1226+204-2340-280+450-119+14889+77, -6745 + 16 + 8595-900+16-1163+16-23-225+10-5000-180+175-222-1105+12484-107.5])

    T_mmi_width_2x2 = layout << gf.components.text(text=f"MMI_Width: {mmi_width}", size=17,
                                                   justify="left", layer=(34, 0))
    T_mmi_width_2x2.move([7739 - 12070 - 97-1225+15+204-2340-280+450-119+10+14889+77, -6785 + 16 + 8595-900+16-1163+16-13-225+10-5000-180+175-222-1105+12484-107.5])

    T_mmi_length_2x2 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_3}", size=16,
                                                    justify="left", layer=(34, 0))
    T_mmi_length_2x2.move(
        [7720 - 12070 - 97+5-1225+5+23+204-2340-280+450-119+14889+77, -6825 + 16 + 8595-900+16-1163+16-225+10-5000-180+175-222-1105+12484-107.5])

    T_taper_width_2x2 = layout << gf.components.text(text=f"Taper_Width: {taper_width}", size=17,
                                                     justify="left", layer=(34, 0))
    T_taper_width_2x2.move(
        [7720 - 12070 - 97-1225+30-6-2+204-2340-280+450-119+14889+77, -6865 + 16 + 8595-900+16-1163+16+30-17-225+10-5000-180+175-222-1105+12484-107.5])

    T_taper_length_2x2 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=17,
                                                      justify="left", layer=(34, 0))
    T_taper_length_2x2.move([7705 - 12070 - 97-1225+25+204-2340-280+450-119+14889+77, -6901 + 16 + 8595-900+16-1163+16+22-225+10-5000-180+175-222-1105+12484-107.5])

    Hanyang_University_2x2 = layout << gf.components.text(text=f"Hanyang", size=30,
                                                          justify="left", layer=(34, 0))
    Hanyang_University_2x2.move([7727 - 12070 - 97-1225+52-26+204-2340-280+450-119+14889+77, -6703 + 16 + 8595-900+16-1163+16-30-225+10-5000-180+175-222-1105+12484 -107.5])

    # (2) 2 X 2 MMI 파라미터 설정
    wg_width = 0.9
    taper_length = 20
    layer = (34, 0)

    mmi_length_4 = 45
    mmi_gap = 0.1 #(구한 GAP 길이에서 TAPER WIDTH 길이를 뺌)
    taper_width = 1.9
    mmi_width = 4

    # (2) 2 X 2 MMI 배치 (오른쪽)
    mmi_2x2 = layout << make_MMI.make_2x2MMI_GC(wg_width, taper_width, taper_length, mmi_length_4,
                                                    mmi_width, mmi_gap, period = 0.87, fill_factor=0.5,layer=(34,0))
    mmi_2x2.move([400+4925+250+974+20+100-70 +100 + 60 -100+2377-450+200-13 + 20 -15132+10+355+173-100-2340-280+450-119+14889+77+1517,  100-756-6783+150 -500+8146+100-30-50-490-5000-180+175-222-1105+12484-107.5])

    T_mmi_gap_2x2 = layout << gf.components.text(text=f"MMI_Gap: {round(mmi_gap + taper_width, 2)}", size=17,
                                                 justify="left", layer=(34, 0))
    T_mmi_gap_2x2.move(
        [7754 + 10 - 12070 - 97-1226+204-2340-280+450-119+14889+77+1517, -6745 + 16 + 8595-900+16-1163+16-23-225+10-5000-180+175-222-1105+12484-107.5])

    T_mmi_width_2x2 = layout << gf.components.text(text=f"MMI_Width: {mmi_width}", size=17,
                                                   justify="left", layer=(34, 0))
    T_mmi_width_2x2.move([7739 - 12070 - 97-1225+15+204-2340-280+450-119+10+14889+77+1517, -6785 + 16 + 8595-900+16-1163+16-13-225+10-5000-180+175-222-1105+12484-107.5])

    T_mmi_length_2x2 = layout << gf.components.text(text=f"MMI_Length: {mmi_length_4}", size=16,
                                                    justify="left", layer=(34, 0))
    T_mmi_length_2x2.move(
        [7720 - 12070 - 97+5-1225+5+23+204-2340-280+450-119+14889+77+1517, -6825 + 16 + 8595-900+16-1163+16-225+10-5000-180+175-222-1105+12484-107.5])

    T_taper_width_2x2 = layout << gf.components.text(text=f"Taper_Width: {taper_width}", size=17,
                                                     justify="left", layer=(34, 0))
    T_taper_width_2x2.move(
        [7720 - 12070 - 97-1225+30-6-2+204-2340-280+450-119+14889+77+1517, -6865 + 16 + 8595-900+16-1163+16+30-17-225+10-5000-180+175-222-1105+12484-107.5])

    T_taper_length_2x2 = layout << gf.components.text(text=f"Taper_Length: {taper_length}", size=17,
                                                      justify="left", layer=(34, 0))
    T_taper_length_2x2.move([7705 - 12070 - 97-1225+25+204-2340-280+450-119+14889+77+1517, -6901 + 16 + 8595-900+16-1163+16+22-225+10-5000-180+175-222-1105+12484-107.5])

    Hanyang_University_2x2 = layout << gf.components.text(text=f"Hanyang", size=30,
                                                          justify="left", layer=(34, 0))
    Hanyang_University_2x2.move([7727 - 12070 - 97-1225+52-26+204-2340-280+450-119+14889+77+1517, -6703 + 16 + 8595-900+16-1163+16-30-225+10-5000-180+175-222-1105+12484 -107.5])


def PCM_Rib(layout):
    layer_rib_full = (34,4)
    # Line space (Shallow)
    Line_width = [0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]
    Space_width = [0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]

    origin_x = -4100
    origin_y = 8800

    for i in range(len(Line_width)):
        for j in range(len(Space_width)):
            if i <= 4:
                y_shift = origin_y + 6 * j + 75 * i
            else:
                y_shift = origin_y + 420 + 6 * j + 75 * (i - 5)
            pattern = layout << make_linespace.line_space_pattern(
                1500, Line_width[i], Space_width[j], 4, layer=(36, 0)
            )
            pattern.move([origin_x, y_shift])

    for i in range(len(Line_width)):
        if i <= 4:
            y_shift = origin_y + 62 + 75 * i
        else:
            y_shift = origin_y + 420 + 62 + 75 * (i - 5)
        T_MD_col = layout << gf.components.text(
            text="(Shallow) & (Line Width = %s) & (Space Width = 0.55, 0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.1, 0.05)"
                 % Line_width[i], size=10, justify="left", layer=(36, 0))
        T_MD_col.move([origin_x, y_shift])

    box_x = origin_x - 75
    box_y = origin_y - 50
    box_w = 1600 + 50
    box_h = 800 + 100

    clad_box = gf.components.rectangle(size=(box_w, box_h), layer=(36, 1))
    ref = layout << clad_box
    ref.move([box_x, box_y])

    # Grating Coupler - Rib GC
    pitch = 0.87
    width_rib = 0.9
    bend_radius = 200
    bend_length = 25
    # layer_rib_full = (34, 0)
    layer_rib_shallow = (36, 0)

    x_gc_base = 7350

    duty_configs = [{"duty": 0.5, "y_gc": 9400}]

    for config in duty_configs:
        duty_cycle = config["duty"]
        fill_factor = 1 - duty_cycle
        y_gc = config["y_gc"]

        for i in range(2):
            x_pos = x_gc_base + i * 1100

            # Full Etch
            gc_full = layout << make_grating.Full_Bend_GC_arc(
                400, bend_length, bend_radius, layer_rib_full, width=width_rib,
                period=pitch, fill_factor=fill_factor
            )
            gc_full.move((x_pos, y_gc))

            # Shallow Etch
            gc_shallow = layout << make_grating.Shallow_Bend_GC_arc(
                400, bend_length, bend_radius, layer_rib_shallow, width=width_rib,
                period=pitch, fill_factor=fill_factor
            )
            gc_shallow.move((x_pos, y_gc))

            txt_P = layout << gf.components.text(text=f"P = {pitch}", size=50, justify="left", layer=(34, 0))
            txt_P.move((x_pos - 50, y_gc - 140))
            txt_D = layout << gf.components.text(text=f"D = {duty_cycle}", size=50, justify="left", layer=(34, 0))
            txt_D.move((x_pos - 50, y_gc - 230))
            txt_W = layout << gf.components.text(text=f"W = {width_rib}", size=50, justify="left", layer=(34, 0))
            txt_W.move((x_pos - 50, y_gc - 320))
            txt_Uni = layout << gf.components.text(text="Hanyang", size=60, justify="left", layer=(34, 0))
            txt_Uni.move((x_pos + 450, y_gc - 120))
            txt4 = layout << gf.components.text(text="ASDL", size=60, justify="left", layer=(34, 0))
            txt4.move((x_pos + 520, y_gc - 230))
            txt3 = layout << gf.components.text(text="Rib-1310", size=60, justify="left", layer=(34, 0))
            txt3.move((x_pos + 440, y_gc - 330))


    # Bending Loss - Rib - 0.9 um
    # Radius = 200 um & Number = 50
    snake = layout << make_bendingloss.make_full_snake_bend(135, 200, 50, layer_rib_full, 0.9, 0.87, 0.5)
    snake.move([-9520, 7400])
    snake = layout << make_bendingloss.make_shallow_snake_bend(135, 200, 50, (36, 0), 0.9, 0.87, 0.5)
    snake.move([-9520, 7400])
    txt1_In = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_In.move([-9520 + 80, 7400 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([-9520 - 30, 7400 - 240])
    txt3_In = layout << gf.components.text(text="N = 50", size=60, justify="left", layer=(34, 0))
    txt3_In.move([-9520 - 30, 7400 - 340])
    txt1_Out = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([900 + 80, 7400 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([900, 7400 - 240])
    txt3_Out = layout << gf.components.text(text="N = 50", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([900, 7400 - 340])

    # Radius = 200 um & Number = 40
    snake = layout << make_bendingloss.make_full_snake_bend(135, 200, 40, layer_rib_full, 0.9, 0.87, 0.5)
    snake.move([-9520, 6800])
    snake = layout << make_bendingloss.make_shallow_snake_bend(135, 200, 40, (36, 0), 0.9, 0.87, 0.5)
    snake.move([-9520, 6800])
    txt1_In = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_In.move([-9520 + 50, 6800 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([-9520 - 30, 6800 - 240])
    txt3_In = layout << gf.components.text(text="N = 40", size=60, justify="left", layer=(34, 0))
    txt3_In.move([-9520 - 30, 6800 - 340])
    txt1_Out = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([-1100 + 80, 6800 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([-1100, 6800 - 240])
    txt3_Out = layout << gf.components.text(text="N = 40", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([-1100, 6800 - 340])

    # Radius = 200 um & Number = 30
    snake = layout << make_bendingloss.make_full_snake_bend(135, 200, 30, layer_rib_full, 0.9, 0.87, 0.5)
    snake.move([1480, 7400])
    snake = layout << make_bendingloss.make_shallow_snake_bend(135, 200, 30, (36, 0), 0.9, 0.87, 0.5)
    snake.move([1480, 7400])
    txt1_In = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_In.move([1480 + 50, 7400 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([1480 - 30, 7400 - 240])
    txt3_In = layout << gf.components.text(text="N = 30", size=60, justify="left", layer=(34, 0))
    txt3_In.move([1480 - 30, 7400 - 340])
    txt1_Out = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([7880 + 80, 7400 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([7880, 7400 - 240])
    txt3_Out = layout << gf.components.text(text="N = 30", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([7880, 7400 - 340])

    # Radius = 200 um & Number = 20
    snake = layout << make_bendingloss.make_full_snake_bend(135, 200, 20, layer_rib_full, 0.9, 0.87, 0.5)
    snake.move([190, 6800])
    snake = layout << make_bendingloss.make_shallow_snake_bend(135, 200, 20, (36, 0), 0.9, 0.87, 0.5)
    snake.move([190, 6800])
    txt1_In = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_In.move([190 + 50, 6800 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([190 - 30, 6800 - 240])
    txt3_In = layout << gf.components.text(text="N = 20", size=60, justify="left", layer=(34, 0))
    txt3_In.move([190 - 30, 6800 - 340])
    txt1_Out = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([4640 + 80, 6800 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([4640, 6800 - 240])
    txt3_Out = layout << gf.components.text(text="N = 20", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([4640, 6800 - 340])

    # Radius = 200 um & Number = 10
    snake = layout << make_bendingloss.make_full_snake_bend(135, 200, 10, layer_rib_full, 0.9, 0.87, 0.5)
    snake.move([5480, 6800])
    snake = layout << make_bendingloss.make_shallow_snake_bend(135, 200, 10, (36, 0), 0.9, 0.87, 0.5)
    snake.move([5480, 6800])
    txt1_In = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_In.move([5480 + 50, 6800 - 140])
    txt2_In = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_In.move([5480 - 30, 6800 - 240])
    txt3_In = layout << gf.components.text(text="N = 10", size=60, justify="left", layer=(34, 0))
    txt3_In.move([5480 - 30, 6800 - 340])
    txt1_Out = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
    txt1_Out.move([7900 + 80, 6800 - 140])
    txt2_Out = layout << gf.components.text(text="R = 200", size=60, justify="left", layer=(34, 0))
    txt2_Out.move([7900, 6800 - 240])
    txt3_Out = layout << gf.components.text(text="N = 10", size=60, justify="left", layer=(34, 0))
    txt3_Out.move([7900, 6800 - 340])

    # Propagation Loss - Rib - 0.9
    rounds = [1, 4, 8, 12, 16, 20]
    lengths = [0.422, 0.847, 1.481, 2.191, 2.979, 3.843]

    # 공통 설정
    base_x = -2110
    base_y = 5600
    spacing_x = 1300
    spacing_y = -16
    text_base_x = -690
    text_base_y = 5700
    text_spacing_x = 1350

    # Rib 텍스트별 X offset
    rib_wg_offsets = [50, 50, 50, 20, 10, 10]
    rib_w_offsets = [10, 0, -20, -40, -60, -60]
    rib_l_offsets = [-30, -50, -30, -80, -110, -110]

    for i in range(len(rounds)):
        # Rib Full Propagation loss 소자 생성
        propa_loss_full = layout << make_propagationloss.make_simple_propagation_full(
            loops=rounds[i], bend_radius=200, core_width=0.9, rotate_up=True
        )
        propa_loss_full.move([base_x + spacing_x * (i + 1), base_y + spacing_y * i])

        # Rib Shallow Propagation loss 소자 생성 (같은 위치)
        propa_loss_shallow = layout << make_propagationloss.make_simple_propagation_shallow(
            loops=rounds[i], bend_radius=200, core_width=0.9, rotate_up=True
        )
        propa_loss_shallow.move([base_x + spacing_x * (i + 1), base_y + spacing_y * i])

        # 텍스트 위치 계산
        text_x = text_base_x + text_spacing_x * i

        # Rib 텍스트 생성
        txt_wg = layout << gf.components.text(text="Rib", size=60, justify="left", layer=(34, 0))
        txt_wg.move((text_x + rib_wg_offsets[i], text_base_y))

        txt_w = layout << gf.components.text(text="W=0.9", size=60, justify="left", layer=(34, 0))
        txt_w.move((text_x + rib_w_offsets[i], text_base_y - 100))

        txt_l = layout << gf.components.text(text=f"L={lengths[i]}", size=60, justify="left", layer=(34, 0))
        txt_l.move((text_x + rib_l_offsets[i], text_base_y - 200))