import numpy as np
from make import make_elements, make_grating
import gdsfactory as gf

def grating(layout):
    import numpy as np
    import gdsfactory as gf

    # === 공통 파라미터 ===
    layer_strip = (34, 0)
    layer_strip2 = (34, 4)
    layer_rib = (36, 0)
    bend_radius = 200
    bend_length = 25
    width_strip = 0.9

    pitch_1310 = np.arange(0.83, 0.95, 0.02).round(3).tolist()
    duty_cycle_1310 = np.arange(0.40, 0.61, 0.05).round(2).tolist()
    fill_factor_1310 = [round(1 - dc, 3) for dc in duty_cycle_1310]

    # === 위치 설정 ===
    base_x = -9520
    text_x_offset = -50
    institution_x_offset = 1340

    positions = {
        'strip': {'x_offset': 0, 'y_base': 2000},
        'rib': {'x_offset': 0, 'y_base': -1160},
        'ver2': {'x_offset': -50.7, 'y_base': -4300}
    }

    # === Strip GC 1310 ===
    pos = positions['strip']
    for j, ff in enumerate(fill_factor_1310):
        for k, pitch in enumerate(pitch_1310):
            x = base_x + 1350 * j + pos['x_offset']
            y = pos['y_base'] + 500 * k

            # Strip WG - GC 형성
            coupler = layout << make_grating.Bend_GC_arc(
                400, bend_length, bend_radius, layer_strip, width_strip,
                period=pitch, fill_factor=ff
            )
            coupler.move((x, y))

            # 파라미터 텍스트
            text_x = x + text_x_offset
            texts = [
                (f"P = {pitch}", y - 140),
                (f"D = {duty_cycle_1310[j]}", y - 230),
                (f"W = {width_strip}", y - 320)
            ]
            for text, text_y in texts:
                txt = layout << gf.components.text(text=text, size=50, justify="left", layer=layer_strip)
                txt.move((text_x, text_y))

            # 기관명 텍스트
            institution_x = base_x + 480 + institution_x_offset * j

            # Hanyang
            txt_hanyang = layout << gf.components.text(text="Hanyang", size=60, justify="left", layer=layer_strip)
            txt_hanyang.move((institution_x, y - 130))

            # ASDL
            txt_asdl = layout << gf.components.text(text="ASDL", size=60, justify="left", layer=layer_strip)
            txt_asdl.move((institution_x + 80, y - 240))

            # Strip-1310
            txt_type = layout << gf.components.text(text="Strip-1310", size=60, justify="left", layer=layer_strip)
            txt_type.move((institution_x - 30, y - 340))

    # === Rib GC 1310 (Full + Shallow) ===
    pos = positions['rib']
    for j, ff in enumerate(fill_factor_1310):
        for k, pitch in enumerate(pitch_1310):
            x = base_x + 1350 * j + pos['x_offset']
            y = pos['y_base'] + 500 * k

            # Full Etch - GC 형성
            coupler = layout << make_grating.Full_Bend_GC_arc(
                400, bend_length, bend_radius, layer_strip2, width=width_strip,
                period=pitch, fill_factor=ff
            )
            coupler.move((x, y))

            # Shallow Etch - GC 형성
            shallow_coupler = layout << make_grating.Shallow_Bend_GC_arc(
                400, bend_length, bend_radius, layer_rib, width=width_strip,
                period=pitch, fill_factor=ff
            )
            shallow_coupler.move((x, y))

            # 파라미터 텍스트
            text_x = x + text_x_offset
            texts = [
                (f"P = {pitch}", y - 140),
                (f"D = {duty_cycle_1310[j]}", y - 230),
                (f"W = {width_strip}", y - 320)
            ]
            for text, text_y in texts:
                txt = layout << gf.components.text(text=text, size=50, justify="left", layer=layer_strip)
                txt.move((text_x, text_y))

            # 기관명 텍스트
            institution_x = base_x + 480 + institution_x_offset * j

            # Hanyang
            txt_hanyang = layout << gf.components.text(text="Hanyang", size=60, justify="left", layer=layer_strip)
            txt_hanyang.move((institution_x, y - 130))

            # ASDL
            txt_asdl = layout << gf.components.text(text="ASDL", size=60, justify="left", layer=layer_strip)
            txt_asdl.move((institution_x + 80, y - 240))

            # Rib-1310
            txt_type = layout << gf.components.text(text="Rib-1310", size=60, justify="left", layer=layer_strip)
            txt_type.move((institution_x, y - 340))

    # === Ver.II - GC 1310 ===
    pos = positions['ver2']
    for j, ff in enumerate(fill_factor_1310):
        for k, pitch in enumerate(pitch_1310):
            x = base_x + 1350 * j + pos['x_offset']
            y = pos['y_base'] + 500 * k

            # Ver. II - GC 형성
            coupler = layout << make_grating.Bend_GC_standard_arc(
                400, bend_length, bend_radius, layer_strip, width_strip,
                period=pitch, fill_factor=ff
            )
            coupler.move((x, y))

            # 파라미터 텍스트
            text_x = base_x + text_x_offset + 1350 * j
            texts = [
                (f"P = {pitch}", y - 140),
                (f"D = {duty_cycle_1310[j]}", y - 230),
                (f"W = {width_strip}", y - 320)
            ]
            for text, text_y in texts:
                txt = layout << gf.components.text(text=text, size=50, justify="left", layer=layer_strip)
                txt.move((text_x, text_y))

            # 기관명 텍스트
            institution_x = base_x + 480 + institution_x_offset * j

            # Hanyang
            txt_hanyang = layout << gf.components.text(text="Hanyang", size=60, justify="left", layer=layer_strip)
            txt_hanyang.move((institution_x, y - 130))

            # ASDL
            txt_asdl = layout << gf.components.text(text="ASDL", size=60, justify="left", layer=layer_strip)
            txt_asdl.move((institution_x + 80, y - 240))

            # Version-2
            txt_type = layout << gf.components.text(text="Version-2", size=60, justify="left", layer=layer_strip)
            txt_type.move((institution_x - 40, y - 340))