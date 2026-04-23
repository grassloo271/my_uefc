import numpy as np
from scipy.optimize import minimize, Bounds
import matplotlib.pyplot as plt
from GetUEFC        import UEFC
from GetObjective   import GetObjective

def opt_obj(UEFC):
    
    # YOU SHOULD NOT NEED TO CHANGE THIS FUNCTION FOR THIS PROBLEM

    # Determine the maximum objective function (velocity)
    # achievable for an airplane with the inputted values of AR, S.

    # Optimization variables: N

    # Maximize objective: minimize negative of objective (ORIGINAL)
    #obj_fcn = lambda opt_vars: -GetObjective(UEFC, opt_vars, AR, S)

    # Modification (otherwise solution not always found)
    obj_fcn = lambda opt_vars: -GetObjective(UEFC, opt_vars) * (1./5.)
    # optimization variable is the load factor of the turn.
    N_initialGuess = 1.25
    N_lowerBound   = 1.01
    N_upperBound   = 5.0

    l_AR_initialGuess = 0.7 #from wing to tail
    l_AR_lowerBound = 0.2
    l_AR_upperBound = 1

    l_m_initialGuess = -0.3 #similar definition to l_AR but for the motor
    l_m_lowerBound = -0.3
    l_m_upperBound = -.05

    AR_initialGuess = 5
    AR_lowerBound = 4
    AR_upperBound = 10

    S_initialGuess = 0.254
    S_lowerBound = 0.05
    S_upperBound = 0.3

    AR = AR_initialGuess
    S = S_initialGuess
    
    Sh_initialGuess = 0.04
    Sh_lowerBound = 0.01
    Sh_upperBound = 0.06

    Sv_initialGuess = 0.02
    Sv_lowerBound = 0.01
    Sv_upperBound = 0.05

    payload_loc = 0
    payload_lower = -0.1
    payload_upper = 0.5
    
    # R_initialGuess = 6.0
    # R_lowerBound   = 0.1
    # R_upperBound   = 12.5

    # mpay_initialGuess = 10.
    # mpay_lowerBound   = 0.01
    # mpay_upperBound   = 1000.
    
    initialGuess = (N_initialGuess, l_AR_initialGuess, l_m_initialGuess, AR_initialGuess, S_initialGuess, Sh_initialGuess, Sv_initialGuess)
    
    bounds       = Bounds(lb=(N_lowerBound, l_AR_lowerBound, l_m_lowerBound, AR_lowerBound, S_lowerBound, Sh_lowerBound, Sv_lowerBound), ub=(N_upperBound, l_AR_upperBound, l_m_upperBound, AR_upperBound, S_upperBound, Sh_upperBound, Sv_upperBound), keep_feasible=True)

    # Constraint format is different, depending on algorithm.
    method = "SLSQP"
    if method == "SLSQP":

        T_constraint = {"type": "ineq","fun": lambda opt_vars: UEFC.excess_thrust(opt_vars, opt_vars[3], opt_vars[4])}
        db_constraint = {"type": "ineq","fun": lambda opt_vars: UEFC.dbmax - UEFC.wing_tip_deflection(opt_vars, opt_vars[3], opt_vars[4])}
        CL_constraint = {"type": "ineq","fun": lambda opt_vars: UEFC.CLdes - UEFC.lift_coefficient(opt_vars, opt_vars[3], opt_vars[4])}
        
        SM_constraint = {
                "type": "ineq",
                "fun" : lambda opt_vars: UEFC.neutral_point(opt_vars, opt_vars[3], opt_vars[4]) - UEFC.tail_COM(opt_vars, 0)
                #coordinate
        }

        wing_size = {
                "type": "ineq",
                "fun" : lambda opt_vars: 4-UEFC.wing_dimensions(opt_vars, opt_vars[3], opt_vars[4])["Root chord"] * 12
                #coordinate
        }

        SM_constraint_upper = {
                "type": "ineq",
                "fun" : lambda opt_vars: 0.2 * UEFC.wing_dimensions(opt_vars, opt_vars[3], opt_vars[4])["Mean chord"] - (UEFC.neutral_point(opt_vars, opt_vars[3], opt_vars[4]) - UEFC.tail_COM(opt_vars,  0))
                #coordinate
        }
    
        Vert_constrant_lower = {
                "type": "ineq",
                "fun" : lambda opt_vars: UEFC.vertical_tail_coeff(opt_vars, opt_vars[3], opt_vars[4])  -  0.02 
        }

        Vert_constrant_upper = {
                "type": "ineq",
                "fun" : lambda opt_vars: 0.06 - UEFC.vertical_tail_coeff(opt_vars, opt_vars[3], opt_vars[4]) 
        }

        Hor_constrant_lower = {
                "type": "ineq",
                "fun" : lambda opt_vars: UEFC.horizontal_tail_coeff(opt_vars, opt_vars[3], opt_vars[4])  -  0.3
        }

        Hor_constrant_upper = {
                "type": "ineq",
                "fun" : lambda opt_vars: 0.6 - UEFC.horizontal_tail_coeff(opt_vars, opt_vars[3], opt_vars[4])
        }

        Spral_constrant = {
                "type": "ineq",
                "fun" : lambda opt_vars:  UEFC.spiral_coeff(opt_vars, opt_vars[3], opt_vars[4]) - 5  
        }
        payload_constraint = {
                "type": "ineq",
                "fun" : lambda opt_vars:  UEFC.payload_loc(opt_vars) + opt_vars[2] * UEFC.wing_dimensions(opt_vars, opt_vars[3], opt_vars[4])["Mean chord"]
        }
        payload_constraint = {
                "type": "ineq",
                "fun" : lambda opt_vars:  - UEFC.payload_loc(opt_vars) + opt_vars[1] * UEFC.wing_dimensions(opt_vars, opt_vars[3], opt_vars[4])["Mean chord"]
        }
        

    else:
        raise AttributeError("Optimization method " + method \
                             + " not recognized.")

    constraints = [T_constraint, db_constraint, CL_constraint, SM_constraint, Spral_constrant,  Hor_constrant_lower ,Vert_constrant_lower, Vert_constrant_upper, Hor_constrant_upper, payload_constraint, SM_constraint_upper, wing_size]
    
    # try:
    result = minimize(fun=obj_fcn, x0=initialGuess, bounds=bounds,
                      constraints=constraints, method=method,
                      options={"maxiter": 20000, "disp":False})
   
    success = result.success
    # print(success)
    # except:  # Optimizer failed
    #     result  = None
    #     success = False

    if success:
        opt_vars_maxObj = result.x  # Variables that maximize objective
        obj_max         = GetObjective(UEFC, opt_vars_maxObj)

    else:  # If optimizer fails
        opt_vars_maxObj = np.zeros(np.size(initialGuess))
        obj_max         = 0

    return opt_vars_maxObj, obj_max, success


if __name__ == "__main__":

    # Simple test case. Feel free to modify this part of the file.
    aircraft = UEFC()

#     S  = (0.1 + 0.2)/2 * 1.5  # m^2
#     AR = 1.5**2 / S

    aircraft.CLdes = 0.8
    aircraft.mpay_g = 250
    aircraft.dihedral = 10
    
    aircraft.Sh = 0.04
    aircraft.Sv = 0.03
    # print(aircraft.weight(1.1, AR, S)["Total"], "total")
    opt_vars_maxobj, obj_max, success = opt_obj(aircraft)

    AR = opt_vars_maxobj[3]
    S = opt_vars_maxobj[4]
    
#     print()
#     print("Load factor:  %0.3f"   % opt_vars_maxobj[0])
#     # print("Turn radius:  %0.2f m" % opt_vars_maxobj[1])
#     # print("Payload mass: %0.0f g" % opt_vars_maxobj[2])

   
# #     print(aircraft.weight(opt_vars_maxobj, AR, S)["Total"]/9.8, "total")
# #     print(aircraft.center_of_mass(opt_vars_maxobj, AR, S))
# #     print(aircraft.neutral_point(opt_vars_maxobj, AR, S))
    
# #     print(aircraft.spiral_coeff(opt_vars_maxobj, AR, S))
# #     print(aircraft.vertical_tail_coeff(opt_vars_maxobj, AR, S))
# #     print(aircraft.horizontal_tail_coeff(opt_vars_maxobj, AR, S))

#     print(aircraft.lift_coefficient(opt_vars_maxobj, AR, S))
#     results = {
#     "Total Weight (kg)": aircraft.weight(opt_vars_maxobj, AR, S)["Total"] / 9.8,
#     "Center of Mass": aircraft.center_of_mass(opt_vars_maxobj, AR, S),
#     "Neutral Point": aircraft.neutral_point(opt_vars_maxobj, AR, S),
#     "Spiral Coefficient": aircraft.spiral_coeff(opt_vars_maxobj, AR, S),
#     "Vertical Tail Coefficient": aircraft.vertical_tail_coeff(opt_vars_maxobj, AR, S),
#     "Horizontal Tail Coefficient": aircraft.horizontal_tail_coeff(opt_vars_maxobj, AR, S),
#     "Lift Coefficient": aircraft.lift_coefficient(opt_vars_maxobj, AR, S),
#     }

#     print("\n=== Aircraft Performance Summary ===")
#     for key, value in results.items():
#           print(f"{key:<30}: {value}")
        
#     print(opt_vars_maxobj)
#     print("Objective: %0.8f " % obj_max)
#     print("Alpha: %0.8f degrees" % aircraft.alpha(opt_vars_maxobj))
    
#     print("Tail_COM: %0.8f m" % aircraft.tail_COM(opt_vars_maxobj, -10))
    
#     print("Payload_loc: %0.8f m" % aircraft.payload_loc(opt_vars_maxobj))
# #     print(aircraft.mass_breakdown(opt_vars_maxobj, None, None))
# (N_initialGuess, l_AR_initialGuess, l_m_initialGuess, AR_initialGuess, S_initialGuess, Sh_initialGuess, Sv_initialGuess)
    
    # opt_vars_maxobj = [1.303, 0.436/0.9173, -0.2739/0.9173, 4.74, 0.1775, 0.0296, 0.0128]
    # aircraft.taper = 0.744
    # aircraft.dihedral = 7.14
    # aircraft.AR_h =  6.877
    aircraft.plot_plane(opt_vars_maxobj, None, None)
    print(GetObjective(aircraft, opt_vars_maxobj))

# #     print(opt_vars_maxobj)

#     pos_ang = 10
    
#     # opt = [1, 0.455, -0.12, 4, 0.22, 0.0566, 0.01] #wonk
    # opt = [1, 0.4, -0.085, 5.85, 0.185, 0.036, 0.01]
    # opt = [1, 0.43, -0.085, 4.74, 0.2,0.0485, 0.01]
    # plen = UEFC()
    # plen.AR_h = 8.2
    # plen.plot_plane(opt, None, None)

#     # print(aircraft.tail_alpha(opt_vars_maxobj) )
#     # print(aircraft.alpha_tail(opt_vars_maxobj, decalage_angle=pos_ang))
#     # print(aircraft.tail_COM(opt_vars_maxobj, pos_ang))
#     # print(aircraft.neutral_point(opt_vars_maxobj, AR, S))


    #check payload and check statc margn locatons.
    
    # print(aircraft.payload_loc(opt_vars_maxobj, -0.248))
    
    AR = opt_vars_maxobj[3]
    S = opt_vars_maxobj[4]

    print("\n=== Full Aircraft Diagnostic ===")
    print(f"opt_vars: {opt_vars_maxobj}")
    # print("Objective: %0.8f " % obj_max)
    print(f"N (load factor):          {opt_vars_maxobj[0]:.4f}")
    print(f"l_AR (tail arm ratio):    {opt_vars_maxobj[1]:.4f}")
    print(f"l_m (motor arm ratio):    {opt_vars_maxobj[2]:.4f}")
    print(f"AR (aspect ratio):        {opt_vars_maxobj[3]:.4f}")
    print(f"S (wing area):            {opt_vars_maxobj[4]:.4f} m^2")
    print(f"Sh (horiz tail area):     {opt_vars_maxobj[5]:.4f} m^2")
    print(f"Sv (vert tail area):      {opt_vars_maxobj[6]:.4f} m^2")

    print("\n--- Geometry ---")
    dims = aircraft.wing_dimensions(opt_vars_maxobj, AR, S)
    for k, v in dims.items():
        print(f"  {k}: {v:.4f}")

    print("\n--- Weights ---")
    weight = aircraft.weight(opt_vars_maxobj, AR, S)
    for k, v in weight.items():
        print(f"  {k}: {v:.4f} N  ({v/9.81*1000:.1f} g)")
    print(f"  Fuselage weight:        {aircraft.fuselage_weight(opt_vars_maxobj, AR, S):.4f} N")
    print(f"  Wing weight:            {aircraft.wing_weight(opt_vars_maxobj, AR, S):.4f} N")
    print(f"  Payload weight:         {aircraft.payload_weight(opt_vars_maxobj, AR, S):.4f} N")
    print(f"  Payload fraction:       {aircraft.payload_fraction(opt_vars_maxobj, AR, S):.4f}")

    print("\n--- Aerodynamics ---")
    print(f"  Alpha:                  {aircraft.alpha(opt_vars_maxobj):.4f} rad  ({np.degrees(aircraft.alpha(opt_vars_maxobj)):.4f} deg)")
    print(f"  Tail alpha:             {aircraft.tail_alpha(opt_vars_maxobj):.4f} rad")
    print(f"  Lift coefficient CL:    {aircraft.lift_coefficient(opt_vars_maxobj, AR, S):.4f}")
    print(f"  Profile drag CDp:       {aircraft.profile_drag_coefficient(opt_vars_maxobj, AR, S):.4f}")
    print(f"  Induced drag CDi:       {aircraft.induced_drag_coefficient(opt_vars_maxobj, AR, S):.4f}")
    print(f"  Fuselage drag CDfuse:   {aircraft.fuse_drag_coefficient(opt_vars_maxobj, AR, S):.4f}")
    print(f"  Payload drag CDpay:     {aircraft.payload_drag_coefficient(opt_vars_maxobj, AR, S):.4f}")
    # print(f"  Total drag CD:          {aircraft.drag_coefficient(opt_vars_maxobj, AR, S):.4f}")
    print(f"  Span efficiency e:      {aircraft.span_efficiency(opt_vars_maxobj, AR, S):.4f}")
    print(f"  Max camber epsilon:     {aircraft.max_camber():.4f}")

    print("\n--- Stability ---")
    print(f"  Neutral point:          {aircraft.neutral_point(opt_vars_maxobj, AR, S):.4f} m")
    print(f"  Center of mass:         {aircraft.center_of_mass(opt_vars_maxobj, AR, S):.4f} m")
    print(f"  Static margin (NP-COM): {aircraft.neutral_point(opt_vars_maxobj, AR, S) - aircraft.center_of_mass(opt_vars_maxobj, AR, S):.4f} m")
    print(f"  Tail COM:               {aircraft.tail_COM(opt_vars_maxobj):.4f} m")
    print(f"  Payload loc:            {aircraft.payload_loc(opt_vars_maxobj):.4f} m")
    print(f"  Spiral coefficient:     {aircraft.spiral_coeff(opt_vars_maxobj, AR, S):.4f}")
    print(f"  Horiz tail coeff:       {aircraft.horizontal_tail_coeff(opt_vars_maxobj, AR, S):.4f}  (bounds: 0.3 - 0.6)")
    print(f"  Vert tail coeff:        {aircraft.vertical_tail_coeff(opt_vars_maxobj, AR, S):.4f}  (bounds: 0.02 - 0.06)")
    print(f"  Wing tip deflection:    {aircraft.wing_tip_deflection(opt_vars_maxobj, AR, S):.4f}  (max: {aircraft.dbmax})")
    
    print("\n--- Performance ---")
    print(f"  Flight velocity:        {aircraft.flight_velocity(opt_vars_maxobj, AR, S):.4f} m/s")
    print(f"  Turn rate:              {aircraft.turn_rate(opt_vars_maxobj, AR, S):.4f} rad/s")
    print(f"  Required thrust:        {aircraft.required_thrust(opt_vars_maxobj, AR, S):.4f} N")
    print(f"  Maximum thrust:         {aircraft.maximum_thrust(aircraft.flight_velocity(opt_vars_maxobj, AR, S)):.4f} N")
    print(f"  Excess thrust:          {aircraft.excess_thrust(opt_vars_maxobj, AR, S):.4f} N")

    print("\n--- Tail deflection sweep ---")
    tail_deflection_bounds = np.linspace(0, 7, 99) * np.pi/180
    
    payload_loc = aircraft.payload_loc(opt_vars_maxobj, tail_deflection_bounds)

    stability = aircraft.isStable(opt_vars_maxobj, tail_deflection_bounds)
    # print(f"{stability=}")

    stable_mask = stability  # boolean array
    stable_indices = np.where(stable_mask)[0]

    if len(stable_indices) == 0:
        payload_diff = 0.01  # no stable region
    else:
        first_stable = stable_indices[0]
        last_stable = stable_indices[-1]
        payload_diff = payload_loc[first_stable] - payload_loc[last_stable]
    # plt.plot(tail_deflection_bounds, com_move)
    # plt.show()
    print(f"{payload_loc[first_stable]=} m")
    print(f"{first_stable=}")
    print(f"{payload_loc[last_stable]=} m")
    print(f"{last_stable=}")
    print(f"{aircraft.flight_velocity(opt_vars_maxobj, None, None)}")
    mass_breakdown = aircraft.mass_breakdown(opt_vars_maxobj, None, None)
    print(f"\n{'Component':<20} {'Mass (kg)':>12} {'Position (m)':>14}")
    print("-" * 48)
    for component, (mass, position) in mass_breakdown.items():
        print(f"{component:<20} {mass:>12.4f} {position:>14.4f}")
    print("-" * 48)
    total_mass = sum(v[0] for v in mass_breakdown.values())
    print(f"{'TOTAL':<20} {total_mass:>12.4f}")
    print(aircraft.payload_fraction(opt_vars_maxobj, AR, S))
    