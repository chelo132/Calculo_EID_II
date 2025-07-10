# gui.py
import customtkinter as ctk
from amdahl import aceleracion, limite_teorico
from plots import plot_A_vs_f, plot_A_vs_k
from pathlib import Path

def create_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Ley de Amdahl - Cálculo dinámico")
    app.geometry("900x550")

    layout = ctk.CTkFrame(app)
    layout.pack(fill="both", expand=True, padx=20, pady=20)

    # ---------- IZQUIERDA ----------
    left_frame = ctk.CTkFrame(layout, corner_radius=12)
    left_frame.grid(row=0, column=0, padx=20, pady=(40, 20), sticky="n")

    ctk.CTkLabel(left_frame, text="Fracción mejorable (f):", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", padx=5, pady=(0, 5))
    entry_f = ctk.CTkEntry(left_frame, width=120, font=ctk.CTkFont(size=13))
    entry_f.grid(row=0, column=1, padx=5, pady=(0, 5))

    ctk.CTkLabel(left_frame, text="Factor de mejora (k):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", padx=5, pady=(20, 5))
    entry_k = ctk.CTkEntry(left_frame, width=120, font=ctk.CTkFont(size=13))
    entry_k.grid(row=1, column=1, padx=5, pady=(20, 5))

    result = ctk.CTkLabel(left_frame, text="A: --    Aₘₐₓ: --", font=ctk.CTkFont(size=15, weight="bold"))
    result.grid(row=2, column=0, columnspan=2, pady=15)

    btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
    ctk.CTkButton(btn_frame, text="🧾 Calcular", width=110, command=lambda: calcular()).grid(row=0, column=0, padx=7)
    ctk.CTkButton(btn_frame, text="📊 A vs f", width=110, command=lambda: graficar_f(True)).grid(row=0, column=1, padx=7)
    ctk.CTkButton(btn_frame, text="📊 A vs k", width=110, command=lambda: graficar_k(True)).grid(row=0, column=2, padx=7)
    ctk.CTkButton(btn_frame, text="🪜 Limpiar", width=110, command=lambda: limpiar_historial()).grid(row=1, column=0, pady=10)
    ctk.CTkButton(btn_frame, text="📀 Exportar", width=110, command=lambda: exportar_historial()).grid(row=1, column=2, pady=10)

    # ---------- DERECHA ----------
    right_frame = ctk.CTkFrame(layout)
    right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    ctk.CTkLabel(right_frame, text="Historial de cálculos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(5, 10))

    scroll_hist = ctk.CTkScrollableFrame(right_frame, width=360, height=320)
    scroll_hist.pack(pady=(0, 10))
    checkboxes = []

    def calcular():
        try:
            raw_f = entry_f.get().strip()
            if raw_f.endswith("%"):
                f = float(raw_f.strip("%")) / 100
            else:
                f = float(raw_f)

            k = float(entry_k.get())

            if not (0 < f < 1):
                result.configure(text="⚠️ f debe estar entre 0 y 1 (ej: 0.90 o 90%)")
                return
            if k <= 0:
                result.configure(text="⚠️ k debe ser un número positivo")
                return

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

    def graficar_f(con_punto=False):
        try:
            raw_f = entry_f.get().strip()
            if raw_f.endswith("%"):
                f = float(raw_f.strip("%")) / 100
            else:
                f = float(raw_f)
            k = float(entry_k.get())
            if con_punto:
                plot_A_vs_f(k, punto_f=f)
            else:
                plot_A_vs_f(k)
        except:
            result.configure(text="Error en valores para graficar")

    def graficar_k(con_punto=False):
        try:
            raw_f = entry_f.get().strip()
            if raw_f.endswith("%"):
                f = float(raw_f.strip("%")) / 100
            else:
                f = float(raw_f)
            k = float(entry_k.get())
            if con_punto:
                plot_A_vs_k(f, punto_k=k)
            else:
                plot_A_vs_k(f)
        except:
            result.configure(text="Error en valores para graficar")

    def eliminar_seleccionados():
        for cb, var in checkboxes[:]:
            if var.get():
                cb.destroy()
                checkboxes.remove((cb, var))
        result.configure(text="🗑️ Eliminados seleccionados")

    def limpiar_historial():
        for cb, _ in checkboxes:
            cb.destroy()
        checkboxes.clear()
        result.configure(text="🧼 Historial limpio")

    def exportar_historial():
        try:
            ruta = Path("historial_amdahl.txt")
            with open(ruta, "w", encoding="utf-8") as f:
                for cb, _ in checkboxes:
                    f.write(cb.cget("text") + "\n")
            result.configure(text="✅ Exportado como historial_amdahl.txt")
        except Exception as e:
            result.configure(text=f"Error al exportar: {e}")

    ctk.CTkButton(
        right_frame, text="Eliminar seleccionados",
        fg_color="#E53935", hover_color="#B71C1C", text_color="white",
        font=ctk.CTkFont(size=13, weight="bold"),
        command=eliminar_seleccionados
    ).pack(pady=10)

    return app
