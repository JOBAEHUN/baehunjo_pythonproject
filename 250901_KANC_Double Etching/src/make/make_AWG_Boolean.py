import numpy as np
import gdsfactory as gf
from make import make_elements
from make import make_grating
from make import make_AWG_gratingcoupler

#(1) C1 = 200, C2 = 400 인 경우
# def make_Boolean():

#     c = gf.Component()
#
#     #Circle 정의
#     c = gf.Component()
#     c1 = c << gf.components.circle(radius=200)
#     c2 = c << gf.components.circle(radius=400)
#     c1.move((700,0))
#     c2.move((500,0))
#
#
#     #Triangle 정의
#     T1 = c << gf.components.triangle(x=600, xtop=0, y=346.4101615137755, ybot=0, layer='WG').copy()
#     T2 = c << gf.components.triangle(x=600, xtop=0, y=346.4101615137755, ybot=0, layer='WG').copy()
#     T1.rotate(180)
#     T1.mirror_y()
#     T2.rotate(180)
#     T1.move((900,0))
#     T2.move((900, 0))
#
#     T3 = c << gf.components.triangle(x=300, xtop=0, y=173.2050807568877, ybot=0, layer='WG').copy()
#     T4 = c << gf.components.triangle(x=300, xtop=0, y=173.2050807568877, ybot=0, layer='WG').copy()
#     T3.rotate(180)
#     T3.mirror_y()
#     T4.rotate(180)
#     T3.move((600,0))
#     T4.move((600, 0))
#
#     #불리언 연산
#     b1 = gf.boolean(T1, c2, operation="A-B", layer=(1, 0))
#     b2 = gf.boolean(T3, c1, operation="A-B", layer=(1, 0))
#     b3 = gf.boolean(b1,b2, operation="or", layer=(1, 0))
#     c = gf.boolean(T1, b3, operation="A-B", layer=(1, 0))
#
#     # # # c 컴포넌트에 'input' 포트를 추가하는 경우
#     # port_input = Port(
#     #     name="input",
#     #     center=(500, 0),  # 포트의 중심 좌표 (예: (100, 0))
#     #     width=1,  # 포트의 폭 (예: 10)
#     #     orientation=0,  # 포트 방향 (0: 오른쪽, 90: 위쪽, 180: 왼쪽, 270: 아래쪽)
#     #     layer=(1, 0)
#     # )
#     # c.add_port(port_input)
#
#     #복제
#     c_clone = c.copy()
#     c_clone.name = "c2"
#     clone_circle = c << c_clone
#     clone_circle.rotate(-180)
#     clone_circle.mirror_x()
#
#
#
#
#     return c

#(0) 포트 설정
# def get_bbox_from_ref(ref):
#     """
#     주어진 ComponentReference(ref)의 변환이 반영된 폴리곤들을 기반으로
#     (min_x, min_y, max_x, max_y) 형태의 바운딩 박스를 계산합니다.
#     """
#     # by_spec=True로 변환이 반영된 폴리곤 정보를 가져옴
#     polys = ref.get_polygons(by_spec=True)
#     # polys는 리스트 형태의 np.ndarray, 모든 점들을 하나의 배열로 합침
#     all_points = np.concatenate(polys, axis=0)
#     min_xy = np.min(all_points, axis=0)
#     max_xy = np.max(all_points, axis=0)
#     return (min_xy[0], min_xy[1], max_xy[0], max_xy[1])
#
# def add_two_output_ports(ref, port_gap=50, port_width=2, layer=(34,0)):
#     """
#     ref: 상위 컴포넌트에 추가된 ComponentReference
#     port_gap: 두 포트 사이의 간격 (예: 50)
#     port_width: 포트 폭
#     layer: 포트가 속할 레이어
#     """
#     # ref의 바운딩 박스를 계산
#     bb = get_bbox_from_ref(ref)  # (min_x, min_y, max_x, max_y)
#     center_y = (bb[1] + bb[3]) / 2
#     right_x = bb[2]
#     # 포트1: 오른쪽 가장자리, 위쪽에 배치
#     p1 = Port(
#         name="o1",
#         center=(right_x, center_y + port_gap/2),
#         width=port_width,
#         orientation=0,
#         layer=layer
#     )
#     # 포트2: 오른쪽 가장자리, 아래쪽에 배치
#     p2 = Port(
#         name="o2",
#         center=(right_x, center_y - port_gap/2),
#         width=port_width,
#         orientation=0,
#         layer=layer
#     )
#     ref.add_port(p1)
#     ref.add_port(p2)


# #(1) C1 = 115, C2 = 230 인 경우
# def make_Boolean():
#     top = gf.Component("top")
#     c = gf.Component("c_internal")
#
#     #Circle 정의
#     c1 = c << gf.components.circle(radius=115,layer=(34,0))
#     c2 = c << gf.components.circle(radius=230,layer=(34,0))
#     c1.move((115,0))
#     c2.move((500,0))
#
#
#     # #Triangle 정의
#     T1 = c << gf.components.triangle(x=345, xtop=0, y=199.1858428704209, ybot=0, layer=(34, 0)).copy()
#     T2 = c << gf.components.triangle(x=345, xtop=0, y=199.1858428704209, ybot=0, layer=(34, 0)).copy()
#     T1.rotate(180)
#     T1.mirror_y()
#     T2.rotate(180)
#     T1.move((230,0))
#     T2.move((230, 0))
#
#     T3 = c << gf.components.triangle(x=172.5, xtop=0, y=99.59292143521044 , ybot=0, layer=(34, 0)).copy()
#     T4 = c << gf.components.triangle(x=172.5, xtop=0, y=99.59292143521044 , ybot=0, layer=(34, 0)).copy()
#     T3.rotate(180)
#     T3.mirror_y()
#     T4.rotate(180)
#     T3.move((57.5,0))
#     T4.move((57.5, 0))
#
#     #불리언 연산
#     b1 = gf.boolean(T1, c2, operation="A-B", layer=(34, 0))
#     b2 = gf.boolean(T3, c1, operation="A-B", layer=(34, 0))
#     b3 = gf.boolean(b1,b2, operation="or", layer=(34, 0))
#     c_boolean = gf.boolean(T1, b3, operation="A-B", layer=(34, 0))
#     ref_c = top << c_boolean
#     ref_c.move((-20, -245.999))


    # #복제
    # c_clone1 = c_boolean.copy()
    # c_clone2 = c_boolean.copy()
    # c_clone3 = c_boolean.copy()
    #
    #
    #
    # clone_circle1 = top << c_clone1
    # clone_circle2 = top << c_clone2
    # clone_circle3 = top << c_clone3
    #
    #
    # clone_circle1.rotate(-180)
    # clone_circle1.mirror_x()
    # clone_circle1.move((-20, -245.999))
    #
    # clone_circle2.move((-20, 915.24))
    #
    # clone_circle3.rotate(-180)
    # clone_circle3.mirror_x()
    # clone_circle3.move((-20, 915.24)


#(1) C1 = 50, C2 = 100 인 경우
def make_Boolean(cell_name="top"):
    top = gf.Component(cell_name)
    # c = gf.Component("c_internal")
    c = gf.Component(f"c_internal_{cell_name}")
    #Circle 정의
    c1 = c << gf.components.circle(radius=25,layer=(34,0))
    c2 = c << gf.components.circle(radius=50,layer=(34,0))
    c1.move((25,0))


    # #Triangle 정의
    T1 = c << gf.components.triangle(x=75, xtop=0, y=43.30127018922193, ybot=0, layer=(34, 0)).copy()
    T2 = c << gf.components.triangle(x=75, xtop=0, y=43.30127018922193, ybot=0, layer=(34, 0)).copy()
    T1.rotate(180)
    T1.mirror_y()
    T2.rotate(180)
    T1.move((50,0))
    T2.move((50, 0))

    T3 = c << gf.components.triangle(x=37.5, xtop=0, y=21.65063509461097 , ybot=0, layer=(34, 0)).copy()
    T4 = c << gf.components.triangle(x=37.5, xtop=0, y=21.65063509461097 , ybot=0, layer=(34, 0)).copy()
    T3.rotate(180)
    T3.mirror_y()
    T4.rotate(180)
    T3.move((12.5,0))
    T4.move((12.5, 0))

    #불리언 연산
    b1 = gf.boolean(T1, c2, operation="A-B", layer=(34, 0))
    b2 = gf.boolean(T3, c1, operation="A-B", layer=(34, 0))
    b3 = gf.boolean(b1,b2, operation="or", layer=(34, 0))
    c_boolean = gf.boolean(T1, b3, operation="A-B", layer=(34, 0))
    ref_c = top << c_boolean
    ref_c.move((-20,-246.752))
    #
    #
    # #복제
    c_clone1 = c_boolean.copy()
    c_clone2 = c_boolean.copy()
    c_clone3 = c_boolean.copy()



    clone_circle1 = top << c_clone1
    clone_circle2 = top << c_clone2
    clone_circle3 = top << c_clone3


    clone_circle1.rotate(-180)
    clone_circle1.mirror_x()
    clone_circle1.move((-20, -246.752))

    clone_circle2.move((-20, 65.648))

    clone_circle3.rotate(-180)
    clone_circle3.mirror_x()
    clone_circle3.move((-20, 65.648))

    return top

