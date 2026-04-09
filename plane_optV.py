import numpy as np
import os
from matplotlib import pyplot as plt
plt.style.use(os.path.join(os.path.dirname(__file__), "uefc.mplstyle"))

# you may have to comment this line out if you are running from the command window
#from IPython    import get_ipython

from GetUEFC           import UEFC
from opt_obj           import opt_obj
from DS_report_opt_obj import report_opt_obj

plane = UEFC()

fuse_len = 1
S = 0.3
AR = 10
c = np.sqrt(S/AR)
b = c * AR
AR_h = 5
plane.Sv = 0.03
plane.Sh = 0.04
plane.l_AR = 2

l_w = 0.3 #where wing is placed with respect to the motor
payload = 0.25

l_h = plane.l_AR * c - l_w #how far horizontal stab is
l_tot = l_w + l_h
l_push = l_h - 1.5 * c

a_w = np.pi * 2 / (1 + 2 / AR)
a_h = 2 * np.pi /(1 + 2/ AR_h)

#tail specs
lv = 0.1

mass = {
    #obj: [weight(kg), location(m), with motor mount being at 0]
    "motor+batt": [0.0942, 0],
    "wing" : [plane.wing_weight(AR, S)/9.8, l_w + 0.25 * c],
    "tail" : [0.014 * (plane.Sh + plane.Sv), l_w + l_h],
    "radio+batt" : [0.1328+0.0091+0.012, l_w + 0.5 * c],
    "servos": [0.0166, l_w + 1.5 * c],
    "fuse_stick" : [0.0389/0.92*(l_w + l_h), (l_w + l_h)/2],
    "push_rods" : [0.024 * l_push / 0.6 , (l_tot + l_w + 1.5 * c )/2]
}

def com(mass):
    val = 0
    tot_mass = 0
    for elem in mass:
        val += mass[elem][0] * mass[elem][1]
        tot_mass += mass[elem][0]
    return val/tot_mass

def to_chord_pos(pos, chord, l_w):
    return (pos-l_w)/chord

def V_h(S_h, l_h, S, c):
    return S_h * l_h / (S * c)

def neutral_point(V_h, c, l_h, a_w, a_h):
    return (a_w/(4*a_h) + V_h *(1+c/(4*l_h)))/(a_w/a_h + V_h*c/l_h)


x_np = neutral_point(V_h(plane.Sh, plane.Sv, S, c), c, l_h, a_w, a_h)
x_com = com(mass)

print(plane.lift_coefficient([1], AR, S) )