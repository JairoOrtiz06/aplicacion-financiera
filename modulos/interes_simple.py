def calcular_interes_simple(capital, tasa, periodos):
    validar_monto(capital)
    validar_tasa(tasa)
    validar_periodos(periodos)

    interes = capital * tasa * periodos
    valor_futuro = capital * (1 + tasa * periodos)

    return interes, valor_futuro


def validar_monto(valor):
    if valor <= 0:
        raise ValueError("El monto debe ser mayor que cero.")


def validar_tasa(valor):
    if valor < 0:
        raise ValueError("La tasa no puede ser negativa.")


def validar_tasa_positiva(valor):
    if valor <= 0:
        raise ValueError("La tasa debe ser mayor que cero.")


def validar_periodos(valor):
    if valor <= 0:
        raise ValueError("El tiempo debe ser mayor que cero.")


def calcular_monto_desde_interes(capital, interes):
    validar_monto(capital)
    if interes < 0:
        raise ValueError("El interés no puede ser negativo.")
    return capital + interes


def calcular_monto(capital, tasa, periodos):
    validar_monto(capital)
    validar_tasa(tasa)
    validar_periodos(periodos)
    return capital * (1 + tasa * periodos)


def calcular_valor_presente(monto, tasa, periodos):
    validar_monto(monto)
    validar_tasa(tasa)
    validar_periodos(periodos)
    return monto / (1 + tasa * periodos)


def calcular_tasa(monto, capital, periodos):
    validar_monto(monto)
    validar_monto(capital)
    validar_periodos(periodos)
    return (monto - capital) / (capital * periodos)


def calcular_tiempo(monto, capital, tasa):
    validar_monto(monto)
    validar_monto(capital)
    validar_tasa_positiva(tasa)
    return (monto - capital) / (capital * tasa)


def calcular_descuento_simple(monto_nominal, tasa_descuento, periodos):
    validar_monto(monto_nominal)
    validar_tasa(tasa_descuento)
    validar_periodos(periodos)
    return monto_nominal * tasa_descuento * periodos


def calcular_valor_actual(monto_nominal, tasa_descuento, periodos):
    validar_monto(monto_nominal)
    validar_tasa(tasa_descuento)
    validar_periodos(periodos)
    return monto_nominal * (1 - tasa_descuento * periodos)


def calcular_tasa_descuento(tasa, periodos):
    validar_tasa_positiva(tasa)
    validar_periodos(periodos)
    return tasa / (1 + tasa * periodos)