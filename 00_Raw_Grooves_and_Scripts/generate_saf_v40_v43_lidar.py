import numpy as np, scipy.io.wavfile as w, scipy.signal as s
SR, DUR = 44100, 10
t = np.linspace(0, DUR, SR * DUR, endpoint=False)

def gen_lidar_saf(v, f_base, symb_val, thresh):
    S = np.clip(symb_val / 999.0, 0.0, 0.999)
    # LiDAR PCD Simulation (Point Cloud Data -> Valency Masking)
    num_points = int(SR * DUR / 100)
    pcd_valency = np.random.rand(num_points)
    lidar_mask = np.repeat(pcd_valency > thresh, 100)[:len(t)].astype(float)
    
    # SAF Phase & Feigenbaum Chaos
    x = 0.5 * np.ones(len(t))
    r = 3.8 + 0.19 * S
    for i in range(1, len(t)): x[i] = r * x[i-1] * (1 - x[i-1])
    
    b, a = s.butter(3, [600/(SR/2), 4800/(SR/2)], 'band')
    chaos = s.lfilter(b, a, x - np.mean(x))
    
    # LiDaR-gefilterter Spatial Mix
    carrier = np.sin(2 * np.pi * f_base * t)
    spatial_pcd = carrier * lidar_mask
    mix_l = (spatial_pcd * (1 - S)) + (chaos * S * 0.4)
    mix_r = (np.roll(spatial_pcd, 150) * (1 - S)) + (np.roll(chaos, 300) * S * 0.4)
    
    m = np.max(np.abs([mix_l, mix_r]))
    w.write(f"opt_saf_{v}.wav", SR, (np.vstack((mix_l/m, mix_r/m)).T * 32767).astype(np.int16))

for v, f, s_val, th in [('v40_lidar_scan_025', 164.81, 250, 0.25), ('v41_lidar_dense_050', 246.94, 500, 0.50), ('v42_lidar_valency_075', 370.00, 750, 0.75), ('v43_lidar_pointcloud_max', 493.88, 999, 0.90)]:
    gen_lidar_saf(v, f, s_val, th); print(f"[SAF+LiDAR] opt_saf_{v}.wav (Threshold {th}) generiert.")
