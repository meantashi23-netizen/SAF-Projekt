import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

class SAF41Render:
    def __init__(self, n_stages=200):
        self.n = n_stages
        self.feigenbaum = np.array([0.987, 0.933, 0.937, 0.954])

    def mesh(self, t):
        u = np.linspace(0, 2*np.pi, self.n)
        v = np.linspace(-np.pi/2, np.pi/2, self.n)
        U, V = np.meshgrid(u, v)
        w = np.sin(U * self.feigenbaum[0] + t) * np.cos(V * self.feigenbaum[1] + np.pi/2)
        X = (1 + 0.5 * np.cos(V + w)) * np.cos(U)
        Y = (1 + 0.5 * np.cos(V + w)) * np.sin(U)
        Z = 0.5 * np.sin(V + w) + 0.2 * np.sin(self.feigenbaum[2] * U * t)
        return X, Y, Z

r = SAF41Render()
fig = plt.figure(figsize=(10, 8), dpi=100)
ax = fig.add_subplot(111, projection="3d")

writer = FFMpegWriter(fps=30, metadata=dict(artist='SAF Engine'), bitrate=1800)

with writer.saving(fig, "saf_v41_hyper_mesh.mp4", 100):
    for i in range(150):
        ax.clear()
        t = i * 0.04
        X, Y, Z = r.mesh(t)
        ax.plot_surface(X, Y, Z, cmap="magma", edgecolor="none", alpha=0.9)
        ax.set_title(f"SAF V41.0 Engine Frame {i:03d}")
        ax.view_init(elev=20 + np.sin(t)*10, azim=i*2)
        writer.grab_frame()
