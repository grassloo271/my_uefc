import numpy as np

def GetNP(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    a_w = np.pi * 2 / (1 + 2 / AR)
    a_h = 2 * np.pi /(1 + 2/ UEFC.AR_h)  
    c = np.sqrt(S / AR)
    b = np.sqrt(S * AR)

    l_h = b * UEFC.l_AR

    V_h = UEFC.Sh * l_h / (S * c)
    
    return (a_w/(4*a_h) + V_h *(1+c/(4*l_h)))/(a_w/a_h + V_h*c/l_h) * UEFC.wing_dimensions(opt_vars, AR, S)["Mean chord"]