def calcular_gradiente_geometrico(pago, tasa, crecimiento, periodos):
    if tasa == crecimiento:
        valor_presente = (pago * periodos) / (1 + tasa)
    else:
        valor_presente = pago * (
            1 - ((1 + crecimiento) / (1 + tasa)) ** periodos
        ) / (tasa - crecimiento)

    flujos = []

    for periodo in range(1, periodos + 1):
        flujo = pago * (1 + crecimiento) ** (periodo - 1)
        flujos.append(flujo)

    return valor_presente, flujos