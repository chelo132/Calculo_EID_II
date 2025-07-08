# Launcher de la app CustomTkinter

from amdahl import aceleracion, limite_teorico

datos = {
    "FPU": (0.25, 6),
    "Cache L1": (0.15, 4),
    "Branch Predictor": (0.10, 8),
    "Memoria principal": (0.50, 2),
}

for nombre, (f, k) in datos.items():
    A = aceleracion(f, k)
    A_max = limite_teorico(f)
    print(f"{nombre}: A = {A:.3f}, Aₘₐₓ = {A_max:.3f}")
