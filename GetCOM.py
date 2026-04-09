import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_plane_cg(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]
    chord = UEFC.wing_dimensions(opt_vars, AR, S)["Mean chord"]
    
    span = UEFC.wing_dimensions(opt_vars, AR, S)["Span"]

    mass_dict = GetMassBreakdown(UEFC, opt_vars, AR, S)
    fig, ax = plt.subplots(figsize=(12, 6))

    # 1. Draw the Wing (Rectangle)
    # Rectangle( (x_start, y_start), width, height )
    # Centered on Y=0, so y_start is -span/2
    wing = patches.Rectangle((0, -span/2), chord, span, 
                             linewidth=2, edgecolor='blue', facecolor='skyblue', 
                             alpha=0.3, label='Wing Planform')
    
    Sh = UEFC.Sh
    span_t = np.sqrt(Sh * UEFC.AR_h)
    chord_t = np.sqrt(Sh / UEFC.AR_h)
    tail_pos = mass_dict["tail"][1]

    tail = patches.Rectangle((tail_pos - chord_t/4, -span_t/2), chord_t, span_t, 
                             linewidth=2, edgecolor='blue', facecolor='skyblue', 
                             alpha=0.3, label='Wing Planform')
    ax.add_patch(wing)
    ax.add_patch(tail)

    # 2. Draw the Fuselage Stick (Line)
    all_x = [m[1] for m in mass_dict.values()]
    plt.plot([min(all_x), max(all_x)], [0, 0], color='black', linewidth=2, zorder=1)

    # 3. Calculate and Plot Mass Dots
    total_moment = 0
    total_mass = 0
    
    for label, (m, pos) in mass_dict.items():
        if m <= 0: continue
        total_moment += m * pos
        total_mass += m
        
        # Plot the component mass dot
        plt.scatter(pos, 0, s=m*10000, alpha=0.8, edgecolors='black', zorder=3)
        plt.text(pos, 0.05, f"{label}\n{m:.3f}kg", ha='center', fontsize=8, rotation=45)

    # 4. Calculate Total CG
    cg_total = total_moment / total_mass
    
    # Draw CG Marker
    plt.axvline(cg_total, color='red', linestyle='--', alpha=0.7)
    plt.scatter(cg_total, 0, color='red', marker='X', s=250, label=f'Total CG: {cg_total:.3f}m', zorder=4)

    # Formatting
    plt.title(f"Wing Geometry & Mass Distribution (Datum: Wing Leading Edge)")
    plt.xlabel("Distance from Wing Leading Edge (meters)")
    plt.ylabel("Wing Span (meters)")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.axis('equal') # Keeps the wing proportions square
    plt.legend(loc='upper right')
    
    # Add a note about the 25% Chord (Aerodynamic Center)
    plt.axvline(0.25 * chord, color='green', linestyle=':', alpha=0.5)
    plt.text(0.25 * chord, -span/2 - 0.1, "Typical 25% MAC", color='green', ha='center')

    plt.show()

def GetMassBreakdown(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    c_bar = UEFC.wing_dimensions(opt_vars, AR, S)["Mean chord"]
    b = UEFC.wing_dimensions(opt_vars, AR, S)["Span"]

    mass_breakdown = {
        #"object" : [mass, position]
        "wing" : [UEFC.wing_weight(opt_vars, AR, S) / 9.8, 0.25 * c_bar],
        "tail" : [(UEFC.Sh + UEFC.Sv) * 0.014 / 0.07, opt_vars[1] * b],
        "motor" : [0.0809 + 0.013, opt_vars[2] * b],
        "radio + batt" : [0.132 + 0.0091+ 0.012, 0.5 * c_bar], 
        "servos" : [0.016, 1.5 * c_bar],
        "boom" : [0.0389 * (opt_vars[1] - opt_vars[2]) *b /0.92,  (opt_vars[1] + opt_vars[2]) * b /2 ],
        "push_rods" : [.024 *  ( opt_vars[1] * b - 1.5 * c_bar )/ (0.92 - 0.17 - 1.5 * 0.15), ( 1.5 * c_bar + opt_vars[1] * b) /2],
        "payload" : [0.25, opt_vars[5] * b]
    }
    return mass_breakdown

def GetCOM(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    mass_breakdown = GetMassBreakdown(UEFC, opt_vars, AR, S)
    mass = 0
    com = 0
    for elem in mass_breakdown:
        mass += mass_breakdown[elem][0]
        com += mass_breakdown[elem][0] * mass_breakdown[elem][1]

    return com/ mass 

def GetMass(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    mass_breakdown = GetMassBreakdown(UEFC, opt_vars, AR, S)
    mass = 0
    
    for elem in mass_breakdown:
        mass += mass_breakdown[elem][0]
        
    return mass 

def GetWeight(UEFC, opt_vars, AR, S):
    AR = opt_vars[3]
    S = opt_vars[4]

    return {"Total" : GetMass(UEFC, opt_vars, AR, S) * 9.8}