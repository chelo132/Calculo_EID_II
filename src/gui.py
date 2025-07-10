# gui.py (interfaz principal)
import customtkinter as ctk
from amdahl import aceleracion, limite_teorico
from plots import plot_A_vs_f, plot_A_vs_k
from pathlib import Path
import os

def create_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Ley de Amdahl - Cálculo dinámico")
    app.geometry("900x500")

    layout = ctk.CTkFrame(app)
    layout.pack(fill="both", expand=True, padx=20, pady=20)

    left_frame = ctk.CTkFrame(layout, corner_radius=12)
    left_frame.grid(row=0, column=0, padx=20, pady=(60, 20), sticky="n")

    ctk.CTkLabel(left_frame, text="", height=10).grid(row=0, column=0, columnspan=2, pady=(20, 0))

    ctk.CTkLabel(left_frame, text="Fracción mejorable (f):", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", padx=5, pady=(0, 5))
    entry_f = ctk.CTkEntry(left_frame, width=120, font=ctk.CTkFont(size=13))
    entry_f.grid(row=1, column=1, padx=5, pady=(0, 5))

    ctk.CTkLabel(left_frame, text="Factor de mejora (k):", font=ctk.CTkFont(size=14)).grid(row=2, column=0, sticky="w", padx=5, pady=(20, 5))
    entry_k = ctk.CTkEntry(left_frame, width=120, font=ctk.CTkFont(size=13))
    entry_k.grid(row=2, column=1, padx=5, pady=(20, 5))

    result = ctk.CTkLabel(left_frame, text="A: --    Aₕₐₓ: --", font=ctk.CTkFont(size=15, weight="bold"))
    result.grid(row=3, column=0, columnspan=2, pady=15)

    btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
    ctk.CTkButton(btn_frame, text="🧾 Calcular", width=110, command=lambda: calcular()).grid(row=0, column=0, padx=7)
    ctk.CTkButton(btn_frame, text="📊 A vs f", width=110, command=lambda: graficar_f()).grid(row=0, column=1, padx=7)
    ctk.CTkButton(btn_frame, text="📊 A vs k", width=110, command=lambda: graficar_k()).grid(row=0, column=2, padx=7)
    ctk.CTkButton(btn_frame, text="🪜 Limpiar", width=110, command=lambda: limpiar_historial()).grid(row=1, column=0, pady=10)
    ctk.CTkButton(btn_frame, text="📀 Exportar", width=110, command=lambda: exportar_historial()).grid(row=1, column=2, pady=10)

    ctk.CTkLabel(left_frame, text="").grid(row=5, column=0, columnspan=2, pady=(0, 15))

    right_frame = ctk.CTkFrame(layout)
    right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    ctk.CTkLabel(right_frame, text="Historial de cálculos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(5, 10))

    listbox = ctk.CTkTextbox(right_frame, height=280, width=350, font=ctk.CTkFont(size=13))
    listbox.pack(pady=5)
    listbox.configure(state="disabled")

    ctk.CTkButton(
        right_frame, text="Eliminar seleccionado",
        fg_color="#E53935", hover_color="#B71C1C", text_color="white",
        font=ctk.CTkFont(size=13, weight="bold"),
        command=lambda: eliminar_seleccion()
    ).pack(pady=12)

    selected_index = [None]
    history_items = []

    def calcular():
        try:
            f = float(entry_f.get())
            k = float(entry_k.get())
            if not (0 < f < 1):
                result.configure(text="⚠️ f debe estar entre 0 y 1 (ej: 0.90)")
                return
            if k <= 0:
                result.configure(text="⚠️ k debe ser un número positivo (ej: 3, 10...)")
                return
            A = aceleracion(f, k)
            Amax = limite_teorico(f)
            result.configure(text=f"A = {A:.4f}    Aₕₐₓ = {Amax:.4f}")
            resumen = f"f={f:.2f}, k={k:.2f} → A={A:.4f}, Aₕₐₓ={Amax:.4f}"
            history_items.append(resumen)
            selected_index[0] = None
            listbox.configure(state="normal")
            listbox.delete("1.0", "end")
            for i, linea in enumerate(history_items):
                listbox.insert("end", f"  {linea}\n")
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
        try:
            idx = selected_index[0]
            if idx is not None and 0 <= idx < len(history_items):
                del history_items[idx]
                selected_index[0] = None
                listbox.configure(state="normal")
                listbox.delete("1.0", "end")
                for linea in history_items:
                    listbox.insert("end", f"  {linea}\n")
                listbox.configure(state="disabled")
        except:
            result.configure(text="Selecciona una línea para eliminar")

    def limpiar_historial():
        history_items.clear()
        listbox.configure(state="normal")
        listbox.delete("1.0", "end")
        listbox.configure(state="disabled")
        result.configure(text="A: --    Aₕₐₓ: --")

    def exportar_historial():
        try:
            ruta = Path("historial_amdahl.txt")  

            with open(ruta, "w", encoding="utf-8") as f:
                f.write("\n".join(history_items))
            result.configure(text="✅ Historial exportado en el escritorio")
        except Exception as e:
            result.configure(text=f"Error al exportar: {e}")

    def resaltar_seleccion(event=None):
        try:
            idx = int(listbox.index("insert").split(".")[0])
            if 0 < idx <= len(history_items):
                selected_index[0] = idx - 1
                seleccionada = history_items[selected_index[0]]
                listbox.configure(state="normal")
                listbox.delete("1.0", "end")
                for i, linea in enumerate(history_items):
                    prefix = "> " if i == selected_index[0] else "  "
                    listbox.insert("end", f"{prefix}{linea}\n")
                parts = seleccionada.split(",")
                entry_f.delete(0, "end")
                entry_k.delete(0, "end")
                entry_f.insert(0, parts[0].split("=")[1].strip())
                entry_k.insert(0, parts[1].split("=")[1].split("\u2192")[0].strip())
                listbox.configure(state="disabled")
        except:
            result.configure(text="⚠️ No se pudo seleccionar")

    listbox.bind("<ButtonRelease-1>", resaltar_seleccion)

    return app