import numpy as np

def Getalpha(UEFC, opt_vars):
    CL_nom = 0.65
    a_w = 2 * np.pi / (1 + 2/ opt_vars[3] )
    return (UEFC.lift_coefficient(opt_vars, None, None) - CL_nom)/a_w

def GetLiftCoeff(UEFC, opt_vars, alpha):
    CL_nom = 0.65
    a_w = 2 * np.pi / (1 + 2/ opt_vars[3] )
    return CL_nom + a_w * alpha

def GetLoading(UEFC, opt_vars, alpha):
    CL = GetLiftCoeff(UEFC, opt_vars)
    AR = opt_vars[3]
    S = opt_vars[4]

    # You need to finish this file

    # Calculate the lift coefficient from UEFC parameters and opt_vars, AR, S
    rho = UEFC.rho
   
    V  = UEFC.flight_velocity(opt_vars, AR, S)
    W  = UEFC.weight(opt_vars, AR, S)["Total"]

    # calculate CL from given variables
    q = 0.5*rho*(V**2)
    N = q * S * CL / W
    return N 