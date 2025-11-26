import numpy as np
import matplotlib.pyplot as plt
import time, sys, shutil

# ================= COOL TERMINAL ANIMATIONS =================

def slow_print(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def animated_title(text):
    cols = shutil.get_terminal_size().columns
    centered = text.center(cols)

    print("\n")
    for ch in centered:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n" + "=" * cols)
    print("   RLC Circuit Analyzer for Frequency Domain Analysis   ")
    print("=" * cols + "\n")

# ================= USER INPUT =================

animated_title(" RLC CIRCUIT ANALYZER")

slow_print(" Enter circuit parameters below:")

R = float(input("Resistance R (Ohms)       : "))
L = float(input("Inductance L (Henrys)     : "))
C = float(input("Capacitance C (Farads)    : "))

f_start = float(input("Start Frequency (Hz)      : "))
f_end   = float(input("End Frequency (Hz)        : "))
points  = int(input("Number of Frequency Points: "))

if points > 1500:
    slow_print("⚠ Too many points! Limiting to 1000 for smooth performance.")
    points = 1000

slow_print("\nProcessing your circuit... Please wait...\n", 0.03)

# ================= FREQUENCY SETUP =================

frequencies = np.linspace(f_start, f_end, points)
omega = 2 * np.pi * frequencies

# ================= CIRCUIT IMPEDANCE =================

Z_total = R + 1j * omega * L + 1 / (1j * omega * C)

# ================= AUTO CIRCUIT IDENTIFICATION =================

if R == 0 and L != 0 and C != 0:
    circuit_type = "LC Circuit"
elif L == 0 and R != 0 and C != 0:
    circuit_type = "RC Circuit"
elif C == 0 and R != 0 and L != 0:
    circuit_type = "RL Circuit"
elif R != 0 and L != 0 and C != 0:
    circuit_type = "RLC Circuit"
else:
    circuit_type = "Pure Resistive Circuit"

slow_print("Detected Circuit Type  : " + circuit_type)

# ================= RESONANT FREQUENCY =================

f_res = None
if L != 0 and C != 0:
    f_res = 1 / (2 * np.pi * np.sqrt(L * C))
    slow_print(f"Resonant Frequency      : {f_res:.2f} Hz")

# ================= TRANSFER FUNCTION =================

H = 1 / Z_total
H_mag = np.abs(H)
H_phase = np.angle(H, deg=True)
H_mag_db = 20 * np.log10(H_mag + 1e-12)  # avoid log(0)

# ================= BODE ESTIMATIONS =================

gain_cross_index = np.argmin(np.abs(H_mag_db))
f_gc = frequencies[gain_cross_index]

phase_cross_index = np.argmin(np.abs(H_phase + 180))
f_pc = frequencies[phase_cross_index]

gain_margin = -H_mag_db[phase_cross_index]
phase_margin = 180 + H_phase[gain_cross_index]

slow_print("\n===== BODE ESTIMATED PARAMETERS =====")
slow_print(f"Gain Crossover Frequency  : {f_gc:.2f} Hz")
slow_print(f"Phase Crossover Frequency : {f_pc:.2f} Hz")
slow_print(f"Gain Margin (GM)          : {gain_margin:.2f} dB")
slow_print(f"Phase Margin (PM)         : {phase_margin:.2f}°")

# ================= FIXED STABILITY CHECK =================

if R < 0:
    stability = "UNSTABLE (Negative Resistance / Active Circuit)"
elif R == 0 and L != 0 and C != 0:
    stability = "MARGINALLY STABLE (Undamped LC Oscillations)"
elif R > 0:
    stability = "STABLE (Passive RLC Circuit)"
else:
    stability = "INDETERMINATE"

slow_print("\nStability Status : " + stability)

# ================= BODE PLOT =================

fig, ax1 = plt.subplots(figsize=(10,6))
ax1.set_xscale("log")
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Gain (dB)")
ax1.grid(True, which="both")

# Gain plot
ax1.plot(frequencies, H_mag_db, label="Gain (dB)")

# Phase plot
ax2 = ax1.twinx()
ax2.plot(frequencies, H_phase, linestyle="--", label="Phase (Degrees)")
ax2.set_ylabel("Phase (Degrees)")

# Markers
ax1.axvline(f_gc, linestyle="--", color="red")
ax2.axvline(f_pc, linestyle=":", color="purple")

if f_res:
    ax1.axvline(f_res, linestyle=":", color="orange")

# ================= INFO BOX =================

res_text = "N/A" if f_res is None else f"{f_res:.2f} Hz"

info_text = (
    f"Circuit Type : {circuit_type}\n"
    f"Resonant Freq: {res_text}\n"
    f"Gain CF      : {f_gc:.2f} Hz\n"
    f"Phase CF     : {f_pc:.2f} Hz\n"
    f"GM : {gain_margin:.2f} dB\n"
    f"PM : {phase_margin:.2f}°\n"
    f"Stability    : {stability}"
)

box_props = dict(boxstyle="round", facecolor="white", edgecolor="black", alpha=0.9)

fig.text(
    0.78,
    0.7,
    info_text,
    fontsize=10,
    verticalalignment="top",
    bbox=box_props
)

# ================= DISPLAY =================

plt.title("Bode Plot")
plt.tight_layout()
plt.show()