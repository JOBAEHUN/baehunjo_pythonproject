from make import make_adiabatic_coupler, make_elements
import gdsfactory as gf

def adiabatic_coupler(layout):
    # 에바네센트 커플러 DOE
    bottom_chip_pitch = 247 - 4 - 35
    top_chip_pitch = 247.5 - 4 - 35
    strip_input_length1 = 100
    strip_input_length2 = 1000 - 0.253
    strip_output_length = 1100
    width = 0.9
    adhesive_tip = [0.6]
    metal_tip = [0.7]
    edge_slab_length = 530 + 120 - 300
    layer = (34,0)
    adhesive_taper_length = [50, 200, 500, 1000, 1500, 2000]
    metal_taper_length = [500, 1000, 2000]
    adhesive_slab_length = [4200 - 2 * length for length in adhesive_taper_length]
    metal_slab_length = [4200 - 2 * length for length in metal_taper_length]

    # top chip, bottom chip 초기 위치
    x_position_bottom = 1540 + 30 + 0.261 - 300 - strip_input_length2 + 600 - 3150 - 0.057 - 200
    y_position_bottom = -1500 + 1200 - 100 + 12500 - 2400 - 10000 - 1400
    metal_y_position_bottom = -1500 + 1200 - 100 + 12500 - 2400 - 10000 -1400 + 6300 - 500

    x_position_top = 7870 - edge_slab_length - 150 - 620 - 500 + 300 - 3150 + 1050
    y_position_top = -1725 + 1200 - 100 + 12500 - 2400 -200 - 10000 - 1400
    metal_y_position_top = -1725 + 1200 - 100 + 12500 - 2400 - 200 - 10000 -1400 + 6300 - 500

    # 텍스트 초기 위치
    x_position_Tip_text = 1540 + 30 + 0.261 - 300 - strip_input_length2 - 65 + 600 - 3150 - 200
    y_position_Tip_text = -1570 + 1200 - 120 + 12500 - 2400 - 10000 - 1400
    metal_y_position_Tip_text = -1570 + 1200 - 120 + 12500 - 2400 - 10000 -1400 + 6300 - 500

    x_position_Ltaper_text = 1540 + 30 + 0.261 - 300 - strip_input_length2 - 65 + 600 - 3150 - 200
    y_position_Ltaper_text = -1610 + 1200 - 102 + 12500 - 2400 - 10000 - 1400
    metal_y_position_Ltaper_text = -1610 + 1200 - 102 + 12500 - 2400 - 10000 -1400 + 6300 - 500

    x_position_Misalignment_text = 1540 + 30 + 0.261 - 300 - strip_input_length2 - 65 + 600 - 3150 - 200
    y_position_Misalignment_text = -1650 + 1200 - 83 + 12500 - 2400 - 10000 - 1400
    metal_y_position_Misalignment_text = -1650 + 1200 - 83 + 12500 - 2400 - 10000 -1400 + 6300 - 500

    # topchip, bottomchip 배치
    for x in range(len(adhesive_slab_length)):
        bottom_coupler = layout << make_adiabatic_coupler.make_ref_bottom_coupler(strip_input_length1, strip_input_length2,
                                                                              adhesive_slab_length[x], strip_output_length,
                                                                              adhesive_taper_length[x], width, layer)

        bottom_coupler.move([x_position_bottom, y_position_bottom - bottom_chip_pitch * 6 * x])

        T_ref = layout << gf.components.text(text="Ref", size=60, justify="left", layer=(34, 0))
        T_ref.move([x_position_Tip_text + 50, y_position_Tip_text - bottom_chip_pitch * 6 * x - 30])

        top_coupler = layout << make_adiabatic_coupler.make_ref_top_coupler(edge_slab_length, adhesive_slab_length[x],
                                                                        adhesive_taper_length[x], width, layer)

        top_coupler.move([x_position_top, y_position_top - bottom_chip_pitch * 6 * x])

        for y in range(0,5):
            bottom_coupler = layout << make_adiabatic_coupler.make_bottom_coupler(strip_input_length1, strip_input_length2, adhesive_slab_length[x], strip_output_length, adhesive_taper_length[x], width, adhesive_tip[0], layer)

            bottom_coupler.move([x_position_bottom, y_position_bottom - bottom_chip_pitch  * y - bottom_chip_pitch * 6 * x - bottom_chip_pitch])

            top_coupler = layout << make_adiabatic_coupler.make_top_coupler(edge_slab_length, adhesive_slab_length[x], adhesive_taper_length[x], width, adhesive_tip[0], layer)

            top_coupler.move([x_position_top, y_position_top - top_chip_pitch * y - bottom_chip_pitch * 6 * x - bottom_chip_pitch])

            T_adiabatic_coupler = layout << gf.components.text(text=f"Tip: {adhesive_tip[0]}", size=15,
                                                               justify="left", layer=(34, 0))
            T_adiabatic_coupler.move(
                [x_position_Tip_text, y_position_Tip_text - bottom_chip_pitch * y - bottom_chip_pitch * 6 * x - bottom_chip_pitch])

            T_adiabatic_coupler = layout << gf.components.text(text=f"Ltaper: {adhesive_taper_length[x]}", size=15, justify="left", layer=(34, 0))
            T_adiabatic_coupler.move([x_position_Ltaper_text, y_position_Ltaper_text - bottom_chip_pitch  * y - bottom_chip_pitch * 6 * x - bottom_chip_pitch])

            T_adiabatic_coupler = layout << gf.components.text(text=f"Misalignment: {0.5 * y}", size=15,
                                                               justify="left", layer=(34, 0))
            T_adiabatic_coupler.move(
                [x_position_Misalignment_text, y_position_Misalignment_text - bottom_chip_pitch * y - bottom_chip_pitch * 6 * x - bottom_chip_pitch])

    for x in range(len(metal_taper_length)):
        bottom_coupler = layout << make_adiabatic_coupler.make_ref_bottom_coupler(strip_input_length1, strip_input_length2,
                                                                              adhesive_slab_length[x], strip_output_length,
                                                                              adhesive_taper_length[x], width, layer)

        bottom_coupler.move([x_position_bottom, metal_y_position_bottom - bottom_chip_pitch * 4 * x])

        T_ref = layout << gf.components.text(text="Ref", size=60, justify="left", layer=(34, 0))
        T_ref.move([x_position_Tip_text + 50, metal_y_position_Tip_text - bottom_chip_pitch * 4 * x - 30])

        top_coupler = layout << make_adiabatic_coupler.make_ref_top_coupler(edge_slab_length, adhesive_slab_length[x],
                                                                        adhesive_taper_length[x], width, layer)

        top_coupler.move([x_position_top, metal_y_position_top - bottom_chip_pitch * 4 * x])

        for y in range(0,3):
            bottom_coupler = layout << make_adiabatic_coupler.make_bottom_coupler(strip_input_length1, strip_input_length2, metal_slab_length[x], strip_output_length, metal_taper_length[x], width, metal_tip[0], layer)

            bottom_coupler.move([x_position_bottom, metal_y_position_bottom - bottom_chip_pitch  * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch])

            top_coupler = layout << make_adiabatic_coupler.make_top_coupler(edge_slab_length, metal_slab_length[x], metal_taper_length[x], width, metal_tip[0], layer)

            top_coupler.move([x_position_top, metal_y_position_top - top_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch])

            T_adiabatic_coupler = layout << gf.components.text(text=f"Tip: {metal_tip[0]}", size=15,
                                                               justify="left", layer=(34, 0))
            T_adiabatic_coupler.move(
                [x_position_Tip_text, metal_y_position_Tip_text - bottom_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch])

            T_adiabatic_coupler = layout << gf.components.text(text=f"Ltaper: {metal_taper_length[x]}", size=15,
                                                               justify="left", layer=(34, 0))
            T_adiabatic_coupler.move(
                [x_position_Ltaper_text, metal_y_position_Ltaper_text - bottom_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch])

            T_adiabatic_coupler = layout << gf.components.text(text=f"Misalignment: {0.5 * y}", size=15,
                                                               justify="left", layer=(34, 0))
            T_adiabatic_coupler.move(
                [x_position_Misalignment_text,
                 metal_y_position_Misalignment_text - bottom_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch])

            # bottom_coupler = layout << make_adiabatic_coupler.make_bottom_coupler(strip_input_length1,
            #                                                                       strip_input_length2,
            #                                                                       metal_slab_length[1],
            #                                                                       strip_output_length,
            #                                                                       metal_taper_length[1], width,
            #                                                                       metal_tip[0], layer)
            #
            # bottom_coupler.move([x_position_bottom,
            #                      y_position_bottom - bottom_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch * 40])
            #
            # top_coupler = layout << make_adiabatic_coupler.make_top_coupler(edge_slab_length, metal_slab_length[1],
            #                                                                 metal_taper_length[1], width, metal_tip[0],
            #                                                                 layer)
            #
            # top_coupler.move([x_position_top,
            #                   y_position_top - top_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch * 40])
            #
            # T_adiabatic_coupler = layout << gf.components.text(text=f"Tip: {metal_tip[0]}", size=15,
            #                                                    justify="left", layer=(34, 0))
            # T_adiabatic_coupler.move(
            #     [x_position_Tip_text,
            #      y_position_Tip_text - bottom_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch * 40])
            #
            # T_adiabatic_coupler = layout << gf.components.text(text=f"Ltaper: {metal_taper_length[1]}", size=15,
            #                                                    justify="left", layer=(34, 0))
            # T_adiabatic_coupler.move(
            #     [x_position_Ltaper_text,
            #      y_position_Ltaper_text - bottom_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch * 40])
            #
            # T_adiabatic_coupler = layout << gf.components.text(text=f"Misalignment: {0.5 * y}", size=15,
            #                                                    justify="left", layer=(34, 0))
            # T_adiabatic_coupler.move(
            #     [x_position_Misalignment_text,
            #      y_position_Misalignment_text - bottom_chip_pitch * y - bottom_chip_pitch * 4 * x - bottom_chip_pitch * 40])

    # Metal 본딩 얼라인 키
    # SiN 풀에칭 영역 - 주변 타일링 제거
    # 가로480, 세로120
    x_length = 480
    y_length = 120

    # 초기 위치
    x_position_bottom_etching_l = 1540 + 180 + 600 - 3150 + 60
    y_position_bottom_etching_lt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400
    metal_y_position_bottom_etching_lt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 - 200 - 1400 + 6300 - 500
    y_position_bottom_etching_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 -200 + 1456 - 1400
    metal_y_position_bottom_etching_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 - 200 + 1456 - 1400 + 6300 + 5000 - 8 - 500

    x_position_bottom_etching_r = 1540 + 180 + 600 - 3150 + 4200 - 300 - 60
    y_position_bottom_etching_rt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400
    metal_y_position_bottom_etching_rt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 - 200 - 1400 + 6300 - 500
    y_position_bottom_etching_rb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 -200 + 1456 - 1400
    metal_y_position_bottom_etching_rb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 - 200 + 1456 - 1400 + 6300 + 5000 - 8 - 500

    x_position_top_etching_l = 12000 - 1500 - 120 - 180 + 300 - 3150 + 2150 - 4200 + 300 + 60
    y_position_top_etching_lt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400
    metal_y_position_top_etching_lt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 - 200 - 1400 + 6300 - 500
    y_position_top_etching_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 -200 + 1456 - 1400
    metal_y_position_top_etching_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 - 200 + 1456 - 1400 + 6300 + 5000 - 8 - 500

    x_position_top_etching_r = 12000 - 1500 - 120 - 180 + 300 - 3150 + 2150 - 60
    y_position_top_etching_rt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400
    metal_y_position_top_etching_rt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 - 200 - 1400 + 6300 - 500
    y_position_top_etching_rb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 -200 + 1456 - 1400
    metal_y_position_top_etching_rb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 - 200 + 1456 - 1400 + 6300 + 5000 - 8 - 500

    oxide_etching_bottom_lt = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    oxide_etching_bottom_lt.move([x_position_bottom_etching_l, y_position_bottom_etching_lt])
    oxide_etching_bottom_lb = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    oxide_etching_bottom_lb.move([x_position_bottom_etching_l, y_position_bottom_etching_lb])

    oxide_etching_bottom_rt = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    oxide_etching_bottom_rt.move([x_position_bottom_etching_r, y_position_bottom_etching_rt])
    oxide_etching_bottom_rb = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    oxide_etching_bottom_rb.move([x_position_bottom_etching_r, y_position_bottom_etching_rb])

    oxide_etching_top_lt = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    oxide_etching_top_lt.move([x_position_top_etching_l, y_position_top_etching_lt])
    oxide_etching_top_lb = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    oxide_etching_top_lb.move([x_position_top_etching_l, y_position_top_etching_lb])

    oxide_etching_top_rt = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    oxide_etching_top_rt.move([x_position_top_etching_r, y_position_top_etching_rt])
    oxide_etching_top_rb = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    oxide_etching_top_rb.move([x_position_top_etching_r, y_position_top_etching_rb])

    # 상부 아디아바틱 커플러
    metal_oxide_etching_bottom_lt = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    metal_oxide_etching_bottom_lt.move([x_position_bottom_etching_l, metal_y_position_bottom_etching_lt])
    metal_oxide_etching_bottom_lb = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    metal_oxide_etching_bottom_lb.move([x_position_bottom_etching_l, metal_y_position_bottom_etching_lb])

    metal_oxide_etching_bottom_rt = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    metal_oxide_etching_bottom_rt.move([x_position_bottom_etching_r, metal_y_position_bottom_etching_rt])
    metal_oxide_etching_bottom_rb = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    metal_oxide_etching_bottom_rb.move([x_position_bottom_etching_r, metal_y_position_bottom_etching_rb])

    metal_oxide_etching_top_lt = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    metal_oxide_etching_top_lt.move([x_position_top_etching_l, metal_y_position_top_etching_lt])
    metal_oxide_etching_top_lb = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    metal_oxide_etching_top_lb.move([x_position_top_etching_l, metal_y_position_top_etching_lb])

    metal_oxide_etching_top_rt = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    metal_oxide_etching_top_rt.move([x_position_top_etching_r, metal_y_position_top_etching_rt])
    metal_oxide_etching_top_rb = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
    metal_oxide_etching_top_rb.move([x_position_top_etching_r, metal_y_position_top_etching_rb])

    # substrate 본딩 얼라인 키
    x_position_alignkey_bottom_lt1 = 1420 + 180 + 600 - 3150
    x_position_alignkey_bottom_lt2 = 1540 + 180 + 600 - 3150
    x_position_alignkey_bottom_lt3 = 1660 + 180 + 600 - 3150
    y_position_alignkey_bottom_lt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400
    metal_y_position_alignkey_bottom_lt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400 + 6300 - 500

    x_position_alignkey_bottom_rt1 = 5700 - 1000 - 180 + 600 - 1870 - 180 - 120
    x_position_alignkey_bottom_rt2 = 5820 - 1000 - 180 + 600 - 1870 - 180 - 120
    x_position_alignkey_bottom_rt3 = 5940 - 1000 - 180 + 600 - 1870 - 180 - 120
    y_position_alignkey_bottom_rt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400
    metal_y_position_alignkey_bottom_rt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400 + 6300 - 500

    x_position_alignkey_bottom_lb1 = 1420 + 180 + 600 - 3150
    x_position_alignkey_bottom_lb2 = 1540 + 180 + 600 - 3150
    x_position_alignkey_bottom_lb3 = 1660 + 180 + 600 - 3150
    y_position_alignkey_bottom_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 -200 + 1456 - 1400
    metal_y_position_alignkey_bottom_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 -200 + 1456 - 1400 + 6300 + 5000 - 8 - 500

    x_position_alignkey_bottom_rb1 = 5700 - 1000 - 180 + 600 - 1870 - 180 - 120
    x_position_alignkey_bottom_rb2 = 5820 - 1000 - 180 + 600 - 1870 - 180 - 120
    x_position_alignkey_bottom_rb3 = 5940 - 1000 - 180 + 600 - 1870 - 180 - 120
    y_position_alignkey_bottom_rb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 -200 + 1456 - 1400
    metal_y_position_alignkey_bottom_rb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 -200 + 1456 - 1400 + 6300 + 5000 - 8 - 500

    alignkey_bottom_lt1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lt1, y_position_alignkey_bottom_lt))
    alignkey_bottom_lt2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lt2, y_position_alignkey_bottom_lt))
    alignkey_bottom_lt3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lt3, y_position_alignkey_bottom_lt))
    alignkey_bottom_rt1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rt1, y_position_alignkey_bottom_rt))
    alignkey_bottom_rt2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rt2, y_position_alignkey_bottom_rt))
    alignkey_bottom_rt3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rt3, y_position_alignkey_bottom_rt))
    alignkey_bottom_lb1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lb1, y_position_alignkey_bottom_lb))
    alignkey_bottom_lb2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lb2, y_position_alignkey_bottom_lb))
    alignkey_bottom_lb3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lb3, y_position_alignkey_bottom_lb))
    alignkey_bottom_rb1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rb1, y_position_alignkey_bottom_rb))
    alignkey_bottom_rb2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rb2, y_position_alignkey_bottom_rb))
    alignkey_bottom_rb3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rb3, y_position_alignkey_bottom_rb))

    # 상부 아디아바틱 커플러
    metal_alignkey_bottom_lt1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lt1, metal_y_position_alignkey_bottom_lt))
    metal_alignkey_bottom_lt2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lt2, metal_y_position_alignkey_bottom_lt))
    metal_alignkey_bottom_lt3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lt3, metal_y_position_alignkey_bottom_lt))
    metal_alignkey_bottom_rt1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rt1, metal_y_position_alignkey_bottom_rt))
    metal_alignkey_bottom_rt2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rt2, metal_y_position_alignkey_bottom_rt))
    metal_alignkey_bottom_rt3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rt3, metal_y_position_alignkey_bottom_rt))
    metal_alignkey_bottom_lb1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lb1, metal_y_position_alignkey_bottom_lb))
    metal_alignkey_bottom_lb2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lb2, metal_y_position_alignkey_bottom_lb))
    metal_alignkey_bottom_lb3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_lb3, metal_y_position_alignkey_bottom_lb))
    metal_alignkey_bottom_rb1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rb1, metal_y_position_alignkey_bottom_rb))
    metal_alignkey_bottom_rb2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rb2, metal_y_position_alignkey_bottom_rb))
    metal_alignkey_bottom_rb3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_bottom_rb3, metal_y_position_alignkey_bottom_rb))

    # topchip 본딩 얼라인 키
    x_position_alignkey_top_lt1 = 7720 - 500 - 120 + 180 + 300 - 2280 + 180
    x_position_alignkey_top_lt2 = 7840 - 500 - 120 + 180 + 300 - 2280 + 180
    x_position_alignkey_top_lt3 = 7960 - 500 - 120 + 180 + 300 - 2280 + 180
    y_position_alignkey_top_lt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400
    metal_y_position_alignkey_top_lt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 - 200 - 1400 + 6300 - 500

    x_position_alignkey_top_rt1 = 12000 - 1500 - 120 - 180 + 300 - 3150 + 2150 - 120
    x_position_alignkey_top_rt2 = 12120 - 1500 - 120 - 180 + 300 - 3150 + 2150 - 120
    x_position_alignkey_top_rt3 = 12240 - 1500 - 120 - 180 + 300 - 3150 + 2150 - 120
    y_position_alignkey_top_rt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 -200 - 1400
    metal_y_position_alignkey_top_rt = -1533 + 1200 - 50 + 12400 - 2400 - 10000 - 200 - 1400 + 6300 - 500

    x_position_alignkey_top_lb1 = 7720 - 500 - 120 + 180 + 300 - 2280 + 180
    x_position_alignkey_top_lb2 = 7840 - 500 - 120 + 180 + 300 - 2280 + 180
    x_position_alignkey_top_lb3 = 7960 - 500 - 120 + 180 + 300 - 2280 + 180
    y_position_alignkey_top_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400  - 200 - 7 - 10000 -200 + 1456 - 1400
    metal_y_position_alignkey_top_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 - 200 + 1456 - 1400 + 6300 + 5000 - 8 - 500

    x_position_alignkey_top_rb1 = 12000 - 1500 - 120 - 180 + 300 - 3150 + 2150 - 120
    x_position_alignkey_top_rb2 = 12120 - 1500 - 120 - 180 + 300 - 3150 + 2150 - 120
    x_position_alignkey_top_rb3 = 12240 - 1500 - 120 - 180 + 300 - 3150 + 2150 - 120
    y_position_alignkey_top_rb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400  - 200 - 7 - 10000 -200 + 1456 - 1400
    metal_y_position_alignkey_top_rb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 10000 - 200 + 1456 - 1400 + 6300 + 5000 - 8 - 500

    alignkey_top_lt1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lt1, y_position_alignkey_top_lt))
    alignkey_top_lt2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lt2, y_position_alignkey_top_lt))
    alignkey_top_lt3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lt3, y_position_alignkey_top_lt))
    alignkey_top_rt1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rt1, y_position_alignkey_top_rt))
    alignkey_top_rt2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rt2, y_position_alignkey_top_rt))
    alignkey_top_rt3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rt3, y_position_alignkey_top_rt))
    alignkey_top_lb1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lb1, y_position_alignkey_top_lb))
    alignkey_top_lb2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lb2, y_position_alignkey_top_lb))
    alignkey_top_lb3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lb3, y_position_alignkey_top_lb))
    alignkey_top_rb1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rb1, y_position_alignkey_top_rb))
    alignkey_top_rb2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rb2, y_position_alignkey_top_rb))
    alignkey_top_rb3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rb3, y_position_alignkey_top_rb))

    # 상부 아디아바틱 커플러
    metal_alignkey_top_lt1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lt1, metal_y_position_alignkey_top_lt))
    metal_alignkey_top_lt2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lt2, metal_y_position_alignkey_top_lt))
    metal_alignkey_top_lt3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lt3, metal_y_position_alignkey_top_lt))
    metal_alignkey_top_rt1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rt1, metal_y_position_alignkey_top_rt))
    metal_alignkey_top_rt2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rt2, metal_y_position_alignkey_top_rt))
    metal_alignkey_top_rt3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rt3, metal_y_position_alignkey_top_rt))
    metal_alignkey_top_lb1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lb1, metal_y_position_alignkey_top_lb))
    metal_alignkey_top_lb2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lb2, metal_y_position_alignkey_top_lb))
    metal_alignkey_top_lb3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_lb3, metal_y_position_alignkey_top_lb))
    metal_alignkey_top_rb1 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rb1, metal_y_position_alignkey_top_rb))
    metal_alignkey_top_rb2 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rb2, metal_y_position_alignkey_top_rb))
    metal_alignkey_top_rb3 = layout << make_adiabatic_coupler.add_cross_align_key(
        (x_position_alignkey_top_rb3, metal_y_position_alignkey_top_rb))

    # Flip-chip 본딩 얼라인 키
    # substrate 본딩 얼라인 키
    x_position_alignkey_bottom_l = 1420 + 180 + 600 + 239 - 3150 + 19 + 1
    x_position_alignkey_bottom_r = 5820 - 1000 - 180 + 600 - 239 - 3150 + 1100 - 19 - 1
    y_position_alignkey_bottom = 11771 - 2400 - 10000 -200 - 1400
    metal_y_position_alignkey_bottom = 11771 - 2400 - 10000 - 200 - 1400 + 6300 - 500

    x_position_alignkey_bottom_pitch = 200 + 240
    y_position_alignkey_bottom_pitch = bottom_chip_pitch

    for x in range(4):
        for y in range(35):
            # alignkey_bottom_l1 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x, y_position_alignkey_bottom), 60, 16)
            # alignkey_bottom_l2 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 60.5, y_position_alignkey_bottom), 21, 5)
            # alignkey_bottom_l3 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 97, y_position_alignkey_bottom), 12, 3)
            # alignkey_bottom_l4 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 127.5, y_position_alignkey_bottom), 9, 2.6)
            #
            # alignkey_bottom_r1 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x, y_position_alignkey_bottom), 60, 16)
            # alignkey_bottom_r2 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 60.5, y_position_alignkey_bottom), 21, 5)
            # alignkey_bottom_r3 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 97, y_position_alignkey_bottom), 12, 3)
            # alignkey_bottom_r4 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 127.5, y_position_alignkey_bottom), 9, 2.6)
            #
            # alignkey_bottom_l1 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x, y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y), 60, 16)
            # alignkey_bottom_l2 = layout << make_adiabatic_coupler.add_cross_align_key((
            #                                                                           x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 60.5,
            #                                                                           y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
            #                                                                           21, 5)
            # alignkey_bottom_l3 = layout << make_adiabatic_coupler.add_cross_align_key((
            #                                                                           x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 97,
            #                                                                           y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
            #                                                                           12, 3)
            # alignkey_bottom_l4 = layout << make_adiabatic_coupler.add_cross_align_key((
            #                                                                           x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 127.5,
            #                                                                           y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
            #                                                                           9, 2.6)
            #
            # alignkey_bottom_r1 = layout << make_adiabatic_coupler.add_cross_align_key((
            #                                                                           x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x,
            #                                                                           y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
            #                                                                           60, 16)
            # alignkey_bottom_r2 = layout << make_adiabatic_coupler.add_cross_align_key((
            #                                                                           x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 60.5,
            #                                                                           y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
            #                                                                           21, 5)
            # alignkey_bottom_r3 = layout << make_adiabatic_coupler.add_cross_align_key((
            #                                                                           x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 97,
            #                                                                           y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
            #                                                                           12, 3)
            # alignkey_bottom_r4 = layout << make_adiabatic_coupler.add_cross_align_key((
            #                                                                           x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 127.5,
            #                                                                           y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
            #                                                                           9, 2.6)

            alignkey_bottom_l1 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x,
                                                                                      y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      60, 16)
            alignkey_bottom_l2 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 60.5,
                                                                                      y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      21, 5)
            alignkey_bottom_l3 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 97,
                                                                                      y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      12, 3)
            alignkey_bottom_l4 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 127.5,
                                                                                      y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      9, 2.6)

            alignkey_bottom_r1 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x,
                                                                                      y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      60, 16)
            alignkey_bottom_r2 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 60.5,
                                                                                      y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      21, 5)
            alignkey_bottom_r3 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 97,
                                                                                      y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      12, 3)
            alignkey_bottom_r4 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 127.5,
                                                                                      y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      9, 2.6)

    # 상부 아디아바틱 커플러
    for x in range(4):
        for y in range(11):
            metal_alignkey_bottom_l1 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x,
                                                                                      metal_y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      60, 16)
            metal_alignkey_bottom_l2 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 60.5,
                                                                                      metal_y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      21, 5)
            metal_alignkey_bottom_l3 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 97,
                                                                                      metal_y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      12, 3)
            metal_alignkey_bottom_l4 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 127.5,
                                                                                      metal_y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      9, 2.6)

            metal_alignkey_bottom_r1 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x,
                                                                                      metal_y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      60, 16)
            metal_alignkey_bottom_r2 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 60.5,
                                                                                      metal_y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      21, 5)
            metal_alignkey_bottom_r3 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 97,
                                                                                      metal_y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      12, 3)
            metal_alignkey_bottom_r4 = layout << make_adiabatic_coupler.add_cross_align_key((
                                                                                      x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 127.5,
                                                                                      metal_y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
                                                                                      9, 2.6)

    # x_position_alignkey_bottom_l = 1420 + 180 + 600
    # x_position_alignkey_bottom_r = 5820 - 1000 - 180 + 600
    # y_position_alignkey_bottom = 7611
    #
    # x_position_alignkey_bottom_pitch = 200
    # y_position_alignkey_bottom_pitch = bottom_chip_pitch * 2
    #
    # for x in range(0,7):
    #     for y in range(1, 3):
    #         alignkey_bottom_l1 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x, y_position_alignkey_bottom), 60, 16)
    #         alignkey_bottom_l2 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 60.5, y_position_alignkey_bottom), 21, 5)
    #         alignkey_bottom_l3 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 97, y_position_alignkey_bottom), 12, 3)
    #         alignkey_bottom_l4 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 127.5, y_position_alignkey_bottom), 9, 2.6)
    #
    #         alignkey_bottom_r1 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x, y_position_alignkey_bottom), 60, 16)
    #         alignkey_bottom_r2 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 60.5, y_position_alignkey_bottom), 21, 5)
    #         alignkey_bottom_r3 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 97, y_position_alignkey_bottom), 12, 3)
    #         alignkey_bottom_r4 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 127.5, y_position_alignkey_bottom), 9, 2.6)
    #
    #         alignkey_bottom_l1 = layout << make_adiabatic_coupler.add_cross_align_key((x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x, y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y), 60, 16)
    #         alignkey_bottom_l2 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 60.5,
    #                                                                                   y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
    #                                                                                   21, 5)
    #         alignkey_bottom_l3 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 97,
    #                                                                                   y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
    #                                                                                   12, 3)
    #         alignkey_bottom_l4 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 127.5,
    #                                                                                   y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
    #                                                                                   9, 2.6)
    #
    #         alignkey_bottom_r1 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x,
    #                                                                                   y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
    #                                                                                   60, 16)
    #         alignkey_bottom_r2 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 60.5,
    #                                                                                   y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
    #                                                                                   21, 5)
    #         alignkey_bottom_r3 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 97,
    #                                                                                   y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
    #                                                                                   12, 3)
    #         alignkey_bottom_r4 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 127.5,
    #                                                                                   y_position_alignkey_bottom + y_position_alignkey_bottom_pitch * y),
    #                                                                                   9, 2.6)
    #
    #         alignkey_bottom_l1 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x,
    #                                                                                   y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
    #                                                                                   60, 16)
    #         alignkey_bottom_l2 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 60.5,
    #                                                                                   y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
    #                                                                                   21, 5)
    #         alignkey_bottom_l3 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 97,
    #                                                                                   y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
    #                                                                                   12, 3)
    #         alignkey_bottom_l4 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_l + x_position_alignkey_bottom_pitch * x + 127.5,
    #                                                                                   y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
    #                                                                                   9, 2.6)
    #
    #         alignkey_bottom_r1 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x,
    #                                                                                   y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
    #                                                                                   60, 16)
    #         alignkey_bottom_r2 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 60.5,
    #                                                                                   y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
    #                                                                                   21, 5)
    #         alignkey_bottom_r3 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 97,
    #                                                                                   y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
    #                                                                                   12, 3)
    #         alignkey_bottom_r4 = layout << make_adiabatic_coupler.add_cross_align_key((
    #                                                                                   x_position_alignkey_bottom_r - x_position_alignkey_bottom_pitch * x - 127.5,
    #                                                                                   y_position_alignkey_bottom - y_position_alignkey_bottom_pitch * y),
    #                                                                                   9, 2.6)

    T_bottom_m = layout << gf.components.text(text="M", size=100, justify="left", layer=(34, 0))
    T_bottom_m.move([3670 - 2570 - 30, 7561 - 2557 - 45.65 - 5.35 - 10000 -200 - 1400 + 624])

    # 상부 아디아바틱 커플러
    T_bottom_m = layout << gf.components.text(text="M", size=100, justify="left", layer=(34, 0))
    T_bottom_m.move([3670 - 2570 - 30, 7561 - 2557 - 45.65 - 5.35 - 10000 -200 - 1400 + 624 + 6300 + 2700 + 4 - 500])

    # top chip 본딩 얼라인 키
    x_position_alignkey_top_l = 7720 - 500 - 120 + 180 + 300 + 239 - 3150 + 1050 + 20
    x_position_alignkey_top_r = 12120 - 1500 - 120 - 180 + 300 - 239 - 3150 + 1050 + 1100 - 20
    y_position_alignkey_top = 11771 - 2400 - 10000 -200 - 1400
    metal_y_position_alignkey_top = 11771 - 2400 - 10000 - 200 - 1400 + 6300 - 500

    x_position_alignkey_top_pitch = 200 + 240
    y_position_alignkey_top_pitch = bottom_chip_pitch

    for x in range(4):
        for y in range(35):
            # alignkey_top_l1 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x, y_position_alignkey_top), 60, 16)
            # alignkey_top_l2 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 60.5, y_position_alignkey_top), 21, 5)
            # alignkey_top_l3 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 97, y_position_alignkey_top), 12, 3)
            # alignkey_top_l4 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 127.5, y_position_alignkey_top), 9, 2.6)
            #
            # alignkey_top_r1 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_r - x_position_alignkey_top_pitch * x, y_position_alignkey_top), 60, 16)
            # alignkey_top_r2 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 60.5, y_position_alignkey_top), 21, 5)
            # alignkey_top_r3 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 97, y_position_alignkey_top), 12, 3)
            # alignkey_top_r4 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 127.5, y_position_alignkey_top), 9, 2.6)
            #
            # alignkey_top_l1 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x, y_position_alignkey_top + y_position_alignkey_top_pitch * y), 60, 16)
            # alignkey_top_l2 = layout << make_adiabatic_coupler.add_square_align_key((
            #                                                                           x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 60.5,
            #                                                                           y_position_alignkey_top + y_position_alignkey_top_pitch * y),
            #                                                                           21, 5)
            # alignkey_top_l3 = layout << make_adiabatic_coupler.add_square_align_key((
            #                                                                           x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 97,
            #                                                                           y_position_alignkey_top + y_position_alignkey_top_pitch * y),
            #                                                                           12, 3)
            # alignkey_top_l4 = layout << make_adiabatic_coupler.add_square_align_key((
            #                                                                           x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 127.5,
            #                                                                           y_position_alignkey_top + y_position_alignkey_top_pitch * y),
            #                                                                           9, 2.6)
            #
            # alignkey_top_r1 = layout << make_adiabatic_coupler.add_square_align_key((
            #                                                                           x_position_alignkey_top_r - x_position_alignkey_top_pitch * x,
            #                                                                           y_position_alignkey_top + y_position_alignkey_top_pitch * y),
            #                                                                           60, 16)
            # alignkey_top_r2 = layout << make_adiabatic_coupler.add_square_align_key((
            #                                                                           x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 60.5,
            #                                                                           y_position_alignkey_top + y_position_alignkey_top_pitch * y),
            #                                                                           21, 5)
            # alignkey_top_r3 = layout << make_adiabatic_coupler.add_square_align_key((
            #                                                                           x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 97,
            #                                                                           y_position_alignkey_top + y_position_alignkey_top_pitch * y),
            #                                                                           12, 3)
            # alignkey_top_r4 = layout << make_adiabatic_coupler.add_square_align_key((
            #                                                                           x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 127.5,
            #                                                                           y_position_alignkey_top + y_position_alignkey_top_pitch * y),
            #                                                                           9, 2.6)

            alignkey_top_l1 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_l + x_position_alignkey_top_pitch * x,
                                                                                      y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      60, 20)
            alignkey_top_l2 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 60.5,
                                                                                      y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      21, 7)
            alignkey_top_l3 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 97,
                                                                                      y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      12, 4)
            alignkey_top_l4 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 127.5,
                                                                                      y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      9, 3)

            alignkey_top_r1 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_r - x_position_alignkey_top_pitch * x,
                                                                                      y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      60, 20)
            alignkey_top_r2 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 60.5,
                                                                                      y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      21, 7)
            alignkey_top_r3 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 97,
                                                                                      y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      12, 4)
            alignkey_top_r4 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 127.5,
                                                                                      y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      9, 3)

    # 상부 아디아바틱 커플러
    for x in range(4):
        for y in range(11):
            metal_alignkey_top_l1 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_l + x_position_alignkey_top_pitch * x,
                                                                                      metal_y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      60, 20)
            metal_alignkey_top_l2 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 60.5,
                                                                                      metal_y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      21, 7)
            metal_alignkey_top_l3 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 97,
                                                                                      metal_y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      12, 4)
            metal_alignkey_top_l4 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 127.5,
                                                                                      metal_y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      9, 3)

            metal_alignkey_top_r1 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_r - x_position_alignkey_top_pitch * x,
                                                                                      metal_y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      60, 20)
            metal_alignkey_top_r2 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 60.5,
                                                                                      metal_y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      21, 7)
            metal_alignkey_top_r3 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 97,
                                                                                      metal_y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      12, 4)
            metal_alignkey_top_r4 = layout << make_adiabatic_coupler.add_square_align_key((
                                                                                      x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 127.5,
                                                                                      metal_y_position_alignkey_top - y_position_alignkey_top_pitch * y),
                                                                                      9, 3)

    # x_position_alignkey_top_l = 7720 - 500 - 120 + 180 + 300
    # x_position_alignkey_top_r = 12120 - 1500 - 120 - 180 + 300
    # y_position_alignkey_top = 7611
    #
    # x_position_alignkey_top_pitch = 200
    # y_position_alignkey_top_pitch = bottom_chip_pitch * 2

    # for x in range(0,7):
    #     for y in range(1, 3):
    #         alignkey_top_l1 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x, y_position_alignkey_top), 60, 16)
    #         alignkey_top_l2 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 60.5, y_position_alignkey_top), 21, 5)
    #         alignkey_top_l3 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 97, y_position_alignkey_top), 12, 3)
    #         alignkey_top_l4 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 127.5, y_position_alignkey_top), 9, 2.6)
    #
    #         alignkey_top_r1 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_r - x_position_alignkey_top_pitch * x, y_position_alignkey_top), 60, 16)
    #         alignkey_top_r2 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 60.5, y_position_alignkey_top), 21, 5)
    #         alignkey_top_r3 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 97, y_position_alignkey_top), 12, 3)
    #         alignkey_top_r4 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 127.5, y_position_alignkey_top), 9, 2.6)
    #
    #         alignkey_top_l1 = layout << make_adiabatic_coupler.add_square_align_key((x_position_alignkey_top_l + x_position_alignkey_top_pitch * x, y_position_alignkey_top + y_position_alignkey_top_pitch * y), 60, 16)
    #         alignkey_top_l2 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 60.5,
    #                                                                                   y_position_alignkey_top + y_position_alignkey_top_pitch * y),
    #                                                                                   21, 5)
    #         alignkey_top_l3 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 97,
    #                                                                                   y_position_alignkey_top + y_position_alignkey_top_pitch * y),
    #                                                                                   12, 3)
    #         alignkey_top_l4 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 127.5,
    #                                                                                   y_position_alignkey_top + y_position_alignkey_top_pitch * y),
    #                                                                                   9, 2.6)
    #
    #         alignkey_top_r1 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_r - x_position_alignkey_top_pitch * x,
    #                                                                                   y_position_alignkey_top + y_position_alignkey_top_pitch * y),
    #                                                                                   60, 16)
    #         alignkey_top_r2 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 60.5,
    #                                                                                   y_position_alignkey_top + y_position_alignkey_top_pitch * y),
    #                                                                                   21, 5)
    #         alignkey_top_r3 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 97,
    #                                                                                   y_position_alignkey_top + y_position_alignkey_top_pitch * y),
    #                                                                                   12, 3)
    #         alignkey_top_r4 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 127.5,
    #                                                                                   y_position_alignkey_top + y_position_alignkey_top_pitch * y),
    #                                                                                   9, 2.6)
    #
    #         alignkey_top_l1 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_l + x_position_alignkey_top_pitch * x,
    #                                                                                   y_position_alignkey_top - y_position_alignkey_top_pitch * y),
    #                                                                                   60, 16)
    #         alignkey_top_l2 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 60.5,
    #                                                                                   y_position_alignkey_top - y_position_alignkey_top_pitch * y),
    #                                                                                   21, 5)
    #         alignkey_top_l3 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 97,
    #                                                                                   y_position_alignkey_top - y_position_alignkey_top_pitch * y),
    #                                                                                   12, 3)
    #         alignkey_top_l4 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_l + x_position_alignkey_top_pitch * x + 127.5,
    #                                                                                   y_position_alignkey_top - y_position_alignkey_top_pitch * y),
    #                                                                                   9, 2.6)
    #
    #         alignkey_top_r1 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_r - x_position_alignkey_top_pitch * x,
    #                                                                                   y_position_alignkey_top - y_position_alignkey_top_pitch * y),
    #                                                                                   60, 16)
    #         alignkey_top_r2 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 60.5,
    #                                                                                   y_position_alignkey_top - y_position_alignkey_top_pitch * y),
    #                                                                                   21, 5)
    #         alignkey_top_r3 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 97,
    #                                                                                   y_position_alignkey_top - y_position_alignkey_top_pitch * y),
    #                                                                                   12, 3)
    #         alignkey_top_r4 = layout << make_adiabatic_coupler.add_square_align_key((
    #                                                                                   x_position_alignkey_top_r - x_position_alignkey_top_pitch * x - 127.5,
    #                                                                                   y_position_alignkey_top - y_position_alignkey_top_pitch * y),
    #                                                                                   9, 2.6)

    T_top_t = layout << gf.components.text(text="T", size=100, justify="left", layer=(34, 0))
    T_top_t.move([9050 - 3150 + 1630 - 30, -1533 + 1200 - 50 + 12400 - 2400 - 30 - 10000 -200 - 1400])

    T_top_m = layout << gf.components.text(text="M", size=100, justify="left", layer=(34, 0))
    T_top_m.move([9050 - 3150 + 1630 - 30, 7561 - 2557 - 45.65 - 5.35 - 10000 -200 - 1400 + 624])

    T_top_b = layout << gf.components.text(text="B", size=100, justify="left", layer=(34, 0))
    T_top_b.move([9050 - 3150 + 1630 - 30, -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 70 - 10000 -200 + 1456 - 1400])

    # 상부 아디아바틱 커플러
    T_top_t = layout << gf.components.text(text="T", size=100, justify="left", layer=(34, 0))
    T_top_t.move([9050 - 3150 + 1630 - 30, -1533 + 1200 - 50 + 12400 - 2400 - 30 - 10000 -200 - 1400 + 6300 - 500])

    T_top_m = layout << gf.components.text(text="M", size=100, justify="left", layer=(34, 0))
    T_top_m.move([9050 - 3150 + 1630 - 30, 7561 - 2557 - 45.65 - 5.35 - 10000 -200 - 1400 + 624 + 6300 + 2700 + 4 - 500])

    T_top_b = layout << gf.components.text(text="B", size=100, justify="left", layer=(34, 0))
    T_top_b.move([9050 - 3150 + 1630 - 30, -11550 + 1200 + 12400 - 5 * (247 - 4) - 731 + 3100 - 2400 - 200 - 7 - 70 - 10000 -200 + 1456 - 1400 + 6300 + 5000 - 7 - 500])

    # Glass 에칭 패턴
    # 공정 얼라인키 글래스 에칭(SiN 풀에칭)
    # 초기위치 (substrate)
    x_position_alignkey_bottom_lt1 = 1420 + 180 + 600 - 3150
    y_position_alignkey_bottom_lt = -1533 + 1200 - 50 + 12400 - 2400

    x_position_alignkey_bottom_lb1 = 1420 + 180 + 600 - 3150
    y_position_alignkey_bottom_lb = -11550 + 1200 + 12400 - 5 * (247 - 4) - 731  + 3100 - 2400

    # 초기위치 (top chip)



    # 가로240, 세로150
    x_length = 240
    y_length = 150

    # 초기 위치
    x_position_bottom_etching = 2285 - 3150 + 5
    x_position_top_etching = 10535 - 3150 + 1050 + 1095
    y_position = 11771 - 2400 - 10000 -200 - 1400
    metal_y_position = 11771 - 2400 - 10000 - 200 - 1400 + 6300 - 500

    # 간격
    x_pitch = 200
    y_pitch = bottom_chip_pitch

    for x in range(10):
        for y in range (35):
            oxide_etching_bottom = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
            oxide_etching_bottom.move([x_position_bottom_etching + x * (x_length + x_pitch), y_position - y * y_pitch])

            oxide_etching_top = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
            oxide_etching_top.move([x_position_top_etching - x * (x_length + x_pitch), y_position - y * y_pitch])

    # 상부 아디아바틱 커플러
    for x in range(10):
        for y in range (11):
            oxide_etching_bottom = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
            oxide_etching_bottom.move([x_position_bottom_etching + x * (x_length + x_pitch), metal_y_position - y * y_pitch])

            oxide_etching_top = layout << make_adiabatic_coupler.make_oxide_etching(x_length, y_length, (34,1))
            oxide_etching_top.move([x_position_top_etching - x * (x_length + x_pitch), metal_y_position - y * y_pitch])


    # # Bonding 패턴 (SiO2 에칭/Cr 증착, In 증착)
    # etching_layer_1 = (6, 0)
    # etching_layer_2 = (6, 1)
    #
    # indium_layer_1 = (41, 0)
    # indium_layer_2 = (42, 0)
    #
    # # SiO2 에칭/ Cr 증착 패턴의 길이
    # x_length_etching_1 = 300
    # y_length_etching_1 = 150
    #
    # x_length_etching_2 = 500
    # y_length_etching_2 = 150
    #
    # # In 증착 패턴의 길이
    # x_length_indium_1 = [96, 120, 144]
    # y_length_indium_1 = [32, 40, 48]
    #
    # x_length_indium_2 = [132, 156, 180]
    # y_length_indium_2 = [44, 52, 60]
    #
    # # 초기 위치
    # x_position_bottom_etching_1 = 1570 + 150
    # x_position_top_etching_1 = 10350 - 150
    #
    # x_position_bottom_etching_2 = 1570 + 350
    # x_position_top_etching_2 = 10350 - 350
    # y_position = -750 + 3.5
    #
    # # SiO2 에칭/ Cr 증착, In 증착 패턴 간격
    # x_pitch_1 = 100
    # y_pitch_1 = 243
    #
    # # SiO2 에칭/ Cr 증착, In 증착 패턴 간격
    # x_pitch_2 = 100
    # y_pitch_2 = 243
    #
    # # SiO2 에칭/ Cr 증착 패턴 얼라인 키 위치
    # x_position_oxide_alignkey_bottom_lt = 1540 + 180
    # y_position_oxide_alignkey_bottom_lt = -1533 + 1200 - 50
    #
    # x_position_oxide_alignkey_bottom_lb = 1540 + 180
    # y_position_oxide_alignkey_bottom_lb = -11550 + 1200
    #
    # x_position_oxide_alignkey_top_rt = 12000 - 1500 - 120 - 180
    # y_position_oxide_alignkey_top_rt = -1533 + 1200 - 50
    #
    # x_position_oxide_alignkey_top_rb = 12000 - 1500 - 120 - 180
    # y_position_oxide_alignkey_top_rb = -11550 + 1200
    #
    # # In 증착 패턴 얼라인 키 위치
    # x_position_indium_alignkey_bottom_lt = 1540 + 180 + 120
    # y_position_indium_alignkey_bottom_lt = -1533 + 1200 - 50
    #
    # x_position_indium_alignkey_bottom_lb = 1540 + 180 + 120
    # y_position_indium_alignkey_bottom_lb = -11550 + 1200
    #
    # x_position_indium_alignkey_top_rt = 12000 - 1500 - 120 - 180 - 120
    # y_position_indium_alignkey_top_rt = -1533 + 1200 - 50
    #
    # x_position_indium_alignkey_top_rb = 12000 - 1500 - 120 - 180 - 120
    # y_position_indium_alignkey_top_rb = -11550 + 1200
    #
    # # SiO2 에칭/ Cr 증착, In 증착 패턴 얼라인 키 크기
    # size_oxide_alignkey_bottom = 60
    # cross_width_oxide_alignkey_bottom = 30
    #
    # size_oxide_alignkey_top = 60
    # cross_width_oxide_alignkey_top = 10
    #
    # size_indium_alignkey_1 = 60
    # cross_width_indium_alignkey_1 = 30
    #
    # size_indium_alignkey_2 = 50
    # cross_width_indium_alignkey_2 = 10
    #
    # x_distance_indium_alignkey = 20
    # y_distance_indium_alignkey = 20
    # x_length_indium_alignkey = 5
    # y_length_indium_alignkey = 5
    #
    # # 텍스트 초기 위치
    # x_position_oxide_alignkey_bottom_text = 1540 + 180 + 120 + 100
    # y_position_oxide_alignkey_bottom_text = -1533 + 1200 - 50
    #
    # x_position_oxide_alignkey_top_text = 12000 - 1500 - 120 - 180 - 120 - 100
    # y_position_oxide_alignkey_top_text = -1533 + 1200 - 50
    #
    # # SiO2 에칭/ Cr 증착 얼라인 키 배치 가로 300 세로 150
    # oxide_alignkey_lt = layout << make_adiabatic_coupler.add_square_align_key((x_position_oxide_alignkey_bottom_lt, y_position_oxide_alignkey_bottom_lt), size_oxide_alignkey_bottom, cross_width_oxide_alignkey_bottom, etching_layer_1)
    # oxide_alignkey_lb = layout << make_adiabatic_coupler.add_square_align_key((x_position_oxide_alignkey_bottom_lb, y_position_oxide_alignkey_bottom_lb), size_oxide_alignkey_bottom, cross_width_oxide_alignkey_bottom, etching_layer_1)
    # oxide_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key((x_position_oxide_alignkey_top_rt, y_position_oxide_alignkey_top_rt), size_oxide_alignkey_top, cross_width_oxide_alignkey_top, etching_layer_1)
    # oxide_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key((x_position_oxide_alignkey_top_rb, y_position_oxide_alignkey_top_rb), size_oxide_alignkey_top, cross_width_oxide_alignkey_top, etching_layer_1)
    #
    # # indium_alignkey_lt = layout << make_adiabatic_coupler.add_square_align_key(
    # #     (x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt), size_indium_alignkey_1,
    # #     cross_width_indium_alignkey_1, etching_layer_1)
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_square_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_1,
    # #     cross_width_indium_alignkey_1, etching_layer_1)
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_square_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_1,
    # #     cross_width_indium_alignkey_1, etching_layer_1)
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_square_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_1,
    # #     cross_width_indium_alignkey_1, etching_layer_1)
    #
    # oxide_etching_alignkey_lt = layout << make_adiabatic_coupler.make_oxide_etching(60, 60, etching_layer_1)
    # oxide_etching_alignkey_lt.move([x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt])
    # oxide_etching_alignkey_lb = layout << make_adiabatic_coupler.make_oxide_etching(60, 60, etching_layer_1)
    # oxide_etching_alignkey_lb.move([x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb])
    # oxide_etching_alignkey_rt = layout << make_adiabatic_coupler.make_oxide_etching(60, 60, etching_layer_1)
    # oxide_etching_alignkey_rt.move([x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt])
    # oxide_etching_alignkey_rb = layout << make_adiabatic_coupler.make_oxide_etching(60, 60, etching_layer_1)
    # oxide_etching_alignkey_rb.move([x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb])
    #
    # # 가로 500 세로 150
    # oxide_alignkey_lt = layout << make_adiabatic_coupler.add_square_align_key(
    #     (x_position_oxide_alignkey_bottom_lt, y_position_oxide_alignkey_bottom_lt), size_oxide_alignkey_bottom,
    #     cross_width_oxide_alignkey_bottom, etching_layer_2)
    # oxide_alignkey_lb = layout << make_adiabatic_coupler.add_square_align_key(
    #     (x_position_oxide_alignkey_bottom_lb, y_position_oxide_alignkey_bottom_lb), size_oxide_alignkey_bottom,
    #     cross_width_oxide_alignkey_bottom, etching_layer_2)
    # oxide_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key(
    #     (x_position_oxide_alignkey_top_rt, y_position_oxide_alignkey_top_rt), size_oxide_alignkey_top,
    #     cross_width_oxide_alignkey_top, etching_layer_2)
    # oxide_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key(
    #     (x_position_oxide_alignkey_top_rb, y_position_oxide_alignkey_top_rb), size_oxide_alignkey_top,
    #     cross_width_oxide_alignkey_top, etching_layer_2)
    #
    # oxide_etching_alignkey_lt = layout << make_adiabatic_coupler.make_oxide_etching(60, 60, etching_layer_2)
    # oxide_etching_alignkey_lt.move([x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt])
    # oxide_etching_alignkey_lb = layout << make_adiabatic_coupler.make_oxide_etching(60, 60, etching_layer_2)
    # oxide_etching_alignkey_lb.move([x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb])
    # oxide_etching_alignkey_rt = layout << make_adiabatic_coupler.make_oxide_etching(60, 60, etching_layer_2)
    # oxide_etching_alignkey_rt.move([x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt])
    # oxide_etching_alignkey_rb = layout << make_adiabatic_coupler.make_oxide_etching(60, 60, etching_layer_2)
    # oxide_etching_alignkey_rb.move([x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb])
    #
    # # indium_alignkey_lt = layout << make_adiabatic_coupler.add_square_align_key(
    # #     (x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt), size_indium_alignkey_1,
    # #     cross_width_indium_alignkey_1, etching_layer_2)
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_square_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_1,
    # #     cross_width_indium_alignkey_1, etching_layer_2)
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_square_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_1,
    # #     cross_width_indium_alignkey_1, etching_layer_2)
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_square_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_1,
    # #     cross_width_indium_alignkey_1, etching_layer_2)
    #
    # # In 증착 패턴 얼라인 키 위치
    # x_position_indium_alignkey_bottom_lt = 1540 + 180 + 120
    # y_position_indium_alignkey_bottom_lt = -1533 + 1200 - 50
    #
    # x_position_indium_alignkey_bottom_lb = 1540 + 180 + 120
    # y_position_indium_alignkey_bottom_lb = -11550 + 1200
    #
    # x_position_indium_alignkey_top_rt = 12000 - 1500 - 120 - 180 - 120
    # y_position_indium_alignkey_top_rt = -1533 + 1200 - 50
    #
    # x_position_indium_alignkey_top_rb = 12000 - 1500 - 120 - 180 - 120
    # y_position_indium_alignkey_top_rb = -11550 + 1200
    #
    # # In 증착 얼라인 키 배치 가로 300 세로 150
    # indium_alignkey_lt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey, y_distance_indium_alignkey, x_length_indium_alignkey, y_length_indium_alignkey, layer=(indium_layer_1[0], indium_layer_1[1]))
    # indium_alignkey_lt.move([x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt])
    # indium_alignkey_lb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #     indium_layer_1[0], indium_layer_1[1]))
    # indium_alignkey_lb.move([x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb])
    # indium_alignkey_rt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #     indium_layer_1[0], indium_layer_1[1]))
    # indium_alignkey_rt.move([x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt])
    # indium_alignkey_rb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #     indium_layer_1[0], indium_layer_1[1]))
    # indium_alignkey_rb.move([x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb])
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1]))
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1]))
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1]))
    #
    # # indium_alignkey_lt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1]))
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1]))
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1]))
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1]))
    #
    # # 가로 500 세로 150
    # indium_alignkey_lt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #     indium_layer_2[0], indium_layer_2[1]))
    # indium_alignkey_lt.move([x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt])
    # indium_alignkey_lb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1]))
    # indium_alignkey_lb.move([x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb])
    # indium_alignkey_rt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1]))
    # indium_alignkey_rt.move([x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt])
    # indium_alignkey_rb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1]))
    # indium_alignkey_rb.move([x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb])
    # # indium_alignkey_lt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1]))
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1]))
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1]))
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1]))
    #
    # # In 증착 얼라인 키 배치 가로 300 세로 150 (2)
    # indium_alignkey_lt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #     indium_layer_1[0], indium_layer_1[1] + 1))
    # indium_alignkey_lt.move([x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt])
    # indium_alignkey_lb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_1[0], indium_layer_1[1] + 1))
    # indium_alignkey_lb.move([x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb])
    # indium_alignkey_rt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_1[0], indium_layer_1[1] + 1))
    # indium_alignkey_rt.move([x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt])
    # indium_alignkey_rb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_1[0], indium_layer_1[1] + 1))
    # indium_alignkey_rb.move([x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb])
    # # indium_alignkey_lt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1] + 1))
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1] + 1))
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1] + 1))
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1] + 1))
    #
    # # 가로 500 세로 150
    # indium_alignkey_lt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1] + 1))
    # indium_alignkey_lt.move([x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt])
    # indium_alignkey_lb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1] + 1))
    # indium_alignkey_lb.move([x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb])
    # indium_alignkey_rt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1] + 1))
    # indium_alignkey_rt.move([x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt])
    # indium_alignkey_rb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1] + 1))
    # indium_alignkey_rb.move([x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb])
    # # indium_alignkey_lt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1] + 1))
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1] + 1))
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1] + 1))
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1] + 1))
    #
    # # In 증착 얼라인 키 배치 가로 300 세로 150 (3)
    # indium_alignkey_lt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #     indium_layer_1[0], indium_layer_1[1] + 2))
    # indium_alignkey_lt.move([x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt])
    # indium_alignkey_lb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_1[0], indium_layer_1[1] + 2))
    # indium_alignkey_lb.move([x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb])
    # indium_alignkey_rt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_1[0], indium_layer_1[1] + 2))
    # indium_alignkey_rt.move([x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt])
    # indium_alignkey_rb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_1[0], indium_layer_1[1] + 2))
    # indium_alignkey_rb.move([x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb])
    # # indium_alignkey_lt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1] + 2))
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1] + 2))
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1] + 2))
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_1[0], indium_layer_1[1] + 2))
    #
    # # 가로 500 세로 150
    # indium_alignkey_lt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1] + 2))
    # indium_alignkey_lt.move([x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt])
    # indium_alignkey_lb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1] + 2))
    # indium_alignkey_lb.move([x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb])
    # indium_alignkey_rt = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1] + 2))
    # indium_alignkey_rt.move([x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt])
    # indium_alignkey_rb = layout << make_adiabatic_coupler.make_indium_align_key(x_distance_indium_alignkey,
    #                                                                             y_distance_indium_alignkey,
    #                                                                             x_length_indium_alignkey,
    #                                                                             y_length_indium_alignkey, layer=(
    #         indium_layer_2[0], indium_layer_2[1] + 2))
    # indium_alignkey_rb.move([x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb])
    # # indium_alignkey_lt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lt, y_position_indium_alignkey_bottom_lt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1] + 2))
    # # indium_alignkey_lb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_bottom_lb, y_position_indium_alignkey_bottom_lb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1] + 2))
    # # indium_alignkey_rt = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rt, y_position_indium_alignkey_top_rt), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1] + 2))
    # # indium_alignkey_rb = layout << make_adiabatic_coupler.add_cross_align_key(
    # #     (x_position_indium_alignkey_top_rb, y_position_indium_alignkey_top_rb), size_indium_alignkey_2,
    # #     cross_width_indium_alignkey_2, layer=(indium_layer_2[0], indium_layer_2[1] + 2))
    #
    # # SiO2 에칭/ Cr 증착 텍스트
    # T_oxide_bottom = layout << gf.components.text(text="(6, 0)", size=15, justify="left", layer=etching_layer_1)
    # T_oxide_bottom.move([x_position_oxide_alignkey_bottom_text, y_position_oxide_alignkey_bottom_text])
    #
    # T_oxide_bottom = layout << gf.components.text(text="(6, 1)", size=15, justify="left", layer=etching_layer_2)
    # T_oxide_bottom.move([x_position_oxide_alignkey_bottom_text, y_position_oxide_alignkey_bottom_text])
    #
    # # SiO2 에칭/ Cr 증착 패턴 가로:300um 세로: 150um
    # for x in range(8):
    #     for y in range (39):
    #         oxide_etching_bc = layout << make_adiabatic_coupler.make_oxide_etching(x_length_etching_1, y_length_etching_1, etching_layer_1)
    #         oxide_etching_bc.move([x_position_bottom_etching_1 + x * (x_length_etching_1 + x_pitch_1), y_position - y * y_pitch_1])
    #
    #         oxide_etching_tc = layout << make_adiabatic_coupler.make_oxide_etching(x_length_etching_1, y_length_etching_1,
    #                                                                                etching_layer_1)
    #         oxide_etching_tc.move([x_position_top_etching_1 - x * (x_length_etching_1 + x_pitch_1),
    #                                y_position - y * y_pitch_1])
    #
    # # In 증착 패턴 가로:300um 세로: 150um
    # for i in range(len(x_length_indium_1)):
    #     for x in range(8):
    #         for y in range(39):
    #             indium_pillar_bc = layout << make_adiabatic_coupler.make_indium_pillar(x_length_indium_1[i], y_length_indium_1[i],
    #                                                                                    layer=(indium_layer_1[0], indium_layer_1[1] + i))
    #             indium_pillar_bc.move([x_position_bottom_etching_1 + x * (x_length_etching_1 + x_pitch_1),
    #                                    y_position - y * y_pitch_1])
    #
    #             indium_pillar_tc = layout << make_adiabatic_coupler.make_indium_pillar(x_length_indium_1[i], y_length_indium_1[i],
    #                                                                                    layer=(indium_layer_1[0], indium_layer_1[1] + i))
    #             indium_pillar_tc.move([x_position_top_etching_1 - x * (x_length_etching_1 + x_pitch_1),
    #                                    y_position - y * y_pitch_1])
    #
    # # SiO2 에칭/ Cr 증착 패턴 가로:500um 세로: 150um
    # for x in range(5):
    #     for y in range (39):
    #         oxide_etching_bc = layout << make_adiabatic_coupler.make_oxide_etching(x_length_etching_2, y_length_etching_2, etching_layer_2)
    #         oxide_etching_bc.move([x_position_bottom_etching_2 + x * (x_length_etching_2 + x_pitch_2), y_position - y * y_pitch_2])
    #
    #         oxide_etching_tc = layout << make_adiabatic_coupler.make_oxide_etching(x_length_etching_2, y_length_etching_2,
    #                                                                                etching_layer_2)
    #         oxide_etching_tc.move([x_position_top_etching_2 - x * (x_length_etching_2 + x_pitch_2),
    #                                y_position - y * y_pitch_2])
    #
    # # In 증착 패턴 가로:300um 세로: 150um
    # for i in range(len(x_length_indium_2)):
    #     for x in range(5):
    #         for y in range(39):
    #             indium_pillar_bc = layout << make_adiabatic_coupler.make_indium_pillar(x_length_indium_2[i], y_length_indium_2[i],
    #                                                                                    layer=(indium_layer_2[0], indium_layer_2[1] + i))
    #             indium_pillar_bc.move([x_position_bottom_etching_2 + x * (x_length_etching_2 + x_pitch_2),
    #                                    y_position - y * y_pitch_2])
    #
    #             indium_pillar_tc = layout << make_adiabatic_coupler.make_indium_pillar(x_length_indium_2[i], y_length_indium_2[i],
    #                                                                                    layer=(indium_layer_2[0], indium_layer_2[1] + i))
    #             indium_pillar_tc.move([x_position_top_etching_2 - x * (x_length_etching_2 + x_pitch_2),
    #                                    y_position - y * y_pitch_2])



