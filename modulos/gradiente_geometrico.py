def _validar(pago, tasa, crecimiento, periodos):
    if pago <= 0:
        raise ValueError("El pago inicial debe ser mayor que cero.")
    if tasa < 0 or crecimiento < 0:
        raise ValueError("Las tasas no pueden ser negativas.")
    if periodos <= 0:
        raise ValueError("El número de períodos debe ser mayor que cero.")


def calcular_presente_gradiente_geometrico(pago, tasa, crecimiento, periodos):
    """Valor presente de un gradiente geométrico vencido."""
    _validar(pago, tasa, crecimiento, periodos)
    if tasa == crecimiento:
        return calcular_presente_gradiente_geometrico_igual(pago, tasa, periodos)

    return pago * (
        ((1 + crecimiento) ** periodos - (1 + tasa) ** periodos)
        / ((crecimiento - tasa) * (1 + tasa) ** periodos)
    )


def calcular_presente_gradiente_geometrico_igual(pago, tasa, periodos):
    """Valor presente cuando el crecimiento es igual a la tasa."""
    if pago <= 0 or tasa < 0 or periodos <= 0:
        raise ValueError("Los datos deben ser válidos y positivos.")
    return pago * periodos / (1 + tasa)


def calcular_futuro_gradiente_geometrico(pago, tasa, crecimiento, periodos):
    """Valor futuro de un gradiente geométrico vencido."""
    _validar(pago, tasa, crecimiento, periodos)
    if tasa == crecimiento:
        return calcular_futuro_gradiente_geometrico_igual(pago, tasa, periodos)

    return pago * (
        ((1 + crecimiento) ** periodos - (1 + tasa) ** periodos)
        / (crecimiento - tasa)
    )


def calcular_futuro_gradiente_geometrico_igual(pago, tasa, periodos):
    """Valor futuro cuando el crecimiento es igual a la tasa."""
    if pago <= 0 or tasa < 0 or periodos <= 0:
        raise ValueError("Los datos deben ser válidos y positivos.")
    return pago * periodos * (1 + tasa) ** (periodos - 1)


def calcular_gradiente_geometrico(pago, tasa, crecimiento, periodos):
    """Devuelve el valor presente y los flujos de la serie."""
    valor_presente = calcular_presente_gradiente_geometrico(pago, tasa, crecimiento, periodos)
    flujos = [
        pago * (1 + crecimiento) ** (periodo - 1)
        for periodo in range(1, periodos + 1)
    ]
    return valor_presente, flujos
