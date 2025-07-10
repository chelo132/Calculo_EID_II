def aceleracion(f: float, k: float) -> float:
    """Ley de Amdahl: A = 1 / ((1 - f) + f / k)."""
    return 1.0 / ((1 - f) + f / k)

def limite_teorico(f: float) -> float:
    """Aₘₐₓ cuando k→∞: Aₘₐₓ = 1 / (1 - f)."""
    return 1.0 / (1 - f)
