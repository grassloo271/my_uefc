# YOU SHOULD NOT NEED TO CHANGE THIS FILE FOR THIS PROBLEM
import numpy as np

def GetWingDimensions(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    taper = UEFC.taper

    b      = np.sqrt(AR*S)
    c_bar  = np.sqrt(S/AR)
    c_root = 2 * c_bar         / (1+taper)
    c_tip  = 2 * c_bar * taper / (1+taper)

    return {
            "Span":       b,
            "Mean chord": c_bar,
            "Root chord": c_root,
            "Tip chord":  c_tip,
                }
