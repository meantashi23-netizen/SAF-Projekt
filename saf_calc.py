import numpy as np
import matplotlib.pyplot as plt

def generate_bifurcation():
    r_values = np.linspace(2.5, 4.0, 1000)
    results = []
    x = 0.5
    for r in r_values:
        for _ in range(100): x = r * x * (1 - x)
        for _ in range(50): 
            x = r * x * (1 - x)
            results.append((r, x))
    r_arr, x_arr = zip(*results)
    plt.figure(figsize=(10, 6))
    plt.scatter(r_arr, x_arr, s=0.1, color='purple', alpha=0.3)
    plt.title("SAF Bifurkations-Diagramm")
    plt.savefig("bifurkation_output.png")
    plt.close()

def generate_mandelbrot_4d():
    width, height = 500, 500
    img = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            # Quaternion Slice (x, y, 0.1, 0.1)
            c = (-0.5 + 2.0*x/width, -1.0 + 2.0*y/height, 0.1, 0.1)
            z = (0, 0, 0, 0)
            iter = 0
            while iter < 50:
                z = (z[0]**2 - z[1]**2 - z[2]**2 - z[3]**2 + c[0],
                     2*z[0]*z[1] + c[1],
                     2*z[0]*z[2] + c[2],
                     2*z[0]*z[3] + c[3])
                if sum(val**2 for val in z) > 4: break
                iter += 1
            img[x, y] = iter
    plt.figure(figsize=(8, 8))
    plt.imshow(img.T, cmap='inferno')
    plt.axis('off')
    plt.savefig("mandelbrot_4d_output.png")
    plt.close()

generate_bifurcation()
generate_mandelbrot_4d()
