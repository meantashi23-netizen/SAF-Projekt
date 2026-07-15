import numpy as np
import matplotlib
# Aktiviert den ladefreien Backend-Modus für Terminal-Umgebungen
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def apply_saf_v29_3_3(grid_size, iterations, alpha_saf):
    # Initialisierung des Parameterraums (Lambda-Gitter)
    lambda_space = np.linspace(2.5, 4.0, grid_size)
    z = np.full(grid_size, 0.5)

    # Speicher für Bifurkations-Grenzwerte
    bifurcation_map = np.zeros((grid_size, iterations))

    for i in range(iterations):
        # SAF-Gleichungskern: Nicht-lineare Kopplung + Spektral-Alpha-Dämpfung
        z = lambda_space * z * (1 - z) + alpha_saf * np.cos(np.pi * z)

        # Aufzeichnen der Trajektorien nach der Einschwingphase
        if i >= (iterations // 2):
            bifurcation_map[:, i] = z

    return lambda_space, bifurcation_map

if __name__ == "__main__":
    print("Starte SAF V29.3.3 Berechnung...")
    
    # Parameter für eine detaillierte Auflösung
    GRID_SIZE = 2000
    ITERATIONS = 1000
    ALPHA_SAF = 0.02  # Intensität der Spektral-Alpha-Dämpfung
    
    lambda_data, b_map = apply_saf_v29_3_3(GRID_SIZE, ITERATIONS, ALPHA_SAF)
    
    print("Berechnung abgeschlossen. Generiere Diagramm...")
    
    # Ausschneiden der Einschwingphase (Spalten mit Index < ITERATIONS // 2 ignorieren)
    recorded_data = b_map[:, ITERATIONS // 2:]
    
    # Erzeugen der passenden X-Matrix (Lambda-Werte für jeden aufgezeichneten Iterationsschritt duplizieren)
    X = np.repeat(lambda_data[:, np.newaxis], recorded_data.shape[1], axis=1)
    
    # Plot-Konfiguration
    plt.figure(figsize=(12, 8), dpi=300)
    
    # ',k' zeichnet Pixel-Punkte in Schwarz für maximale Performance und Schärfe bei hoher Dichte
    plt.plot(X, recorded_data, ',k', alpha=0.1)
    
    plt.title(f"SAF V29.3.3 Bifurkationsdiagramm (alpha = {ALPHA_SAF})", fontsize=14)
    plt.xlabel(r"$\lambda$ (Parameterraum)", fontsize=12)
    plt.ylabel("$z$ (Attraktor-Zustände)", fontsize=12)
    plt.xlim(2.5, 4.0)
    plt.grid(True, which='both', alpha=0.2, linestyle='--')
    
    # Bild exportieren
    output_filename = "saf_bifurcation.png"
    plt.savefig(output_filename, bbox_inches='tight')
    plt.close()
    
    print(f"Ergebnis erfolgreich gespeichert unter: {output_filename}")
