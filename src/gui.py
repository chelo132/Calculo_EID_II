# Definición de la interfaz con 
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from amdahl import aceleracion, limite_teorico
from plots import plot_A_vs_f, plot_A_vs_k

# Datos de entrada para Grupo 5 (CPU)
datos = {
    "Unidad de punto flotante (FPU)": (0.25, 6),
    "Caché L1": (0.15, 4),
    "Predictor de saltos": (0.10, 8),
    "Memoria principal": (0.50, 2),
}

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def create_app():
    app = ctk.CTk()
    app.title("Aceleración CPU - Ley de Amdahl")
    app.geometry("520x480")

    # Dropdown
    sel = ctk.StringVar(value=list(datos.keys())[0])
    menu = ctk.CTkOptionMenu(app, values=list(datos.keys()), variable=sel,
                             command=lambda _: update_entries())
    menu.pack(pady=10)

    # Frame de entradas
    frame = ctk.CTkFrame(app)
    frame.pack(padx=20, pady=10, fill="x")
    ctk.CTkLabel(frame, text="Fracción mejorable (f):").grid(row=0, column=0, sticky="w", padx=5)
    entry_f = ctk.CTkEntry(frame); entry_f.grid(row=0, column=1, padx=5)
    ctk.CTkLabel(frame, text="Factor de mejora (k):").grid(row=1, column=0, sticky="w", padx=5)
    entry_k = ctk.CTkEntry(frame); entry_k.grid(row=1, column=1, padx=5)

    # Resultado
    result = ctk.CTkLabel(app, text="A: --    Aₘₐₓ: --",
                         font=ctk.CTkFont(size=16, weight="bold"))
    result.pack(pady=10)

    # Funciones internas
    def update_entries():
        f0, k0 = datos[sel.get()]
        entry_f.delete(0, ctk.END); entry_f.insert(0, str(f0))
        entry_k.delete(0, ctk.END); entry_k.insert(0, str(k0))
        result.configure(text="A: --    Aₘₐₓ: --")

    def calcular():
        try:
            f_val, k_val = float(entry_f.get()), float(entry_k.get())
            A = aceleracion(f_val, k_val)
            A_max = limite_teorico(f_val)
            result.configure(text=f"A = {A:.3f}    Aₘₐₓ = {A_max:.3f}")
        except:
            result.configure(text="Entrada inválida. Usa números.")

    def graficar_f():
        try:
            plot_A_vs_f(float(entry_k.get()))
        except:
            result.configure(text="Invalid k")

    def graficar_k():
        try:
            plot_A_vs_k(float(entry_f.get()))
        except:
            result.configure(text="Invalid f")

    # Botonera
    btns = ctk.CTkFrame(app); btns.pack(pady=10)
    ctk.CTkButton(btns, text="Calcular", command=calcular).grid(row=0, column=0, padx=5)
    ctk.CTkButton(btns, text="Graf. A vs f", command=graficar_f).grid(row=0, column=1, padx=5)
    ctk.CTkButton(btns, text="Graf. A vs k", command=graficar_k).grid(row=0, column=2, padx=5)

    update_entries()
    return app
