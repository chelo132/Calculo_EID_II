# gui.py (interfaz principal)
import customtkinter as ctk
from amdahl import aceleracion, limite_teorico
from plots import plot_A_vs_f, plot_A_vs_k

def create_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Ley de Amdahl - Cálculo dinámico")
    app.geometry("720x460")

    # Layout principal (izquierda = input, derecha = historial)
    layout = ctk.CTkFrame(app)
    layout.pack(fill="both", expand=True, padx=20, pady=20)

    # ----- Sección izquierda -----
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

    # Botones
    btn_frame = ctk.CTkFrame(left_frame)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
    ctk.CTkButton(btn_frame, text="Calcular", command=lambda: calcular()).grid(row=0, column=0, padx=5)
    ctk.CTkButton(btn_frame, text="Graf. A vs f", command=lambda: graficar_f()).grid(row=0, column=1, padx=5)
    ctk.CTkButton(btn_frame, text="Graf. A vs k", command=lambda: graficar_k()).grid(row=0, column=2, padx=5)

    # ----- Sección derecha (Historial) -----
    right_frame = ctk.CTkFrame(layout)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    ctk.CTkLabel(right_frame, text="Historial de cálculos", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=5)

    listbox = ctk.CTkTextbox(right_frame, height=250, width=300)
    listbox.pack(pady=5)
    listbox.configure(state="disabled")  # Modo solo lectura

    selected_index = [None]  # Usamos lista mutable para acceder dentro de funciones anidadas
    history_items = []       # Guardamos texto para editar y eliminar

    def calcular():
        try:
            f = float(entry_f.get())
            k = float(entry_k.get())
            A = aceleracion(f, k)
            Amax = limite_teorico(f)
            result.configure(text=f"A = {A:.4f}    Aₘₐₓ = {Amax:.4f}")

            # Guardar en historial
            resumen = f"f={f:.2f}, k={k:.2f} → A={A:.4f}, Aₘₐₓ={Amax:.4f}\n"
            history_items.append(resumen)

            listbox.configure(state="normal")
            listbox.insert("end", resumen)
            listbox.configure(state="disabled")
        except Exception as e:
            result.configure(text=f"Error: {e}")

    def graficar_f():
        try:
            k = float(entry_k.get())
            plot_A_vs_f(k)
        except:
            result.configure(text="Error: k inválido")

    def graficar_k():
        try:
            f = float(entry_f.get())
            plot_A_vs_k(f)
        except:
            result.configure(text="Error: f inválido")

    def eliminar_seleccion():
        # Obtener línea seleccionada por índice
        try:
            idx = listbox.index("insert").split(".")[0]
            idx = int(idx)
            if idx <= len(history_items):
                # Eliminar del historial
                del history_items[idx - 1]
                # Actualizar visual
                listbox.configure(state="normal")
                listbox.delete("1.0", "end")
                for linea in history_items:
                    listbox.insert("end", linea)
                listbox.configure(state="disabled")
        except:
            result.configure(text="Selecciona una línea para eliminar")

    # Botón eliminar
    ctk.CTkButton(right_frame, text="Eliminar seleccionado", fg_color="red",
                  command=eliminar_seleccion).pack(pady=5)

    return app
