import numpy as np

def Getalpha(UEFC, opt_vars):
    CL_nom = 0.65
    a_w = 2 * np.pi / (1 + 2/ opt_vars[3] )
    return (UEFC.lift_coefficient(opt_vars, None, None) -CL_nom)/a_w