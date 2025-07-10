import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from amdahl import aceleracion, limite_teorico

class GraficoAvsFConBotones:
    def __init__(self, datos_fk, mostrar_linea_A=True, mostrar_linea_Amax=True):
        """
        datos_fk: lista de tuplas [(f1,k1), (f2,k2), ...]
        """
        self.datos_fk = datos_fk
        self.mostrar_linea_A = mostrar_linea_A
        self.mostrar_linea_Amax = mostrar_linea_Amax

        self.root = tk.Tk()
        self.root.title("Gráfico A vs f")

        self.fig, self.ax = plt.subplots(figsize=(8,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Botones para mostrar/ocultar líneas
        botones_frame = tk.Frame(self.root)
        botones_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.btn_linea_A = tk.Button(botones_frame, text="Mostrar línea A", command=self.toggle_linea_A)
        self.btn_linea_A.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_linea_Amax = tk.Button(botones_frame, text="Mostrar línea Amax", command=self.toggle_linea_Amax)
        self.btn_linea_Amax.pack(side=tk.LEFT, padx=5, pady=5)

        self.lineas_A = []
        self.lineas_Amax = []
        self.puntos_rojos = []

        self.plot_inicial()
        self.root.mainloop()

    def plot_inicial(self):
        self.ax.clear()
        f_vals = np.linspace(0.01, 0.99, 200)

        for f, k in self.datos_fk:
            A_vals = [aceleracion(fx, k) for fx in f_vals]
            self.ax.plot(f_vals, A_vals, label=f"k={k}, f={f:.2f}")

            A_punto = aceleracion(f, k)
            A_max = limite_teorico(f)

            p, = self.ax.plot(f, A_punto, "ro")
            self.puntos_rojos.append(p)

            if self.mostrar_linea_A:
                linea_A, = self.ax.plot([0, 1], [A_punto, A_punto], linestyle="--", color="#8B4513", label=f"A para f={f:.2f}")
            else:
                linea_A, = self.ax.plot([], [], linestyle="--", color="#8B4513")
            self.lineas_A.append(linea_A)

            if self.mostrar_linea_Amax:
                linea_Amax, = self.ax.plot([0, 1], [A_max, A_max], linestyle="--", color="#4169E1", label=f"Amax para f={f:.2f}")
            else:
                linea_Amax, = self.ax.plot([], [], linestyle="--", color="#4169E1")
            self.lineas_Amax.append(linea_Amax)

            self.ax.axvline(x=f, color="red", linestyle="--")

        self.ax.set_xlabel("Fracción mejorable (f)")
        self.ax.set_ylabel("Aceleración (A)")
        self.ax.set_title("A vs f")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def toggle_linea_A(self):
        self.mostrar_linea_A = not self.mostrar_linea_A
        for linea, (f, k) in zip(self.lineas_A, self.datos_fk):
            if self.mostrar_linea_A:
                A_punto = aceleracion(f, k)
                linea.set_data([0, 1], [A_punto, A_punto])
            else:
                linea.set_data([], [])
        self.canvas.draw()

    def toggle_linea_Amax(self):
        self.mostrar_linea_Amax = not self.mostrar_linea_Amax
        for linea, (f, _) in zip(self.lineas_Amax, self.datos_fk):
            if self.mostrar_linea_Amax:
                A_max = limite_teorico(f)
                linea.set_data([0, 1], [A_max, A_max])
            else:
                linea.set_data([], [])
        self.canvas.draw()

def plot_A_vs_f_con_botones(datos_fk):
    GraficoAvsFConBotones(datos_fk)
