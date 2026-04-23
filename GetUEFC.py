# Implement UEFC (Unified Engineering Flight Competition) aircraft as a class.

import numpy as np

from GetWingDimensions import GetWingDimensions

from GetWfuse      import GetWfuse
from GetWingWeight import GetWingWeight
from GetWpay       import GetWpay
# from GetWeight     import GetWeight
from Getpf         import Getpf
# from GetMass       import GetMass
from GetCOM        import *
from GetNP         import GetNP
from GetStability  import *
from Getalpha      import Getalpha
from GetTailAngle  import *
from GetTailCOM    import GetTailCOM

from GetV       import GetV
from GetCL      import GetCL
from Getspaneff import Getspaneff
from GetCDp     import GetCDp
from GetCDi     import GetCDi
from GetCDfuse  import GetCDfuse
from GetCDpay   import GetCDpay
from GetCD      import GetCD

from Getepsilon import Getepsilon
from Getdb      import Getdb

from GetRequiredThrust import GetRequiredThrust
from GetMaxThrust      import GetMaxThrust
from GetExcessThrust   import GetExcessThrust
from GetOmega          import GetOmega

class UEFC:

    def __init__(self):

        # EXCEPT FOR CHANGING THE CONSTANTS AS YOU LOOK AT DIFFERENT
        # TAPER, DBMAX, MPAY_G, ETC YOU SHOULD NOT NEED TO CHANGE THIS CLASS.

        # Payload weight
        self.mpay_g   = 0.0 # payload weight in grams

        # Geometry parameters
        self.taper    = 0.5   # taper ratio
        self.dihedral = 10.0  # Wing dihedral (degrees)
        self.tau      = 0.12  # thickness-to-chord ratio

        # Tail parameters
        self.Sh = 0.04  # Wing area of horizontal tail (m^2)
        self.Sv = 0.03  # Wing area of vertical tail (m^2)

        # Fuselage parameters
        self.l_AR = 1.63  # Fuselage wingspan to length ratio (-)

        # Aerodynamic parameters
        self.CLdes = 0.75  # maximum CL wing will be designed to fly at (in cruise)
        self.e0    = 1.0   # Span efficiency for straight level flight

        # Wing bending and material properties
        self.dbmax   = 0.1     # tip displacement bending constraint
        self.rhofoam = 32.     # kg/m^3. high load foam
        self.Efoam   = 19.3E6  # Pa.     high load foam

        # Other modeling parameters
        self.rho = 1.225     # air density kg/m^3
        self.mu  = 1.789E-5  # dynamic viscosity of air N s/m^2
        self.g   = 9.81      # gravity, m/s^2
        self.R   = 12.5      # turn radius, meters. Track turn diameter / 2
        self.AR_h = 5

        self.CL_nom = 0.65
        self.Cm_nom = {
            0.08: -0.17,
            0.09: -0.16, 
            0.10: -0.15,
            0.11: -0.14,
            0.12: -0.13
        }
    # opt_vars is a vector representing the optimization variables
    # opt_vars[0]: Load factor (-)

    # YOU SHOULD NOT NEED TO CHANGE THESE METHOD CALLS
    def fuselage_weight(self, opt_vars, AR, S):
        return GetWfuse(self, opt_vars, AR, S)  # Fuselage weight (N)

    def wing_weight(self, opt_vars, AR, S):
        return GetWingWeight(self, opt_vars, AR, S)  # Wing weight (N)
    
    def horizontal_tail_coeff(self, opt_vars, AR, S):
        return GetHorTailVolume(self, opt_vars, AR, S)
    
    def plot_plane(self, opt_vars, AR, S):
        plot_plane_cg(self, opt_vars, AR, S)

    def tail_alpha(self, opt_vars):
        return GetTailAlpha(self, opt_vars)
    
    def alpha(self, opt_vars):
        return Getalpha(self, opt_vars)
    
    def alpha_tail(self, opt_vars, decalage_angle):
        return GetAlphaTail(self, opt_vars, decalage_angle)

    def vertical_tail_coeff(self, opt_vars, AR, S):
        return GetVertTailVolume(self, opt_vars, AR, S)
    
    def isStable(self, opt_vars, tail_angle):
        return isStable(self, opt_vars, tail_angle)
    
    def spiral_coeff(self, opt_vars, AR, S):
        return GetSpiral(self, opt_vars, AR, S)
    
    def mass_breakdown(self, opt_vars, AR, S):
        return GetMassBreakdown(self, opt_vars, AR, S)
    
    def payload_weight(self, opt_vars, AR, S):
        return GetWpay(self, opt_vars, AR, S)  # Payload weight (N)

    def weight(self, opt_vars, AR, S):
        return GetWeight(self, opt_vars, AR, S)  # Total weight; breakdown (N)

    def payload_fraction(self, opt_vars, AR, S):
        return Getpf(self, opt_vars, AR, S)

    def neutral_point(self, opt_vars, AR, S):
        return GetNP(self, opt_vars, AR, S)

    def tail_COM(self, opt_vars, tail_angle = None):
        return GetTailCOM(self, opt_vars, tail_angle)

    def mass(self, opt_vars, AR, S):
        return GetMass(self, opt_vars, AR, S)  # Total mass, and a breakdown (g)

    def flight_velocity(self, opt_vars, AR, S):
        return GetV(self, opt_vars, AR, S)  # Flight velocity (m/s)

    def lift_coefficient(self, opt_vars, AR, S):
        return GetCL(self, opt_vars, AR, S)  # Lift coefficient (-)

    def span_efficiency(self, opt_vars, AR, S):
        return Getspaneff(self, opt_vars, AR, S)  # Wing span efficiency (-)

    def profile_drag_coefficient(self, opt_vars, AR, S):
        return GetCDp(self, opt_vars, AR, S)  # Profile drag coefficient (-)

    def induced_drag_coefficient(self, opt_vars, AR, S):
        return GetCDi(self, opt_vars, AR, S)  # Induced drag coefficient (-)

    def fuse_drag_coefficient(self, opt_vars, AR, S):
        return GetCDfuse(self, opt_vars, AR, S)  # Fuselage drag coefficient (-)

    def payload_drag_coefficient(self, opt_vars, AR, S):
        return GetCDpay(self, opt_vars, AR, S)  # Payload drag coefficient (-)
    
    def payload_loc(self, opt_vars, tail_angle = None):
        return GetPayloadLoc(self, opt_vars, tail_angle)

    def drag_coefficient(self, opt_vars, AR, S):
        return GetCD(self, opt_vars, AR, S)  # Total drag coefficient; breakdown
    
    def center_of_mass(self, opt_vars, AR, S):
        return GetTailCOM(self, opt_vars)

    def max_camber(self):
        return Getepsilon(self)  # Maximum wing camber (-)

    def wing_tip_deflection(self, opt_vars, AR, S):
        return Getdb(self, opt_vars, AR, S)  # Wing tip deflection / wingspan

    def required_thrust(self, opt_vars, AR, S):
        return GetRequiredThrust(self, opt_vars, AR, S)  # Required thrust (N)

    def maximum_thrust(self, V):
        return GetMaxThrust(self, V)  # Maximum thrust (N)

    def excess_thrust(self, opt_vars, AR, S):  # Maximum - required thrust (N)
        return GetExcessThrust(self, opt_vars, AR, S)

    def wing_dimensions(self, opt_vars, AR, S):
        return GetWingDimensions(self, opt_vars, AR, S)

    def turn_rate(self, opt_vars, AR, S):  # Turn rate (rad/s)
        return GetOmega(self, opt_vars, AR, S)


if __name__ == "__main__":

    pass



