from make import make_edgecoupler 
import gdsfactory as gf

# layout = gf.Component()

# layout.add_polygon([(-10000,10000),(10000,10000),(10000,-10000),(-10000,-10000)], layer=(82,0))


def edge_coupler(layout):
    #석현 파라미터
    #Text
    EC_length = [0.5, 1, 1.5, 2]

    # Vaules
    width_condition = [0.7,0.8,0.9,1,1.5,2]
    width = 0.7
    width_max = [4, 6, 8, 10, 12, 14]
    Taper_length = [30, 50, 90, 142, 208, 264]
    misalign = [0,1,2,3,4,5]
    period = 0.87
    fill_factor = 0.55
    length1 = 400
    length2 = 25
    radius = 100
    strip_length = [0, 10, 20, 30, 40, 50]

    bend_radius = [30,50]
    bend_length = [3400,470,450]
    EC_bot = 400

    layer_clad = (34,0)
    layer_core = (34,0)

    #Dicing key
    Dicing_key_top_l = layout << make_edgecoupler.Dicing_key(layer_clad, 50, 250, 1)
    Dicing_key_top_r = layout << make_edgecoupler.Dicing_key(layer_clad, 50, 250, 1)
    # Dicing_key_top_1 = layout << make_edgecoupler.Dicing_key(layer_clad, 50, 250, 2)
    # Dicing_key_mid_r = layout << make_edgecoupler.Dicing_key(layer_clad, 50, 250, 2)
    # Dicing_key_top_3 = layout << make_edgecoupler.Dicing_key((34, 1), 50, 250, 2)

    Dicing_key_bot_l = layout << make_edgecoupler.Dicing_key(layer_clad, 50, 250, 1)
    Dicing_key_bot_r = layout << make_edgecoupler.Dicing_key(layer_clad, 50, 250, 1)
    # Dicing_key_bot_1 = layout << make_edgecoupler.Dicing_key(layer_clad, 50, 250, 2)
    # Dicing_key_mid_l = layout << make_edgecoupler.Dicing_key(layer_clad, 50, 250, 2)
    # Dicing_key_bot_3 = layout << make_edgecoupler.Dicing_key((34, 1), 50, 250, 2)

    # Dicing_key_origin = layout << make_edgecoupler.Dicing_key(layer_clad, 100, 250, 3)
    # Dicing_key_origin.move([0,0])

    Dicing_key_top_l.rotate(-90)
    Dicing_key_top_l.move([-9975,9975])
    # Dicing_key_top_1.rotate(-180)
    # Dicing_key_top_1.move([0,10975])
    # Dicing_key_mid_r.rotate(90)
    # Dicing_key_mid_r.move([10975,0])
    # Dicing_key_top_3.rotate(-180)
    # Dicing_key_top_3.move([5000,12475])
    Dicing_key_top_r.rotate(-180)
    Dicing_key_top_r.move([9975,9975])


    Dicing_key_bot_l.move([-9975,-9975])
    # Dicing_key_bot_1.move([0, -10975])
    # Dicing_key_mid_l.rotate(-90)
    # Dicing_key_mid_l.move([-10975,0])
    # Dicing_key_bot_3.move([5000, -12475])
    Dicing_key_bot_r.rotate(90)
    Dicing_key_bot_r.move([9975,-9975])

    #-------------------------------------------------------------------------------------------------------------------------------
    x_position =7400
    y_position = 10400
    # for x in range(0,6):
    #     for y in range(0,6):
    #         Ref_GC = layout << make_edgecoupler.Ref_GC(layer_core,layer_clad, width, period, fill_factor, length1, length2, radius)
    #         Ref_GC.move([x_position,y_position])
    #         Ref_GC = layout << make_edgecoupler.Ref_GC(layer_core, layer_clad, width, period, fill_factor, length1,
    #                                                    length2, radius)
    #         Ref_GC.move([x_position+1600, y_position])
    #
    #         if x in [0,1,2]:
    #             Taper_edge = layout << make_edgecoupler.Taper_Coupler(layer_core, layer_clad, width, width_max[x],
    #                                                                   Taper_length[x], misalign[y], period, fill_factor,
    #                                                                   length1, length2, radius)
    #             Taper_edge.move([x_position, (y_position-400)-(280*y)-(1750*x)])
    #         else:
    #             Taper_edge = layout << make_edgecoupler.Taper_Coupler(layer_core, layer_clad, width, width_max[x],
    #                                                                   Taper_length[x], misalign[y], period, fill_factor,
    #                                                                   length1, length2, radius)
    #             Taper_edge.move([x_position+1600, (y_position-400) - (280 * y) - (1750 * (x-3))])
    #
    # # text
    # for x in range(0, 2):
    #     T_Ref_GC = layout << gf.components.text(text='Ref GC', size=80,
    #                                               justify="left",
    #                                               layer=layer_core)
    #     T_Ref_GC.move([x_position+400+(1600*x), y_position-150])
    #
    # for x in range(0,6):
    #     if x in [0,1,2]:
    #         T_Taper_EC = layout << gf.components.text(
    #             text='W : {} L : {}'.format(width_max[x], Taper_length[x]),
    #             size=80,
    #             justify="left",
    #             layer=layer_core
    #         )
    #         T_Taper_EC.move([x_position+400, (y_position-500)-(1750*x)])
    #     else:
    #         T_Taper_EC = layout << gf.components.text(
    #             text='W : {} L : {}'.format(width_max[x], Taper_length[x]),
    #             size=80,
    #             justify="left",
    #             layer=layer_core
    #         )
    #         T_Taper_EC.move([x_position+600+1400, (y_position-500) - (1750 * (x-3))])
    # #
    # for x in range(0,2):
    #     Edge_Coupler = layout << make_edgecoupler.Sbend_Edge_Coupler(layer_core, layer_clad, width_condition[x],
    #                                                                  radius,bend_length[0])
    #     Edge_Coupler.move([-11000, (EC_bot+400 + 300 * x)])

    #     Edge_Coupler = layout << make_edgecoupler.Edge_Coupler1(layer_core, layer_clad, width_condition[x])
    #     Edge_Coupler.move([-11000, (EC_bot+120*x)])
    #Sbend text
    # for y in range(0, 2):
    #     T_Sbend_EC = layout << gf.components.text(text='Sbend.EC_W : 0.7 0.8', size=80,
    #                                               justify="left",
    #                                               layer=layer_core)
    #     T_Sbend_EC.move([-10500+20000*y, EC_bot+500])
    #     T_Sbend_EC = layout << gf.components.text(text='Sbend.EC_W : 0.7 0.8' , size=80,
    #                                               justify="left",
    #                                               layer=layer_core)
    #     T_Sbend_EC.move([-5300 + 9500 * y, EC_bot+520])
    # #length 1,2 text
    # for x in range(0, 2):
    #     # T_Edge_Coupler = layout << gf.components.text(text='EC_length : %s' % EC_length[1], size=80,
    #     #                                               justify="left",
    #     #                                               layer=layer_core)
    #     # T_Edge_Coupler.move([-12000 + 23000 * x, EC_top-1000 - 120 * 4+100])
    #     T_Edge_Coupler = layout << gf.components.text(text='EC_length : %s' % EC_length[3], size=80,
    #                                                   justify="left",
    #                                                   layer=layer_core)
    #     T_Edge_Coupler.move([-10500 + 20300 * x, EC_bot+200])

    # step = 400
    # #Stitching error
    # for i in range(5):
    #     if i == 0 :
    #         for x in range(2):
    #             Stitching_bot = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
    #             Stitching_bot.rotate(90)
    #             Stitching_bot.move([-10500+x*(step*2), -11000])
    #
    #             Stitching_top = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
    #             Stitching_top.rotate(-90)
    #             Stitching_top.move([-9700+x*(step*2), 11000])
    #
    #     elif i == 1:
    #         for x in range(10):
    #             Stitching_bot = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
    #             Stitching_bot.rotate(90)
    #             Stitching_bot.move([-10500+(step*2)+(step*3) + x * (step*2), -11000])
    #
    #             Stitching_top = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
    #             Stitching_top.rotate(-90)
    #             Stitching_top.move([-9700+(step*2)+(step*3) + x * (step*2), 11000])
    #
    #     elif i == 2:
    #         for x in range(4):
    #             Stitching_bot = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
    #             Stitching_bot.rotate(90)
    #             Stitching_bot.move([0 +(step*1) + x * (step*2), -11000])
    #
    #             Stitching_top = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
    #             Stitching_top.rotate(-90)
    #             Stitching_top.move([800+(step*1) + x * (step*2),11000])
    #
    #     elif i == 3:
    #         for x in range(7):
    #             Stitching_bot = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
    #             Stitching_bot.rotate(90)
    #             Stitching_bot.move([0 +(step*1) +(step*9) + x * (step*2), -11000])
    #
    #             Stitching_top = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
    #             Stitching_top.rotate(-90)
    #             Stitching_top.move([800+(step*1)+(step*9)  + x * (step*2),11000])

        # elif i == 2:
        #     for x in range(8):
        #         Stitching_bot = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
        #         Stitching_bot.rotate(90)
        #         Stitching_bot.move([-10500+(step*3)+(step*5) + x * (step*2), -11000])
        #
        #         Stitching_top = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
        #         Stitching_top.rotate(-90)
        #         Stitching_top.move([-9700+(step*3)+(step*5) + x * (step*2),11000])
        #
        # elif i == 3:
        #     for x in range(6):
        #         Stitching_bot = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
        #         Stitching_bot.rotate(90)
        #         Stitching_bot.move([-12000+(step*3)+(step*5)+(step*9) + x * (step*2), -12500])
        #
        #         Stitching_top = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
        #         Stitching_top.rotate(-90)
        #         Stitching_top.move([-11200 +(step*3)+(step*5)+(step*9) + x * (step*2), 12500])
        #
        # elif i == 4:
        #     for x in range(13):
        #         Stitching_bot = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
        #         Stitching_bot.rotate(90)
        #         Stitching_bot.move([-12000+step +(step*3)+(step*5)+(step*9)+(step*13) + x * (step*2), -12500])
        #
        #         Stitching_top = layout << make_edgecoupler.Stitching_wg(layer_core, layer_clad, width, radius)
        #         Stitching_top.rotate(-90)
        #         Stitching_top.move([-11200+step +(step*3)+(step*5)+(step*9)+(step*13) + x * (step*2), 12500])

    # Stitching_Ref_GC = layout << make_edgecoupler.Stitching_Ref_GC(layer_core,layer_clad,width,period,fill_factor,radius)
    # Stitching_Ref_GC.rotate(-90)
    # Stitching_Ref_GC.move([300+ (step * 9)+ (step * 16) , -10999.739])
    #
    # GC_top = layout << make_edgecoupler.GC_single(layer_core,layer_clad,width,period,fill_factor)
    # GC_top.rotate(-90)
    # GC_top.move([-10500 , 10750.261])
    # GC_top = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_top.rotate(-90)
    # GC_top.move([-10500+(step*2)+(step*3), 10750.261])
    # GC_top = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_top.rotate(-90)
    # GC_top.move([0 + (step * 1), 10750.261])
    # GC_top = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_top.rotate(-90)
    # GC_top.move([0 + (step * 1)+ (step * 9),10750.261])
    # GC_top = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_top.rotate(-90)
    # GC_top.move([300+ (step * 9)+ (step * 16) , 10750.261])
    #
    # GC_bot = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_bot.rotate(90)
    # GC_bot.move([-10500+(step*2)+(step*2), -10750.261])
    # GC_bot = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_bot.rotate(90)
    # GC_bot.move([-10500+(step*2)+(step*2)+(step*21), -10750.261])
    # GC_bot = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_bot.rotate(90)
    # GC_bot.move([0 +(step*9), -10750.261])
    # GC_bot = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_bot.rotate(90)
    # GC_bot.move([0 + (step * 9)+ (step * 15), -10750.261])
    # GC_bot = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_bot.rotate(90)
    # GC_bot.move([-12000+(step*2)+(step*5)+(step*9)+(step*13), -12250.18])
    # GC_bot = layout << make_edgecoupler.GC_single(layer_core, layer_clad, width, period, fill_factor)
    # GC_bot.rotate(90)
    # GC_bot.move([-12000+step+(step*2)+(step*5)+(step*9)+(step*13)+(step*27), -12250.18])
    #
    # stitching_bend_num = [2,4,7,10]
    # T_bend_top = 10650
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[0]),
    #     size=50,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([-10650, T_bend_top])
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[3]),
    #     size=50,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([-9900+(step*3), T_bend_top])
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[1]),
    #     size=50,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([300 +(step*1), T_bend_top])
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[2]),
    #     size=50,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([300 +(step*1)+(step*8), T_bend_top])
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[4]),
    #     size=80,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([-12150+(step*3)+(step*5) +(step*9)+(step*14), T_bend_top])
    #
    # T_Stitching_Ref = layout << gf.components.text(text='Ref GC', size=80,
    #                                           justify="left",
    #                                           layer=layer_core)
    # T_Stitching_Ref.rotate(90)
    # T_Stitching_Ref.move([-12150 + (step * 3) + (step * 5) + (step * 9) + (step * 14)+ (step * 27), T_bend_top])
    #
    # #Bot
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[0]),
    #     size=80,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([-11400, -T_bend_top-500])
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[1]),
    #     size=80,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([-11400 + (step * 5), -T_bend_top-500])
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[2]),
    #     size=80,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([-11400 + (step * 5) + (step * 9) , -T_bend_top-500])
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[3]),
    #     size=80,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([-11400 + (step * 5) + (step * 9) + (step *13) , -T_bend_top-500])
    # T_Stitching = layout << gf.components.text(
    #     text='Bend : {}'.format(stitching_bend_num[4]),
    #     size=80,
    #     justify="left",
    #     layer=layer_core
    # )
    # T_Stitching.rotate(90)
    # T_Stitching.move([-11400 + (step * 5) + (step * 9) + (step * 14)+ (step * 27), -T_bend_top-500])