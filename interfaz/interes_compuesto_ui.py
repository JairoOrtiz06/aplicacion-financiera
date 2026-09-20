import tkinter as tk
from tkinter import messagebox, ttk

from modulos.interes_compuesto import (
    calcular_futuro,
    calcular_futuro_anualidad,
    calcular_pago_desde_futuro,
    calcular_pago_desde_presente,
    calcular_presente,
    calcular_presente_anualidad,
)


FONDO = "#F3F7F5"
BLANCO = "#FFFFFF"
VERDE = "#0B5D4B"
TERRACOTA = "#2E7D5B"
VINO = "#244F45"
NEGRO = "#173A31"
GRIS = "#60766E"
BORDE = "#D2E2DB"
CAMPO = "#F8FBF9"


OPERACIONES = {
    "Valor futuro (F)": {
        "descripcion": "Calcula el monto acumulado a partir de un capital presente.",
        "campos": (
            ("capital", "Capital presente (P)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_futuro,
        "argumentos": ("capital", "tasa", "periodos"),
        "resultado": "Valor futuro",
    },
    "Valor presente (P)": {
        "descripcion": "Calcula el capital actual equivalente a un valor futuro.",
        "campos": (
            ("futuro", "Valor futuro (F)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_presente,
        "argumentos": ("futuro", "tasa", "periodos"),
        "resultado": "Valor presente",
    },
    "Presente de anualidad (P/A)": {
        "descripcion": "Calcula el valor presente de una serie uniforme de pagos.",
        "campos": (
            ("pago", "Pago periodico (A)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_presente_anualidad,
        "argumentos": ("pago", "tasa", "periodos"),
        "resultado": "Valor presente de la anualidad",
    },
    "Futuro de anualidad (F/A)": {
        "descripcion": "Calcula el valor futuro acumulado de una serie uniforme.",
        "campos": (
            ("pago", "Pago periodico (A)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_futuro_anualidad,
        "argumentos": ("pago", "tasa", "periodos"),
        "resultado": "Valor futuro de la anualidad",
    },
    "Pago desde futuro (A/F)": {
        "descripcion": "Calcula el pago periodico necesario para alcanzar un monto futuro.",
        "campos": (
            ("futuro", "Valor futuro (F)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_pago_desde_futuro,
        "argumentos": ("futuro", "tasa", "periodos"),
        "resultado": "Pago periodico",
    },
    "Pago desde presente (A/P)": {
        "descripcion": "Calcula el pago periodico equivalente a un capital presente.",
        "campos": (
            ("presente", "Valor presente (P)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_pago_desde_presente,
        "argumentos": ("presente", "tasa", "periodos"),
        "resultado": "Pago periodico",
    },
}


def leer_numero(entrada):
    return float(entrada.get().strip().replace(",", "."))





def crear_caja_entrada(parent, color):
    caja = tk.Frame(
        parent,
        bg=CAMPO,
        highlightthickness=1,
        highlightbackground=BORDE,
    )
    caja.pack(fill="x")

    entrada = tk.Entry(
        caja,
        font=("Segoe UI", 11),
        bg=CAMPO,
        fg=NEGRO,
        insertbackground=color,
        relief="flat",
        bd=0,
    )
    entrada.pack(fill="x", padx=14, pady=9)
    entrada.bind(
        "<FocusIn>",
        lambda _evento: caja.config(highlightbackground=color, highlightthickness=2),
    )
    entrada.bind(
        "<FocusOut>",
        lambda _evento: caja.config(highlightbackground=BORDE, highlightthickness=1),
    )

    return entrada


def mostrar_interes_compuesto_ui(contenido):

    estilo = ttk.Style(contenido)
    estilo.theme_use("clam")
    estilo.configure(
        "Compuesto.TCombobox",
        fieldbackground=CAMPO,
        background=CAMPO,
        foreground=NEGRO,
        bordercolor=BORDE,
        lightcolor=BORDE,
        darkcolor=BORDE,
        arrowcolor=VERDE,
        padding=8,
    )
    estilo.map(
        "Compuesto.TCombobox",
        fieldbackground=[("readonly", CAMPO)],
        selectbackground=[("readonly", CAMPO)],
        selectforeground=[("readonly", NEGRO)],
        bordercolor=[("focus", TERRACOTA)],
    )

    encabezado = tk.Frame(contenido, bg=VERDE, height=92)
    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="INTERES COMPUESTO",
        font=("Segoe UI", 18, "bold"),
        bg=VERDE,
        fg=BLANCO,
    ).pack(anchor="w", padx=34, pady=(20, 0))

    tk.Label(
        encabezado,
        text="Capitalizacion, anualidades y pagos equivalentes",
        font=("Segoe UI", 9),
        bg=VERDE,
        fg="#CBE7DD",
    ).pack(anchor="w", padx=34, pady=(3, 0))

    cuerpo = tk.Frame(contenido, bg=FONDO)
    cuerpo.pack(fill="both", expand=True, padx=34, pady=28)

    formulario = tk.Frame(
        cuerpo,
        bg=BLANCO,
        highlightthickness=1,
        highlightbackground=BORDE,
    )
    formulario.pack(fill="both", expand=True)

    tk.Frame(formulario, bg=TERRACOTA, height=8).pack(fill="x")

    tk.Label(
        formulario,
        text="OPERACION",
        font=("Segoe UI", 8, "bold"),
        bg=BLANCO,
        fg=GRIS,
    ).pack(anchor="w", padx=28, pady=(24, 7))

    operacion = tk.StringVar(value=next(iter(OPERACIONES)))

    selector = ttk.Combobox(
        formulario,
        textvariable=operacion,
        values=list(OPERACIONES.keys()),
        state="readonly",
        font=("Segoe UI", 10),
        style="Compuesto.TCombobox",
    )
    selector.pack(fill="x", padx=28)

    descripcion = tk.Label(
        formulario,
        text="",
        font=("Segoe UI", 9),
        bg=BLANCO,
        fg=GRIS,
        justify="left",
        wraplength=500,
    )
    descripcion.pack(anchor="w", padx=28, pady=(10, 10))

    separador = tk.Frame(formulario, bg=BORDE, height=1)
    separador.pack(fill="x", padx=28, pady=(0, 12))

    campos = tk.Frame(formulario, bg=BLANCO)
    campos.pack(fill="x", padx=28)

    entradas = {}

    resultado = tk.Label(
        formulario,
        text="Complete los datos y presione CALCULAR.",
        font=("Segoe UI", 12, "bold"),
        bg=BLANCO,
        fg=TERRACOTA,
        justify="left",
        wraplength=500,
    )
    resultado.pack(anchor="w", padx=28, pady=(18, 18))

    def mostrar_campos(_evento=None):
        for widget in campos.winfo_children():
            widget.destroy()

        entradas.clear()
        datos_operacion = OPERACIONES[operacion.get()]
        descripcion.config(text=datos_operacion["descripcion"])
        resultado.config(text="Complete los datos y presione CALCULAR.")

        for nombre, texto in datos_operacion["campos"]:
            bloque = tk.Frame(campos, bg=BLANCO)
            bloque.pack(fill="x", pady=7)

            tk.Label(
                bloque,
                text=texto,
                font=("Segoe UI", 10, "bold"),
                bg=BLANCO,
                fg=NEGRO,
            ).pack(anchor="w", pady=(0, 6))

            entradas[nombre] = crear_caja_entrada(bloque, TERRACOTA)

        primera_entrada = next(iter(entradas.values()), None)
        if primera_entrada is not None:
            primera_entrada.focus_set()

    def valores_para_operacion(datos_operacion):
        valores = {}

        for nombre in datos_operacion["argumentos"]:
            if nombre == "tasa":
                valores[nombre] = leer_numero(entradas[nombre]) / 100
            elif nombre == "periodos":
                valores[nombre] = int(entradas[nombre].get().strip())
            else:
                valores[nombre] = leer_numero(entradas[nombre])

        return [valores[nombre] for nombre in datos_operacion["argumentos"]]

    def calcular():
        try:
            datos_operacion = OPERACIONES[operacion.get()]
            argumentos = valores_para_operacion(datos_operacion)
            valor = datos_operacion["funcion"](*argumentos)

            resultado.config(
                text=f'{datos_operacion["resultado"]}: ${valor:,.2f}'
            )
        except ValueError as error:
            mensaje = str(error) or "Ingrese valores numericos validos."
            messagebox.showerror("Datos invalidos", mensaje, parent=contenido)
        except ZeroDivisionError:
            messagebox.showerror(
                "Datos invalidos",
                "La tasa y los periodos no generan una operacion valida.",
                parent=contenido,
            )

    botones = tk.Frame(cuerpo, bg=FONDO)
    botones.pack(fill="x", pady=(16, 0))

    boton_calcular = tk.Button(
        botones,
        text="CALCULAR",
        command=calcular,
        font=("Segoe UI", 10, "bold"),
        bg=TERRACOTA,
        fg=BLANCO,
        activebackground="#216346",
        activeforeground=BLANCO,
        relief="flat",
        bd=0,
        padx=26,
        pady=11,
        cursor="hand2",
    )
    boton_calcular.pack(side="left")

    boton_cerrar = tk.Button(
        botones,
        text="CERRAR",
        command=contenido.destroy,
        font=("Segoe UI", 10, "bold"),
        bg=VINO,
        fg=BLANCO,
        activebackground="#173A31",
        activeforeground=BLANCO,
        relief="flat",
        bd=0,
        padx=24,
        pady=11,
        cursor="hand2",
    )
    boton_cerrar.pack(side="left", padx=(10, 0))

    selector.bind("<<ComboboxSelected>>", mostrar_campos)
    contenido.bind("<Return>", lambda _evento: calcular())

    mostrar_campos()

