import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class SAF41AnimatedEngine:
    def __init__(self, n_stages=150): # Geringere Punkte für flüssige 60 FPS Animation
        self.n = n_stages
        self.feigenbaum_constants = np.array([0.987, 0.933, 0.937, 0.954])
        self.phase_shift = np.pi / 2.0

    def get_mesh(self, t):
        theta = np.linspace(0, 2 * np.pi, self.n)
        phi = np.linspace(-np.pi / 2, np.pi / 2, self.n)
        u, v = np.meshgrid(theta, phi)

        w_phase = np.sin(u * self.feigenbaum_constants[0] + t) * np.cos(
            v * self.feigenbaum_constants[1] + self.phase_shift
        )

        x = (1 + 0.5 * np.cos(v + w_phase)) * np.cos(u)
        y = (1 + 0.5 * np.cos(v + w_phase)) * np.sin(u)
        z = 0.5 * np.sin(v + w_phase) + 0.2 * np.sin(
            self.feigenbaum_constants[2] * u * t
        )
        return x, y, z

engine = SAF41AnimatedEngine()
fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection="3d")

def update(frame):
    ax.clear()
    t = frame * 0.05
    x, y, z = engine.get_mesh(t)
    ax.plot_surface(x, y, z, cmap="plasma", edgecolor="k", linewidth=0.05, alpha=0.85)
    ax.set_title(f"SAF V41.0 QFS Resonanz-Dyn (t={t:.2f})")
    ax.set_zlim(-1, 1)

ani = FuncAnimation(fig, update, frames=200, interval=30)
plt.show()
