def validar_monto(valor):
    """
    Valida que un monto sea mayor que cero.
    """
    if valor <= 0:
        raise ValueError("El monto debe ser mayor que cero.")
    
    return True


def validar_tasa(r):
    """
    Valida que la tasa de interés no sea negativa.
    """
    if r < 0:
        raise ValueError("La tasa de interés no puede ser negativa.")
    
    return True


def validar_tasa_anualidad(r):
    """
    Valida la tasa utilizada en las fórmulas de anualidades.
    Debe ser mayor que cero porque las fórmulas
    de P/A, F/A, A/F y A/P contienen división entre r.
    """
    if r <= 0:
        raise ValueError("La tasa de interés debe ser mayor que cero.")
    
    return True


def validar_periodos(n):
    """
    Valida que el número de períodos sea un entero mayor que cero.
    """
    if n <= 0:
        raise ValueError("El número de períodos debe ser mayor que cero.")
    
    if not isinstance(n, int):
        raise ValueError("El número de períodos debe ser un entero.")
    
    return True