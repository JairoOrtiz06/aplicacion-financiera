import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graficas.lineas_tiempo import (
    grafica_anualidad,
    grafica_interes_compuesto,
)
from modulos.interes_compuesto import (
    calcular_futuro,
    calcular_futuro_anualidad,
    calcular_pago_desde_futuro,
    calcular_pago_desde_presente,
    calcular_presente,
    calcular_presente_anualidad,
)
from utilidades.validaciones import (
    validar_monto,
    validar_periodos,
    validar_tasa,
    validar_tasa_anualidad,
)


FONDO = "#F3F7F5"
BLANCO = "#FFFFFF"
VERDE = "#0B5D4B"
DORADO = "#A67C18"
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
        "tipo_tasa": "compuesto",
        "tipo_grafica": "capital_futuro",
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
        "tipo_tasa": "compuesto",
        "tipo_grafica": "capital_futuro",
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
        "tipo_tasa": "anualidad",
        "tipo_grafica": "anualidad",
        "etiqueta_grafica": "VP equivalente",
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
        "tipo_tasa": "anualidad",
        "tipo_grafica": "anualidad",
        "etiqueta_grafica": "VF equivalente",
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
        "tipo_tasa": "anualidad",
        "tipo_grafica": "anualidad_pago",
        "etiqueta_grafica": "VF objetivo",
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
        "tipo_tasa": "anualidad",
        "tipo_grafica": "anualidad_pago",
        "etiqueta_grafica": "VP origen",
    },
}


def leer_numero(entrada):
    texto = entrada.get().strip().replace(",", ".")

    if texto == "":
        raise ValueError("Todos los campos son obligatorios.")

    try:
        return float(texto)
    except ValueError:
        raise ValueError("Ingrese únicamente valores numéricos.")



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

    def validar_tecla(texto):
        if texto == "":
            return True

        texto = texto.replace(",", ".")

        if texto.count(".") > 1:
            return False

        try:
            float(texto)
            return True
        except ValueError:
            return False

    validar_cmd = entrada.register(validar_tecla)

    entrada.config(
        validate="key",
        validatecommand=(validar_cmd, "%P")
    )

    entrada.pack(fill="x", padx=14, pady=9)

    entrada.bind(
        "<FocusIn>",
        lambda _evento: caja.config(
            highlightbackground=color,
            highlightthickness=2
        ),
    )

    entrada.bind(
        "<FocusOut>",
        lambda _evento: caja.config(
            highlightbackground=BORDE,
            highlightthickness=1
        ),
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

    titulo = tk.Frame(contenido, bg=FONDO)
    titulo.pack(fill="x", padx=42, pady=(28, 4))
    tk.Label(titulo, text="Interés Compuesto", font=("Segoe UI", 26, "bold"), bg=FONDO, fg=NEGRO).pack(anchor="w")
    tk.Label(titulo, text="Capitalización, anualidades y pagos equivalentes.", font=("Segoe UI", 10), bg=FONDO, fg=GRIS).pack(anchor="w", pady=(5, 0))

    cuerpo = tk.Frame(contenido, bg=FONDO)
    cuerpo.pack(fill="both", expand=True, padx=42, pady=28)

    formulario = tk.Frame(
        cuerpo,
        bg=BLANCO,
        highlightthickness=1,
        highlightbackground=BORDE,
    )
    formulario.pack(fill="both", expand=True)

    tk.Frame(formulario, bg=TERRACOTA, height=8).pack(fill="x")
    cabecera = tk.Frame(formulario, bg=VERDE)
    cabecera.pack(fill="x", padx=20, pady=(18, 0))
    tk.Label(cabecera, text="INTERÉS COMPUESTO", font=("Segoe UI", 9, "bold"), bg=DORADO, fg=BLANCO, padx=10, pady=5).pack(side="left", padx=(14, 12), pady=12)
    tk.Label(cabecera, text="Laboratorio de fórmulas", font=("Segoe UI", 13, "bold"), bg=VERDE, fg=BLANCO).pack(side="left", pady=12)

    tk.Label(
        formulario,
        text="SELECCIONE LA OPERACIÓN",
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

    grafica_panel = tk.Frame(
        cuerpo,
        bg=BLANCO,
        highlightthickness=1,
        highlightbackground=BORDE,
    )
    grafica_canvas = {"widget": None}

    def limpiar_grafica():
        for widget in grafica_panel.winfo_children():
            widget.destroy()

        grafica_canvas["widget"] = None

        if grafica_panel.winfo_ismapped():
            grafica_panel.pack_forget()

    def mostrar_grafica(fig):
        limpiar_grafica()
        grafica_panel.pack(fill="x", pady=(16, 0))

        tk.Label(
            grafica_panel,
            text="LÍNEA DE TIEMPO",
            font=("Segoe UI", 9, "bold"),
            bg=BLANCO,
            fg=NEGRO,
        ).pack(anchor="w", padx=18, pady=(12, 0))

        canvas = FigureCanvasTkAgg(fig, master=grafica_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=12, pady=12)
        grafica_canvas["widget"] = canvas

    def mostrar_campos(_evento=None):
        for widget in campos.winfo_children():
            widget.destroy()

        entradas.clear()
        datos_operacion = OPERACIONES[operacion.get()]
        descripcion.config(text=datos_operacion["descripcion"])
        resultado.config(text="Complete los datos y presione CALCULAR.")
        limpiar_grafica()

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

        return valores

    def validar_valores(datos_operacion, valores):
        for nombre, valor in valores.items():
            if nombre in ("capital", "futuro", "presente", "pago"):
                validar_monto(valor)
            elif nombre == "periodos":
                validar_periodos(valor)

        if datos_operacion["tipo_tasa"] == "anualidad":
            validar_tasa_anualidad(valores["tasa"])
        else:
            validar_tasa(valores["tasa"])

    def crear_figura(datos_operacion, valores, valor_resultado):
        tipo_grafica = datos_operacion["tipo_grafica"]
        periodos = valores["periodos"]

        if tipo_grafica == "capital_futuro":
            capital = valores.get("capital", valor_resultado)
            futuro = valores.get("futuro", valor_resultado)
            return grafica_interes_compuesto(capital, futuro, periodos)

        if tipo_grafica == "anualidad":
            return grafica_anualidad(
                valores["pago"],
                periodos,
                valor_resultado,
                datos_operacion["etiqueta_grafica"],
                TERRACOTA,
            )

        pago = valor_resultado
        equivalente = valores.get("futuro", valores.get("presente"))
        return grafica_anualidad(
            pago,
            periodos,
            equivalente,
            datos_operacion["etiqueta_grafica"],
            TERRACOTA,
        )

    def calcular():
        try:
            datos_operacion = OPERACIONES[operacion.get()]
            valores = valores_para_operacion(datos_operacion)
            validar_valores(datos_operacion, valores)
            argumentos = [valores[nombre] for nombre in datos_operacion["argumentos"]]
            valor = datos_operacion["funcion"](*argumentos)

            resultado.config(
                text=f'{datos_operacion["resultado"]}: ${valor:,.2f}'
            )
            mostrar_grafica(crear_figura(datos_operacion, valores, valor))
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
