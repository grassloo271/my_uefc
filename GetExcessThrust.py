def GetExcessThrust(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    # YOU SHOULD NOT NEED TO CHANGE THIS FILE FOR THIS PROBLEM

    # Get excess thrust: maximum thrust - required thrust
    
    V    = UEFC.flight_velocity(opt_vars, AR, S)
    Tmax = UEFC.maximum_thrust(V)
    Treq = UEFC.required_thrust(opt_vars, AR, S)
    
    return Tmax - Treq
