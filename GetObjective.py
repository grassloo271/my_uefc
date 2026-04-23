from GetV import GetV
import numpy as np

def GetObjective(UEFC, opt_vars):
    AR = opt_vars[3]
    S = opt_vars[4]

    # YOU SHOULD NOT NEED TO CHANGE THIS FUNCTION FOR THIS PROBLEM

    # Calculate the objective function (payload mass x turn rate^3) in g/s^3

    # mpay  = opt_vars[2]
    # Omega = UEFC.turn_rate(opt_vars, AR, S)
    # b = UEFC.wing_dimensions(AR, S)['Span']
    #mwing = UEFC.wing_weight(AR,S) * 1000 / UEFC.g

    #obj = mpay * Omega / b.

    # Calculate the objective function (velocity) in m/s
    # print("objective called")
    
    v = GetV(UEFC, opt_vars, AR, S)   

    tail_deflection_bounds = np.linspace(0, 7, 99) * np.pi/180
    
    payload_loc = UEFC.payload_loc(opt_vars, tail_deflection_bounds)

    stability = UEFC.isStable(opt_vars, tail_deflection_bounds)

    stable_mask = stability  # boolean array
    stable_indices = np.where(stable_mask)[0]

    if len(stable_indices) == 0:
        payload_diff = 0.01  # no stable region
    else:
        first_stable = stable_indices[0]
        last_stable = stable_indices[-1]
        payload_diff = payload_loc[first_stable] - payload_loc[last_stable]
    
    
    obj = (-payload_diff * (1 - np.log10(0.8) + np.log10(UEFC.payload_fraction(opt_vars, None, None))) / 0.11621545  ) +( v/11.14)
    # obj = -payload_diff * (1 - np.log10(0.8) + np.log10(UEFC.payload_fraction(opt_vars, None, None))) 
    
    return obj



