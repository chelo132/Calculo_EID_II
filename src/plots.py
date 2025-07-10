import numpy as np
import matplotlib.pyplot as plt
from amdahl import aceleracion, limite_teorico

def plot_A_vs_f(k: float, f_min=0.01, f_max=0.99, num=100, punto_f=None):
    f_vals = np.linspace(f_min, f_max, num)
    A_vals = [aceleracion(f, k) for f in f_vals]
    plt.plot(f_vals, A_vals, label=f"k = {k}")

    if punto_f is not None:
        A_punto = aceleracion(punto_f, k)
        A_max = limite_teorico(punto_f)
        # Línea vertical roja punteada
        plt.axvline(x=punto_f, color="red", linestyle="--", label=f"f = {punto_f:.2f}")
        # Punto rojo
        plt.plot(punto_f, A_punto, "ro")
        # Línea horizontal café punteada
        plt.axhline(y=A_punto, color="#8B4513", linestyle="--", label=f"A = {A_punto:.4f}")
        # Línea horizontal azul punteada
        plt.axhline(y=A_max, color="#4169E1", linestyle="--", label=f"Aₘₐₓ = {A_max:.4f}")

    plt.xlabel("Fracción mejorable (f)")
    plt.ylabel("Aceleración (A)")
    plt.title("A vs f")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_A_vs_k(f: float, k_min=1, k_max=20, num=100, punto_k=None):
    k_vals = np.linspace(k_min, k_max, num)
    A_vals = [aceleracion(f, k) for k in k_vals]
    plt.plot(k_vals, A_vals, label=f"f = {f}")

    if punto_k is not None:
        A_punto = aceleracion(f, punto_k)
        A_max = limite_teorico(f)
        # Línea vertical roja punteada
        plt.axvline(x=punto_k, color="red", linestyle="--", label=f"k = {punto_k:.2f}")
        # Punto rojo
        plt.plot(punto_k, A_punto, "ro")
        # Línea horizontal café punteada
        plt.axhline(y=A_punto, color="#8B4513", linestyle="--", label=f"A = {A_punto:.4f}")
        # Línea horizontal azul punteada
        plt.axhline(y=A_max, color="#4169E1", linestyle="--", label=f"Aₘₐₓ = {A_max:.4f}")

    plt.xlabel("Factor de mejora (k)")
    plt.ylabel("Aceleración (A)")
    plt.title("A vs k")
    plt.grid(True)
    plt.legend()
    plt.show()
