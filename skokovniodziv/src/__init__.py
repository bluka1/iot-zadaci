from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

# Funkcija za prikaz skokovnog odziva
brojnik = [27]
nazivnik = [1, 4, 36]
prijenosna_funkcija = signal.TransferFunction(brojnik, nazivnik)

niz_vremena = np.linspace(0, 4, 4001)

t, y = signal.step(prijenosna_funkcija, T=niz_vremena)

max_y = max(y)
# max_y je 0.997 (default)
# nakon što se dodalo 4001 vremenskih točaka, max_y je 0.997

max_y_index = y.argmax()

max_y_t = t[max_y_index]
# max_y_t je 0.5656 (default)
# nakon što se dodalo 4001 vremenskih točaka, max_y_t je 0.555

plt.plot(t, y, label="Skokovni odziv")
plt.grid(True)
plt.xlabel("t [s]")
plt.ylabel("y(t)")
plt.title("Skokovni odziv sustava drugog reda - G(s) = 27 / ($s^2$ + 4s + 36)")

# Tp
plt.axvline(x=max_y_t, color="red", linestyle="--", label="Vrijeme prvog maksimuma Tp")

plt.plot(max_y_t, max_y, 'o', markersize=10, color="black", label="Maksimum odziva y(Tp)")

# y(∞)
y_inf = brojnik[-1] / nazivnik[-1] # dobiveno kad se s = 0 uvrsti u prijenosnu funkciju
plt.axhline(y=y_inf, color="green", linestyle="--", label="Vrijednost odziva u ustaljenom stanju y(∞)")

# Analitički izračun (usporedba s općim oblikom wn^2 / (s^2 + 2*zeta*wn*s + wn^2))
wn = np.sqrt(nazivnik[2]) # wn^2 = 36  ->  wn = 6
zeta = nazivnik[1] / (2 * wn) # 2*zeta*wn = 4  ->  zeta = 0.333
wd = wn * np.sqrt(1 - zeta**2) # frekvencija prigušenih oscilacija
Tp_izr = np.pi / wd # vrijeme prvog maksimuma
PO_izr = 100 * np.exp(-zeta * np.pi / np.sqrt(1 - zeta**2)) # postotak nadvišenja [%]
max_y_izr = y_inf * (1 + PO_izr / 100) # maksimum odziva

plt.legend()
plt.savefig("skokovniodziv.png")


def main() -> None:
    print("Funkcija za prikaz skokovnog odziva")
    print("--------------------------------")
    print("broj vremenskih točaka: ", len(t))
    print("raspon vremena između dvije susjedne vremenske točke: ", t[1] - t[0])
    print("maksimalna vrijednost y: ", max_y.round(3))
    print("vrijeme za maksimalnu vrijednost y: ", max_y_t.round(3))
    print("--------------------------------")
    print(f"{'veličina':<10}{'izračunato':>12}{'simulirano':>12}")
    print(f"{'Tp [s]':<10}{Tp_izr:>12.3f}{max_y_t:>12.3f}")
    print(f"{'y_max':<10}{max_y_izr:>12.3f}{max_y:>12.3f}")
    print(f"{'y(∞)':<10}{y_inf:>12.3f}{y[-1]:>12.3f}")
    plt.show()


if __name__ == "__main__":
    main()