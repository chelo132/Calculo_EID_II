# plots.py
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from amdahl import aceleracion, limite_teorico

class GraficoAvsFConBotones:
    def __init__(self, datos_fk):
        self.datos_fk = datos_fk
        self.mostrar_linea_A = True
        self.mostrar_linea_Amax = True

        self.root = tk.Tk()
        self.root.title("Gráfico A vs f")

        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        botones_frame = tk.Frame(self.root)
        botones_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.btn_linea_A = tk.Button(botones_frame, text="Mostrar/Ocultar A", command=self.toggle_linea_A)
        self.btn_linea_A.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_linea_Amax = tk.Button(botones_frame, text="Mostrar/Ocultar Aₘₐₓ", command=self.toggle_linea_Amax)
        self.btn_linea_Amax.pack(side=tk.LEFT, padx=5, pady=5)

        self.lineas_A = []
        self.lineas_Amax = []

        self.plot_inicial()
        self.root.mainloop()

    def plot_inicial(self):
        self.ax.clear()
        self.lineas_A.clear()
        self.lineas_Amax.clear()
        f_vals = np.linspace(0.01, 0.99, 200)

        for f, k in self.datos_fk:
            A_vals = [aceleracion(fx, k) for fx in f_vals]
            self.ax.plot(f_vals, A_vals, label=f"k={k}, f={f:.2f}")

            A_punto = aceleracion(f, k)
            A_max = limite_teorico(f)

            self.ax.plot(f, A_punto, "ro")
            self.ax.axvline(x=f, color="red", linestyle="--")

            l_a = self.ax.axhline(y=A_punto, color="#8B4513", linestyle="--", label=f"A = {A_punto:.4f}")
            l_amax = self.ax.axhline(y=A_max, color="#4169E1", linestyle="--", label=f"Aₘₐₓ = {A_max:.4f}")
            self.lineas_A.append(l_a)
            self.lineas_Amax.append(l_amax)

        self.ax.set_xlabel("Fracción mejorable (f)")
        self.ax.set_ylabel("Aceleración (A)")
        self.ax.set_title("A vs f")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def toggle_linea_A(self):
        self.mostrar_linea_A = not self.mostrar_linea_A
        for l in self.lineas_A:
            l.set_visible(self.mostrar_linea_A)
        self.canvas.draw()

    def toggle_linea_Amax(self):
        self.mostrar_linea_Amax = not self.mostrar_linea_Amax
        for l in self.lineas_Amax:
            l.set_visible(self.mostrar_linea_Amax)
        self.canvas.draw()


class GraficoAvsKConBotones:
    def __init__(self, datos_fk):
        self.datos_fk = datos_fk
        self.mostrar_linea_A = True
        self.mostrar_linea_Amax = True

        self.root = tk.Tk()
        self.root.title("Gráfico A vs k")

        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        botones_frame = tk.Frame(self.root)
        botones_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.btn_linea_A = tk.Button(botones_frame, text="Mostrar/Ocultar A", command=self.toggle_linea_A)
        self.btn_linea_A.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_linea_Amax = tk.Button(botones_frame, text="Mostrar/Ocultar Aₘₐₓ", command=self.toggle_linea_Amax)
        self.btn_linea_Amax.pack(side=tk.LEFT, padx=5, pady=5)

        self.lineas_A = []
        self.lineas_Amax = []

        self.plot_inicial()
        self.root.mainloop()

    def plot_inicial(self):
        self.ax.clear()
        self.lineas_A.clear()
        self.lineas_Amax.clear()
        k_vals = np.linspace(1, 20, 200)

        for f, k in self.datos_fk:
            A_vals = [aceleracion(f, kx) for kx in k_vals]
            self.ax.plot(k_vals, A_vals, label=f"f={f:.2f}, k={k}")

            A_punto = aceleracion(f, k)
            A_max = limite_teorico(f)

            self.ax.plot(k, A_punto, "ro")
            self.ax.axvline(x=k, color="red", linestyle="--")

            l_a = self.ax.axhline(y=A_punto, color="#8B4513", linestyle="--", label=f"A = {A_punto:.4f}")
            l_amax = self.ax.axhline(y=A_max, color="#4169E1", linestyle="--", label=f"Aₘₐₓ = {A_max:.4f}")
            self.lineas_A.append(l_a)
            self.lineas_Amax.append(l_amax)

        self.ax.set_xlabel("Factor de mejora (k)")
        self.ax.set_ylabel("Aceleración (A)")
        self.ax.set_title("A vs k")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def toggle_linea_A(self):
        self.mostrar_linea_A = not self.mostrar_linea_A
        for l in self.lineas_A:
            l.set_visible(self.mostrar_linea_A)
        self.canvas.draw()

    def toggle_linea_Amax(self):
        self.mostrar_linea_Amax = not self.mostrar_linea_Amax
        for l in self.lineas_Amax:
            l.set_visible(self.mostrar_linea_Amax)
        self.canvas.draw()


# Funciones accesibles desde gui.py
def plot_A_vs_f_con_botones(pares_fk):
    GraficoAvsFConBotones(pares_fk)

def plot_A_vs_k_con_botones(pares_fk):
    GraficoAvsKConBotones(pares_fk)
