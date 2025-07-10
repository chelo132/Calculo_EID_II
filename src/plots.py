import numpy as np
import matplotlib.pyplot as plt
from amdahl import aceleracion, limite_teorico

def parse_f_input(f_raw):
    """
    Convierte entrada de fracción mejorable (f) a decimal entre 0 y 1.
    - Soporta entradas como "50%", "50", "0.5"
    - También reemplaza comas decimales por puntos (ej: "50,5%")
    """
    if isinstance(f_raw, str):
        f_raw = f_raw.strip().replace(",", ".")
        if "%" in f_raw:
            return float(f_raw.replace("%", "")) / 100
        else:
            f_val = float(f_raw)
            return f_val / 100 if f_val > 1 else f_val
    return float(f_raw)

def plot_A_vs_f(k: float, f_min=0.01, f_max=0.99, num=100, punto_f=None):
    f_vals = np.linspace(f_min, f_max, num)
    A_vals = [aceleracion(f, k) for f in f_vals]
    plt.plot(f_vals, A_vals, label=f"k = {k}")

    if punto_f is not None:
        f = parse_f_input(punto_f)
        A_punto = aceleracion(f, k)
        A_max = limite_teorico(f)

        plt.axvline(x=f, color="red", linestyle="--", linewidth=1.5, label=f"f = {f:.2f}", zorder=1)
        plt.plot(f, A_punto, "ro", markersize=8, zorder=3)

        plt.axhline(y=A_punto, color="#8B4513", linestyle="--", linewidth=1.8,
                    label=f"A = {A_punto:.4f}", zorder=2)

        # A_max en gris
        plt.axhline(y=A_max, color="#555555", linestyle="--", linewidth=1.8,
                    label=f"Aₘₐₓ = {A_max:.4f}", zorder=2)

    plt.xlabel("Fracción mejorable (f)")
    plt.ylabel("Aceleración (A)")
    plt.title("A vs f")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_A_vs_k(f: float, k_min=1, k_max=20, num=100, punto_k=None):
    f = parse_f_input(f)
    k_vals = np.linspace(k_min, k_max, num)
    A_vals = [aceleracion(f, k) for k in k_vals]
    plt.plot(k_vals, A_vals, label=f"f = {f:.2f}")

    if punto_k is not None:
        A_punto = aceleracion(f, punto_k)
        A_max = limite_teorico(f)

        plt.axvline(x=punto_k, color="red", linestyle="--", linewidth=1.5,
                    label=f"k = {punto_k:.2f}", zorder=1)
        plt.plot(punto_k, A_punto, "ro", markersize=8, zorder=3)

        plt.axhline(y=A_punto, color="#8B4513", linestyle="--", linewidth=1.8,
                    label=f"A = {A_punto:.4f}", zorder=2)

        # A_max en gris
        plt.axhline(y=A_max, color="#555555", linestyle="--", linewidth=1.8,
                    label=f"Aₘₐₓ = {A_max:.4f}", zorder=2)

    plt.xlabel("Factor de mejora (k)")
    plt.ylabel("Aceleración (A)")
    plt.title("A vs k")
    plt.grid(True)
    plt.legend()
    plt.show()
