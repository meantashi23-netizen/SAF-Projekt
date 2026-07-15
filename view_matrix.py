import mmap, time, os, datetime
shared_mem_path = 'saf_data/saf_shared_mem'
r_file = 'saf_data/r_val'
GRADIENT = " .:-=+*#%@"

print("Warte auf Kernel-Initialisierung...")
while not os.path.exists(shared_mem_path):
    time.sleep(1)

while True:
    try:
        with open(shared_mem_path, 'rb') as f:
            mm = mmap.mmap(f.fileno(), 1024, access=mmap.ACCESS_READ)
            data = mm.read(1024)
            mm.close()
            
            with open(r_file, 'r') as fr: r_val = fr.read().strip()
            
            os.system('clear')
            print(f"--- SAF SYSTEM | r: {r_val} ---")
            for y in range(32):
                row = "".join([GRADIENT[int((data[y*32+x] / 255) * (len(GRADIENT) - 1))] for x in range(32)])
                print(row)
    except Exception as e:
        print(f"Sync-Warten: {e}")
    time.sleep(0.1)
