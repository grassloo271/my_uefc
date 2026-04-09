
def GetSpiral(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    # print(f"{UEFC.lift_coefficient(opt_vars, AR, S)=}")
    return opt_vars[1] * UEFC.dihedral / UEFC.lift_coefficient(opt_vars, AR, S)

def GetHorTailVolume(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    # print(UEFC.wing_dimensions(AR, S)["Span"] )
    return UEFC.Sh * opt_vars[1] * UEFC.wing_dimensions(opt_vars, AR, S)["Span"] / (S * UEFC.wing_dimensions(opt_vars, AR, S)["Mean chord"] )

def GetVertTailVolume(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    return UEFC.Sv * opt_vars[1] / S

