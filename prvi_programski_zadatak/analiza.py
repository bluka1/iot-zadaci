from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal

MAPA = Path(__file__).parent
SLIKE = MAPA / "slike"
SLIKE.mkdir(exist_ok=True)
ispis_redovi = []


def ispis(tekst=""):
    print(tekst)
    ispis_redovi.append(tekst)


def spremi(fig, naziv):
    fig.tight_layout()
    fig.savefig(SLIKE / f"{naziv}.svg")
    plt.close(fig)


G1 = signal.TransferFunction([27], [1, 4, 36])
G2 = signal.TransferFunction([34, 68], np.polymul([1, 4], [1, 6, 34]))
G3 = signal.TransferFunction([1, 5], [1, 4, 3, 18])
G4 = signal.TransferFunction([36], np.polymul([1, 1], [1, 36]))
A0 = np.polymul(np.polymul([1, 3], [1, 7]), [1, 10])
K_t = 442

# Task 1: G1 step response
wn = np.sqrt(36)
zeta = 4 / (2 * wn)
wd = wn * np.sqrt(1 - zeta**2)
Tp = np.pi / wd
PO = 100 * np.exp(-zeta * np.pi / np.sqrt(1 - zeta**2))
Ts = 4 / (zeta * wn)
y_inf = 27 / 36
y_max = y_inf * (1 + PO / 100)

t = np.linspace(0, 4, 8001)
t1, y1 = signal.step(G1, T=t)
i_max = np.argmax(y1)
van_pojasa = np.flatnonzero(np.abs(y1 - y_inf) > 0.02 * y_inf)
Ts_sim = t1[van_pojasa[-1] + 1]

ispis("ZADATAK 1")
ispis(f"polovi G1: {np.round(np.roots(G1.den), 3)}")
ispis(f"wn = {wn:.3f} rad/s, zeta = {zeta:.3f}, wd = {wd:.3f} rad/s")
ispis(f"Tp:     izracun {Tp:.3f} s,  signal.step {t1[i_max]:.3f} s")
ispis(f"y_max:  izracun {y_max:.3f},    signal.step {y1[i_max]:.3f}")
ispis(f"P.O.:   izracun {PO:.3f} %, signal.step {100 * (y1[i_max] - y_inf) / y_inf:.3f} %")
ispis(f"y(inf): izracun {y_inf:.3f},    signal.step {y1[-1]:.3f}")
ispis(f"Ts:     procjena {Ts:.3f} s, signal.step (pojas 2 %) {Ts_sim:.3f} s")
ispis(f"e_ss = {1 - y_inf:.3f}")

fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(t1, y1, color="tab:blue", label="y(t), signal.step")
ax.axhline(y_inf, color="tab:gray", ls="--", label=f"y(∞) = {y_inf:.3f}")
ax.axhspan(0.98 * y_inf, 1.02 * y_inf, color="tab:gray", alpha=0.15, label="pojas ±2 %")
ax.axvline(Tp, color="tab:red", ls=":", label=f"Tp = {Tp:.3f} s")
ax.plot(t1[i_max], y1[i_max], "o", color="tab:red", label=f"y_max = {y1[i_max]:.3f}")
ax.set_xlabel("t [s]"); ax.set_ylabel("y(t)")
ax.legend(fontsize=8, loc="lower right"); ax.grid(alpha=0.3)
spremi(fig, "z1_skokovni_G1")

# Task 2: G2 impulse and step, simulated against the analytical expressions
t = np.linspace(0, 4, 4001)
t2, yi = signal.impulse(G2, T=t)
_, ys = signal.step(G2, T=t)
kos, sin = np.cos(5 * t), np.sin(5 * t)
yi_an = -34 / 13 * np.exp(-4 * t) + np.exp(-3 * t) * (34 / 13 * kos + 408 / 65 * sin)
ys_an = 0.5 + 17 / 26 * np.exp(-4 * t) - np.exp(-3 * t) * (15 / 13 * kos + 11 / 65 * sin)

ispis()
ispis("ZADATAK 2")
ispis(f"polovi G2: {np.round(np.roots(G2.den), 3)}, nula: {np.round(np.roots(G2.num), 3)}")
ispis(f"najveca razlika impulsnog odziva i izraza: {np.max(np.abs(yi - yi_an)):.3e}")
ispis(f"najveca razlika skokovnog odziva i izraza: {np.max(np.abs(ys - ys_an)):.3e}")
razlika = np.gradient(ys_an, t)[1:-1] - yi_an[1:-1]
ispis(f"razlika dy_step/dt i y_imp: {np.max(np.abs(razlika)):.3e}")
ispis(f"y_imp(0) = {yi_an[0]:.3f}, y_step(0) = {ys_an[0]:.3f}, y_step(4 s) = {ys_an[-1]:.3f}")

fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(t2, yi, color="tab:blue", label="impulsni, signal.impulse")
ax.plot(t2, yi_an, color="tab:cyan", ls="--", label="impulsni, analitički")
ax.plot(t2, ys, color="tab:orange", label="skokovni, signal.step")
ax.plot(t2, ys_an, color="tab:red", ls="--", label="skokovni, analitički")
ax.set_xlabel("t [s]"); ax.set_ylabel("y(t)")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
spremi(fig, "z2_odzivi_G2")

# Task 3.1: G3 poles, Hurwitz determinants and step response
polovi = np.roots(G3.den)
a3, a2, a1, a0 = G3.den
H3 = np.array([[a2, a0, 0], [a3, a1, 0], [0, a2, a0]])
D = [H3[0, 0], np.linalg.det(H3[:2, :2]), np.linalg.det(H3)]

ispis()
ispis("ZADATAK 3.1")
ispis(f"polovi G3: {np.round(polovi, 3)}")
ispis(f"D1 = {D[0]:.3f}, D2 = {D[1]:.3f}, D3 = {D[2]:.3f}")

t = np.linspace(0, 30, 6001)
t3, y3 = signal.step(G3, T=t)
r, p, _ = signal.residue(G3.num, np.polymul(G3.den, [1, 0]))
par = np.argmax(p.imag)
ovojnica = 2 * np.abs(r[par]) * np.exp(p[par].real * t)
pomak = 5 / 18
ispis(f"ovojnica odziva: {pomak:.3f} +- {2 * np.abs(r[par]):.3f} exp({p[par].real:.3f} t)")
ispis(f"period oscilacija: {2 * np.pi / p[par].imag:.3f} s")

fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(t3, y3, color="tab:red", label="y(t), signal.step")
ax.plot(t, pomak + ovojnica, color="tab:gray", ls="--", label="ovojnica")
ax.plot(t, pomak - ovojnica, color="tab:gray", ls="--")
ax.set_xlabel("t [s]"); ax.set_ylabel("y(t)")
ax.legend(fontsize=8, loc="upper left"); ax.grid(alpha=0.3)
spremi(fig, "z31_skokovni_G3")

# Task 3.2: closed loop for K_t, K_kr and 1.2 K_kr
K_kr = A0[1] * A0[2] - A0[0] * A0[3]
w_kr = np.sqrt(A0[2])

ispis()
ispis("ZADATAK 3.2")
ispis(f"nazivnik zatvorenog kruga: s^3 + {A0[1]} s^2 + {A0[2]} s + ({A0[3]} + K)")
ispis(f"K_kr = {K_kr:.3f}, w_kr = {w_kr:.3f} rad/s, period = {2 * np.pi / w_kr:.3f} s")

t = np.linspace(0, 6, 6001)
fig, osi = plt.subplots(3, 1, figsize=(7, 5.6), sharex=True)
for ax, K, naziv in zip(osi, (K_t, K_kr, 1.2 * K_kr), ("K = K_t", "K = K_kr", "K = 1.2 K_kr")):
    Gz = signal.TransferFunction([K], A0 + np.array([0, 0, 0, K]))
    _, yz = signal.step(Gz, T=t)
    polovi_z = np.round(np.roots(Gz.den), 3) + 0
    ispis(f"K = {K:.1f}: polovi {polovi_z}, max|y| = {np.max(np.abs(yz)):.3f}")
    ax.plot(t, yz, color="tab:blue")
    ax.axhline(K / (210 + K), color="tab:gray", ls="--", linewidth=1)
    ax.set_ylabel("y(t)"); ax.set_title(f"{naziv} = {K:.0f}", fontsize=9); ax.grid(alpha=0.3)
osi[-1].set_xlabel("t [s]")
spremi(fig, "z32_zatvoreni_krug")

# Task 4.1: G4 Bode plot with the three computed points
w_nisko = 1e-3
w, mag, phase = signal.bode(G4, w=np.logspace(-3, 3, 2000))
tocke = [("0", 0.0), ("6", 6.0), ("36", 36.0)]

ispis()
ispis("ZADATAK 4.1")
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 5))
ax1.margins(y=0.12); ax2.margins(y=0.12)
ax1.semilogx(w, mag, color="tab:blue"); ax1.set_ylabel("A(ω) [dB]")
ax2.semilogx(w, phase, color="tab:red"); ax2.set_ylabel("φ(ω) [°]")
ax1.grid(True, which="both", alpha=0.3); ax2.grid(True, which="both", alpha=0.3)
ax2.set_xlabel("ω [rad/s]")
for oznaka, w_t in tocke:
    G_t = 36 / ((1j * w_t + 1) * (1j * w_t + 36))
    A_t = 20 * np.log10(np.abs(G_t))
    fi_t = np.degrees(np.angle(G_t)) + 0.0
    ispis(f"w = {w_t:6.3f}: |G4| = {np.abs(G_t):.3f}, A = {A_t:.3f} dB, fi = {fi_t:.3f} st")
    w_crtanje = max(w_t, w_nisko)
    ax1.plot(w_crtanje, A_t, "ko", markersize=4)
    ax2.plot(w_crtanje, fi_t, "ko", markersize=4)
    ax1.annotate(f"ω = {oznaka}: {A_t:.3f} dB", (w_crtanje, A_t), xytext=(6, 6),
                 textcoords="offset points", fontsize=8)
    ax2.annotate(f"ω = {oznaka}: {fi_t:.3f}°", (w_crtanje, fi_t), xytext=(6, 6),
                 textcoords="offset points", fontsize=8)
spremi(fig, "z41_bode_G4")

# Task 4.2: G0 Bode plot, phase crossover and gain margin
G0 = signal.TransferFunction([K_t], A0)
w, mag, phase = signal.bode(G0, w=np.logspace(-1, 3, 20001))
w180 = np.interp(180, -phase, w)
A180 = np.interp(np.log10(w180), np.log10(w), mag)
GM = -A180

ispis()
ispis("ZADATAK 4.2")
ispis(f"w_180 = {w180:.3f} rad/s, w_kr = {w_kr:.3f} rad/s")
GM_hurwitz = 20 * np.log10(K_kr / K_t)
ispis(f"A(w_180) = {A180:.3f} dB, GM = {GM:.3f} dB, 20 log(K_kr / K_t) = {GM_hurwitz:.3f} dB")

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 5))
ax1.semilogx(w, mag, color="tab:blue"); ax1.set_ylabel("A(ω) [dB]")
ax2.semilogx(w, phase, color="tab:red"); ax2.set_ylabel("φ(ω) [°]")
ax1.grid(True, which="both", alpha=0.3); ax2.grid(True, which="both", alpha=0.3)
ax2.set_xlabel("ω [rad/s]")
ax1.axhline(0, color="tab:gray", ls="--", linewidth=1)
ax2.axhline(-180, color="tab:gray", ls="--", linewidth=1)
ax1.axvline(w180, color="k", ls=":", linewidth=1)
ax2.axvline(w180, color="k", ls=":", linewidth=1)
ax1.plot(w180, A180, "ko", markersize=4)
ax2.plot(w180, -180, "ko", markersize=4)
ax1.annotate(rf"$A(\omega_{{180}})$ = {A180:.3f} dB", (w180, A180), xytext=(8, 6),
             textcoords="offset points", fontsize=8)
ax2.annotate(rf"$\omega_{{180}}$ = {w180:.3f} rad/s", (w180, -180), xytext=(8, 6),
             textcoords="offset points", fontsize=8)
spremi(fig, "z42_bode_G0")

(MAPA / "rezultati.txt").write_text("\n".join(ispis_redovi) + "\n", encoding="utf-8")
