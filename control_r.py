import os, sys, tty, termios
r_file = 'saf_data/r_val'

def get_r():
    try:
        with open(r_file, 'r') as f:
            c = f.read().strip()
            return float(c) if c else 3.0
    except: return 3.0

print("Steuerung aktiv: 'w' (+0.01), 's' (-0.01), 'e' (+0.001), 'd' (-0.001). 'q' zum Beenden.")
while True:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    r = get_r()
    if ch == 'w': r += 0.01
    elif ch == 's': r -= 0.01
    elif ch == 'e': r += 0.001
    elif ch == 'd': r -= 0.001
    elif ch == 'q': break
    
    with open(r_file, 'w') as f: f.write(str(round(r, 4)))
    print(f"\rNeuer r-Wert: {round(r, 4)}   ", end="")
