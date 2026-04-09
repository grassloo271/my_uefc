
def GetMassBreakdown(UEFC, opt_vars, AR, S):
    c_bar = UEFC.wing_dimensions(AR, S)["Mean chord"]
    b = UEFC.wing_dimensions(AR, S)["Span"]

    mass_breakdown = {
        #"object" : [mass, position]
        "wing" : [UEFC.wing_weight(AR, S) / 9.8, 0.25 * c_bar],
        "tail" : [(UEFC.Sh + UEFC.Sv) * 0.014 / 0.07, opt_vars[1] * b],
        "motor" : [0.0809 + 0.013, opt_vars[2] * b],
        "radio + batt" : [0.132 + 0.0091+ 0.012, 0.5 * c_bar], 
        "servos" : [0.016, 1.5 * c_bar],
        "boom" : [0.0389 * (opt_vars[1] - opt_vars[2]) *b /0.92,  (opt_vars[1] + opt_vars[2]) * b /2 ],
        "push_rods" : [.024 *  ( opt_vars[1] * b / - 1.5 * c_bar )/ (0.92 - 0.17 - 1.5 * 0.15), ( 1.5 * c_bar + opt_vars[1] * b) /2]
    }
    return mass_breakdown

def GetCOM(UEFC, opt_vars, AR, S):
    mass_breakdown = GetMassBreakdown(UEFC, opt_vars, AR, S)
    mass = 0
    com = 0
    for elem in mass_breakdown:
        mass += mass_breakdown[elem][0]
        com += mass_breakdown[elem][0] * mass_breakdown[elem][1]

    return com/ mass 

def GetMass(UEFC, opt_vars, AR, S):
    mass_breakdown = GetMassBreakdown(UEFC, opt_vars, AR, S)
    mass = 0
    
    for elem in mass_breakdown:
        mass += mass_breakdown[elem][0]
        
    return mass 

def GetWeight(UEFC, opt_vars, AR, S):
    return {"Total" : GetMass(UEFC, opt_vars, AR, S) * 9.8}