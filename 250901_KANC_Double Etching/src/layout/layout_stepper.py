# import gdsfactory as gf
# from make.make_stepper import add_stepper_rect_key
#
# # ✅ 레이어 설정 (1층: (1, 0), 2층: (2, 0))
# stepper_layer_1 = (34, 0)
# stepper_layer_2 = (34, 3)
# text_layer_1 = (34, 0)
# text_layer_2 = (34, 3)
#
# # ✅ 기준 좌표 (Wx-T1)
# center_x_WxT1, center_y_WxT1 = (-9650, -9050)
#
# # ✅ Stepper 설정 (Wx, LSAx, LSAy: 4x4 / Wy: 3x4)
# stepper_configs = [
#     ("Wx-T1", [-20, 0, 26], 8, 7, 3, (center_x_WxT1, center_y_WxT1), 4, 4, 0, 35),
#     ("LSAx-T1", [-20, 0, 20], 8, 7, 3, (center_x_WxT1 + 201, center_y_WxT1), 4, 4, 0, 35),
#     ("LSAy-T1", 8, [-20, 0, 20], 3, 7, (center_x_WxT1 + 201 + 197, center_y_WxT1), 4, 4, 0, 35),
#     ("Wy-T1", 7, [-26, 0, 20], 3, 51, (center_x_WxT1 + 201, center_y_WxT1 - 196), 3, 4, -210, -5),
#     ("Wx-M1", [-20, 0, 26], 8, 7, 3, (center_x_WxT1 + 700, center_y_WxT1), 4, 4, 0, 35),
#     ("LSAx-M1", [-20, 0, 20], 8, 7, 3, (center_x_WxT1 + 700 + 201, center_y_WxT1), 4, 4, 0, 35),
#     ("LSAy-M1", 8, [-20, 0, 20], 3, 7, (center_x_WxT1 + 700 + 201 + 197, center_y_WxT1), 4, 4, 0, 35),
#     ("Wy-M1", 7, [-26, 0, 20], 3, 51, (center_x_WxT1 + 700 + 201, center_y_WxT1 - 196), 3, 4, -210, -5),
# ]
#
#
# def add_stepper_text(layout, text, x, y, x_offset=0, y_offset=35, layer=(1, 0)):
#     """Stepper 키 이름을 텍스트로 추가"""
#     text_label = layout << gf.components.text(text=text, size=10, justify="center", layer=layer)
#     text_label.move((x + x_offset, y + y_offset))
#
#
# def stepper_all(layout):
#     """모든 Stepper 키를 자동 배치 (1층 & 2층 추가)"""
#     for name, x_offsets, y_spacing, num_rows, num_cols, (center_x, center_y), width, height, x_offset, y_offset in stepper_configs:
#         for layer, y_shift in [(stepper_layer_1, 0), (stepper_layer_2, -400)]:  # ✅ 1층과 2층 추가
#             text_layer = text_layer_1 if layer == stepper_layer_1 else text_layer_2  # 텍스트도 같은 층으로 배치
#
#             if "Wy" in name:  # ✅ Wy-T1, Wy-M1만 적용 (가로 길이 3)
#                 x_spacing = 6  # 중심 기준으로 6 간격
#                 x_start = center_x - ((num_cols - 1) * x_spacing) / 2
#
#             elif "LSAy" in name:  # ✅ LSAy-T1, LSAy-M1 위치 수정
#                 x_start = center_x - ((num_cols - 1) * x_offsets) / 2  # LSAy는 x축 중심 기준 배치
#                 x_spacing = x_offsets  # 기존 x_offsets 유지
#
#             else:
#                 x_spacing = x_offsets if isinstance(x_offsets, int) else None
#                 x_start = center_x - ((num_cols - 1) * x_spacing + width) / 2 if x_spacing else center_x  # 기본 가로 고려
#
#             if isinstance(x_offsets, list):  # ✅ 세로형 (Wx, LSAx, Wy)
#                 y_start = center_y + y_shift - ((num_rows - 1) * y_spacing) / 2
#                 for col in range(num_cols):
#                     x = center_x + x_offsets[col]
#                     for row in range(num_rows):
#                         y = y_start + row * y_spacing
#                         layout << add_stepper_rect_key((x, y), width, height, layer)
#             else:  # ✅ 가로형 (LSAy)
#                 for row in range(num_rows):
#                     y = center_y + y_shift + y_spacing[row]
#                     for col in range(num_cols):
#                         x = x_start + col * x_spacing
#                         layout << add_stepper_rect_key((x, y), width, height, layer)
#
#             # ✅ 텍스트 추가 (해당 층의 레이어 사용)
#             add_stepper_text(layout, name, center_x, center_y + y_shift, x_offset, y_offset, text_layer)


import gdsfactory as gf
from make.make_stepper import add_stepper_rect_key

# ✅ 레이어 설정 (1층: (1, 0), 2층: (2, 0))
stepper_layer_1 = (34, 0)
stepper_layer_2 = (37, 0)
text_layer_1 = (34, 0)
text_layer_2 = (37, 0)

# ✅ 기준 좌표 (왼쪽 상단 기준점)
center_x_WxT1, center_y_WxT1 = (-9450, 9300)

# ✅ 왼쪽 상단 스테퍼 키만 구성
stepper_configs = [
    ("Wx-T1", [-20, 0, 26], 8, 7, 3, (center_x_WxT1, center_y_WxT1), 4, 4, 0, 35),
    ("LSAx-T1", [-20, 0, 20], 8, 7, 3, (center_x_WxT1 + 201, center_y_WxT1), 4, 4, 0, 35),
    ("LSAy-T1", 8, [-20, 0, 20], 3, 7, (center_x_WxT1 + 201 + 197, center_y_WxT1), 4, 4, 0, 35),
    ("Wy-T1", 7, [-26, 0, 20], 3, 51, (center_x_WxT1 + 201, center_y_WxT1 - 196), 3, 4, -210, -5),
]

def add_stepper_text(layout, text, x, y, x_offset=0, y_offset=35, layer=(1, 0)):
    """Stepper 키 이름을 텍스트로 추가"""
    text_label = layout << gf.components.text(text=text, size=10, justify="center", layer=layer)
    text_label.move((x + x_offset, y + y_offset))

def stepper(layout):
    """왼쪽 상단의 Stepper 키 자동 배치 및 전체 감싸는 박스 추가"""
    for name, x_offsets, y_spacing, num_rows, num_cols, (center_x, center_y), width, height, x_offset, y_offset in stepper_configs:
        for layer, y_shift in [(stepper_layer_1, 0)]:  # ✅ 2층 생략
            text_layer = text_layer_1

            if "Wy" in name:
                x_spacing = 6
                x_start = center_x - ((num_cols - 1) * x_spacing) / 2

            elif "LSAy" in name:
                x_start = center_x - ((num_cols - 1) * x_offsets) / 2
                x_spacing = x_offsets

            else:
                x_spacing = x_offsets if isinstance(x_offsets, int) else None
                x_start = center_x - ((num_cols - 1) * x_spacing + width) / 2 if x_spacing else center_x

            if isinstance(x_offsets, list):
                y_start = center_y + y_shift - ((num_rows - 1) * y_spacing) / 2
                for col in range(num_cols):
                    x = center_x + x_offsets[col]
                    for row in range(num_rows):
                        y = y_start + row * y_spacing
                        layout << add_stepper_rect_key((x, y), width, height, layer)
            else:
                for row in range(num_rows):
                    y = center_y + y_shift + y_spacing[row]
                    for col in range(num_cols):
                        x = x_start + col * x_spacing
                        layout << add_stepper_rect_key((x, y), width, height, layer)

            add_stepper_text(layout, name, center_x, center_y + y_shift, x_offset, y_offset, text_layer)

    # ✅ 전체 스테퍼 그룹을 감싸는 박스 추가 (좌표: 기준점에서 이동)
    box_center_x = center_x_WxT1 + 201
    box_center_y = center_y_WxT1 - 100
    box_points = [
        (box_center_x - 350, box_center_y - 200),  # 좌하단
        (box_center_x + 350, box_center_y - 200),  # 우하단
        (box_center_x + 350, box_center_y + 200),  # 우상단
        (box_center_x - 350, box_center_y + 200),  # 좌상단
    ]
    layout.add_polygon(box_points, layer=(34, 1))

    # 2번째 포토마스크 스텝퍼 키
    for name, x_offsets, y_spacing, num_rows, num_cols, (center_x, center_y), width, height, x_offset, y_offset in stepper_configs:
        for layer, y_shift in [(stepper_layer_2, 0)]:  # ✅ 2층 생략
            text_layer = text_layer_2

            if "Wy" in name:
                x_spacing = 6
                x_start = center_x - ((num_cols - 1) * x_spacing) / 2

            elif "LSAy" in name:
                x_start = center_x - ((num_cols - 1) * x_offsets) / 2
                x_spacing = x_offsets

            else:
                x_spacing = x_offsets if isinstance(x_offsets, int) else None
                x_start = center_x - ((num_cols - 1) * x_spacing + width) / 2 if x_spacing else center_x

            if isinstance(x_offsets, list):
                y_start = center_y + y_shift - ((num_rows - 1) * y_spacing) / 2
                for col in range(num_cols):
                    x = center_x + x_offsets[col]
                    for row in range(num_rows):
                        y = y_start + row * y_spacing
                        layout << add_stepper_rect_key((x, y), width, height, layer)
            else:
                for row in range(num_rows):
                    y = center_y + y_shift + y_spacing[row]
                    for col in range(num_cols):
                        x = x_start + col * x_spacing
                        layout << add_stepper_rect_key((x, y), width, height, layer)

            add_stepper_text(layout, name, center_x, center_y + y_shift, x_offset, y_offset, text_layer)

    # ✅ 전체 스테퍼 그룹을 감싸는 박스 추가 (좌표: 기준점에서 이동)
    box_center_x = center_x_WxT1 + 201
    box_center_y = center_y_WxT1 - 100
    box_points = [
        (box_center_x - 350, box_center_y - 200),  # 좌하단
        (box_center_x + 350, box_center_y - 200),  # 우하단
        (box_center_x + 350, box_center_y + 200),  # 우상단
        (box_center_x - 350, box_center_y + 200),  # 좌상단
    ]
    layout.add_polygon(box_points, layer=(37, 1))


