import numpy as np

def GetTailCOM(UEFC, opt_vars, tail_alpha = None):
    Sh = opt_vars[5]
    Sv = opt_vars[6]
    AR = opt_vars[3]
    S = opt_vars[4]
    a_h = 2 * np.pi /( 1 + 2/UEFC.AR_h)

    a_w = 2 * np.pi / (1 + 2/ opt_vars[3] )

    f_e = 0.6
    xi = np.arccos(1 - 2*f_e)
    a_e = 2 * (np.pi - xi  + np.sin(xi))/(1 + 2 /UEFC.AR_h)
    

    Cm_nom = UEFC.Cm_nom[UEFC.tau]

    CL_w = UEFC.lift_coefficient(opt_vars, None, None)

    if tail_alpha is None:
        CL_h = a_h * UEFC.alpha(opt_vars) + a_e * UEFC.tail_alpha(opt_vars)
    else:
        CL_h = a_h * UEFC.alpha(opt_vars) + a_e * tail_alpha

    c = UEFC.wing_dimensions(opt_vars, AR, S)["Mean chord"]
    b = UEFC.wing_dimensions(opt_vars, AR, S)["Span"]

    l_h = b * opt_vars[1]

    V_h = Sh * l_h / (S * c)

    num = (1/4 * CL_w  + (1 + 0.25 * c/l_h)* V_h*CL_h - Cm_nom) * c
    denom = (CL_w + c/l_h * V_h * CL_h)
    
    return num/denom