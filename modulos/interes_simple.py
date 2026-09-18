def calcular_interes_simple(capital, tasa, periodos):
    interes = capital * tasa * periodos
    valor_futuro = capital * (1 + tasa * periodos)

    return interes, valor_futuro