from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

# funkcija za prikaz impulsnog odziva sustava trećeg reda
# G2(s) = K2 (s + z) / ((s + p) (s^2 + C1 s + C0))
K2 = 34
z = 2
p = 4
C1 = 6
C0 = 34

brojnik = np.polymul([K2], [1, z])  # 34 (s + 2)  ->  [34, 68]
nazivnik = np.polymul([1, p], [1, C1, C0])  # (s + 4)(s^2 + 6s + 34)  ->  [1, 10, 58, 136]
prijenosna_funkcija = signal.TransferFunction(brojnik, nazivnik)

# nule i polovi sustava (zadatak a)
nule = prijenosna_funkcija.zeros  # -2
polovi = prijenosna_funkcija.poles  # -4 i -3 ± j5

niz_vremena = np.linspace(0, 4, 4001)

t, y_imp = signal.impulse(prijenosna_funkcija, T=niz_vremena)
t, y_step = signal.step(prijenosna_funkcija, T=niz_vremena)

# Pomoćne veličine za kompleksni par: s^2 + 6s + 34 = (s + 3)^2 + 5^2
sigma = C1 / 2  # 3  (realni dio kompleksnih polova, s predznakom minus)
wd = np.sqrt(C0 - sigma**2)  # 5  (imaginarni dio kompleksnih polova)

# --- Analitički impulsni odziv (zadatak b) ---
# G2(s) = A/(s + 4) + (B s + C)/(s^2 + 6s + 34)
A = (K2 * (-p + z)) / ((-p) ** 2 + C1 * (-p) + C0)  # pokrivanje: s = -4
B = -A  # uz s^2: A + B = 0 (lijevo nema s^2)
C = (brojnik[-1] - A * C0) / p  # uz s^0: C0*A + p*C = brojnik[-1]
imp_cos = B
imp_sin = (C - sigma * B) / wd
y_imp_an = A * np.exp(-p * t) + np.exp(-sigma * t) * (imp_cos * np.cos(wd * t) + imp_sin * np.sin(wd * t))

# --- Analitički skokovni odziv (zadatak c) ---
# G2(s)/s = A0/s + As/(s + 4) + (Bs s + Cs)/(s^2 + 6s + 34)
A0 = brojnik[-1] / nazivnik[-1]  # pokrivanje: s = 0  ->  G2(0) = 68/136
As = (K2 * (-p + z)) / ((-p) * ((-p) ** 2 + C1 * (-p) + C0))  # pokrivanje: s = -4
Bs = -(A0 + As)  # uz s^3: A0 + As + Bs = 0
Cs = -(A0 * (p + C1) + As * C1 + Bs * p)  # uz s^2: A0*(p + C1) + As*C1 + Bs*p + Cs = 0
step_cos = Bs
step_sin = (Cs - sigma * Bs) / wd
y_step_an = A0 + As * np.exp(-p * t) + np.exp(-sigma * t) * (step_cos * np.cos(wd * t) + step_sin * np.sin(wd * t))

# --- Teoremi o početnoj i konačnoj vrijednosti (zadatak d) ---
# impulsni: y(0+) = lim s->inf s*G2(s) = 0  (red nazivnika veći od reda brojnika za 2)
# skokovni: y(0+) = lim s->inf G2(s) = 0,  y(inf) = lim s->0 G2(s) = G2(0)
y0_imp_teorem = 0.0
y0_step_teorem = 0.0
y_inf_step_teorem = brojnik[-1] / nazivnik[-1]  # 68/136 = 0.5

# --- Graf ---
plt.plot(t, y_imp, color="tab:blue", label="Impulsni odziv - signal.impulse")
plt.plot(t[::100], y_imp_an[::100], "o", markersize=4, color="tab:blue", mfc="white",
         label="Impulsni odziv - analitički")
plt.plot(t, y_step, color="tab:orange", label="Skokovni odziv - signal.step")
plt.plot(t[::100], y_step_an[::100], "s", markersize=4, color="tab:orange", mfc="white",
         label="Skokovni odziv - analitički")
plt.axhline(y=0, color="gray", linewidth=0.8)
plt.axhline(y=y_inf_step_teorem, color="green", linestyle="--",
            label=f"y_step(∞) = {y_inf_step_teorem:.3f}")

plt.grid(True)
plt.xlabel("t [s]")
plt.ylabel("y(t)")
plt.title("Odzivi sustava trećeg reda - G(s) = 34(s+2) / ((s+4)($s^2$ + 6s + 34))")
plt.legend()
plt.savefig("odzivi_zadatak2.png")


def main() -> None:
    print("2. zadatak - impulsni i skokovni odziv")
    print("--------------------------------")
    print("nule sustava:   ", np.round(nule, 3))
    print("polovi sustava: ", np.round(polovi, 3))
    print("--------------------------------")
    print("Analitički impulsni odziv:")
    print(f"  y(t) = {A:.3f} e^(-4t) + e^(-3t) ( {imp_cos:.3f} cos(5t) + {imp_sin:.3f} sin(5t) )")
    print("Analitički skokovni odziv:")
    print(f"  y(t) = {A0:.3f} + {As:.3f} e^(-4t) + e^(-3t) ( {step_cos:.3f} cos(5t) + {step_sin:.3f} sin(5t) )")
    print("--------------------------------")
    print(f"max |impulse - analitički| = {np.max(np.abs(y_imp - y_imp_an)):.2e}")
    print(f"max |step - analitički|    = {np.max(np.abs(y_step - y_step_an)):.2e}")
    print("--------------------------------")
    print(f"{'veličina':<14}{'teorem':>10}{'analitički':>12}{'simulirano':>12}")
    print(f"{'y_imp(0+)':<14}{y0_imp_teorem:>10.3f}{y_imp_an[0]:>12.3f}{y_imp[0]:>12.3f}")
    print(f"{'y_step(0+)':<14}{y0_step_teorem:>10.3f}{y_step_an[0]:>12.3f}{y_step[0]:>12.3f}")
    print(f"{'y_step(∞)':<14}{y_inf_step_teorem:>10.3f}{A0:>12.3f}{y_step[-1]:>12.3f}")
    plt.show()


if __name__ == "__main__":
    main()
