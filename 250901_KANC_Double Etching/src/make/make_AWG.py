import numpy as np
import gdsfactory as gf
from make import make_elements
from make import make_grating
from make import make_AWG_gratingcoupler

#awg 정의
def make_AWG(WG_num,offset,width,layer):
    c=gf.Component()

#(1)기존 예제 Array waveguide 정의
    # for i in range(1,WG_num+1):
    #     FIRST_WG = c << make_elements.make_path([gf.path.arc(10),gf.path.straight(10.5),gf.path.arc(10)], layer=layer, width=width)
    #
    #     OTHER_WG = c << make_elements.make_path([gf.path.straight(offset+3*i),gf.path.arc(10),gf.path.straight(10.5+i*2.167*2),gf.path.arc(10),gf.path.straight(offset+3*i),], layer=layer, width=width)
    #
    #     OTHER_WG.move([0, -i * 2])

# (2)GC에 맞춘 Array waveguide 정의
    TotalWG = ([])
    Totalslab = ([])
    for i in range(1, WG_num + 1):
        OTHER_WG = c << make_elements.make_path([gf.path.straight(22+(6-0.3)* i), gf.path.arc(100),
                                                 gf.path.straight(44+(6+6-0.3-0.3)*i), gf.path.arc(100), gf.path.straight(22+(6-0.3) * i) ], layer=layer, width=width)
        OTHER_WG.move([680, -i * (6-0.3)])
        TotalWG.append(OTHER_WG)

        OTHER_WG_clad = c << make_elements.make_path([gf.path.straight(22+(6-0.3)* i), gf.path.arc(100),
                                                 gf.path.straight(44+(6+6-0.3-0.3)*i), gf.path.arc(100), gf.path.straight(22+(6-0.3) * i) ], layer=(layer[0], layer[1]+1), width=width+16)
        OTHER_WG_clad.move([680, -i * (6-0.3)])
        Totalslab.append(OTHER_WG_clad)

    for gc in TotalWG:
        gc.move([-650,-212.552])

    for gc in Totalslab:
        gc.move([-650, -212.552])





#FSR 정의
    # (1) 예제 fsr 크기
    # Input_FSR1 = c << make_elements.make_taper(2, 24.34, 20, layer=layer)
    # Input_FSR1.move([-20,42.169])
    # Input_FSR2 = c << make_elements.make_taper(10, 21, 20, layer=layer)
    # Input_FSR2.move([-20, -10])

    # (2) GC에 맞춘 fsr크기
    # Input_FSR1 = c << make_elements.make_taper(200, 809, 700, layer=layer)
    # Input_FSR1.move([-20, 890.001])
    # Input_FSR2 = c << make_elements.make_taper(617, 809, 700, layer=layer)
    # Input_FSR2.move([-20, -319.99931])

#INPUT GC
    # GC1 = c << make_AWG_gratingcoupler.Bend_leftGC_arc(100, 25, 100, (34,0), 1, 0.87, 0.55)
    # GC1.rotate(-90)
    # GC1.mirror_x()
    # GC1.move([-144.99977,265.40898127])

    GC1 = c << make_AWG_gratingcoupler.Bend_leftGC_arc0(100, 106, 100, (34, 0), 0.7, 0.87, 0.55)
    GC1.rotate(-90)
    GC1.move([-144.99977-74.999953,265.40898127+6.4978799-0.5+0.002])
    # TotalGC2.append(GC2)

#OUTPUT GC 반복구조
    TotalGC2 = []
    TotalGC3 = []

    # for i in range(1,3):
    #     GC2 = c << make_AWG_gratingcoupler.Bend_leftGC_arc0(235*i , 106*i, 100, (34, 0), 1, 0.87, 0.55)
    #     GC2.mirror_x()
    #     GC2.rotate(-90)
    #     GC2.move([-235*i, -100*i])
    #     TotalGC2.append(GC2)
    # for gc in TotalGC2:
    #     gc.move([-120.00011 , -360.762842-1.75+0.5-2+2.5])


    GC2 = c << make_AWG_gratingcoupler.Bend_leftGC_arc0(100, 106+0.3+0.15, 100, (34, 0), 0.7, 0.87, 0.55)
    GC2.mirror_x()
    GC2.rotate(-90)
    GC2.move([-235-118.097-1.903+135, -100-352.013-9.5])
    # TotalGC2.append(GC2)



    GC3 = c << make_AWG_gratingcoupler.Bend_leftGC_arc0(168*2-1, 106*2+0.15, 100, (34, 0), 0.7, 0.87, 0.55)
    GC3.mirror_x()
    GC3.rotate(-90)
    GC3.move([-235*2-119.74954-0.25+135, -100*2-358.013-3.5])
    # TotalGC3.append(GC3)

    GC4 = c << make_AWG_gratingcoupler.Bend_leftGC_arc0(572, 123-0.15, 100, (34, 0), 0.7, 0.87, 0.55)
    GC4.mirror_x()
    GC4.rotate(-90)
    GC4.move([-705-118.097-1.903+135-2, -100-352.013-9.5-5])

    GC5 = c << make_AWG_gratingcoupler.Bend_leftGC_arc0(471*2-135+7, 106*2-0.45, 100, (34, 0), 0.7, 0.87, 0.55)
    GC5.mirror_x()
    GC5.rotate(-90)
    GC5.move([-471*2-119.74954-0.25+135-7, -100*2-358.013-3.5+8+4])
    # TotalGC3.append(GC3)






    # for i in range(1,3):
    #     GC3 = c << make_AWG_gratingcoupler.Bend_leftGC_arc0(600*i , 106*i, 100, (34, 0), 1, 0.87, 0.55)
    #     GC3.mirror_x()
    #     GC3.rotate(-90)
    #     GC3.move([-300*i, -100*i])
    #     TotalGC3.append(GC3)
    # for gc in TotalGC3:
    #     gc.move([-120.00011-400 , -360.762842-1.75+0.5-2+2.5+9.5+2.5])



    # for i in range(1,3):
    #     GC2 = c << make_AWG_gratingcoupler.Bend_leftGC_arc0(231*i , 160*i, 100, (34, 0), 1, 0.87, 0.55)
    #     GC2.mirror_x()
    #     GC2.rotate(-90)
    #     GC2.move([-i*231, -i*294+144.5])
    #     TotalGC2.append(GC2)
    # for gc in TotalGC2:
    #     gc.move([-120.00011 , -360.762842-1.75+0.5-2+2.5])

    # #3번째 gc
    #     GC3 = c << make_AWG_gratingcoupler.Bend_leftGC_arc1(289.7 * i, 300 * i, 100, (34, 0), 1, 0.87, 0.55)
    #     GC3.mirror_x()
    #     GC3.rotate(-90)
    #     GC3.move([-i * 249.7-200, -i * 294-358.013+9-6-0.5])
    #
    # # 4번째 gc
    #     GC4 = c << make_AWG_gratingcoupler.Bend_leftGC_arc1(350.7 * i, 300 * i, 100, (34, 0), 1, 0.87, 0.55)
    #     GC4.mirror_x()
    #     GC4.rotate(-90)
    #     GC4.move([-i * 249.7 - 200-100, -i * 294 - 358.013 + 9 - 6 - 0.5+6])



#포트연결
#    OTHER_WG.connect('o1', GC1.ports['o1'], allow_layer_mismatch=True, allow_width_mismatch=True)


    return c




