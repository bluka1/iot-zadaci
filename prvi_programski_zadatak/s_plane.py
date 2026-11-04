from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal

SLIKE = Path(__file__).parent / "slike"
SLIKE.mkdir(exist_ok=True)

G1 = signal.TransferFunction([27], [1, 4, 36])
G2 = signal.TransferFunction([34, 68], np.polymul([1, 4], [1, 6, 34]))
G3 = signal.TransferFunction([1, 5], [1, 4, 3, 18])
G4 = signal.TransferFunction([36], np.polymul([1, 1], [1, 36]))

systems = {
    "G1": G1,
    "G2": G2,
    "G3": G3,
    "G4": G4,
}

colors = {"G1": "tab:blue", "G2": "tab:orange", "G3": "tab:red", "G4": "tab:green"}
fig, (ax_cijela, ax_blizu) = plt.subplots(1, 2, figsize=(10, 4.8),
                                          gridspec_kw={"width_ratios": [3, 2]})

for ax, granice in ((ax_cijela, (-40, 10)), (ax_blizu, (-6, 1.5))):
    ax.axvline(0, color="black", linewidth=1)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvspan(granice[0], 0, color="#e8f4e8", zorder=0)
    ax.axvspan(0, granice[1], color="#f8e8e8", zorder=0)
    for name, sys_ in systems.items():
        poles = np.roots(sys_.den)
        zeros = np.roots(sys_.num)
        ax.scatter(poles.real, poles.imag, marker="x", s=90, color=colors[name],
                   linewidths=2, label=f"{name} polovi")
        if zeros.size:
            ax.scatter(zeros.real, zeros.imag, marker="o", s=60, facecolors="none",
                       edgecolors=colors[name], linewidths=2, label=f"{name} nule")
    ax.set_xlim(*granice)
    ax.set_ylim(-7, 7)
    ax.set_xlabel(r"Re(s) = $\sigma$ [rad/s]")
    ax.grid(True, alpha=0.3)

ax_cijela.text(-20, 6.3, "lijeva poluravnina (stabilno)", ha="center", fontsize=9, color="#2a6a2a")
ax_cijela.text(5, 6.3, "desna", ha="center", fontsize=9, color="#8a2a2a")
ax_cijela.set_ylabel(r"Im(s) = $j\omega$ [rad/s]")
ax_cijela.set_title("cijeli raspon", fontsize=10)
ax_blizu.set_title("uvećano oko ishodišta", fontsize=10)
ax_cijela.legend(loc="lower left", fontsize=8)
fig.tight_layout()
fig.savefig(SLIKE / "s_plane.svg")
fig.savefig(SLIKE / "s_plane.png", dpi=150)
print("saved")
