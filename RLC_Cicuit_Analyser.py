import numpy as np
import matplotlib.pyplot as plt
import shutil

# ================= CENTER HEADING FUNCTION =================

def center_heading(text):
    width = shutil.get_terminal_size().columns
    print("\n" + text.center(width))
    print("=" * width)

# ================= MAIN HEADING =================

center_heading("RLC CIRCUIT ANALYSER")

# ================= USER INPUT =================

R = float(input("\nEnter Resistance R (Ohms): "))
L = float(input("Enter Inductance L (Henrys): "))
C = float(input("Enter Capacitance C (Farads): "))

# ================= FREQUENCY RANGE =================

frequencies = np.linspace(10, 5000, 2000)
omega = 2 * np.pi * frequencies

# ================= IMPEDANCE =================

if C != 0:
    Z = R + 1j * omega * L + 1 / (1j * omega * C)
else:
    Z = R + 1j * omega * L

# ================= TRANSFER FUNCTION =================

H = 1 / Z
H_mag = np.abs(H)
H_phase = np.angle(H, deg=True)
H_mag_db = 20 * np.log10(H_mag + 1e-12)

# ================= CIRCUIT IDENTIFICATION =================

if R == 0 and L != 0 and C != 0:
    circuit = "LC Circuit"
elif L == 0 and R != 0 and C != 0:
    circuit = "RC Circuit"
elif C == 0 and R != 0 and L != 0:
    circuit = "RL Circuit"
elif R != 0 and L != 0 and C != 0:
    circuit = "RLC Circuit"
else:
    circuit = "Pure Resistive Circuit"

print("\nDetected Circuit Type :", circuit)

# ================= RESONANT FREQUENCY =================

f_res = None
if L != 0 and C != 0:
    f_res = 1 / (2 * np.pi * np.sqrt(L * C))
    print("Resonant Frequency    :", round(f_res, 2), "Hz")

# ================= STABILITY =================

if R < 0:
    stability = "UNSTABLE"
elif R == 0 and L != 0 and C != 0:
    stability = "MARGINALLY STABLE"
else:
    stability = "STABLE"

print("Stability Status      :", stability)

# ================= BODE VALUE HEADING =================

center_heading("BODE PLOT CALCULATED VALUES")

# ================= BODE VALUES =================

gain_cross_index = np.argmin(np.abs(H_mag_db))
f_gc = frequencies[gain_cross_index]

phase_cross_index = np.argmin(np.abs(H_phase + 180))
f_pc = frequencies[phase_cross_index]

gain_margin = -H_mag_db[phase_cross_index]
phase_margin = 180 + H_phase[gain_cross_index]

print(f"Gain Crossover Frequency : {f_gc:.2f} Hz")
print(f"Phase Crossover Frequency: {f_pc:.2f} Hz")
print(f"Gain Margin              : {gain_margin:.2f} dB")
print(f"Phase Margin             : {phase_margin:.2f} degrees")

# ================= COMBINED BODE PLOT =================

fig, ax1 = plt.subplots(figsize=(10,6))

ax1.set_xscale("log")
ax1.plot(frequencies, H_mag_db, label="Gain (dB)")
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Gain (dB)")
ax1.grid(True, which="both")

ax2 = ax1.twinx()
ax2.plot(frequencies, H_phase, linestyle="--", label="Phase (Degrees)")
ax2.set_ylabel("Phase (Degrees)")

if f_res:
    ax1.axvline(f_res, linestyle=":")

plt.title("Bode Plot (Gain & Phase Combined)")
plt.tight_layout()
plt.show()