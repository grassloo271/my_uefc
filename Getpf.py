
def Getpf(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    # Returns the total weight, as well as a breakdown, in N.

    # YOU SHOULD NOT NEED TO CHANGE THIS FILE FOR THIS PROBLEM

    W = UEFC.weight(opt_vars, AR, S)
    Wpay  = UEFC.payload_weight(opt_vars, AR, S)

    payload_fraction = Wpay / W['Total']

    return payload_fraction