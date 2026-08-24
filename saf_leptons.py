import numpy as np

class SAFLeptonData:
    ELEMENTARY_CHARGE_C = 1.602176634e-19
    PROTON_MASS_KG = 1.6726219e-27
    
    LEPTONS = {
        "elektron": {"symbol": "e-", "generation": 1, "charge_e": -1, "mass_MeV": 0.511, "mass_kg": 9.1093837015e-31, "lifetime_s": np.inf, "saf_freq_band": "WIF", "plasma_relevant": True},
        "elektron_neutrino": {"symbol": "nu_e", "generation": 1, "charge_e": 0, "mass_MeV": 8e-7, "mass_kg": 1.426e-36, "lifetime_s": np.inf, "saf_freq_band": "WIF", "plasma_relevant": False},
        "myon": {"symbol": "mu-", "generation": 2, "charge_e": -1, "mass_MeV": 105.66, "mass_kg": 1.883531627e-28, "lifetime_s": 2.1969811e-6, "saf_freq_band": "MIF", "plasma_relevant": False},
        "myon_neutrino": {"symbol": "nu_mu", "generation": 2, "charge_e": 0, "mass_MeV": 0.17, "mass_kg": 3.03e-31, "lifetime_s": np.inf, "saf_freq_band": "MIF", "plasma_relevant": False},
        "tauon": {"symbol": "tau-", "generation": 3, "charge_e": -1, "mass_MeV": 1776.86, "mass_kg": 3.16754e-27, "lifetime_s": 2.903e-13, "saf_freq_band": "HIF", "plasma_relevant": False},
        "tauon_neutrino": {"symbol": "nu_tau", "generation": 3, "charge_e": 0, "mass_MeV": 15.5, "mass_kg": 2.76e-29, "lifetime_s": np.inf, "saf_freq_band": "HIF", "plasma_relevant": False}
    }

    @classmethod
    def get_cyclotron_frequency(cls, particle_key: str, B_field_tesla: float) -> float:
        p = cls.LEPTONS.get(particle_key)
        if not p or p["charge_e"] == 0:
            return 0.0
        q = abs(p["charge_e"]) * cls.ELEMENTARY_CHARGE_C
        m = p["mass_kg"]
        return (q * B_field_tesla) / m

if __name__ == "__main__":
    omega_ce = SAFLeptonData.get_cyclotron_frequency("elektron", B_field_tesla=5.0)
    print(f"{omega_ce:.4e}")
