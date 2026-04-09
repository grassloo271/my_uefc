import numpy as np
from scipy.optimize import minimize, Bounds
from GetUEFC        import UEFC
from GetObjective   import GetObjective

def opt_obj(UEFC):
    AR = 1
    S = 1
    # YOU SHOULD NOT NEED TO CHANGE THIS FUNCTION FOR THIS PROBLEM

    # Determine the maximum objective function (velocity)
    # achievable for an airplane with the inputted values of AR, S.

    # Optimization variables: N

    # Maximize objective: minimize negative of objective (ORIGINAL)
    #obj_fcn = lambda opt_vars: -GetObjective(UEFC, opt_vars, AR, S)

    # Modification (otherwise solution not always found)
    obj_fcn = lambda opt_vars: -GetObjective(UEFC, opt_vars) * (1./3.)
    # optimization variable is the load factor of the turn.
    N_initialGuess = 1.25
    N_lowerBound   = 1.01
    N_upperBound   = 5.0

    l_AR_initialGuess = 1 #from wing to tail
    l_AR_lowerBound = 0.2
    l_AR_upperBound = 3

    l_m_initialGuess = -0.3 #similar definition to l_AR but for the motor
    l_m_lowerBound = -0.5
    l_m_upperBound = -.05

    AR_initialGuess = 5
    AR_lowerBound = 1
    AR_upperBound = 10

    S_initialGuess = 0.354
    S_lowerBound = 0.05
    S_upperBound = 0.5

    # R_initialGuess = 6.0
    # R_lowerBound   = 0.1
    # R_upperBound   = 12.5

    # mpay_initialGuess = 10.
    # mpay_lowerBound   = 0.01
    # mpay_upperBound   = 1000.
    
    initialGuess = (N_initialGuess, l_AR_initialGuess, l_m_initialGuess, AR_initialGuess, S_initialGuess)
    
    bounds       = Bounds(lb=(N_lowerBound, l_AR_lowerBound, l_m_lowerBound, AR_lowerBound, S_lowerBound), ub=(N_upperBound, l_AR_upperBound, l_m_upperBound, AR_upperBound, S_upperBound), keep_feasible=True)

    # Constraint format is different, depending on algorithm.
    method = "SLSQP"
    if method == "SLSQP":

        # Excess thrust (max - required thrust) must be positive.
        T_constraint = {
                "type": "ineq",
                "fun":  lambda opt_vars: UEFC.excess_thrust(opt_vars, AR, S)
                }

        # Wingtip deflection must be less than the maximum allowed value.
        db_constraint = {
                "type": "ineq",
                "fun":  lambda opt_vars: UEFC.dbmax \
                - UEFC.wing_tip_deflection(opt_vars, AR, S)
                }

        # Lift coefficient must be less than the maximum allowed cruise value.
        CL_constraint = {
                "type": "ineq",
                "fun": lambda opt_vars: UEFC.CLdes \
                - UEFC.lift_coefficient(opt_vars, AR, S)
            }
        
        SM_constraint = {
                "type": "ineq",
                "fun" : lambda opt_vars: UEFC.neutral_point(opt_vars, AR, S) - UEFC.center_of_mass(opt_vars, AR, S)  
                #coordinate
        }
    
        Vert_constrant_lower = {
                "type": "ineq",
                "fun" : lambda opt_vars: UEFC.vertical_tail_coeff(opt_vars, AR, S)  -  0.02 
        }

        Vert_constrant_upper = {
                "type": "ineq",
                "fun" : lambda opt_vars: 0.06 - UEFC.vertical_tail_coeff(opt_vars, AR, S)   
        }

        Hor_constrant_lower = {
                "type": "ineq",
                "fun" : lambda opt_vars: UEFC.horizontal_tail_coeff(opt_vars, AR, S)  -  0.3
        }

        Hor_constrant_upper = {
                "type": "ineq",
                "fun" : lambda opt_vars: 0.6 - UEFC.horizontal_tail_coeff(opt_vars, AR, S)   
        }

        Spral_constrant = {
                "type": "ineq",
                "fun" : lambda opt_vars:  UEFC.spiral_coeff(opt_vars, AR, S) - 5  
        }

    else:
        raise AttributeError("Optimization method " + method \
                             + " not recognized.")

    constraints = [T_constraint, db_constraint, CL_constraint, SM_constraint, Spral_constrant,  Hor_constrant_lower ,Vert_constrant_lower, Vert_constrant_upper, Hor_constrant_upper]
    
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
    aircraft.dihedral = 5
    
    aircraft.Sh = 0.03
    aircraft.Sv = 0.01
    # print(aircraft.weight(1.1, AR, S)["Total"], "total")
    opt_vars_maxobj, obj_max, success = opt_obj(aircraft)

    AR = opt_vars_maxobj[3]
    S = opt_vars_maxobj[4]
    
    print()
    print("Load factor:  %0.3f"   % opt_vars_maxobj[0])
    # print("Turn radius:  %0.2f m" % opt_vars_maxobj[1])
    # print("Payload mass: %0.0f g" % opt_vars_maxobj[2])

   
#     print(aircraft.weight(opt_vars_maxobj, AR, S)["Total"]/9.8, "total")
#     print(aircraft.center_of_mass(opt_vars_maxobj, AR, S))
#     print(aircraft.neutral_point(opt_vars_maxobj, AR, S))
    
#     print(aircraft.spiral_coeff(opt_vars_maxobj, AR, S))
#     print(aircraft.vertical_tail_coeff(opt_vars_maxobj, AR, S))
#     print(aircraft.horizontal_tail_coeff(opt_vars_maxobj, AR, S))

    print(aircraft.lift_coefficient(opt_vars_maxobj, AR, S))
    results = {
    "Total Weight (kg)": aircraft.weight(opt_vars_maxobj, AR, S)["Total"] / 9.8,
    "Center of Mass": aircraft.center_of_mass(opt_vars_maxobj, AR, S),
    "Neutral Point": aircraft.neutral_point(opt_vars_maxobj, AR, S),
    "Spiral Coefficient": aircraft.spiral_coeff(opt_vars_maxobj, AR, S),
    "Vertical Tail Coefficient": aircraft.vertical_tail_coeff(opt_vars_maxobj, AR, S),
    "Horizontal Tail Coefficient": aircraft.horizontal_tail_coeff(opt_vars_maxobj, AR, S),
    "Lift Coefficient": aircraft.lift_coefficient(opt_vars_maxobj, AR, S),
    }

    print("\n=== Aircraft Performance Summary ===")
    for key, value in results.items():
          print(f"{key:<30}: {value}")
        
    print(opt_vars_maxobj)
    print("Objective: %0.8f m/s" % obj_max)
#     print(aircraft.mass_breakdown(opt_vars_maxobj, None, None))
    aircraft.plot_plane(opt_vars_maxobj, None, None)
#     print(opt_vars_maxobj)
