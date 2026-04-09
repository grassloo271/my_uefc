
def GetSpiral(UEFC, opt_vars, AR, S):
    # print(f"{UEFC.lift_coefficient(opt_vars, AR, S)=}")
    return opt_vars[1] * UEFC.dihedral / UEFC.lift_coefficient(opt_vars, AR, S)

def GetHorTailVolume(UEFC, opt_vars, AR, S):
    # print(UEFC.wing_dimensions(AR, S)["Span"] )
    return UEFC.Sh * opt_vars[1] * UEFC.wing_dimensions(AR, S)["Span"] / (S * UEFC.wing_dimensions(AR, S)["Mean chord"] )

def GetVertTailVolume(UEFC, opt_vars, AR, S):
    return UEFC.Sv * opt_vars[1] / S

