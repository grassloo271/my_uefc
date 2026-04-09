import numpy as np
def GetWfuse(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]


    # You need to finish this file

    # YOU MAY NEED TO ADJUST THE CONSTANTS TO BETTER FIT YOUR ESTIMATED
    # AIRPLANE.

    # Calculate fuselage weight from UEFC parameters and S and AR
    mfuse0 = 0.2527     # fixed mass, e.g. servos, motor, etc. (kg)
    mfusel = 0.0629     # span (length) dependent mass (kg)
    mfuseS = 0.012     # wing area dependent mass (kg)
    mfuset = 0.014     # tail area dependent mass (kg)

    l0 = 0.92          # Fuselage length for which mfusel were calculated (m)
    S0 = 0.354         # Wing area for which mfuseS were calculated (m^2)
    St0 = 0.04 + 0.03  # Tail area for which mfuset were calculated (m^2)

    b = UEFC.wing_dimensions(opt_vars, AR, S)["Span"] # wingspan thta corresponds to the given AR and S
    l_AR = opt_vars[1] - opt_vars[2]  # Fuselage wingspan to length ratio (-)
    l = b/l_AR        # fuselage length (m)


    Sh = UEFC.Sh      # area of horizontal tail (m^2)
    Sv = UEFC.Sv      # area of vertical tail (m^2)
    St = Sh + Sv      # total tail area (m^2)

    # Calculate Wfuse from the given variables
    Wfuse = (mfuse0 + mfusel * l/l0 + mfuseS * S / S0 + mfuset * St / St0)  * UEFC.g

    return Wfuse

# DO NOT MODIFY THIS
def check_close(truth_val, test_val, close_tol):
    return np.abs(truth_val - test_val) < close_tol

def tests() -> None:
    # DO NOT CHANGE THE VALUES HERE
    from GetUEFC        import UEFC
    CLOSE_TOL = 1E-10
    aircraft = UEFC()
    AR = 9

    aircraft.Sh = 0.04
    aircraft.Sv = 0.03
    aircraft.l = 0.92
    S = 0.354
    Wfuse = GetWfuse(aircraft, AR, S)
    assert check_close(Wfuse, 3.476826094096035, CLOSE_TOL)

    aircraft.Sh = 0.074
    aircraft.Sv = 0.04
    aircraft.l = 0.72
    S = 0.354
    Wfuse = GetWfuse(aircraft, AR, S)
    assert check_close(Wfuse, 3.5384889512388917, CLOSE_TOL)

    aircraft.Sh = 0.024
    aircraft.Sv = 0.02
    aircraft.l = 0.92
    S = 1.0
    Wfuse = GetWfuse(aircraft, AR, S)
    assert check_close(Wfuse, 4.382755335453457, CLOSE_TOL)

    print(f"==> All GetWfuse tests have passed!")


if __name__ == "__main__":
    tests()
