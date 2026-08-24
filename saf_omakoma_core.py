import numpy as np

class SAFOmakomaCore:
    FEIGENBAUM_DELTA = 4.669201609102990
    FEIGENBAUM_ALPHA = 2.502907875095892
    ELEMENTARY_CHARGE_C = 1.602176634e-19
    ELECTRON_MASS_KG = 9.1093837015e-31
    BIFURCATION_LEVELS = 11

    @classmethod
    def calculate_bifurcation_matrix(cls, r_start=2.5, steps=11):
        """Berechnet 11 diskrete Stabilitäts-Bifurkationspunkte nach Feigenbaum"""
        r_vals = [r_start]
        for i in range(1, steps):
            r_next = r_vals[-1] + (r_vals[-1] / (cls.FEIGENBAUM_DELTA ** (i / 3.0)))
            r_vals.append(round(r_next, 6))
        return r_vals

    @classmethod
    def get_cyclotron_frequency(cls, B_field_tesla=5.0):
        q = cls.ELEMENTARY_CHARGE_C
        m = cls.ELECTRON_MASS_KG
        return (q * B_field_tesla) / m

if __name__ == "__main__":
    matrix = SAFOmakomaCore.calculate_bifurcation_matrix()
    omega_ce = SAFOmakomaCore.get_cyclotron_frequency()
    print(f"OMAKOMA N=11 Matrix: {matrix}")
    print(f"Plasma Resonanz omega_ce: {omega_ce:.4e} rad/s")
