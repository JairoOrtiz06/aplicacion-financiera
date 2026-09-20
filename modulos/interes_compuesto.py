from utilidades.validaciones import (
    validar_monto,
    validar_tasa,
    validar_tasa_anualidad,
    validar_periodos
)


def calcular_futuro(P, r, n):
    """
    Calcula el valor futuro mediante interés compuesto.

    F = P(1 + r)^n
    """

    validar_monto(P)
    validar_tasa(r)
    validar_periodos(n)

    F = P * (1 + r) ** n

    return F

def calcular_presente(F, r, n):
    """
    Calcula el valor presente mediante interés compuesto.

    P = F / (1 + r)^n
    """

    validar_monto(F)
    validar_tasa(r)
    validar_periodos(n)

    P = F / (1 + r) ** n

    return P

def calcular_presente_anualidad(A, r, n):
    """
    Calcula el valor presente de una serie uniforme.

    P = A[((1 + r)^n - 1) / (r(1 + r)^n)]
    """

    validar_monto(A)
    validar_tasa_anualidad(r)
    validar_periodos(n)

    P = A * (((1 + r) ** n - 1) / (r * (1 + r) ** n))

    return P

def calcular_futuro_anualidad(A, r, n):
    """
    Calcula el valor futuro de una serie uniforme.

    F = A[((1 + r)^n - 1) / r]
    """

    validar_monto(A)
    validar_tasa_anualidad(r)
    validar_periodos(n)

    F = A * (((1 + r) ** n - 1) / r)

    return F


def calcular_pago_desde_futuro(F, r, n):
    """
    Calcula el pago periódico A a partir del valor futuro F.

    A = F[r / ((1 + r)^n - 1)]
    """

    validar_monto(F)
    validar_tasa_anualidad(r)
    validar_periodos(n)

    A = F * (r / ((1 + r) ** n - 1))

    return A


def calcular_pago_desde_presente(P, r, n):
    """
    Calcula el pago periódico A a partir del valor presente P.

    A = P[r(1 + r)^n / ((1 + r)^n - 1)]
    """

    validar_monto(P)
    validar_tasa_anualidad(r)
    validar_periodos(n)

    A = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    return A