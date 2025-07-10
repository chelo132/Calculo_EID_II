import customtkinter as ctk
from amdahl import aceleracion, limite_teorico
from plots import plot_A_vs_f, plot_A_vs_k, parse_f_input

def create_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Ley de Amdahl - Cálculo dinámico")
    app.geometry("840x500")

    layout = ctk.CTkFrame(app)
    layout.pack(fill="both", expand=True, padx=20, pady=20)

    # ----- Sección izquierda (inputs y botones) -----
    left_frame = ctk.CTkFrame(layout)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    ctk.CTkLabel(left_frame, text="Fracción mejorable (f):").grid(row=0, column=0, sticky="w", padx=5)
    entry_f = ctk.CTkEntry(left_frame, width=100)
    entry_f.grid(row=0, column=1, padx=5)

    ctk.CTkLabel(left_frame, text="Factor de mejora (k):").grid(row=1, column=0, sticky="w", padx=5)
    entry_k = ctk.CTkEntry(left_frame, width=100)
    entry_k.grid(row=1, column=1, padx=5)

    result = ctk.CTkLabel(left_frame, text="A: --    Aₘₐₓ: --", font=ctk.CTkFont(size=14, weight="bold"))
    result.grid(row=2, column=0, columnspan=2, pady=10)

    btn_frame = ctk.CTkFrame(left_frame)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
    ctk.CTkButton(btn_frame, text="Calcular", command=lambda: calcular()).grid(row=0, column=0, padx=5)
    ctk.CTkButton(btn_frame, text="Graf. A vs f", command=lambda: graficar_f()).grid(row=0, column=1, padx=5)
    ctk.CTkButton(btn_frame, text="Graf. A vs k", command=lambda: graficar_k()).grid(row=0, column=2, padx=5)

    # ----- Sección derecha (Historial con selección) -----
    right_frame = ctk.CTkFrame(layout)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    ctk.CTkLabel(right_frame, text="Historial de cálculos", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=5)

    scroll_hist = ctk.CTkScrollableFrame(right_frame, width=340, height=300)
    scroll_hist.pack(pady=5)
    checkboxes = []

    def calcular():
        try:
            f_input = entry_f.get()
            f = parse_f_input(f_input)
            k = float(entry_k.get())

            A = aceleracion(f, k)
            Amax = limite_teorico(f)
            result.configure(text=f"A = {A:.4f}    Aₘₐₓ = {Amax:.4f}")

            resumen = f"f={f:.2f}, k={k:.2f} → A={A:.4f}, Aₘₐₓ={Amax:.4f}"
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(scroll_hist, text=resumen, variable=var)
            checkbox.pack(anchor="w", pady=2)
            checkboxes.append((checkbox, var))
        except Exception as e:
            result.configure(text=f"Error: {e}")

    def graficar_f():
        try:
            k = float(entry_k.get())
            f_raw = entry_f.get()
            plot_A_vs_f(k, punto_f=f_raw)
        except Exception as e:
            result.configure(text=f"Error: k inválido ({e})")

    def graficar_k():
        try:
            f_input = entry_f.get()
            f = parse_f_input(f_input)
            k_raw = entry_k.get()
            plot_A_vs_k(f, punto_k=float(k_raw))
        except Exception as e:
            result.configure(text=f"Error: f inválido ({e})")

    def eliminar_seleccionados():
        for cb, var in checkboxes[:]:
            if var.get():
                cb.destroy()
                checkboxes.remove((cb, var))

    ctk.CTkButton(right_frame, text="Eliminar seleccionados", fg_color="red",
                  command=eliminar_seleccionados).pack(pady=5)

    return app
