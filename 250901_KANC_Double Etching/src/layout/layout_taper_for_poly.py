from pathlib import Path
import os
import numpy as np
from make import make_grating
from make import make_propagationloss
import gdsfactory as gf
from gdsfactory.technology import LayerViews
from gdsfactory.config import PATH
from gdsfactory.path import straight, euler, arc
from make import make_taper_for_poly,make_adiabatic_coupler


def taper_for_poly(layout):
    # C-Band (1550nm) 기본
    ## Coupling Length 조건 [500,1000,2500,5000]
    ## Taper Tip Width 조건 [100,150,200,250,300,350,400,450,500] 
    period_c = 1.06
    fill_factor_c = 0.5
    taper_tip_width_default = [0.3,0.35,0.4,0.45]
    coupling_length_default = [500,1000,2500,5000]
    coupling_length_default_xaxis=[0,2000,5000]
    for i in range(0,len(taper_tip_width_default)):
        for j in range(0,len(coupling_length_default)):
            if j!=3:
                taper = layout<<make_taper_for_poly.taper(taper_length = coupling_length_default[j],
                                                          taper_tip_width=taper_tip_width_default[i],
                                                          propagtion_length=500,
                                                          polymer_width=8,
                                                          period=period_c,
                                                          fill_factor=fill_factor_c)
                taper.move([coupling_length_default_xaxis[j],10100-610*i])
                taper.move([-10000,0])
            else:
                taper = layout<<make_taper_for_poly.taper(taper_length = coupling_length_default[j],
                                                          taper_tip_width=taper_tip_width_default[i],
                                                          propagtion_length=500,
                                                          polymer_width=8,
                                                          period=period_c,
                                                          fill_factor=fill_factor_c)
                taper.move([-100,9950-610*i])
                taper.move([-10000,0])

    # Text C-Band
    Text = layout << gf.components.text(text="C-Band", size=100, justify="left", layer=(34,0))
    Text.move([-7000,10300])

    # C-Band Polymer Sweep
    ## Taper Tip Width 조건 [350] 
    ## Coupling Length 조건 [5000]
    ## Polymer Width 조건 [4,6,8,10]
    polymer_width_c = [4,6,8,10]
    for i in range(0,len(polymer_width_c)):
            taper = layout<<make_taper_for_poly.taper(taper_length = 5000,
                                                          taper_tip_width=0.35,
                                                          propagtion_length=500,
                                                          polymer_width=polymer_width_c[i],
                                                          period=period_c,
                                                          fill_factor=fill_factor_c)
            taper.move([-100,5370-230*i])
            taper.move([-10000,0])

    # Text C-Band
    Text = layout << gf.components.text(text="C-Band", size=100, justify="left", layer=(34,0))
    Text.move([-7000,5500])

    # O-Band (1310nm) 기본
    ## Coupling Length 조건 [500,1000,2500,5000]
    ## Taper Tip Width 조건 [250,300,350,400,450,500] 
    ## O-Band Pitch, Duty, Fill_factor 조건 [0.87, 0.55, 0.45]
    period_o = 0.87
    fill_factor_o = 0.55
    taper_tip_width_default = [0.3,0.35,0.4,0.45]
    coupling_length_default = [500,1000,2500,5000]
    coupling_length_default_xaxis=[0,2000,5000]
    for i in range(0,len(taper_tip_width_default)):
        for j in range(0,len(coupling_length_default)):
            if j!=3:
                taper = layout<<make_taper_for_poly.taper(taper_length = coupling_length_default[j],
                                                          taper_tip_width=taper_tip_width_default[i],
                                                          propagtion_length=500,
                                                          polymer_width=8,
                                                          period=period_o,
                                                          fill_factor=fill_factor_o)
                taper.move([coupling_length_default_xaxis[j],7600-610*i])
                taper.move([-10000,0])
            else:
                taper = layout<<make_taper_for_poly.taper(taper_length = coupling_length_default[j],
                                                          taper_tip_width=taper_tip_width_default[i],
                                                          propagtion_length=500,
                                                          polymer_width=8,
                                                          period=period_o,
                                                          fill_factor=fill_factor_o)
                taper.move([-100,7450-610*i])
                taper.move([-10000,0])
    # Text O-Band
    Text = layout << gf.components.text(text="O-Band", size=100, justify="left", layer=(34,0))
    Text.move([-7000,7800])

    # O-Band Polymer Sweep
    ## Taper Tip Width 조건 [350] 
    ## Coupling Length 조건 [5000]
    ## Polymer Width 조건 [4,6,8,10]
    polymer_width_c = [4,6,8,10]
    for i in range(0,len(polymer_width_c)):
            taper = layout<<make_taper_for_poly.taper(taper_length = 5000,
                                                          taper_tip_width=0.35,
                                                          propagtion_length=500,
                                                          polymer_width=polymer_width_c[i],
                                                          period=period_o,
                                                          fill_factor=fill_factor_o)
            taper.move([-100,4400-230*i])
            taper.move([-10000,0])
    # Text O-Band
    Text = layout << gf.components.text(text="O-Band", size=100, justify="left", layer=(34,0))
    Text.move([-7000,4500])

    ## Propagation, Bending for C-Band
    propagation = layout<<make_taper_for_poly.polymer_propagation_loss(2500,0.35,20000,10,period_o,fill_factor_o,10)
    propagation.move([-9900,2850])
    propagation = layout<<make_taper_for_poly.polymer_propagation_loss(2500,0.35,40000,10,period_o,fill_factor_o,10)
    propagation.move([-9900,1850])
    propagation = layout<<make_taper_for_poly.polymer_propagation_loss(2500,0.35,60000,10,period_o,fill_factor_o,10)
    propagation.move([-9900,900])
    ## Bending [20], [10,20,50,100,200]

    bending = layout<<make_taper_for_poly.make_snake_bend_KANC(100,20,20,(35,0),10,2500,0.35,period_o,fill_factor_o)
    bending.move([-100,2160])

    bending = layout<<make_taper_for_poly.make_snake_bend_KANC(100,50,20,(35,0),10,2500,0.35,period_o,fill_factor_o)
    bending.move([-1000,900])

    bending = layout<<make_taper_for_poly.make_snake_bend_KANC(100,100,20,(35,0),10,2500,0.35,period_o,fill_factor_o)
    bending.move([-3000,1800])

    bending = layout<<make_taper_for_poly.make_snake_bend_KANC(100,200,20,(35,0),10,2500,0.35,period_o,fill_factor_o)
    bending.move([-5300,2700])

    # Text C-Band
    Text = layout << gf.components.text(text="C-Band", size=150, justify="left", layer=(34,0))
    Text.move([-7000,3200])

    #Add Alignkey
    for i in range(0,4):
        for j in range(0,4):
            # Add SiN Alignkey
            layout << make_adiabatic_coupler.add_cross_align_key((-10000+3250*i,10500-700*j),layer=(34,0))
            layout << make_adiabatic_coupler.add_square_align_key((-9900+3250*i,10500-700*j),layer=(34,0),size=50)

            # Add Polymer Alignkey
            layout << make_adiabatic_coupler.add_cross_align_key((-9900+3250*i,10500-700*j),layer=(35,0))
            layout << make_adiabatic_coupler.add_square_align_key((-10000+3250*i,10500-700*j),layer=(35,0),size=50)
        for j in range(4,8):
            # Add SiN Alignkey
            layout << make_adiabatic_coupler.add_cross_align_key((-10000+3250*i,10800-690*j),layer=(34,0))
            layout << make_adiabatic_coupler.add_square_align_key((-9900+3250*i,10800-690*j),layer=(34,0),size=50)

            # Add Polymer Alignkey
            layout << make_adiabatic_coupler.add_cross_align_key((-9900+3250*i,10800-690*j),layer=(35,0))
            layout << make_adiabatic_coupler.add_square_align_key((-10000+3250*i,10800-690*j),layer=(35,0),size=50)
    
    for i in range(0,4):
        for j in range(0,2):
            # Add SiN Alignkey
            layout << make_adiabatic_coupler.add_cross_align_key((-10000+3250*i,3600-3200*j),layer=(34,0))
            layout << make_adiabatic_coupler.add_square_align_key((-9900+3250*i,3600-3200*j),layer=(34,0),size=50)

            # Add Polymer Alignkey
            layout << make_adiabatic_coupler.add_cross_align_key((-9900+3250*i,3600-3200*j),layer=(35,0))
            layout << make_adiabatic_coupler.add_square_align_key((-10000+3250*i,3600-3200*j),layer=(35,0),size=50)

