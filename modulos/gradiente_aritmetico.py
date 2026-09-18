from utilidades.validaciones import (
    validar_monto,
    validar_gradiente,
    validar_tasa_anualidad,
    validar_periodos
)

def calcular_presente_gradiente(K, G, i, n):
    """
    Calcula el valor presente de un gradiente aritmético vencido.

    P = [(K + G/i)((1+i)^n - 1) - Gn] / [i(1+i)^n]
    """

    validar_monto(K)
    validar_gradiente(G)
    validar_tasa_anualidad(i)
    validar_periodos(n)

    P = ((K + G / i) * ((1 + i) ** n - 1) - G * n) / (i * (1 + i) ** n)

    return P

def calcular_pago_uniforme_gradiente(K, G, i, n):
    """
    Calcula el pago uniforme equivalente de un gradiente
    aritmético vencido.

    R = K + G[1/i - n/((1+i)^n - 1)]
    """

    validar_monto(K)
    validar_gradiente(G)
    validar_tasa_anualidad(i)
    validar_periodos(n)

    R = K + G * (1 / i - n / ((1 + i) ** n - 1))

    return R

def calcular_futuro_gradiente(K, G, i, n):
    """
    Calcula el valor futuro de un gradiente aritmético vencido.

    F = [(K + G/i)((1+i)^n - 1) - Gn] / i
    """

    validar_monto(K)
    validar_gradiente(G)
    validar_tasa_anualidad(i)
    validar_periodos(n)

    F = ((K + G / i) * ((1 + i) ** n - 1) - G * n) / i

    return F