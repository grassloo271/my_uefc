import numpy as np

def GetTailAlpha(UEFC, opt_vars):
    Sh = opt_vars[5]
    Sv = opt_vars[6]
    s_frac = Sh / opt_vars[4]
    a_h = 2 * np.pi /( 1 + 2/UEFC.AR_h)

    a_w = 2 * np.pi / (1 + 2/ opt_vars[3] )

    f_e = 0.6
    xi = np.arccos(1 - 2*f_e)
    a_e = 2 * (np.pi - xi  + np.sin(xi))/(1 + 2 /UEFC.AR_h)

    frac = -s_frac / ( a_w / a_e + (a_h / a_e) * s_frac)

    return UEFC.alpha(opt_vars) / frac

def GetAlphaTail(UEFC, opt_vars, tail_alpha):
    Sh = opt_vars[5]
    Sv = opt_vars[6]
    s_frac = Sh / opt_vars[4]
    a_h = 2 * np.pi /( 1 + 2/UEFC.AR_h)

    a_w = 2 * np.pi / (1 + 2/ opt_vars[3] )

    f_e = 0.6
    xi = np.arccos(1 - 2*f_e)
    a_e = 2 * (np.pi - xi  + np.sin(xi))/(1 + 2 /UEFC.AR_h)

    frac = -s_frac / ( a_w / a_e + (a_h / a_e) * s_frac)

    return tail_alpha * frac