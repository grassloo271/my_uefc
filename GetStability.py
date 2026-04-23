import numpy as np
def GetSpiral(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    # print(f"{UEFC.lift_coefficient(opt_vars, AR, S)=}")
    return opt_vars[1] * UEFC.dihedral / UEFC.lift_coefficient(opt_vars, AR, S)

def GetHorTailVolume(UEFC, opt_vars, AR, S):
    Sh = opt_vars[5]
    Sv = opt_vars[6]
    AR = opt_vars[3]
    S = opt_vars[4]

    # print(UEFC.wing_dimensions(AR, S)["Span"] )
    return Sh * opt_vars[1] * UEFC.wing_dimensions(opt_vars, AR, S)["Span"] / (S * UEFC.wing_dimensions(opt_vars, AR, S)["Mean chord"] )

def GetVertTailVolume(UEFC, opt_vars, AR, S):
    Sh = opt_vars[5]
    Sv = opt_vars[6]
    AR = opt_vars[3]
    S = opt_vars[4]

    return Sv * opt_vars[1] / S

def isStable(self, opt_vars, tail_angle, verbose=False):
    AR = opt_vars[3]
    S = opt_vars[4] 
    """
    Checks whether all stability and design constraints are satisfied.
    
    Parameters:
        opt_vars : array-like  — optimization variables
        AR       : float       — aspect ratio
        S        : float       — wing area
        verbose  : bool        — if True, prints status of each constraint
    
    Returns:
        bool — True if all constraints are satisfied, False otherwise
    """
    constraints = {
        "Static margin / Neutral point (must be > 0)":
            self.neutral_point(opt_vars, AR, S) - self.tail_COM(opt_vars, tail_angle),

        "Static margin / Neutral point (must be > 0), upper bound":
            self.wing_dimensions(opt_vars, AR, S)["Mean chord"] * 0.2 - (self.neutral_point(opt_vars, AR, S) - self.tail_COM(opt_vars, tail_angle)),

        "Payload location (must be >= 0)":
            self.payload_loc(opt_vars, tail_angle) - opt_vars[2] * self.wing_dimensions(opt_vars, AR, S)["Span"],

        "Payload location (must be > 0)":
            opt_vars[1] * self.wing_dimensions(opt_vars, AR, S)["Span"] - self.payload_loc(opt_vars, tail_angle)  ,
    }

    all_satisfied = np.ones(len(tail_angle), dtype=bool)
    for value in constraints:
        # print(opt_vars[2] * self.wing_dimensions(opt_vars, AR, S)["Span"])
        all_satisfied &= (constraints[value] >= 0)

    return all_satisfied
