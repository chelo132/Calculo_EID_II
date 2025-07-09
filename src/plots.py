 # Funciones para generar gráficos con matplotlib
import numpy as np
import matplotlib.pyplot as plt
from amdahl import aceleracion


def plot_A_vs_f(k: float, f_min=0.01, f_max=0.99, num=99):
    """
    Grafica A vs f usando un único valor de k.
    :param k: factor de mejora actual
    :param f_min: valor mínimo de f
    :param f_max: valor máximo de f
    :param num: número de puntos
    """
    f_vals = np.linspace(f_min, f_max, num)
    A_vals = [aceleracion(f, k) for f in f_vals]
    plt.figure()
    plt.plot(f_vals, A_vals, label=f'k = {k:.2f}')
    plt.xlabel('Fracción mejorable (f)')
    plt.ylabel('Aceleración (A)')
    plt.title(f'Ley de Amdahl: A vs f (k={k:.2f})')
    plt.legend()
    plt.show()


def plot_A_vs_k(f: float, k_min=1, k_max=20, num=100):
    """
    Grafica A vs k usando un único valor de f.
    :param f: fracción mejorable actual
    :param k_min: factor mínimo
    :param k_max: factor máximo
    :param num: número de puntos
    """
    k_vals = np.linspace(k_min, k_max, num)
    A_vals = [aceleracion(f, k) for k in k_vals]
    plt.figure()
    plt.plot(k_vals, A_vals, label=f'f = {f:.2f}')
    plt.xlabel('Factor de mejora (k)')
    plt.ylabel('Aceleración (A)')
    plt.title(f'Ley de Amdahl: A vs k (f={f:.2f})')
    plt.legend()
    plt.show()