from make import make_elements
#from make import make_assembly
from make import make_grating
from make import make_bendingloss
from make import make_AWG
from make import make_AWG_gratingcoupler
from make import make_AWG_Boolean


def AWG(layout):
    for i in range(0,5):
        AWG1 = layout << make_AWG.make_AWG(11, 0, 0.7, (34, 0))
        AWG1.rotate(90)
        AWG1.move([10020,-1170*i-770])
    # for i in range(5,8):
    #     AWG2 = layout << make_AWG.make_AWG(11, 0, 0.7, (34, 0))
    #     AWG2.rotate(90)
    #     AWG2.move([-350*i-730*(i-5)+920, -8900+3450-1200-300])



def Boolean(layout):
    for i in range(0,5):
        Bool1 = layout << make_AWG_Boolean.make_Boolean(cell_name=f"top_{i}")
        Bool1.rotate(90)
        Bool1.move([10020 , -1170*i-770])
    # for i in range(5,8):
    #     Bool2 = layout << make_AWG_Boolean.make_Boolean(cell_name=f"top_{i}")
    #     Bool2.rotate(90)
    #     Bool2.move([-350*i-730*(i-5)+920 , -8900+3450-1200-300])





