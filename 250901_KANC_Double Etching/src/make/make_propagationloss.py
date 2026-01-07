import numpy as np
from make import make_elements
import gdsfactory as gf
from gdsfactory.path import straight, arc


def make_simple_propagation(loops, bend_radius, core_width, rotate_up):
    c = gf.Component()
    # propagation loss
    custom_xs = gf.cross_section.cross_section(width=core_width, layer=(34, 0))
    bend_euler_custom = gf.components.bend_circular(radius=bend_radius, cross_section=custom_xs)
    propa_loss = c << gf.components.spiral(length=0, bend=bend_euler_custom, straight='straight',
                                           cross_section=custom_xs, spacing=8, n_loops=loops)
    if rotate_up == True:
        propa_loss.rotate(90)
    else:
        propa_loss.rotate(270)

    port_o1_path = [gf.path.arc(radius=200, angle=-90),
                    gf.path.straight(200), ]
    port_o1_to_wg = c << make_elements.make_path(port_o1_path, layer=(34, 0), width=core_width)

    c.add_port(name='o1', port=port_o1_to_wg.ports[0])
    c.add_port(name='o2', port=port_o1_to_wg.ports[1])

    port_o2_path = [gf.path.straight(300),
                    gf.path.arc(radius=200, angle=90),
                    gf.path.straight(200), ]

    port_o2_to_wg = c << make_elements.make_path(port_o2_path, layer=(34, 0), width=core_width)

    c.add_port(name='o1', port=port_o2_to_wg.ports[0])
    c.add_port(name='o2', port=port_o2_to_wg.ports[1])

    port_o1_to_wg.connect('o1', propa_loss.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    port_o2_to_wg.connect('o1', propa_loss.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # propa_loss.connect('o1', port_o1_to_wg.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    # propa_loss.connect('o2', port_o2_to_wg.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    custom_xs = gf.cross_section.cross_section(width=16 + core_width, layer=(34, 1))
    bend_euler_custom = gf.components.bend_circular(radius=bend_radius, cross_section=custom_xs)
    propa_loss = c << gf.components.spiral(length=0, bend=bend_euler_custom, straight='straight',
                                           cross_section=custom_xs, spacing=8, n_loops=loops)
    if rotate_up == True:
        propa_loss.rotate(90)
    else:
        propa_loss.rotate(270)

    port_o1_path = [gf.path.arc(radius=200, angle=-90),
                    gf.path.straight(200), ]
    port_o1_to_wg = c << make_elements.make_path(port_o1_path, layer=(34, 1), width=16 + core_width)

    c.add_port(name='o1', port=port_o1_to_wg.ports[0])
    c.add_port(name='o2', port=port_o1_to_wg.ports[1])

    port_o2_path = [gf.path.straight(300),
                    gf.path.arc(radius=200, angle=90),
                    gf.path.straight(200), ]

    port_o2_to_wg = c << make_elements.make_path(port_o2_path, layer=(34, 1), width=16 + core_width)

    c.add_port(name='o1', port=port_o2_to_wg.ports[0])
    c.add_port(name='o2', port=port_o2_to_wg.ports[1])

    port_o1_to_wg.connect('o1', propa_loss.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    port_o2_to_wg.connect('o1', propa_loss.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    GC1 = c << make_elements.grating_coupler_elliptical_arc(core_width, 0.87, 0.5)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(core_width, 0.87, 0.5)

    # propa_loss.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC1.connect('o1', port_o1_to_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    GC2.connect('o1', port_o2_to_wg.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # GC1.move([0, 10])
    # GC2.move([0, -10])

    if rotate_up == True:
        GC1.move([-10, 0])
        GC2.move([10, 0])
    else:
        GC1.move([10, 0])
        GC2.move([-10, 0])

    c.flatten()

    return c


PROP_LENGTH = {
    1: 0.422,
    4: 0.847,
    8: 1.481,
    12: 2.192,
    16: 2.979,
    20: 3.843,
    24: 4.784
}


def find_propagation_length(loops: int) -> float:
    """Return propagation length [cm] for a given number of loops."""
    try:
        return PROP_LENGTH[loops]
    except KeyError:
        raise ValueError(
            f"Supported loop counts are {list(PROP_LENGTH)}; got {loops}."
        )


def make_simple_propagation_full(loops, bend_radius, core_width, rotate_up):
    c = gf.Component()

    # 파라미터 설정
    width_rib = 7  # Rib waveguide 폭
    strip_length = 40  # Strip 구간 길이
    taper_length = 60  # Taper 구간 길이
    wide_length = 100  # Wide(rib) 구간 길이
    # 총 200μm = 40 + 60 + 100

    # === CORE LAYER (34, 0) ===
    # Spiral 생성
    custom_xs_rib = gf.cross_section.cross_section(width=width_rib, layer=(34, 4))
    bend_euler_rib = gf.components.bend_circular(radius=bend_radius, cross_section=custom_xs_rib)
    propa_loss = c << gf.components.spiral(length=0, bend=bend_euler_rib, straight='straight',
                                           cross_section=custom_xs_rib, spacing=8, n_loops=loops)

    if rotate_up == True:
        propa_loss.rotate(90)
    else:
        propa_loss.rotate(270)

    # Input path: Arc + Wide 구간 (rib 너비로 생성)
    port_o1_path = [gf.path.arc(radius=200, angle=-90),
                    gf.path.straight(wide_length)]  # Wide 구간만 rib 너비
    port_o1_to_wg = c << make_elements.make_path(port_o1_path, layer=(34, 4), width=width_rib)

    # Taper 구간 (60μm): rib → core_width
    taper_in = c << make_elements.make_taper(left_width=width_rib, right_width=core_width,
                                             length=taper_length, layer=(34, 4))

    # Strip 구간 (40μm)
    strip_in = c << make_elements.make_path([gf.path.straight(strip_length)],
                                            layer=(34, 4), width=core_width)

    # Output path: Wide 구간 (rib 너비로 생성)
    port_o2_path = [gf.path.straight(300),
                    gf.path.arc(radius=200, angle=90),
                    gf.path.straight(wide_length)]  # Wide 구간만 rib 너비
    port_o2_to_wg = c << make_elements.make_path(port_o2_path, layer=(34, 4), width=width_rib)

    # Output taper (60μm): rib → core_width
    taper_out = c << make_elements.make_taper(left_width=width_rib, right_width=core_width,
                                              length=taper_length, layer=(34, 4))

    # Output strip (40μm)
    strip_out = c << make_elements.make_path([gf.path.straight(strip_length)],
                                             layer=(34, 4), width=core_width)

    # Core layer connections - 너비 맞춤
    # Input side: spiral → wide path → taper → strip → GC
    port_o1_to_wg.connect('o1', propa_loss.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_in.connect('o1', port_o1_to_wg.ports['o2'])  # rib width끼리 연결
    strip_in.connect('o1', taper_in.ports['o2'])  # core_width끼리 연결

    # Output side: spiral → wide path → taper → strip → GC
    port_o2_to_wg.connect('o1', propa_loss.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_out.connect('o1', port_o2_to_wg.ports['o2'])  # rib width끼리 연결
    strip_out.connect('o1', taper_out.ports['o2'])  # core_width끼리 연결

    # === CLADDING LAYER (34, 1) ===
    custom_xs_clad = gf.cross_section.cross_section(width=16 + core_width, layer=(34, 1))
    bend_euler_clad = gf.components.bend_circular(radius=bend_radius, cross_section=custom_xs_clad)
    propa_loss_clad = c << gf.components.spiral(length=0, bend=bend_euler_clad, straight='straight',
                                                cross_section=custom_xs_clad, spacing=8, n_loops=loops)

    if rotate_up == True:
        propa_loss_clad.rotate(90)
    else:
        propa_loss_clad.rotate(270)

    # Cladding paths - 일정한 clad_width 유지
    clad_width = 16 + core_width

    # Input cladding
    port_o1_path_clad = [gf.path.arc(radius=200, angle=-90),
                         gf.path.straight(wide_length)]
    port_o1_to_wg_clad = c << make_elements.make_path(port_o1_path_clad, layer=(34, 1), width=clad_width)

    taper_in_clad = c << make_elements.make_taper(left_width=clad_width, right_width=clad_width,
                                                  length=taper_length, layer=(34, 1))
    strip_in_clad = c << make_elements.make_path([gf.path.straight(strip_length)],
                                                 layer=(34, 1), width=clad_width)

    # Output cladding
    port_o2_path_clad = [gf.path.straight(300),
                         gf.path.arc(radius=200, angle=90),
                         gf.path.straight(wide_length)]
    port_o2_to_wg_clad = c << make_elements.make_path(port_o2_path_clad, layer=(34, 1), width=clad_width)

    taper_out_clad = c << make_elements.make_taper(left_width=clad_width, right_width=clad_width,
                                                   length=taper_length, layer=(34, 1))
    strip_out_clad = c << make_elements.make_path([gf.path.straight(strip_length)],
                                                  layer=(34, 1), width=clad_width)

    port_o1_to_wg_clad.connect('o1', propa_loss_clad.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_in_clad.connect('o1', port_o1_to_wg_clad.ports['o2'])
    strip_in_clad.connect('o1', taper_in_clad.ports['o2'])

    port_o2_to_wg_clad.connect('o1', propa_loss_clad.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)
    taper_out_clad.connect('o1', port_o2_to_wg_clad.ports['o2'])
    strip_out_clad.connect('o1', taper_out_clad.ports['o2'])

    GC1 = c << make_elements.grating_coupler_elliptical_arc(core_width, 0.87, 0.5)
    GC2 = c << make_elements.grating_coupler_elliptical_arc(core_width, 0.87, 0.5)

    GC1.connect('o1', strip_in.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)  # strip의 반대편 포트
    GC2.connect('o1', strip_out.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)

    if rotate_up == True:
        GC1.move([-10, 0])
        GC2.move([10, 0])
    else:
        GC1.move([10, 0])
        GC2.move([-10, 0])

    c.flatten()
    return c


def make_simple_propagation_shallow(loops, bend_radius, core_width, rotate_up):
    c = gf.Component()

    # === SHALLOW LAYER (36, 0) - 순수 Strip 구조 ===
    # Spiral 생성 (shallow layer)
    custom_xs = gf.cross_section.cross_section(width=core_width, layer=(36, 0))
    bend_euler_custom = gf.components.bend_circular(radius=bend_radius, cross_section=custom_xs)
    propa_loss = c << gf.components.spiral(length=0, bend=bend_euler_custom, straight='straight',
                                           cross_section=custom_xs, spacing=8, n_loops=loops)

    if rotate_up == True:
        propa_loss.rotate(90)
    else:
        propa_loss.rotate(270)

    # Input path: 원본과 동일한 구조 (Arc → Straight)
    port_o1_path = [gf.path.arc(radius=200, angle=-90),
                    gf.path.straight(200)]
    port_o1_to_wg = c << make_elements.make_path(port_o1_path, layer=(36, 0), width=core_width)

    # Output path
    port_o2_path = [gf.path.straight(300),
                    gf.path.arc(radius=200, angle=90),
                    gf.path.straight(200)]
    port_o2_to_wg = c << make_elements.make_path(port_o2_path, layer=(36, 0), width=core_width)

    # Connections
    port_o1_to_wg.connect('o1', propa_loss.ports['o2'], allow_layer_mismatch=True, allow_width_mismatch=True)
    port_o2_to_wg.connect('o1', propa_loss.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)

    # === GRATING COUPLERS ===
    GC1 = c << make_elements.grating_coupler_elliptical_arc(core_width, 0.87, 0.5, layer=(36, 0))
    GC2 = c << make_elements.grating_coupler_elliptical_arc(core_width, 0.87, 0.5, layer=(36, 0))

    # GC 연결
    GC1.connect('o1', port_o1_to_wg.ports['o2'], allow_width_mismatch=True)
    GC2.connect('o1', port_o2_to_wg.ports['o2'], allow_width_mismatch=True)

    # GC 위치 조정
    if rotate_up == True:
        GC1.move([-10, 0])
        GC2.move([10, 0])
    else:
        GC1.move([10, 0])
        GC2.move([-10, 0])

    # 포트 등록
    c.add_port("o1", GC1.ports["o1"])
    c.add_port("o2", GC2.ports["o1"])

    c.flatten()
    return c