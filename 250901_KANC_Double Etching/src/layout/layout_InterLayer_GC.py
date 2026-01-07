from make import make_grating, make_adiabatic_coupler
import gdsfactory as gf
import numpy as np

def InterLayer_GC(layout, y_spacing= 220):

    # # 1st x sweep Array -------------------------------------------
    start_x = -2280
    start_y = -50
    num_rows = 28    # Total rows. x sweep + y sweep
    num_rows_xsweep = 13
    num_rows_ysweep = 13
    best_misalignment = 2.6

    tooth_grating_align = 57.658052    # for tester align
    right_tooth_grating = 215.31607    # for length align
    wg_to_first_grating = 21.217       # for align key align
    wg_to_last_grating = 36.44105      # for align key align
    space_cut = 1200   # space for cutting with glass cutter
    space_top = 1200   # space for top grating coupler between bend and straight
    mis_align= np.arange(3, -3.5, -0.5)    # for txt sweep

    params_bend = {"length1": 400, "length2": 25, "radius": 100, "layer": (34, 0), "width": 0.7, "period": 0.87,
                   "fill_factor": 0.5}

    params_straight = {"length1": 400, "length2": 400, "radius": 0, "layer": (34, 0), "width": 0.7, "period": 0.87,
                       "fill_factor": 0.5}

    params_top = {"length1": (space_top / 2), "length2": (space_top / 2) - right_tooth_grating, "radius": 0,
                  "layer": (34, 0), "width": 0.7, "period": 0.87, "fill_factor": 0.5}

    params_ref = {"length1": params_bend['length1'] + space_top + params_straight['length1'] + params_straight[
        'length2'] + 100,
                  "length2": 25, "radius": 100, "layer": (34, 0), "width": 0.7, "period": 0.87, "fill_factor": 0.5}

    y_row = 0
    for i in range(len(mis_align)):
        M = mis_align[i]
        y_offset = y_row * y_spacing
        length2_sweep = params_top['length2'] + M

        # Text 설정
        txt1 = layout << gf.components.text(text=f"X_Mis = {M}", size=20, justify="left", layer=params_bend['layer'])
        txt1.move((start_x, start_y - y_offset - 80))

        # 1. Bending GC 추가
        gc = make_grating.Bend_GC_arc(**params_bend)
        ref_bend = layout.add_ref(gc)
        ref_bend.move((start_x+0.217, start_y - y_offset))   #0.217은 grating 구조가 딱 start_x에서 시작하지 않고 -0.217 더 당겨진 부분에서 시작하기 때문에 추가

        # 2. Straight GC 추가
        gc_straight = make_grating.Straight_GC_arc(**params_straight)
        ref_straight = layout.add_ref(gc_straight)
        ref_straight.move((
            start_x + 0.217 + 100 + (params_bend["radius"] * 2) + params_bend["length1"] + space_top,
            start_y - (2 * params_bend["radius"]) - params_bend["length2"] - y_offset
        ))

        # 3. Top Straight GC 추가
        top_straight = make_grating.Straight_GC_arc(
            length1=params_top["length1"],
            length2=length2_sweep - (2*best_misalignment),
            radius=0,
            layer=params_top["layer"],
            width=params_top["width"],
            period=params_top["period"],
            fill_factor=params_top["fill_factor"]
        )
        ref_top = layout.add_ref(top_straight)
        ref_top.move((
            start_x + 0.217 + 100 + (params_bend["radius"] * 2) + params_bend["length1"] +
            space_cut + 100 + params_straight['length1'] + params_straight['length2'] + space_top + best_misalignment,
            start_y - (2 * params_bend["radius"]) - params_bend["length2"] - y_offset
        ))

        y_row += 1

        if M == 0:
            # 레퍼런스 소자 추가 (M == 0 다음 줄에 삽입)
            ref_y_offset = y_row * y_spacing
            ref_gc = make_grating.Bend_GC_arc(**params_ref)
            ref_ref = layout.add_ref(ref_gc)
            ref_ref.move((start_x, start_y - ref_y_offset))
            y_row += 1

    y_row_y = 0
    start_y_sweep = start_y - (y_spacing * (num_rows_xsweep + 1))
    for i in range(num_rows_ysweep):
        M = mis_align[i]
        y_offset = y_row_y * y_spacing
        y_posi_sweep = M

        # Text 설정
        txt_val = mis_align[i]
        txt1 = layout << gf.components.text(text=f"Y_Mis = {M}", size=20, justify="left", layer=params_bend['layer'])
        txt1.move((start_x, start_y_sweep - y_offset - 80))

        # 1. Bending GC 추가
        gc = make_grating.Bend_GC_arc(**params_bend)
        ref = layout.add_ref(gc)
        ref.move((start_x + 0.217, start_y_sweep - y_offset))    # 0.217은 grating 구조가 딱 start_x에서 시작하지 않고 -0.217 더 당겨진 부분에서 시작하기 때문에 추가

        # 2. Straight GC 추가
        gc_straight = make_grating.Straight_GC_arc(**params_straight)
        ref_straight = layout.add_ref(gc_straight)
        ref_straight.move((
            start_x + 0.217 + 100 + (params_bend["radius"] * 2) + params_bend["length1"] + space_top,
            start_y_sweep - (2 * params_bend["radius"]) - params_bend["length2"] - y_offset + y_posi_sweep
        ))

        # 3. Top Straight GC 추가
        top_straight = make_grating.Straight_GC_arc(
            length1=params_top["length1"],
            length2=params_top['length2']- (2*best_misalignment),
            radius=0,
            layer=params_top["layer"],
            width=params_top["width"],
            period=params_top["period"],
            fill_factor=params_top["fill_factor"])
        ref_top = layout.add_ref(top_straight)
        ref_top.move((
            start_x + 0.217 + 100 + (params_bend["radius"] * 2) + params_bend["length1"] +
            space_cut + 100 + params_straight['length1'] + params_straight['length2'] + space_top + best_misalignment,
            start_y_sweep - (2 * params_bend["radius"]) - params_bend["length2"] - y_offset
        ))

        y_row_y += 1

        if M == 0:
            ref_y_offset = y_row_y * y_spacing
            ref_gc_y = make_grating.Bend_GC_arc(**params_ref)
            ref_ref_y = layout.add_ref(ref_gc_y)
            ref_ref_y.move((start_x, start_y_sweep - ref_y_offset))
            y_row_y += 1

    # ---------------------------------------------------
                    # align key
    bend_gc_length = 100 + params_bend['length1'] + (2*params_bend['radius'])
    straight_gc_length = params_straight['length1'] + params_straight['length2'] + 100
    top_gc_length = params_top['length1'] + params_top['length2'] + 100

    align_start_x = start_x + bend_gc_length
    align_start_y = start_y - (params_bend['radius'] * 2 + params_bend["length2"]) + (y_spacing / 2)

    for i in range(num_rows + 1):
        y_offset = i * y_spacing

        # Bottom cross align keys
        layout << make_adiabatic_coupler.add_cross_align_key(
            (align_start_x + wg_to_first_grating, align_start_y - y_offset), cross_width=16)
        layout << make_adiabatic_coupler.add_cross_align_key(
            (align_start_x + wg_to_first_grating + 100, align_start_y - y_offset), cross_width=16)
        layout << make_adiabatic_coupler.add_cross_align_key(
            (align_start_x + space_top - wg_to_first_grating, align_start_y - y_offset), cross_width=16)
        layout << make_adiabatic_coupler.add_cross_align_key(
            (align_start_x + space_top - wg_to_first_grating - 100, align_start_y - y_offset), cross_width=16)

        # Top square align keys
        layout << make_adiabatic_coupler.add_square_align_key(
            (align_start_x + space_top + straight_gc_length + space_cut - wg_to_last_grating, align_start_y - y_offset))
        layout << make_adiabatic_coupler.add_square_align_key(
            (align_start_x + space_top + straight_gc_length + space_cut - wg_to_last_grating + 100,
             align_start_y - y_offset))
        layout << make_adiabatic_coupler.add_square_align_key(
            (align_start_x + space_top + straight_gc_length + space_cut + top_gc_length + wg_to_last_grating,
             align_start_y - y_offset))
        layout << make_adiabatic_coupler.add_square_align_key(
            (align_start_x + space_top + straight_gc_length + space_cut + top_gc_length + wg_to_last_grating - 100,
             align_start_y - y_offset))

    # -----------------------------------------------------
                      # test
    # y_row = 0
    # for i in range(len(mis_align)):
    #     M = mis_align[i]
    #     y_offset = y_row * y_spacing
    #     length2_sweep = params_top['length2'] + M
    # # 3. Top Straight GC 추가
    #     top_straight = make_grating.Straight_GC_arc(
    #         length1=params_top["length1"],
    #         length2=length2_sweep - (2*best_misalignment),
    #         radius=0,
    #         layer=params_top["layer"],
    #         width=params_top["width"],
    #         period=params_top["period"],
    #         fill_factor=params_top["fill_factor"]
    #     )
    #     ref_top = layout.add_ref(top_straight)
    #     ref_top.move((
    #         start_x + 100 + (params_bend["radius"] * 2) + params_bend["length1"] + best_misalignment + tooth_grating_align,
    #         start_y - (2 * params_bend["radius"]) - params_bend["length2"] - y_offset
    #     ))
    #
    # for i in range(num_rows_ysweep):
    #     start_y_sweep = start_y - (y_spacing * num_rows_xsweep)
    #     y_offset = i * y_spacing
    #     M = mis_align[i]
    #     y_posi_sweep = M
    #     # 3. Top Straight GC 추가
    #     top_straight = make_grating.Straight_GC_arc(**params_top)
    #     ref_top = layout.add_ref(top_straight)
    #     ref_top.move((
    #         start_x + 100 + (params_bend["radius"] * 2) + params_bend["length1"] + tooth_grating_align,
    #         start_y_sweep - (2 * params_bend["radius"]) - params_bend["length2"] - y_offset
    #     ))

# -----------------------------------------------------

    # 2nd x sweep Array -------------------------------------------
    wg_to_clad_end = 50.700314

    start_x_2 = (start_x + 100 + (params_bend["radius"] * 2) + params_bend["length1"] + space_cut + 100
                 + params_straight['length1'] + params_straight['length2'] + 100 + space_top + params_top['length1'] +
                 params_top['length2'] + space_cut)
    start_y_2 = start_y

    standard_tooth_grating_align = 54.89215  # for tester align (standard gc arc)
    standard_right_tooth_grating = 209.7842  # for length align (standard gc arc)
    imec_wg_to_first_grating = 19.834  # for align key align
    imec_wg_to_last_grating = 35.0579  # for align key align
    space_cut = 1200  # space for cutting with glass cutter
    space_top = 1200  # space for top grating coupler between bend and straight
    mis_align = np.arange(3, -3.5, -0.5)  # for txt sweep

    params_standard_bend = {"length1": 400, "length2": 25, "radius": 100, "layer": (34, 0), "width": 0.7,
                            "period": 0.87,
                            "fill_factor": 0.5}

    params_standard_straight = {"length1": 400, "length2": 400, "radius": 0, "layer": (34, 0), "width": 0.7,
                                "period": 0.87,
                                "fill_factor": 0.5}

    params_standard_top = {"length1": (space_top / 2), "length2": (space_top / 2) - standard_right_tooth_grating,
                           "radius": 0,
                           "layer": (34, 0), "width": 0.7, "period": 0.87,
                           "fill_factor": 0.5}

    params_standard_ref = {
        "length1": params_standard_bend['length1'] + space_top + params_standard_straight['length1'] +
                   params_standard_straight['length2'] + 100,
        "length2": 25, "radius": 100, "layer": (34, 0), "width": 0.7, "period": 0.87, "fill_factor": 0.5}

    y_row = 0
    for i in range(len(mis_align)):  # x sweep
        M = mis_align[i]
        y_offset = y_row * y_spacing
        length2_sweep = params_standard_top['length2'] + M

        txt1 = layout << gf.components.text(text=f"X_Mis = {M}", size=20, justify="left",
                                            layer=params_standard_bend['layer'])
        txt1.move((start_x_2, start_y_2 - y_offset - 80))

        gc = make_grating.Bend_GC_standard_arc(**params_standard_bend)
        ref = layout.add_ref(gc)
        ref.move((start_x_2 - wg_to_clad_end, start_y_2 - y_offset))

        gc_straight = make_grating.Straight_GC_standard_arc(**params_standard_straight)
        ref_straight = layout.add_ref(gc_straight)
        ref_straight.move((
            start_x_2 - wg_to_clad_end + 100 + (params_standard_bend["radius"] * 2) + params_standard_bend["length1"] + space_top,
            start_y_2 - (2 * params_standard_bend["radius"]) - params_standard_bend["length2"] - y_offset
        ))

        top_straight = make_grating.Straight_GC_standard_arc(
            length1=params_standard_top["length1"],
            length2=length2_sweep - (2*best_misalignment),
            radius=0,
            layer=params_standard_top["layer"],
            width=params_standard_top["width"],
            period=params_standard_top["period"],
            fill_factor=params_standard_top["fill_factor"]
        )
        ref_top = layout.add_ref(top_straight)
        ref_top.move((
            start_x_2 - wg_to_clad_end + 100 + (params_standard_bend["radius"] * 2) + params_standard_bend["length1"] +
            space_cut + 100 + params_standard_straight['length1'] + params_standard_straight['length2'] + space_top + best_misalignment,
            start_y_2 - (2 * params_standard_bend["radius"]) - params_standard_bend["length2"] - y_offset
        ))

        y_row += 1

        if M == 0:
            ref_gc = make_grating.Bend_GC_standard_arc(**params_standard_ref)
            ref_ref = layout.add_ref(ref_gc)
            ref_ref.move((start_x_2 - wg_to_clad_end, start_y_2 - y_row * y_spacing))
            y_row += 1

    y_row_y = 0
    start_y_sweep = start_y_2 - (y_spacing * (num_rows_xsweep + 1))
    for i in range(len(mis_align)):
        y_offset = y_row_y * y_spacing
        M = mis_align[i]

        # Text 설정
        txt1 = layout << gf.components.text(text=f"Y_Mis = {M}", size=20, justify="left", layer=params_bend['layer'])
        txt1.move((start_x_2, start_y_sweep - y_offset - 80))

        # 1. Bending GC 추가
        gc = make_grating.Bend_GC_standard_arc(**params_standard_bend)
        ref = layout.add_ref(gc)
        ref.move((start_x_2 - wg_to_clad_end, start_y_sweep - y_offset))

        # 2. Straight GC 추가
        gc_straight = make_grating.Straight_GC_standard_arc(**params_standard_straight)
        ref_straight = layout.add_ref(gc_straight)
        ref_straight.move((
            start_x_2 - wg_to_clad_end + 100 + (params_standard_bend["radius"] * 2) + params_standard_bend["length1"] + space_top,
            start_y_sweep - (2 * params_standard_bend["radius"]) - params_standard_bend[
                "length2"] - y_offset + M
        ))

        # 3. Top Straight GC 추가
        top_straight = make_grating.Straight_GC_standard_arc(
            length1=params_standard_top["length1"],
            length2=params_standard_top['length2'] - (2*best_misalignment),
            radius=0,
            layer=params_standard_bend["layer"],
            width=params_standard_top["width"],
            period=params_standard_top["period"],
            fill_factor=params_standard_top["fill_factor"])
        ref_top = layout.add_ref(top_straight)
        ref_top.move((
            start_x_2 - wg_to_clad_end + 100 + (params_standard_bend["radius"] * 2) + params_standard_bend["length1"] +
            space_cut + 100 + params_standard_straight['length1'] + params_standard_straight['length2'] + space_top + best_misalignment
            ,
            start_y_sweep - (2 * params_standard_bend["radius"]) - params_standard_bend["length2"] - y_offset
        ))

        y_row_y += 1
        if M == 0:
            ref_gc = make_grating.Bend_GC_standard_arc(**params_standard_ref)
            ref_ref = layout.add_ref(ref_gc)
            ref_ref.move((start_x_2 - wg_to_clad_end, start_y_sweep - y_row_y * y_spacing))
            y_row_y += 1


    #
    # # ---------------------------------------------------
    # # align key

    standard_top_gc_length = 100 + params_standard_top['length1'] + params_standard_top['length2']

    align_start_x_2 = start_x_2 + bend_gc_length
    align_start_y_2 = start_y_2 - (params_bend['radius'] * 2 + params_bend["length2"]) + (y_spacing / 2)

    for i in range(num_rows + 1):
        y_offset = i * y_spacing

        # Bottom cross align keys
        layout << make_adiabatic_coupler.add_cross_align_key(
            (align_start_x_2 + imec_wg_to_first_grating, align_start_y_2 - y_offset), cross_width=16)
        layout << make_adiabatic_coupler.add_cross_align_key(
            (align_start_x_2 + imec_wg_to_first_grating + 100, align_start_y_2 - y_offset), cross_width=16)
        layout << make_adiabatic_coupler.add_cross_align_key(
            (align_start_x_2 + space_top - imec_wg_to_first_grating, align_start_y_2 - y_offset), cross_width=16)
        layout << make_adiabatic_coupler.add_cross_align_key(
            (align_start_x_2 + space_top - imec_wg_to_first_grating - 100, align_start_y_2 - y_offset), cross_width=16)

        # Top square align keys
        layout << make_adiabatic_coupler.add_square_align_key(
            (align_start_x_2 + space_top + straight_gc_length + space_cut - imec_wg_to_last_grating, align_start_y_2 - y_offset))
        layout << make_adiabatic_coupler.add_square_align_key(
            (align_start_x_2 + space_top + straight_gc_length + space_cut - imec_wg_to_last_grating + 100,
             align_start_y_2 - y_offset))
        layout << make_adiabatic_coupler.add_square_align_key(
            (align_start_x_2 + space_top + straight_gc_length + space_cut + standard_top_gc_length + imec_wg_to_last_grating,
             align_start_y_2 - y_offset))
        layout << make_adiabatic_coupler.add_square_align_key(
            (align_start_x_2 + space_top + straight_gc_length + space_cut + standard_top_gc_length + imec_wg_to_last_grating - 100,
             align_start_y_2 - y_offset))
    # -----------------------------------------------------
    # test
    # for i in range(num_rows_xsweep):  # x sweep
    #     y_offset = i * y_spacing
    #     M = mis_align[i]
    #     length2_sweep = params_standard_top['length2'] + M
    #
    #     # 3. Top Straight GC 추가
    #     top_straight = make_grating.Straight_GC_standard_arc(
    #         length1=params_standard_top["length1"],
    #         length2=length2_sweep,
    #         radius=0,
    #         layer=params_standard_top["layer"],
    #         width=params_standard_top["width"],
    #         period=params_standard_top["period"],
    #         fill_factor=params_standard_top["fill_factor"]
    #     )
    #     ref_top = layout.add_ref(top_straight)
    #     ref_top.move((
    #         start_x_2 + 100 + (params_standard_bend["radius"] * 2) + params_standard_bend["length1"] + standard_tooth_grating_align,
    #         start_y_2 - (2 * params_standard_bend["radius"]) - params_standard_bend["length2"] - y_offset
    #     ))
    #
    #
    # for i in range(num_rows_ysweep):
    #     start_y_sweep = start_y_2 - (y_spacing * num_rows_xsweep)
    #     y_offset = i * y_spacing
    #     M = mis_align[i]
    #     y_posi_sweep = M
    #
    #     # 3. Top Straight GC 추가
    #     test = make_grating.Straight_GC_standard_arc(**params_standard_top)
    #     ref_top = layout.add_ref(test)
    #     ref_top.move((
    #         start_x_2 + 100 + (params_standard_bend["radius"] * 2) + params_standard_bend["length1"] + standard_tooth_grating_align,
    #         start_y_sweep - (2 * params_standard_bend["radius"]) - params_standard_bend["length2"] - y_offset
    #     ))
    # -----------------------------------------------------

    return layout