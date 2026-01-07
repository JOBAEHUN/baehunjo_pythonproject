import kfactory as kf
from kfactory.utils.fill import fill_tiled
import gdsfactory as gf
# from layout import layout_propagation_straight, layout_adiabatic_coupler, layout_edgecoupler,layout_grating,layout_propagationloss, layout_bendingloss, layout_MZIMMI,layout_Ringmicro,layout_crow,layout_bendingloss_edge,layout_linespace,layout_MZIMMI_edge,layout_taper_for_poly

from layout import  layout_InterLayer_GC, layout_edgecoupler, layout_stepper, layout_grating,layout_edgecoupler,layout_taper_for_poly,layout_adiabatic_coupler,layout_PCM, layout_AWG, layout_MMI

# import pya

layout = gf.Component()

layout.add_polygon([(-10000,10000),(10000,10000),(10000,-10000),(-10000,-10000)], layer=(82,0))


# layout_adiabatic_coupler.adiabatic_coupler(layout)
# layout_edgecoupler.edge_coupler(layout)
layout_grating.grating(layout)
# layout_stepper.stepper(layout)
# layout_InterLayer_GC.InterLayer_GC(layout)
# layout_PCM.PCM_Strip(layout)
# layout_PCM.PCM_Rib(layout)
# layout_taper_for_poly.taper_for_poly(layout)
# layout_AWG.AWG(layout)
# layout_AWG.Boolean(layout)
# layout_MMI.make_8x8_GC_MMI(layout)
# layout_MMI.make_4x4_GC_MMI(layout)
# layout_MMI.make_2x2_GC_MMI(layout)


# fc = kf.KCell()
# fc.shapes(fc.kcl.layer(2, 0)).insert(kf.kdb.DBox(2, 1))
# # fc.shapes(fc.kcl.layer(3, 0)).insert(kf.kdb.DBox(2, -0.5, 4, 0.5))
#
# fill_tiled(
#     layout,
#     fc,
#     [(kf.kdb.LayerInfo(82, 0), 0)],
#     exclude_layers=[
#         (kf.kdb.LayerInfo(34, 1), 3),
#         (kf.kdb.LayerInfo(34, 0), 3),
#         (kf.kdb.LayerInfo(2, 0), 0), (kf.kdb.LayerInfo(36, 0), 3), (kf.kdb.LayerInfo(36, 1), 3), (kf.kdb.LayerInfo(34, 4), 3), (kf.kdb.LayerInfo(34, 5), 3), (kf.kdb.LayerInfo(37, 0), 3), (kf.kdb.LayerInfo(37, 1), 3)
#     ],
#     x_space=1,
#     y_space=2,
# )
#
# fc.layout().update()
layout.show()

# gds_file = "component.gds"
# layout.write_gds(gds_file)
#
# ly = pya.Layout()
# ly.read("./component.gds")
#
# dss = pya.DeepShapeStore()
#
# rA = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(82, 0)), dss)
# rB = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(34, 0)), dss)
# rC = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(34, 1)), dss)
# rD = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(34, 3)), dss)
# rE = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(36, 0)), dss)
# rF = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(36, 1)), dss)
# rG = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(34, 4)), dss)
# rH = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(34, 5)), dss)
# rI = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(37, 0)), dss)
# tile = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(2,0)), dss)
#
# # 1번 포토마스크
# # chrome_part = rB + rG + rF + tile
# chrome_part = rB + rG + rF + tile
# ly.top_cell().shapes(ly.layer(39, 0)).insert(chrome_part)
#
# # 2번 포토마스크
# chrome_part0 = rA - rF
# ly.top_cell().shapes(ly.layer(41, 0)).insert(chrome_part0)
# r0 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(41, 0)), dss)
#
# chrome_part1 = r0 - tile
# ly.top_cell().shapes(ly.layer(41, 1)).insert(chrome_part1)
# r00 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(41, 1)), dss)
#
# chrome_part2 = r00 - rG
# ly.top_cell().shapes(ly.layer(40, 0)).insert(chrome_part2)
# r1 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(40, 0)), dss)
#
# chrome_part3 = r1 + rE
# ly.top_cell().shapes(ly.layer(40, 1)).insert(chrome_part3)
# r2 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(40, 1)), dss)
#
# # 스트립 GC 날개
# chrome_part4 = rB & rD
# ly.top_cell().shapes(ly.layer(40, 2)).insert(chrome_part4)
# r3 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(40, 2)), dss)
#
# # 립 GC 날개
# chrome_part5 = rD & rG
# ly.top_cell().shapes(ly.layer(40, 3)).insert(chrome_part5)
# r4 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(40, 3)), dss)
#
# chrome_part6 = r2 - r3
# ly.top_cell().shapes(ly.layer(40, 4)).insert(chrome_part6)
# r5 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(40, 4)), dss)
#
# chrome_part7 = r5 - r4
# ly.top_cell().shapes(ly.layer(40, 5)).insert(chrome_part7)
# r6 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(40, 5)), dss)
#
# # 스텝퍼 키 반전
# chrome_part8 = r6 - rI
# ly.top_cell().shapes(ly.layer(40, 6)).insert(chrome_part8)
# r7 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(40, 6)), dss)
#
# # chrome_part9 = r7 - tile
# # ly.top_cell().shapes(ly.layer(40, 7)).insert(chrome_part9)
# # # r8 = pya.Region(ly.top_cell().begin_shapes_rec(ly.layer(40, 7)), dss)
#
# # final2 = r8
#
# # ly.delete_layer([2,0])
# ly.delete_layer([30,0])
# ly.delete_layer([34,0])
# ly.delete_layer([34,1])
# ly.delete_layer([34,3])
# ly.delete_layer([34,4])
# ly.delete_layer([34,5])
# ly.delete_layer([34,6])
# ly.delete_layer([34,7])
# ly.delete_layer([36,0])
# ly.delete_layer([36,1])
# ly.delete_layer([36,2])
# ly.delete_layer([82,0])
# # ly.delete_layer([40,0])
# # ly.delete_layer([40,1])
# # ly.delete_layer([40,2])
# # ly.delete_layer([40,3])
# # ly.delete_layer([40,4])
# # ly.delete_layer([40,5])
# # ly.delete_layer([40,6])
# # ly.delete_layer([37,0])
# # ly.delete_layer([37,1])
#
#
# # ly.top_cell().shapes(ly.layer(34,0)).insert(final)
# # ly.top_cell().shapes(ly.layer(40, 4)).insert(final2)
#
# ly.write("after_tiling.oas")
