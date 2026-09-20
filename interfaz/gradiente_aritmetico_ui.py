import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graficas.lineas_tiempo import grafica_gradiente_aritmetico
from modulos.gradiente_aritmetico import (
    calcular_futuro_gradiente,
    calcular_pago_uniforme_gradiente,
    calcular_presente_gradiente,
)
from utilidades.validaciones import (
    validar_gradiente,
    validar_monto,
    validar_periodos,
    validar_tasa_anualidad,
)


FONDO = "#F3F7F5"
BLANCO = "#FFFFFF"
VERDE = "#0B5D4B"
DORADO = "#A67C18"
VINO = "#244F45"
NEGRO = "#173A31"
GRIS = "#60766E"
BORDE = "#D2E2DB"
CAMPO = "#F8FBF9"


OPERACIONES = {
    "Valor presente del gradiente (P)": {
        "descripcion": "Calcula el valor presente equivalente de un gradiente aritmetico vencido.",
        "campos": (
            ("pago", "Pago inicial (K)"),
            ("gradiente", "Gradiente aritmetico (G)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_presente_gradiente,
        "argumentos": ("pago", "gradiente", "tasa", "periodos"),
        "resultado": "Valor presente",
        "etiqueta_grafica": "VP equivalente",
    },
    "Pago uniforme equivalente (R)": {
        "descripcion": "Calcula el pago uniforme equivalente de un gradiente aritmetico vencido.",
        "campos": (
            ("pago", "Pago inicial (K)"),
            ("gradiente", "Gradiente aritmetico (G)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_pago_uniforme_gradiente,
        "argumentos": ("pago", "gradiente", "tasa", "periodos"),
        "resultado": "Pago uniforme equivalente",
        "etiqueta_grafica": "R equivalente",
    },
    "Valor futuro del gradiente (F)": {
        "descripcion": "Calcula el valor futuro acumulado de un gradiente aritmetico vencido.",
        "campos": (
            ("pago", "Pago inicial (K)"),
            ("gradiente", "Gradiente aritmetico (G)"),
            ("tasa", "Tasa de interes (%)"),
            ("periodos", "Numero de periodos (n)"),
        ),
        "funcion": calcular_futuro_gradiente,
        "argumentos": ("pago", "gradiente", "tasa", "periodos"),
        "resultado": "Valor futuro",
        "etiqueta_grafica": "VF equivalente",
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


def mostrar_gradiente_aritmetico_ui(contenido):
    estilo = ttk.Style(contenido)
    estilo.theme_use("clam")
    estilo.configure(
        "GradienteAritmetico.TCombobox",
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
        "GradienteAritmetico.TCombobox",
        fieldbackground=[("readonly", CAMPO)],
        selectbackground=[("readonly", CAMPO)],
        selectforeground=[("readonly", NEGRO)],
        bordercolor=[("focus", DORADO)],
    )

    encabezado = tk.Frame(contenido, bg=VERDE, height=92)
    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="GRADIENTE ARITMETICO",
        font=("Segoe UI", 18, "bold"),
        bg=VERDE,
        fg=BLANCO,
    ).pack(anchor="w", padx=34, pady=(20, 0))

    tk.Label(
        encabezado,
        text="Series con variacion constante por periodo",
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

    tk.Frame(formulario, bg=DORADO, height=8).pack(fill="x")

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
        style="GradienteAritmetico.TCombobox",
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

    tk.Frame(formulario, bg=BORDE, height=1).pack(fill="x", padx=28, pady=(0, 12))

    campos = tk.Frame(formulario, bg=BLANCO)
    campos.pack(fill="x", padx=28)

    entradas = {}

    resultado = tk.Label(
        formulario,
        text="Complete los datos y presione CALCULAR.",
        font=("Segoe UI", 12, "bold"),
        bg=BLANCO,
        fg=DORADO,
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
            text="LINEA DE TIEMPO",
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

            entradas[nombre] = crear_caja_entrada(bloque, DORADO)

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

    def validar_valores(valores):
        validar_monto(valores["pago"])
        validar_gradiente(valores["gradiente"])
        validar_tasa_anualidad(valores["tasa"])
        validar_periodos(valores["periodos"])

    def calcular():
        try:
            datos_operacion = OPERACIONES[operacion.get()]
            valores = valores_para_operacion(datos_operacion)
            validar_valores(valores)
            argumentos = [valores[nombre] for nombre in datos_operacion["argumentos"]]
            valor = datos_operacion["funcion"](*argumentos)

            resultado.config(text=f'{datos_operacion["resultado"]}: ${valor:,.2f}')
            mostrar_grafica(
                grafica_gradiente_aritmetico(
                    valores["pago"],
                    valores["gradiente"],
                    valores["periodos"],
                    valor,
                    datos_operacion["etiqueta_grafica"],
                )
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

    tk.Button(
        botones,
        text="CALCULAR",
        command=calcular,
        font=("Segoe UI", 10, "bold"),
        bg=DORADO,
        fg=BLANCO,
        activebackground="#856313",
        activeforeground=BLANCO,
        relief="flat",
        bd=0,
        padx=26,
        pady=11,
        cursor="hand2",
    ).pack(side="left")

    tk.Button(
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
    ).pack(side="left", padx=(10, 0))

    selector.bind("<<ComboboxSelected>>", mostrar_campos)
    contenido.bind("<Return>", lambda _evento: calcular())

    mostrar_campos()
