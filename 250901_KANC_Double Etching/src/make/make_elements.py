from __future__ import annotations
from gdsfactory.cross_section import Section
from functools import partial
import numpy as np
import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.grating_couplers.grating_coupler_elliptical import (
    grating_taper_points,
    grating_tooth_points,
)
from gdsfactory.functions import DEG2RAD
from gdsfactory.typings import CrossSectionSpec, Floats, LayerSpec


gf.config.rich_output() #GDS 파일 시각화
layout = gf.Component('Top')

def grating_coupler_elliptical_trenches(
    taper_tip_width, wavelength, grating_line_width,
    polarization: str = "te",
    taper_length: float = 22,
    taper_angle: float = 39.8646,
    trenches_extra_angle: float = 30.0,
    fiber_angle: float = 15.0,
    neff: float = 2.0,  # Adjusted effective index
    ncladding: float = 1.0,  # Cladding index
    layer_trench: float = (34,1),
    p_start: int = 26,
    n_periods: int = 17,
    end_straight_length: float = 8,
    cross_section: CrossSectionSpec = "strip",
    **kwargs,
) -> Component:
    xs = gf.get_cross_section(cross_section, **kwargs)
    wg_width = xs.width
    # layer = xs.layer
    layer = (34,0)

    sthc = np.sin(fiber_angle * DEG2RAD)
    d = neff**2 - ncladding**2 * sthc**2
    a1 = wavelength * neff / d
    b1 = wavelength / np.sqrt(d)
    x1 = wavelength * ncladding * sthc / d

    a1 = round(a1, 3)
    b1 = round(b1, 3)
    x1 = round(x1, 3)

    period = float(a1 + x1)
    trench_line_width = period - grating_line_width

    c = gf.Component()

    for p in range(p_start, p_start + n_periods + 1):
        pts = grating_tooth_points(
            p * a1,
            p * b1,
            p * x1,
            width=trench_line_width,
            taper_angle=taper_angle + trenches_extra_angle,
        )
        c.add_polygon(pts, (34,3))

    p_taper = p_start - 1
    p_taper_eff = p_taper
    a_taper = a1 * p_taper_eff
    x_taper = x1 * p_taper_eff
    x_output = a_taper + x_taper - taper_length + grating_line_width / 2

    # Adjusted taper width
    taper_width = taper_tip_width  # New taper width value

    xmax = x_output + taper_length + n_periods * period + 3
    y = taper_width / 2 + np.tan(taper_angle / 2 * np.pi / 180) * xmax
    pts = [
        (x_output, -taper_width / 2),
        (x_output, +taper_width / 2),
        (xmax, +y),
        (xmax + end_straight_length, +y),
        (xmax + end_straight_length + 5, -y + 0.5),
        (xmax + end_straight_length + 5, -y),
        (xmax, -y),
    ]
    c.add_polygon(pts, layer)

    pts = [
        (x_output, -(taper_width+16) / 2),
        (x_output, +(taper_width+16) / 2),
        (xmax+25, +y+25),
        (xmax + end_straight_length+20, +y+25),
        (xmax + end_straight_length + 30, -y + 0.5-25),
        (xmax + end_straight_length + 30, -y-25),
        (xmax+25, -y-25),
    ]
    c.add_polygon(pts, (34,1))

    c.add_port(
        name="o1",
        center=(x_output, 0),
        width=taper_width,  # Adjusted taper width
        orientation=180,
        layer=layer,
        cross_section=xs,
    )
    c.info["period"] = float(np.round(period, 3))
    c.info["polarization"] = polarization
    c.info["wavelength"] = wavelength
    xs.add_bbox(c)

    x = np.round(taper_length + period * n_periods / 2, 3)
    c.add_port(
        name="o2",
        center=(x, 0),
        width=10,
        orientation=0,
        layer=layer,
        port_type=f"vertical_{polarization}",
    )
    return c


@gf.cell
def grating_coupler_elliptical_arbitrary(
    gaps: Floats = (0.1,) * 10,
    widths: Floats = (0.5,) * 10,
    taper_length: float = 26,
    taper_angle: float = 32.8646,
    wavelength: float = 1.554,
    fiber_angle: float = 2.0,
    nclad: float = 1.443,
    layer_slab: LayerSpec | None = "SLAB150",
    layer_grating: LayerSpec | None = None,
    taper_to_slab_offset: float = -3.0,
    polarization: str = "te",
    spiked: bool = True,
    bias_gap: float = 0,
    cross_section: CrossSectionSpec = "strip",
    period: float =0,
    n_periods: int = 0,
    taper_tip_width: float = 5,
    layer: float = (34,0),
    **kwargs,
) -> Component:
    r"""Grating coupler with parametrization based on Lumerical FDTD simulation.

    The ellipticity is derived from Lumerical knowledge base
    it depends on fiber_angle (degrees), neff, and nclad

    Args:
        gaps: list of gaps.
        widths: list of widths.
        taper_length: taper length from input.
        taper_angle: grating flare angle.
        wavelength: grating transmission central wavelength (um).
        fiber_angle: fibre angle in degrees determines ellipticity.
        nclad: cladding effective index to compute ellipticity.
        layer_slab: Optional slab.
        layer_grating: Optional layer for grating.
            by default None uses cross_section.layer.
            if different from cross_section.layer expands taper.
        taper_to_slab_offset: 0 is where taper ends.
        polarization: te or tm.
        spiked: grating teeth have spikes to avoid drc errors.
        bias_gap: etch gap (um).
            Positive bias increases gap and reduces width to keep period constant.
        cross_section: cross_section spec for waveguide port.
        kwargs: cross_section settings.

    https://en.wikipedia.org/wiki/Ellipse
    c = (a1 ** 2 - b1 ** 2) ** 0.5
    e = (1 - (b1 / a1) ** 2) ** 0.5
    print(e)

    .. code::

                      fiber

                   /  /  /  /
                  /  /  /  /

                _|-|_|-|_|-|___ layer
                   layer_slab |
            o1  ______________|

    """
    xs = gf.get_cross_section(cross_section, **kwargs)
    wg_width = xs.width
    layer_wg = (34,0)

    layer_grating = (34,1)
    sthc = np.sin(fiber_angle * DEG2RAD)

    # generate component
    c = gf.Component()
    c.info["polarization"] = polarization
    c.info["wavelength"] = wavelength

    # get the physical parameters needed to compute ellipses
    gaps = gf.snap.snap_to_grid(np.array(gaps) + bias_gap)
    widths = gf.snap.snap_to_grid(np.array(widths) - bias_gap)
    periods = [g + w for g, w in zip(gaps, widths)]
    neffs = [wavelength / p + nclad * sthc for p in periods]
    ds = [neff**2 - nclad**2 * sthc**2 for neff in neffs]
    a1s = [round(wavelength * neff / d, 3) for neff, d in zip(neffs, ds)]
    b1s = [round(wavelength / np.sqrt(d), 3) for d in ds]
    x1s = [round(wavelength * nclad * sthc / d, 3) for d in ds]
    xis = np.add(
        taper_length + np.cumsum(periods), -widths / 2
    )  # position of middle of each tooth
    ps = np.divide(xis, periods)

    # grating teeth
    for a1, b1, x1, p, width in zip(a1s, b1s, x1s, ps, widths):
        pts = grating_tooth_points(
            p * a1, p * b1, p * x1, width, taper_angle, spiked=spiked
        )
        c.add_polygon(pts, (34,3))

    # taper
    p = taper_length / periods[0]  # (gaps[0]+widths[0])
    a_taper = p * a1s[0]
    b_taper = p * b1s[0]
    x_taper = p * x1s[0]
    x_output = a_taper + x_taper - taper_length + widths[0] / 2

    taper_width = taper_tip_width

    # 기존의 직선형 폴리곤을 곡선형 폴리곤으로 변경
    taper_start_x = x_output  # Taper 시작 지점
    radius = taper_start_x + taper_length + n_periods * period + 10
    theta = taper_angle
    num_points = 50

    # 직선 폴리곤 생성
    points = [
        (x_output, -taper_width / 2),
        (x_output, taper_width / 2),
        (x_output + 10, taper_width / 2),
        (x_output + 10, -taper_width / 2),
    ]

    # 불필요한 부분 제거
    cut_x_position = x_output + 5  # 자를 x 위치
    new_points = [(x, y) for x, y in points if x > cut_x_position]

    # 곡선 폴리곤 추가
    for i in range(num_points + 1):
        angle = -theta / 2 + theta * i / num_points
        x = radius * np.cos(np.deg2rad(angle))
        y = radius * np.sin(np.deg2rad(angle))
        new_points.append((x, y))

    c.add_polygon(new_points, layer)

    # 직선 폴리곤 생성
    points = [
        (x_output, -(taper_width+16) / 2),
        (x_output, (taper_width+16) / 2),
        (x_output + 10, (taper_width+16) / 2),
        (x_output + 10, -(taper_width+16) / 2),
    ]

    # 불필요한 부분 제거
    cut_x_position = x_output + 5  # 자를 x 위치
    new_points = [(x, y) for x, y in points if x > cut_x_position]

    # 곡선 폴리곤 추가
    for i in range(num_points + 1):
        angle = -theta / 2 + theta * i / num_points
        x = radius * np.cos(np.deg2rad(angle))
        y = radius * np.sin(np.deg2rad(angle))
        if y < 0:
            new_points.append((x+16, y-20))
        else:
            new_points.append((x+16, y+20))

    c.add_polygon(new_points, (34,1))

    c.add_port(
        name="o1",
        center=(taper_start_x, 0),
        width=taper_width,
        orientation=180,
        layer=layer,
        cross_section=xs,
    )
    c.info["period"] = float(np.round(period, 3))
    c.info["polarization"] = polarization
    c.info["wavelength"] = wavelength
    xs.add_bbox(c)

    if layer_grating == layer_wg:
        pts = grating_taper_points(
            a_taper, b_taper, x_output, x_taper, taper_angle, wg_width=wg_width
        )
    else:
        pts = grating_taper_points(
            a_taper,
            b_taper,
            x_output,
            x_taper + np.sum(widths) + np.sum(gaps) + 1,
            taper_angle,
            wg_width=wg_width,
        )

    if layer_slab:
        slab_xmin = taper_length + taper_to_slab_offset
        slab_xmax = c.dxmax + 0.5
        slab_ysize = c.dysize + 2.0
        yslab = slab_ysize / 2

    xs.add_bbox(c)
    x = (taper_length + xis[-1]) / 2
    c.add_port(
        name="o2",
        center=(x, 0),
        width=10,
        orientation=0,
        layer=xs.layer,
        port_type=f"vertical_{polarization}",
    )
    # 127 um 범위 확인용 테스트 패턴
    circle = gf.components.circle(radius=127, layer=(30,0))
    circle = c << circle
    circle.move([1.5*taper_length,0])
    return c


@gf.cell
def grating_coupler_elliptical_arc(
    taper_tip_width, period, fill_factor,
    n_periods: int = 16,
    total_length: float= 16,
    taper_length: float = 31,
    **kwargs,
) -> Component:
    r"""Grating coupler with parametrization based on Lumerical FDTD simulation.

    The ellipticity is derived from Lumerical knowledge base
    it depends on fiber_angle (degrees), neff, and nclad

    Args:
        n_periods: number of grating periods.
        period: grating pitch in um.
        fill_factor: ratio of grating width vs gap.

    Keyword Args:
        taper_length: taper length from input.
        taper_angle: grating flare angle.
        wavelength: grating transmission central wavelength (um).
        fiber_angle: fibre angle in degrees determines ellipticity.
        neff: tooth effective index to compute ellipticity.
        nclad: cladding effective index to compute ellipticity.
        layer_slab: Optional slab.
        taper_to_slab_offset: where 0 is at the start of the taper.
        polarization: te or tm.
        spiked: grating teeth have spikes to avoid drc errors..
        bias_gap: etch gap (um).
            Positive bias increases gap and reduces width to keep period constant.
        cross_section: cross_section spec for waveguide port.
        kwargs: cross_section settings.

    .. code::

                      fiber

                   /  /  /  /
                  /  /  /  /

                _|-|_|-|_|-|___ layer
                   layer_slab |
            o1  ______________|

    """
    n_periods = int(round(total_length / period))
    widths = (period * fill_factor,) * n_periods
    gaps = (period * (1 - fill_factor),) * n_periods

    return grating_coupler_elliptical_arbitrary(gaps=gaps, widths=widths, **kwargs,period=period, n_periods = n_periods, taper_tip_width= taper_tip_width, taper_length=taper_length)

def make_box(layer, width_dic,type):
    c = gf.Component()

    if type ==1 :
        c.add_polygon([(-width_dic / 2, -width_dic / 2),
                       (width_dic / 2, -width_dic / 2),
                       (width_dic / 2, width_dic / 2),
                       (-width_dic / 2, width_dic / 2), ],
                      layer=layer)

        c.add_port(name='o1', center=[-width_dic / 2, 0], width=width_dic, orientation=180, layer=layer)
        c.add_port(name='o2', center=[0, width_dic / 2], width=width_dic, orientation=90, layer=layer)
        c.add_port(name='o3', center=[width_dic / 2, 0], width=width_dic, orientation=0, layer=layer)
        c.add_port(name='o4', center=[0, -width_dic / 2], width=width_dic, orientation=-90, layer=layer)

        return c

    elif type == 2 :
        c.add_polygon([(-width_dic, -width_dic / 2),
                       (width_dic, -width_dic /2),
                       (width_dic, width_dic / 2),
                       (-width_dic, width_dic /2), ],
                      layer=layer)

        c.add_port(name='o1', center=[-width_dic, 0], width=width_dic, orientation=180, layer=layer)
        c.add_port(name='o2', center=[0, width_dic / 2], width=width_dic*2, orientation=90, layer=layer)
        c.add_port(name='o3', center=[width_dic, 0], width=width_dic, orientation=0, layer=layer)
        c.add_port(name='o4', center=[0, -width_dic / 2], width=width_dic*2, orientation=-90, layer=layer)

        return c

    else :
        c.add_polygon([(-width_dic/2, -width_dic/2),
                       (width_dic/2, -width_dic/2),
                       (width_dic/2, width_dic/2 ),
                       (-width_dic/2, width_dic/2), ],
                      layer=layer)

        c.add_port(name='o1', center=[-width_dic/2, 0], width=width_dic, orientation=180, layer=layer)
        c.add_port(name='o2', center=[0, width_dic/2], width=width_dic, orientation=90, layer=layer)
        c.add_port(name='o3', center=[width_dic/2, 0], width=width_dic, orientation=0, layer=layer)
        c.add_port(name='o4', center=[0, -width_dic/2], width=width_dic, orientation=-90, layer=layer)

        return c




def make_path_mis(width, length, layer,misalign):
    c = gf.Component()
    c.add_polygon(
        [(0, -width / 2), (length, -width / 2), (length, width / 2), (0, width / 2)],
        layer=layer
    )
    c.add_port(
        name="o1",
        center=[0, 0+misalign],
        width=width,
        orientation=180,
        layer=layer
    )
    c.add_port(
        name="o2",
        center=[length, 0+misalign],
        width=width,
        orientation=0,
        layer=layer
    )

    return c

def make_taper_mis(left_width, right_width, length, layer,misalign):
    c = gf.Component()
    c.add_polygon(
        [(0, -left_width / 2), (length, -right_width / 2), (length, right_width / 2), (0, left_width / 2)],
        layer=layer
    )
    c.add_port(
        name="o1",
        center=[0, 0+misalign],
        width=left_width,
        orientation=180,
        layer=layer
    )
    c.add_port(
        name="o2",
        center=[length, 0],
        width=right_width,
        orientation=0,
        layer=layer
    )

    return c

def make_taper(left_width, right_width, length, layer):
    c = gf.Component()
    c.add_polygon(
        [(0, -left_width / 2), (length, -right_width / 2), (length, right_width / 2), (0, left_width / 2)],
        layer=layer
    )
    c.add_port(
        name="o1",
        center=[0, 0],
        width=left_width,
        orientation=180,
        layer=layer
    )
    c.add_port(
        name="o2",
        center=[length, 0],
        width=right_width,
        orientation=0,
        layer=layer
    )

    return c

def make_path(paths_list, layer, width):
    P = gf.Path()
    for path in paths_list:
        P += path

    result = gf.path.extrude(P, layer=layer, width=width)

    return result

# def Sbend_waveguide(length):
#     c = gf.Component()
#
#     S_wg = c << make_path(
#         [gf.path.straight(100), gf.path.arc(radius=10, angle=-90), gf.path.straight(25),
#          gf.path.arc(radius=10, angle=90), gf.path.straight(length)], layer=(1, 0), width=0.7)
#
#     # for port_name, port in S_wg.ports.items():
#     #     c.add_port(name=port_name, port=port)
#     c.add_port(name='o1', port=S_wg.ports[0])
#     c.add_port(name='o2', port=S_wg.ports[1])
#
#     return c

#유진스 파트

def make_mmicore(length, width, center, layer):

    # 새로운 컴포넌트 생성
    c = gf.Component()

    # 직사각형을 추가합니다. 중심을 기준으로 너비와 높이의 절반만큼의 위치를 계산합니다.
    c.add_polygon([(-length / 2, -width / 2),
            (length / 2, -width / 2),
            (length / 2, width / 2),
            (-length / 2, width / 2),],
        layer=layer)

    # 주의: (0,0)은 중심임. y값 주의
    # 입력 포트 left upper
    c.add_port(name='coreinput1', center=(-length / 2, 1.255), width=2, orientation=180, layer=layer)
    # 입력 포트 left lower
    c.add_port(name='coreinput2', center=(-length / 2, -1.255), width=2, orientation=180, layer=layer)

    # 출력 포트 right upper
    c.add_port(name='coreoutput1', center=(length / 2, 1.255), width=2, orientation=0, layer=layer)
    # 출력 포트 right lower
    c.add_port(name='coreoutput2', center=(length / 2, -1.255), width=2, orientation=0, layer=layer)

    return c

def make_MZI_Sbend_waveguide(width_um, layer):
    # S-bend 웨이브가이드의 복사본을 생성합니다.
    original_component = gf.components.bend_s(size=(32, 5), npoints=99, cross_section=gf.cross_section.strip(width = width_um, layer = layer), allow_min_radius_violation=False)
    c = original_component.copy()  # 복사본을 생성합니다.
    # 입력 포트를 추가합니다.
    c.add_port(name='input', center=(0, 0), width=width_um, orientation=180,layer=layer)
    # 출력 포트를 추가합니다.
    ###값 바뀔때마다 바꿔줘야함
    c.add_port(name='output', center=(32, 5), width=width_um, orientation=0,layer=layer)

    # 복사본에 레이어 정보 추가
    c.layer = (34, 0)

    return c


def make_mziflat(length, width, layer, center):
    c = gf.Component()

    # 직사각형을 추가합니다. 중심을 기준으로 너비와 높이의 절반만큼의 위치를 계산합니다.
    c.add_polygon([
        (-length / 2, -width / 2),
        (length / 2, -width / 2),
        (length / 2, width / 2),
        (-length / 2, width / 2),
    ], layer=layer)

    # 입력 포트
    c.add_port(name='input', center=(-length/2, 0), width=width, orientation=180, layer=layer)
    # 출력 포트
    c.add_port(name='output', center=(length/2, 0), width=width, orientation=0, layer=layer)

    return c

#경진 파트
def Sbend_waveguide(length, layer, width, wavelength, grating_line_width):
    c = gf.Component()

    # S-bend 경로 설정
    S_wg = c << make_path(
        [gf.path.straight(100), gf.path.arc(radius=10, angle=-90), gf.path.straight(25),
         gf.path.arc(radius=10, angle=90), gf.path.straight(length)], layer=layer, width=width)

    # 포트 설정
    c.add_port(name='o1', port=S_wg.ports[0])
    c.add_port(name='o2', port=S_wg.ports[1])
    # c.add_port(
    #     name="o2",
    #     center=[117.134 + length, -45],
    #     width=width,
    #     orientation=0,
    #     layer=layer
    # )

    GC1 = c << grating_coupler_elliptical_trenches(width, wavelength, grating_line_width)

    GC1.mirror_x()
    S_wg.mirror_x()
    S_wg.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True)
    return c

# 강석이형 CROW 구조에 사용
def make_polygon(width, length, layer):
    c = gf.Component()
    c.add_polygon([(0,0),(length,0),(length,width),(0,width)], layer)
    c.add_port(
        name="o1", center=[0, width / 2], width=width, orientation=180, layer=layer
    )
    c.add_port(
        name="o2", center=[length, width / 2], width=width, orientation=0, layer=layer
    )
    c.add_port(
        name='o3', center=[length/2, width], width=width, orientation=90, layer=layer
    )
    c.add_port(
        name='o4', center=[length/2, 0], width=width, orientation=270, layer=layer
    )
    c.add_port(
        name='o5', center=[0, width/2], width=width, orientation=0, layer=layer
    )
    return c


@gf.cell
def grating_coupler_standard(
    gaps: Floats = (0.3,) * 20,
    widths: Floats = (0.4,) * 20,
    taper_length: float = 38.7,
    taper_angle: float = 22.8646,
    wavelength: float = 1.31,
    fiber_angle: float = 8.0,
    nclad: float = 1.443,
    polarization: str = "te",
    spiked: bool = True,
    bias_gap: float = 0,
    cross_section: CrossSectionSpec = "strip",
    period: float = 0,
    fill_factor: float = 0.5,
    n_periods: int = 0,
    total_length: float = 16,
    grating_shift: float = 70.0,
    taper_tip_width: float = 0.7,
    port_width_o1: float = None,
    layer: LayerSpec = (34, 0),
    layer_box: LayerSpec = (34, 1),
    layer_grating: LayerSpec = (34, 3),
    fiber_y_offset: float = 8.5,
    slab_height: float = 17.0,
    **kwargs,
) -> Component:
    c = gf.Component()
    kwargs.pop("fill_factor", None)
    xs = gf.get_cross_section(cross_section, **kwargs)
    wg_width = taper_tip_width

    sthc = np.sin(fiber_angle * DEG2RAD)

    if period > 0 and 0 < fill_factor < 1:
        n_periods = int(round(total_length / period)) if n_periods == 0 else n_periods
        widths = (period * fill_factor,) * n_periods
        gaps = (period * (1 - fill_factor),) * n_periods

    periods = [g + w for g, w in zip(gaps, widths)]
    neffs = [wavelength / p + nclad * sthc for p in periods]
    ds = [neff**2 - nclad**2 * sthc**2 for neff in neffs]
    a1s = [round(wavelength * neff / d, 3) for neff, d in zip(neffs, ds)]
    b1s = [round(wavelength / np.sqrt(d), 3) for d in ds]
    x1s = [round(wavelength * nclad * sthc / d, 3) for d in ds]
    xis = np.add(taper_length + np.cumsum(periods), -np.array(widths) / 2)
    ps = np.divide(xis, periods)

    x_shift = grating_shift

    # Grating teeth
    for a1, b1, x1, p, width in zip(a1s, b1s, x1s, ps, widths):
        pts = grating_tooth_points(-p * a1, p * b1, -p * x1, width, taper_angle, spiked=spiked)
        pts = [(x + x_shift, y + fiber_y_offset) for (x, y) in pts]
        c.add_polygon(pts, layer_grating)

    # Slab triangle (mode filter)
    triangle = [
        (0, 0),
        (2, 0),
        (2, slab_height),
    ]
    c.add_polygon(triangle, layer)

    # Taper rectangle
    taper_start_x = 12
    taper_end_x = taper_start_x + taper_length
    rect = [
        (2, 0),
        (2, slab_height),
        (taper_start_x, slab_height),
        (taper_start_x, 0),
    ]
    c.add_polygon(rect, layer)

    # Linear taper
    taper = [
        (taper_start_x, 0),
        (taper_start_x, slab_height),
        (taper_end_x, fiber_y_offset + wg_width / 2),
        (taper_end_x, fiber_y_offset - wg_width / 2),
    ]
    c.add_polygon(taper, layer)

    # 기준 파라미터
    clad_offset = 8
    clad_total_width = wg_width + 16

    # 1번: Slab triangle 전체 감싸는 직사각형 box
    slab_clad = [
        (-10, fiber_y_offset - clad_total_width / 2 - clad_offset),
        (2, fiber_y_offset - clad_total_width / 2 - clad_offset),
        (2, fiber_y_offset + clad_total_width / 2 + clad_offset),
        (-7, fiber_y_offset + clad_total_width / 2 + clad_offset),
    ]
    c.add_polygon(slab_clad, layer_box)

    # 2. Taper rectangle box
    taper_rect_clad = [
        (2, fiber_y_offset - clad_total_width / 2 - clad_offset),
        (taper_start_x, fiber_y_offset - clad_total_width / 2 - clad_offset),
        (taper_start_x, fiber_y_offset + clad_total_width / 2 + clad_offset),
        (2, fiber_y_offset + clad_total_width / 2 + clad_offset),
    ]
    c.add_polygon(taper_rect_clad, layer_box)

    # 3. 기존 taper 사다리꼴 (조정 필요 없음 – 그대로 유지)
    taper_clad = [
        (taper_start_x, fiber_y_offset - clad_total_width / 2 - clad_offset),
        (taper_end_x, fiber_y_offset - clad_total_width / 2),
        (taper_end_x, fiber_y_offset + clad_total_width / 2),
        (taper_start_x, fiber_y_offset + clad_total_width / 2 + clad_offset),
    ]
    c.add_polygon(taper_clad, layer_box)

    # 포트 설정
    c.add_port(
        name="o1",
        center=(taper_end_x, fiber_y_offset),
        width=port_width_o1 if port_width_o1 else wg_width,
        orientation=0,
        layer=layer,
        cross_section=xs,
    )
    c.add_port(
        name="o2",
        center=(0, fiber_y_offset),
        width=taper_tip_width,
        orientation=180,
        layer=layer,
        cross_section=xs,
    )

    return c


