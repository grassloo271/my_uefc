import numpy as np
import matplotlib.pyplot as plt

tau_sweep = np.linspace(0.12, 0.08, 10)
lam_sweep = np.linspace(1, .5, 10)
X, Y = np.meshgrid(tau_sweep, lam_sweep)
print(X.shape)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

Z = np.load("data_DS4_test.npz")['z']
Z=np.reshape(Z, (10, 10))
print(Z)
surf = ax.plot_surface(X, Y, Z)
ax.set_xlabel(r'$\tau$'+ " (tau)")
ax.set_ylabel(r'$\lambda$'+" (lambda)")
ax.set_zlabel('Speed')
plt.show()