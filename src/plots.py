# plots.py
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
        plt.axvline(x=punto_f, color="red", linestyle="--", label=f"f = {punto_f:.2f}")
        plt.plot(punto_f, A_punto, "ro")
        plt.axhline(y=A_punto, color="#8B4513", linestyle="--", label=f"A = {A_punto:.4f}")
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
        plt.axvline(x=punto_k, color="red", linestyle="--", label=f"k = {punto_k:.2f}")
        plt.plot(punto_k, A_punto, "ro")
        plt.axhline(y=A_punto, color="#8B4513", linestyle="--", label=f"A = {A_punto:.4f}")
        plt.axhline(y=A_max, color="#4169E1", linestyle="--", label=f"Aₘₐₓ = {A_max:.4f}")

    plt.xlabel("Factor de mejora (k)")
    plt.ylabel("Aceleración (A)")
    plt.title("A vs k")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_multi_A_vs_f(pares_fk):
    f_vals = np.linspace(0.01, 0.99, 100)
    for f, k in pares_fk:
        A_vals = [aceleracion(f_, k) for f_ in f_vals]
        A = aceleracion(f, k)
        Amax = limite_teorico(f)

        plt.plot(f_vals, A_vals, label=f"k={k:.2f}, f={f:.2f}")
        plt.axvline(x=f, color="red", linestyle="--")
        plt.axhline(y=A, color="#8B4513", linestyle="--")
        plt.axhline(y=Amax, color="#4169E1", linestyle="--")
        plt.plot(f, A, "ro")

    plt.xlabel("Fracción mejorable (f)")
    plt.ylabel("Aceleración (A)")
    plt.title("A vs f (múltiples)")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_multi_A_vs_k(pares_fk):
    k_vals = np.linspace(1, 20, 100)
    for f, k in pares_fk:
        A_vals = [aceleracion(f, k_) for k_ in k_vals]
        A = aceleracion(f, k)
        Amax = limite_teorico(f)

        plt.plot(k_vals, A_vals, label=f"f={f:.2f}, k={k:.2f}")
        plt.axvline(x=k, color="red", linestyle="--")
        plt.axhline(y=A, color="#8B4513", linestyle="--")
        plt.axhline(y=Amax, color="#4169E1", linestyle="--")
        plt.plot(k, A, "ro")

    plt.xlabel("Factor de mejora (k)")
    plt.ylabel("Aceleración (A)")
    plt.title("A vs k (múltiples)")
    plt.grid(True)
    plt.legend()
    plt.show()
