import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modulos.interes_simple import (
    calcular_interes_simple,
    calcular_monto_desde_interes,
    calcular_monto,
    calcular_valor_presente,
    calcular_tasa,
    calcular_tiempo,
    calcular_descuento_simple,
    calcular_valor_actual,
    calcular_tasa_descuento,
)
from modulos.interes_compuesto import calcular_futuro
from modulos.gradiente_geometrico import calcular_gradiente_geometrico
from interfaz.interes_compuesto_ui import mostrar_interes_compuesto_ui
from interfaz.gradiente_aritmetico_ui import mostrar_gradiente_aritmetico_ui
from modulos.gradiente_aritmetico import calcular_presente_gradiente
from modulos.gradiente_geometrico import (
    calcular_gradiente_geometrico,
    calcular_presente_gradiente_geometrico,
    calcular_presente_gradiente_geometrico_igual,
    calcular_futuro_gradiente_geometrico,
    calcular_futuro_gradiente_geometrico_igual,
)
from interfaz.interes_compuesto_ui import mostrar_interes_compuesto_ui

from graficas.lineas_tiempo import (
    grafica_interes_simple,
    grafica_interes_compuesto,
    grafica_gradiente_aritmetico,
    grafica_gradiente_geometrico
)


# Sistema visual: verdes institucionales, blanco y acento dorado.
FONDO = "#F3F7F5"
BLANCO = "#FFFFFF"
VERDE = "#0B5D4B"
VERDE_CLARO = "#138A72"
DORADO = "#A67C18"
TERRACOTA = "#2E7D5B"
VINO = "#244F45"
NEGRO = "#173A31"
GRIS = "#60766E"
GRIS_CLARO = "#9AAEA7"
BORDE = "#D2E2DB"
CAMPO = "#F8FBF9"

COLORES_HOVER = {
    VERDE: "#084738",
    VERDE_CLARO: "#0E6F5B",
    DORADO: "#856313",
    TERRACOTA: "#216346",
    VINO: "#173A31",
}


ventana = None
navegacion = {}
contenido = None
visor_contenido = None


def crear_ventana():
    global ventana, contenido, visor_contenido

    ventana = tk.Tk()
    ventana.title("Ingeniería Económica")
    ventana.geometry("1200x760")
    ventana.minsize(1160, 700)
    ventana.configure(bg=FONDO)

    encabezado_superior()

    visor_contenido = tk.Canvas(
        ventana,
        bg=FONDO,
        highlightthickness=0
    )
    barra_contenido = tk.Scrollbar(
        ventana,
        orient="vertical",
        command=visor_contenido.yview
    )
    visor_contenido.configure(yscrollcommand=barra_contenido.set)
    barra_contenido.pack(side="right", fill="y")
    visor_contenido.pack(
        side="left",
        fill="both",
        expand=True
    )

    contenido = tk.Frame(visor_contenido, bg=FONDO)
    ventana_contenido = visor_contenido.create_window(
        (0, 0),
        window=contenido,
        anchor="nw"
    )

    def actualizar_contenido(event=None):
        visor_contenido.configure(scrollregion=visor_contenido.bbox("all"))
        visor_contenido.itemconfigure(ventana_contenido, width=visor_contenido.winfo_width())

    contenido.bind("<Configure>", actualizar_contenido)
    visor_contenido.bind("<Configure>", actualizar_contenido)

    def desplazar_contenido(event):
        if event.delta:
            visor_contenido.yview_scroll(int(-event.delta / 120), "units")
        elif event.num == 4:
            visor_contenido.yview_scroll(-1, "units")
        elif event.num == 5:
            visor_contenido.yview_scroll(1, "units")

    visor_contenido.bind("<MouseWheel>", desplazar_contenido)
    visor_contenido.bind("<Button-4>", desplazar_contenido)
    visor_contenido.bind("<Button-5>", desplazar_contenido)
    ventana.bind_all("<MouseWheel>", desplazar_contenido)

    mostrar_menu()
    return ventana


def limpiar():
    for widget in contenido.winfo_children():
        widget.destroy()


def leer_numero(entrada):
    """Acepta valores escritos con coma o punto decimal."""
    return float(entrada.get().strip().replace(",", "."))


def redondeado(canvas, x1, y1, x2, y2, radio, color, outline=None, ancho=1):
    """Dibuja una tarjeta redondeada, con tramos rectos y esquinas suaves."""
    puntos = [
        x1 + radio, y1,
        x2 - radio, y1,
        x2, y1,
        x2, y1 + radio,
        x2, y2 - radio,
        x2, y2,
        x2 - radio, y2,
        x1 + radio, y2,
        x1, y2,
        x1, y2 - radio,
        x1, y1 + radio,
        x1, y1,
    ]
    return canvas.create_polygon(
        puntos,
        smooth=True,
        splinesteps=18,
        fill=color,
        outline=outline or color,
        width=ancho,
    )


def boton_redondeado(parent, texto, color, comando, width=180, height=44):
    """Botón de canvas con color de interacción propio para cada acción."""
    canvas = tk.Canvas(
        parent,
        width=width,
        height=height,
        bg=parent.cget("bg"),
        highlightthickness=0,
        bd=0
    )

    figura = redondeado(
        canvas,
        1,
        1,
        width - 1,
        height - 1,
        14,
        color
    )

    canvas.create_text(
        width // 2,
        height // 2,
        text=texto,
        font=("Segoe UI", 10, "bold"),
        fill=BLANCO
    )

    canvas.bind("<Button-1>", lambda e: comando())
    canvas.bind(
        "<Enter>",
        lambda e: canvas.itemconfig(
            figura,
            fill=COLORES_HOVER.get(color, VERDE)
        )
    )
    canvas.bind(
        "<Leave>",
        lambda e: canvas.itemconfig(figura, fill=color)
    )

    return canvas


def encabezado_lateral():
    lateral = tk.Frame(
        ventana,
        bg=VERDE,
        width=245
    )
    lateral.pack(side="left", fill="y")
    lateral.pack_propagate(False)

    logo = tk.Canvas(
        lateral,
        width=70,
        height=70,
        bg=VERDE,
        highlightthickness=0
    )
    logo.pack(pady=(45, 10))

    redondeado(
        logo,
        3,
        3,
        67,
        67,
        18,
        DORADO
    )

    logo.create_text(
        35,
        35,
        text="UES",
        font=("Arial Rounded MT Bold", 16, "bold"),
        fill=BLANCO
    )

    tk.Label(
        lateral,
        text="INGENIERÍA",
        font=("Segoe UI", 11, "bold"),
        bg=VERDE,
        fg="#D9EDE6"
    ).pack()

    tk.Label(
        lateral,
        text="ECONÓMICA",
        font=("Arial Rounded MT Bold", 20, "bold"),
        bg=VERDE,
        fg=BLANCO
    ).pack(pady=(0, 45))

    tk.Frame(
        lateral,
        bg="#2A7663",
        height=1
    ).pack(fill="x", padx=30)

    tk.Label(
        lateral,
        text="MENÚ PRINCIPAL",
        font=("Segoe UI", 8, "bold"),
        bg=VERDE,
        fg="#A9D4C7"
    ).pack(anchor="w", padx=30, pady=(30, 15))

    crear_item_menu(
        lateral,
        "Inicio",
        mostrar_menu,
        True
    )

    crear_item_menu(
        lateral,
        "Interés Simple",
        mostrar_interes_simple
    )

    crear_item_menu(
        lateral,
        "Interés Compuesto",
        mostrar_interes_compuesto
    )

    crear_item_menu(
        lateral,
        "Gradiente Aritmético",
        mostrar_gradiente_aritmetico
    )

    crear_item_menu(
        lateral,
        "Gradiente Geométrico",
        mostrar_gradiente_geometrico
    )

    separador = tk.Frame(
        lateral,
        bg=VERDE
    )
    separador.pack(expand=True, fill="both")

    tk.Label(
        lateral,
        text="UES • Ingeniería",
        font=("Segoe UI", 8),
        bg=VERDE,
        fg="#A9D4C7"
    ).pack(pady=(0, 5))

    tk.Label(
        lateral,
        text="Análisis financiero",
        font=("Segoe UI", 8),
        bg=VERDE,
        fg="#A9D4C7"
    ).pack(pady=(0, 30))


def crear_item_menu(parent, texto, comando, activo=False):
    color = VERDE_CLARO if activo else VERDE

    item = tk.Frame(
        parent,
        bg=color,
        height=48
    )
    item.pack(fill="x", padx=18, pady=3)
    item.pack_propagate(False)

    tk.Label(
        item,
        text=texto,
        font=("Segoe UI", 10, "bold" if activo else "normal"),
        bg=color,
        fg=BLANCO if activo else "#D9EDE6"
    ).pack(
        side="left",
        padx=18
    )

    item.bind("<Button-1>", lambda e: comando())

    for widget in item.winfo_children():
        widget.bind("<Button-1>", lambda e: comando())
        widget.bind(
            "<Enter>",
            lambda e: item.config(bg=VERDE_CLARO)
        )
        widget.bind(
            "<Leave>",
            lambda e: item.config(bg=color)
        )

    item.bind(
        "<Enter>",
        lambda e: item.config(bg=VERDE_CLARO)
    )

    item.bind(
        "<Leave>",
        lambda e: item.config(bg=color)
    )


def actualizar_navegacion(seccion):
    """Marca visualmente la sección activa en la barra superior."""
    for nombre, elementos in navegacion.items():
        marco, etiqueta, indicador = elementos
        activo = nombre == seccion
        fondo = VERDE_CLARO if activo else VERDE
        marco.config(bg=fondo)
        etiqueta.config(bg=fondo, fg=BLANCO if activo else "#D9EDE6")
        indicador.config(bg=DORADO if activo else fondo)


def item_navegacion(parent, texto, comando):
    marco = tk.Frame(parent, bg=VERDE, width=132, height=58)
    marco.pack(side="left", padx=2)
    marco.pack_propagate(False)

    indicador = tk.Frame(marco, bg=VERDE, height=3)
    indicador.pack(side="bottom", fill="x")

    etiqueta = tk.Label(
        marco,
        text=texto,
        font=("Segoe UI", 9, "bold"),
        bg=VERDE,
        fg="#D9EDE6",
        cursor="hand2",
    )
    etiqueta.pack(expand=True, fill="both")

    def entrar(_evento):
        if marco.cget("bg") != VERDE_CLARO:
            marco.config(bg="#0F735E")
            etiqueta.config(bg="#0F735E")

    def salir(_evento):
        if marco.cget("bg") != VERDE_CLARO:
            marco.config(bg=VERDE)
            etiqueta.config(bg=VERDE)

    for widget in (marco, etiqueta):
        widget.bind("<Button-1>", lambda _evento: comando())
        widget.bind("<Enter>", entrar)
        widget.bind("<Leave>", salir)

    navegacion[texto] = (marco, etiqueta, indicador)


def encabezado_superior():
    """Construye una barra de navegación horizontal estilo aplicación de escritorio."""
    barra = tk.Frame(ventana, bg=VERDE, height=76)
    barra.pack(fill="x", side="top")
    barra.pack_propagate(False)

    marca = tk.Frame(barra, bg=VERDE, width=282)
    marca.pack(side="left", fill="y", padx=(32, 22))
    marca.pack_propagate(False)

    insignia = tk.Label(
        marca,
        text="UES",
        font=("Segoe UI", 11, "bold"),
        bg=DORADO,
        fg=BLANCO,
        padx=10,
        pady=6,
    )
    insignia.pack(side="left", pady=18)

    texto_marca = tk.Frame(marca, bg=VERDE)
    texto_marca.pack(side="left", padx=10, pady=15)
    tk.Label(
        texto_marca,
        text="INGENIERÍA ECONÓMICA",
        font=("Segoe UI", 11, "bold"),
        bg=VERDE,
        fg=BLANCO,
    ).pack(anchor="w")
    tk.Label(
        texto_marca,
        text="Panel financiero",
        font=("Segoe UI", 8),
        bg=VERDE,
        fg="#A9D4C7",
    ).pack(anchor="w")

    menu = tk.Frame(barra, bg=VERDE)
    menu.pack(side="right", padx=30, pady=9)

    item_navegacion(menu, "Inicio", lambda: mostrar_menu())
    item_navegacion(menu, "Interés simple", lambda: mostrar_interes_simple())
    item_navegacion(menu, "Interés compuesto", lambda: mostrar_interes_compuesto())
    item_navegacion(menu, "Gradiente aritmético", lambda: mostrar_gradiente_aritmetico())
    item_navegacion(menu, "Gradiente geométrico", lambda: mostrar_gradiente_geometrico())
    actualizar_navegacion("Inicio")


def titulo_pagina(titulo, subtitulo):
    zona = tk.Frame(
        contenido,
        bg=FONDO
    )
    zona.pack(
        fill="x",
        padx=42,
        pady=(28, 4)
    )

    tk.Label(
        zona,
        text=titulo,
        font=("Segoe UI", 26, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(anchor="w")

    tk.Label(
        zona,
        text=subtitulo,
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=GRIS
    ).pack(anchor="w", pady=(5, 0))


def crear_banner_inicio(parent):
    """Crea la cabecera ejecutiva del panel principal."""
    banner = tk.Frame(parent, bg=VERDE, height=112)
    banner.pack(fill="x", padx=42, pady=(18, 16))
    banner.pack_propagate(False)

    informacion = tk.Frame(banner, bg=VERDE)
    informacion.pack(side="left", fill="both", expand=True, padx=24, pady=18)

    tk.Label(
        informacion,
        text="Panel de análisis financiero",
        font=("Segoe UI", 15, "bold"),
        bg=VERDE,
        fg=BLANCO,
    ).pack(anchor="w")
    tk.Label(
        informacion,
        text="Selecciona un método para iniciar un nuevo cálculo.",
        font=("Segoe UI", 9),
        bg=VERDE,
        fg="#CBE7DD",
    ).pack(anchor="w", pady=(5, 0))

    indicadores = tk.Frame(banner, bg=VERDE)
    indicadores.pack(side="right", padx=22, pady=18)

    for numero, etiqueta, color in (
        ("04", "MÉTODOS", TERRACOTA),
        ("02", "GRADIENTES", DORADO),
    ):
        indicador = tk.Frame(indicadores, bg="#174F41", width=92, height=72)
        indicador.pack(side="left", padx=4)
        indicador.pack_propagate(False)
        tk.Frame(indicador, bg=color, height=3).pack(fill="x")
        tk.Label(
            indicador,
            text=numero,
            font=("Segoe UI", 16, "bold"),
            bg="#174F41",
            fg=BLANCO,
        ).pack(pady=(8, 0))
        tk.Label(
            indicador,
            text=etiqueta,
            font=("Segoe UI", 7, "bold"),
            bg="#174F41",
            fg="#CBE7DD",
        ).pack()


def tarjeta_metodo(parent, numero, titulo, descripcion, color, comando):
    ancho = 525
    alto = 170

    marco = tk.Frame(
        parent,
        bg=BLANCO,
        width=ancho,
        height=alto,
        highlightthickness=1,
        highlightbackground=BORDE
    )
    marco.pack_propagate(False)

    canvas = tk.Canvas(
        marco,
        width=ancho,
        height=alto,
        bg=BLANCO,
        highlightthickness=0,
        bd=0
    )
    canvas.pack(fill="both", expand=True)

    fondo_tarjeta = redondeado(
        canvas,
        1,
        1,
        ancho - 1,
        alto - 1,
        22,
        BLANCO,
        BORDE
    )

    redondeado(
        canvas,
        0,
        0,
        8,
        alto,
        4,
        color
    )

    redondeado(
        canvas,
        ancho - 128,
        22,
        ancho - 24,
        48,
        8,
        "#E7F4EF",
    )
    canvas.create_text(
        ancho - 76,
        35,
        text="CALCULADORA",
        font=("Segoe UI", 7, "bold"),
        fill=color,
    )

    redondeado(
        canvas,
        24,
        22,
        74,
        52,
        10,
        color
    )

    canvas.create_text(
        49,
        38,
        text=numero,
        font=("Segoe UI", 10, "bold"),
        fill=BLANCO
    )

    canvas.create_text(
        24,
        74,
        text=titulo,
        anchor="w",
        font=("Segoe UI", 17, "bold"),
        fill=NEGRO
    )

    canvas.create_text(
        24,
        99,
        text=descripcion,
        anchor="nw",
        width=470,
        font=("Segoe UI", 9),
        fill=GRIS
    )

    btn = boton_redondeado(
        marco,
        "ABRIR MÉTODO",
        color,
        comando,
        158,
        36
    )

    btn.place(
        x=24,
        y=126
    )

    def resaltar(_evento):
        canvas.itemconfig(fondo_tarjeta, outline=color, width=2)

    def restaurar(_evento):
        canvas.itemconfig(fondo_tarjeta, outline=BORDE, width=1)

    canvas.bind("<Enter>", resaltar)
    canvas.bind("<Leave>", restaurar)

    return marco


def mostrar_menu():
    actualizar_navegacion("Inicio")
    limpiar()

    titulo_pagina(
        "Ingeniería Económica",
        "Analiza el comportamiento del dinero mediante métodos financieros."
    )

    crear_banner_inicio(contenido)

    tk.Label(
        contenido,
        text="Métodos disponibles",
        font=("Segoe UI", 10, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        anchor="w",
        padx=42,
        pady=(0, 6)
    )

    tarjetas = tk.Frame(
        contenido,
        bg=FONDO
    )
    tarjetas.pack(
        padx=42,
        fill="x"
    )

    cuadricula = tk.Frame(
        tarjetas,
        bg=FONDO
    )
    cuadricula.pack(anchor="center")

    fila1 = tk.Frame(
        cuadricula,
        bg=FONDO
    )
    fila1.pack(fill="x", pady=5)

    tarjeta_metodo(
        fila1,
        "01",
        "Interés Simple",
        "Interés generado y valor futuro de una inversión.",
        VERDE_CLARO,
        mostrar_interes_simple
    ).pack(side="left", padx=(0, 10))

    tarjeta_metodo(
        fila1,
        "02",
        "Interés Compuesto",
        "Crecimiento de capital con capitalización periódica.",
        TERRACOTA,
        mostrar_interes_compuesto
    ).pack(side="left", padx=10)

    fila2 = tk.Frame(
        cuadricula,
        bg=FONDO
    )
    fila2.pack(fill="x", pady=5)

    tarjeta_metodo(
        fila2,
        "03",
        "Gradiente Aritmético",
        "Flujos que varían por una cantidad monetaria constante.",
        DORADO,
        mostrar_gradiente_aritmetico
    ).pack(side="left", padx=(0, 10))

    tarjeta_metodo(
        fila2,
        "04",
        "Gradiente Geométrico",
        "Flujos que cambian con una tasa porcentual constante.",
        VINO,
        mostrar_gradiente_geometrico
    ).pack(side="left", padx=10)

    pie = tk.Frame(
        contenido,
        bg=FONDO
    )
    pie.pack(
        fill="x",
        padx=42,
        pady=(15, 0)
    )

    tk.Label(
        pie,
        text="Herramienta académica • Ingeniería Económica • UES",
        font=("Segoe UI", 9),
        bg=FONDO,
        fg=GRIS_CLARO
    ).pack(side="left")

    boton_redondeado(
        pie,
        "CERRAR",
        VINO,
        ventana.destroy,
        110,
        38
    ).pack(side="right")


def crear_resumen(parent, numero, titulo, subtitulo, color):
    marco = tk.Frame(
        parent,
        bg=BLANCO,
        width=170,
        height=72,
        highlightthickness=1,
        highlightbackground=BORDE
    )
    marco.pack_propagate(False)

    canvas = tk.Canvas(
        marco,
        width=170,
        height=72,
        bg=BLANCO,
        highlightthickness=0
    )
    canvas.pack(fill="both", expand=True)

    redondeado(
        canvas,
        1,
        1,
        169,
        71,
        18,
        BLANCO,
        BORDE
    )

    redondeado(
        canvas,
        14,
        17,
        55,
        55,
        11,
        color
    )

    canvas.create_text(
        34,
        36,
        text=numero,
        font=("Arial Rounded MT Bold", 11, "bold"),
        fill=BLANCO
    )

    canvas.create_text(
        70,
        27,
        text=titulo,
        anchor="w",
        font=("Segoe UI", 9, "bold"),
        fill=NEGRO
    )

    canvas.create_text(
        70,
        45,
        text=subtitulo,
        anchor="w",
        font=("Segoe UI", 8),
        fill=GRIS
    )

    return marco


def crear_formulario(titulo, subtitulo, color, campos):
    limpiar()

    titulo_pagina(
        titulo,
        subtitulo
    )

    contenedor = tk.Frame(
        contenido,
        bg=FONDO
    )
    contenedor.pack(
        fill="both",
        expand=True,
        padx=42,
        pady=20
    )

    formulario = tk.Frame(
        contenedor,
        bg=BLANCO,
        highlightthickness=1,
        highlightbackground=BORDE
    )
    formulario.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 12)
    )

    barra = tk.Frame(
        formulario,
        bg=color,
        height=8
    )
    barra.pack(
        fill="x"
    )

    tk.Label(
        formulario,
        text="DATOS DE ENTRADA",
        font=("Segoe UI", 9, "bold"),
        bg=BLANCO,
        fg=GRIS
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 18)
    )

    entradas = {}

    for nombre, texto in campos:
        bloque = tk.Frame(
            formulario,
            bg=BLANCO
        )
        bloque.pack(
            fill="x",
            padx=30,
            pady=7
        )

        tk.Label(
            bloque,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            bg=BLANCO,
            fg=NEGRO
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        caja = tk.Frame(
            bloque,
            bg=CAMPO,
            highlightthickness=1,
            highlightbackground=BORDE
        )
        caja.pack(
            fill="x"
        )

        entrada = tk.Entry(
            caja,
            font=("Segoe UI", 11),
            bg=CAMPO,
            fg=NEGRO,
            insertbackground=VERDE,
            relief="flat",
            bd=0
        )
        entrada.pack(
            fill="x",
            padx=14,
            pady=9
        )

        entrada.bind(
            "<FocusIn>",
            lambda _evento, marco=caja: marco.config(
                highlightbackground=color,
                highlightthickness=2,
            ),
        )
        entrada.bind(
            "<FocusOut>",
            lambda _evento, marco=caja: marco.config(
                highlightbackground=BORDE,
                highlightthickness=1,
            ),
        )

        entradas[nombre] = entrada

    return entradas


def panel_resultado(color):
    panel = tk.Frame(
        contenido,
        bg=BLANCO,
        highlightthickness=1,
        highlightbackground=BORDE
    )
    panel.pack(
        fill="x",
        padx=42,
        pady=(0, 10)
    )

    tk.Frame(
        panel,
        bg=color,
        width=7
    ).pack(
        side="left",
        fill="y"
    )

    contenido_resultado = tk.Frame(
        panel,
        bg=BLANCO
    )
    contenido_resultado.pack(
        fill="both",
        expand=True,
        padx=22,
        pady=15
    )

    tk.Label(
        contenido_resultado,
        text="RESULTADO",
        font=("Segoe UI", 8, "bold"),
        bg=BLANCO,
        fg=GRIS
    ).pack(anchor="w")

    resultado = tk.Label(
        contenido_resultado,
        text="Complete los datos y presione CALCULAR.",
        font=("Segoe UI", 12, "bold"),
        bg=BLANCO,
        fg=color,
        justify="left"
    )
    resultado.pack(
        anchor="w",
        pady=(5, 0)
    )

    return resultado


def mostrar_grafica(fig):
    for widget in contenido.winfo_children():
        if getattr(widget, "grafica_activa", False):
            widget.destroy()

    contenedor = tk.Frame(
        contenido,
        bg=BLANCO,
        highlightthickness=1,
        highlightbackground=BORDE
    )
    contenedor.grafica_activa = True
    contenedor.pack(fill="x", padx=42, pady=(0, 24))

    encabezado = tk.Frame(contenedor, bg=BLANCO, highlightthickness=1, highlightbackground=BORDE)
    encabezado.pack(fill="x")
    tk.Label(
        encabezado,
        text="LÍNEA DE TIEMPO",
        font=("Segoe UI", 9, "bold"),
        bg=BLANCO,
        fg=NEGRO,
    ).pack(anchor="w", padx=18, pady=(12, 10))

    fig_canvas = FigureCanvasTkAgg(fig, master=contenedor)
    fig_canvas.draw()
    fig_canvas.get_tk_widget().pack(fill="x", padx=12, pady=12)

    return contenedor


def botones_formulario(color, calcular):
    zona = tk.Frame(
        contenido,
        bg=FONDO
    )
    zona.pack(
        fill="x",
        padx=42,
        pady=(5, 18)
    )

    boton_redondeado(
        zona,
        "CALCULAR",
        color,
        calcular,
        155,
        42
    ).pack(side="left", padx=(0, 10))

    boton_redondeado(
        zona,
        "VOLVER AL INICIO",
        VINO,
        mostrar_menu,
        165,
        42
    ).pack(side="left")


def mostrar_interes_simple():
    actualizar_navegacion("Interés simple")
    limpiar()
    titulo_pagina(
        "Interés Simple",
        "Seleccione una fórmula y complete las variables de la operación."
    )

    operaciones = {
        "Interés (I = P r t)": {
            "campos": [("P", "Capital inicial (P)"), ("r", "Tasa por período (%)"), ("t", "Tiempo (t)")],
            "calcular": lambda v: ("Interés (I)", calcular_interes_simple(v["P"], v["r"], v["t"])[0], v["P"], calcular_interes_simple(v["P"], v["r"], v["t"])[1], v["t"]),
        },
        "Monto (F = P + I)": {
            "campos": [("P", "Capital inicial (P)"), ("I", "Interés ganado (I)"), ("t", "Tiempo (t)")],
            "calcular": lambda v: ("Monto (F)", calcular_monto_desde_interes(v["P"], v["I"]), v["P"], calcular_monto_desde_interes(v["P"], v["I"]), v["t"]),
        },
        "Monto (F = P(1 + r t))": {
            "campos": [("P", "Capital inicial (P)"), ("r", "Tasa por período (%)"), ("t", "Tiempo (t)")],
            "calcular": lambda v: ("Monto (F)", calcular_monto(v["P"], v["r"], v["t"]), v["P"], calcular_monto(v["P"], v["r"], v["t"]), v["t"]),
        },
        "Valor presente (P = F / (1 + r t))": {
            "campos": [("F", "Monto total (F)"), ("r", "Tasa por período (%)"), ("t", "Tiempo (t)")],
            "calcular": lambda v: ("Valor presente (P)", calcular_valor_presente(v["F"], v["r"], v["t"]), calcular_valor_presente(v["F"], v["r"], v["t"]), v["F"], v["t"]),
        },
        "Tasa (r = (F - P) / (P t))": {
            "campos": [("F", "Monto total (F)"), ("P", "Capital inicial (P)"), ("t", "Tiempo (t)")],
            "calcular": lambda v: ("Tasa por período (r)", calcular_tasa(v["F"], v["P"], v["t"]), v["P"], v["F"], v["t"]),
        },
        "Tiempo (t = (F - P) / (P r))": {
            "campos": [("F", "Monto total (F)"), ("P", "Capital inicial (P)"), ("r", "Tasa por período (%)")],
            "calcular": lambda v: ("Tiempo (t)", calcular_tiempo(v["F"], v["P"], v["r"]), v["P"], v["F"], calcular_tiempo(v["F"], v["P"], v["r"])),
        },
        "Descuento simple (D = F d t)": {
            "campos": [("F", "Monto nominal (F)"), ("d", "Tasa de descuento (%)"), ("t", "Tiempo (t)")],
            "calcular": lambda v: ("Descuento (D)", calcular_descuento_simple(v["F"], v["d"], v["t"]), calcular_valor_actual(v["F"], v["d"], v["t"]), v["F"], v["t"]),
        },
        "Valor actual (P = F(1 - d t))": {
            "campos": [("F", "Monto nominal (F)"), ("d", "Tasa de descuento (%)"), ("t", "Tiempo (t)")],
            "calcular": lambda v: ("Valor actual (P)", calcular_valor_actual(v["F"], v["d"], v["t"]), calcular_valor_actual(v["F"], v["d"], v["t"]), v["F"], v["t"]),
        },
        "Tasa de descuento (d = r / (1 + r t))": {
            "campos": [("r", "Tasa de interés (%)"), ("t", "Tiempo (t)")],
            "calcular": lambda v: ("Tasa de descuento (d)", calcular_tasa_descuento(v["r"], v["t"]), None, None, None),
        },
    }

    descripciones = {
        "Interés (I = P r t)": "Obtenga el interés generado a partir del capital, la tasa y el tiempo.",
        "Monto (F = P + I)": "Sume el capital inicial y el interés ganado para encontrar el monto.",
        "Monto (F = P(1 + r t))": "Calcule directamente el monto acumulado con interés simple.",
        "Valor presente (P = F / (1 + r t))": "Descuente un monto futuro para encontrar su equivalente actual.",
        "Tasa (r = (F - P) / (P t))": "Determine la tasa por período conociendo el capital, el monto y el tiempo.",
        "Tiempo (t = (F - P) / (P r))": "Encuentre cuántos períodos necesita la operación para alcanzar el monto.",
        "Descuento simple (D = F d t)": "Calcule el descuento aplicado a un monto nominal.",
        "Valor actual (P = F(1 - d t))": "Obtenga el valor actual usando una tasa de descuento simple.",
        "Tasa de descuento (d = r / (1 + r t))": "Convierta una tasa de interés simple en su tasa de descuento equivalente.",
    }

    tarjeta = tk.Frame(contenido, bg=BLANCO, highlightthickness=1, highlightbackground=BORDE)
    tarjeta.pack(fill="x", padx=42, pady=20)
    tk.Frame(tarjeta, bg=VERDE_CLARO, height=8).pack(fill="x")
    cabecera_operacion = tk.Frame(tarjeta, bg=VERDE)
    cabecera_operacion.pack(fill="x", padx=20, pady=(18, 0))
    tk.Label(
        cabecera_operacion,
        text="INTERÉS SIMPLE",
        font=("Segoe UI", 9, "bold"),
        bg=DORADO,
        fg=BLANCO,
        padx=10,
        pady=5,
    ).pack(side="left", padx=(14, 12), pady=12)
    tk.Label(
        cabecera_operacion,
        text="Laboratorio de fórmulas",
        font=("Segoe UI", 13, "bold"),
        bg=VERDE,
        fg=BLANCO,
    ).pack(side="left", pady=12)
    guia_simple = tk.Frame(tarjeta, bg="#F4F8F6")
    guia_simple.pack(fill="x", padx=30, pady=(16, 4))
    tk.Label(
        guia_simple,
        text="CÓMO ELEGIR LA FÓRMULA",
        font=("Segoe UI", 8, "bold"),
        bg="#F4F8F6",
        fg=VERDE,
    ).pack(anchor="w", padx=14, pady=(11, 7))
    pasos_simple = tk.Frame(guia_simple, bg="#F4F8F6")
    pasos_simple.pack(fill="x", padx=10, pady=(0, 11))
    for columna, numero, titulo, detalle in (
        (0, "01", "Identifique la incógnita", "I, F, P, r, t, D o d"),
        (1, "02", "Elija la ecuación", "La incógnita debe quedar despejada"),
    ):
        paso = tk.Frame(pasos_simple, bg=BLANCO, highlightthickness=1, highlightbackground=BORDE)
        paso.grid(row=0, column=columna, sticky="ew", padx=(0, 8 if columna == 0 else 0))
        pasos_simple.columnconfigure(columna, weight=1)
        tk.Label(paso, text=numero, font=("Segoe UI", 8, "bold"), bg=DORADO, fg=BLANCO, padx=7, pady=4).pack(side="left", padx=10, pady=8)
        texto_paso = tk.Frame(paso, bg=BLANCO)
        texto_paso.pack(side="left", anchor="w", pady=6)
        tk.Label(texto_paso, text=titulo, font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=NEGRO).pack(anchor="w")
        tk.Label(texto_paso, text=detalle, font=("Segoe UI", 8), bg=BLANCO, fg=GRIS).pack(anchor="w")
    estilo = ttk.Style(tarjeta)
    estilo.theme_use("clam")
    estilo.configure(
        "Simple.TCombobox",
        fieldbackground=CAMPO,
        background=CAMPO,
        foreground=NEGRO,
        bordercolor=BORDE,
        lightcolor=BORDE,
        darkcolor=BORDE,
        arrowcolor=VERDE_CLARO,
        padding=10,
        font=("Segoe UI", 10),
    )
    estilo.map(
        "Simple.TCombobox",
        fieldbackground=[("readonly", CAMPO)],
        selectbackground=[("readonly", CAMPO)],
        selectforeground=[("readonly", NEGRO)],
        bordercolor=[("focus", VERDE_CLARO)],
    )

    tk.Label(
        tarjeta,
        text="ELIJA EL MODELO QUE DESEA RESOLVER",
        font=("Segoe UI", 9, "bold"),
        bg=BLANCO,
        fg=GRIS,
    ).pack(anchor="w", padx=30, pady=(22, 4))
    seleccion = tk.StringVar(value=next(iter(operaciones)))
    selector = ttk.Combobox(
        tarjeta,
        textvariable=seleccion,
        values=list(operaciones),
        state="readonly",
        style="Simple.TCombobox",
    )
    selector.pack(fill="x", padx=30, ipady=2)
    detalle = tk.Frame(tarjeta, bg="#EAF6F2")
    detalle.pack(fill="x", padx=30, pady=(14, 4))
    formula_activa = tk.Label(
        detalle,
        text="",
        font=("Segoe UI", 11, "bold"),
        bg="#EAF6F2",
        fg=VERDE,
    )
    formula_activa.pack(anchor="w", padx=14, pady=(10, 2))
    tk.Label(
        detalle,
        text="SE USA PARA",
        font=("Segoe UI", 8, "bold"),
        bg="#EAF6F2",
        fg=VERDE,
    ).pack(anchor="w", padx=14, pady=(4, 0))
    descripcion_activa = tk.Label(
        detalle,
        text="",
        font=("Segoe UI", 9),
        bg="#EAF6F2",
        fg=GRIS,
        justify="left",
        wraplength=900,
    )
    descripcion_activa.pack(anchor="w", padx=14, pady=(0, 10))
    tk.Label(tarjeta, text="DATOS DE LA OPERACIÓN", font=("Segoe UI", 8, "bold"), bg=BLANCO, fg=GRIS).pack(anchor="w", padx=30)
    campos_frame = tk.Frame(tarjeta, bg=BLANCO)
    campos_frame.pack(fill="x", padx=30, pady=12)
    campos_frame.columnconfigure(0, weight=1)
    campos_frame.columnconfigure(1, weight=1)
    entradas = {}
    resultado = tk.Label(tarjeta, text="Complete los datos y presione CALCULAR.", font=("Segoe UI", 12, "bold"), bg=BLANCO, fg=VERDE_CLARO, justify="left")
    resultado.pack(anchor="w", padx=30, pady=(4, 22))

    def cargar_campos(_evento=None):
        for widget in campos_frame.winfo_children():
            widget.destroy()
        entradas.clear()
        formula_activa.config(text=seleccion.get())
        descripcion_activa.config(text=descripciones[seleccion.get()])
        for indice, (nombre, etiqueta) in enumerate(operaciones[seleccion.get()]["campos"]):
            bloque = tk.Frame(campos_frame, bg=BLANCO)
            columna = indice % 2
            fila = indice // 2
            bloque.grid(row=fila, column=columna, sticky="ew", padx=(0 if columna == 0 else 8, 8 if columna == 0 else 0), pady=6)
            tk.Label(bloque, text=etiqueta, font=("Segoe UI", 10, "bold"), bg=BLANCO, fg=NEGRO).pack(anchor="w", pady=(0, 5))
            entrada = tk.Entry(bloque, font=("Segoe UI", 11), bg=CAMPO, fg=NEGRO, insertbackground=VERDE, relief="flat", bd=0)
            entrada.pack(fill="x", padx=12, pady=8)
            entradas[nombre] = entrada

    def calcular():
        try:
            valores = {}
            for nombre in entradas:
                valores[nombre] = leer_numero(entradas[nombre])
                if nombre in ("r", "d"):
                    valores[nombre] /= 100
            if any(valor <= 0 for valor in valores.values()):
                raise ValueError
            nombre_resultado, valor, capital, futuro, periodos = operaciones[seleccion.get()]["calcular"](valores)
            if nombre_resultado == "Tasa por período (r)" or nombre_resultado == "Tasa de descuento (d)":
                texto = f"{nombre_resultado}: {valor * 100:,.4f}%"
            else:
                texto = f"{nombre_resultado}: ${valor:,.2f}"
            resultado.config(text=texto)
            if capital is not None and futuro is not None:
                if float(periodos).is_integer():
                    mostrar_grafica(
                        grafica_interes_simple(
                            capital,
                            futuro,
                            int(periodos),
                        )
                    )
                else:
                    resultado.config(
                        text=(
                            f"{texto}\n"
                            "La línea de tiempo requiere períodos enteros."
                        )
                    )
        except (ValueError, ZeroDivisionError):
            messagebox.showerror("Datos inválidos", "Ingrese valores positivos y numéricos válidos.")

    selector.bind("<<ComboboxSelected>>", cargar_campos)
    cargar_campos()
    botones_formulario(VERDE_CLARO, calcular)


def mostrar_interes_compuesto():
    actualizar_navegacion("Interés compuesto")
    limpiar()
    mostrar_interes_compuesto_ui(contenido)

def mostrar_gradiente_aritmetico():
    actualizar_navegacion("Gradiente aritmético")
    limpiar()
    mostrar_gradiente_aritmetico_ui(contenido)
    return
    


def mostrar_gradiente_geometrico():
    actualizar_navegacion("Gradiente geométrico")
    limpiar()
    titulo_pagina(
        "Gradiente Geométrico",
        "Analice series de pagos que crecen por una razón porcentual constante."
    )

    operaciones = {
        "P = K[((1+g)^n - (1+i)^n) / ((g-i)(1+i)^n)]": {
            "campos": [("pago", "Pago inicial K"), ("tasa", "Tasa de interés i (%)"), ("crecimiento", "Razón geométrica g (%)"), ("periodos", "Número de períodos n")],
            "calcular": lambda v: ("Valor presente (P)", calcular_presente_gradiente_geometrico(v["pago"], v["tasa"], v["crecimiento"], v["periodos"]), v),
        },
        "P = Kn / (1+i)  si g = i": {
            "campos": [("pago", "Pago inicial K"), ("tasa", "Tasa de interés i (%)"), ("periodos", "Número de períodos n")],
            "calcular": lambda v: ("Valor presente (P)", calcular_presente_gradiente_geometrico_igual(v["pago"], v["tasa"], v["periodos"]), v),
        },
        "F = K[((1+g)^n - (1+i)^n) / (g-i)]": {
            "campos": [("pago", "Pago inicial K"), ("tasa", "Tasa de interés i (%)"), ("crecimiento", "Razón geométrica g (%)"), ("periodos", "Número de períodos n")],
            "calcular": lambda v: ("Valor futuro (F)", calcular_futuro_gradiente_geometrico(v["pago"], v["tasa"], v["crecimiento"], v["periodos"]), v),
        },
        "F = Kn(1+i)^(n-1)  si g = i": {
            "campos": [("pago", "Pago inicial K"), ("tasa", "Tasa de interés i (%)"), ("periodos", "Número de períodos n")],
            "calcular": lambda v: ("Valor futuro (F)", calcular_futuro_gradiente_geometrico_igual(v["pago"], v["tasa"], v["periodos"]), v),
        },
    }
    descripciones = {
        "P = K[((1+g)^n - (1+i)^n) / ((g-i)(1+i)^n)]": "Se usa para encontrar el valor presente de pagos que crecen por una razón g cuando g e i son diferentes.",
        "P = Kn / (1+i)  si g = i": "Se usa para encontrar el valor presente cuando los pagos crecen exactamente al mismo ritmo que la tasa de interés.",
        "F = K[((1+g)^n - (1+i)^n) / (g-i)]": "Se usa para encontrar el valor futuro acumulado de un gradiente geométrico cuando g e i son diferentes.",
        "F = Kn(1+i)^(n-1)  si g = i": "Se usa para encontrar el valor futuro cuando el crecimiento de los pagos coincide con la tasa de interés.",
    }

    tarjeta = tk.Frame(contenido, bg=BLANCO, highlightthickness=1, highlightbackground=BORDE)
    tarjeta.pack(fill="x", padx=42, pady=20)
    tk.Frame(tarjeta, bg=VINO, height=8).pack(fill="x")
    cabecera = tk.Frame(tarjeta, bg=VERDE)
    cabecera.pack(fill="x", padx=20, pady=(18, 0))
    tk.Label(cabecera, text="GRADIENTE GEOMÉTRICO", font=("Segoe UI", 8, "bold"), bg=DORADO, fg=BLANCO, padx=10, pady=5).pack(side="left", padx=(14, 12), pady=12)
    tk.Label(cabecera, text="Laboratorio de gradientes", font=("Segoe UI", 13, "bold"), bg=VERDE, fg=BLANCO).pack(side="left", pady=12)
    guia = tk.Frame(tarjeta, bg="#F4F8F6")
    guia.pack(fill="x", padx=30, pady=(16, 4))
    tk.Label(
        guia,
        text="CÓMO ELEGIR",
        font=("Segoe UI", 8, "bold"),
        bg="#F4F8F6",
        fg=VINO,
    ).pack(anchor="w", padx=14, pady=(11, 7))
    pasos = tk.Frame(guia, bg="#F4F8F6")
    pasos.pack(fill="x", padx=10, pady=(0, 11))
    for columna, numero, titulo, detalle in (
        (0, "01", "Resultado", "P = hoy  |  F = final"),
        (1, "02", "Relación de tasas", "g = i  |  g != i"),
    ):
        paso = tk.Frame(pasos, bg=BLANCO, highlightthickness=1, highlightbackground=BORDE)
        paso.grid(row=0, column=columna, sticky="ew", padx=(0, 8 if columna == 0 else 0))
        pasos.columnconfigure(columna, weight=1)
        tk.Label(paso, text=numero, font=("Segoe UI", 8, "bold"), bg=DORADO, fg=BLANCO, padx=7, pady=4).pack(side="left", padx=10, pady=8)
        texto_paso = tk.Frame(paso, bg=BLANCO)
        texto_paso.pack(side="left", anchor="w", pady=6)
        tk.Label(texto_paso, text=titulo, font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=NEGRO).pack(anchor="w")
        tk.Label(texto_paso, text=detalle, font=("Segoe UI", 8), bg=BLANCO, fg=GRIS).pack(anchor="w")
    tk.Label(tarjeta, text="ELIJA LA FÓRMULA", font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=GRIS).pack(anchor="w", padx=30, pady=(22, 4))
    seleccion = tk.StringVar(value=next(iter(operaciones)))
    selector = ttk.Combobox(tarjeta, textvariable=seleccion, values=list(operaciones), state="readonly", font=("Segoe UI", 10))
    selector.pack(fill="x", padx=30, ipady=2)
    detalle = tk.Frame(tarjeta, bg="#EAF6F2")
    detalle.pack(fill="x", padx=30, pady=(14, 4))
    formula_activa = tk.Label(detalle, text="", font=("Segoe UI", 11, "bold"), bg="#EAF6F2", fg=VINO)
    formula_activa.pack(anchor="w", padx=14, pady=(10, 2))
    tk.Label(
        detalle,
        text="SE USA PARA",
        font=("Segoe UI", 8, "bold"),
        bg="#EAF6F2",
        fg=VINO,
    ).pack(anchor="w", padx=14, pady=(4, 0))
    descripcion = tk.Label(detalle, text="", font=("Segoe UI", 9), bg="#EAF6F2", fg=GRIS, wraplength=900, justify="left")
    descripcion.pack(anchor="w", padx=14, pady=(0, 10))
    campos_frame = tk.Frame(tarjeta, bg=BLANCO)
    campos_frame.pack(fill="x", padx=30, pady=12)
    entradas = {}
    resultado = tk.Label(tarjeta, text="Complete los datos y presione CALCULAR.", font=("Segoe UI", 12, "bold"), bg=BLANCO, fg=VINO, justify="left")
    resultado.pack(anchor="w", padx=30, pady=(4, 22))

    def cargar_campos(_evento=None):
        for widget in campos_frame.winfo_children():
            widget.destroy()
        entradas.clear()
        formula_activa.config(text=seleccion.get())
        descripcion.config(text=descripciones[seleccion.get()])
        for indice, (nombre, etiqueta) in enumerate(operaciones[seleccion.get()]["campos"]):
            bloque = tk.Frame(campos_frame, bg=BLANCO)
            bloque.grid(row=indice // 2, column=indice % 2, sticky="ew", padx=8, pady=6)
            campos_frame.columnconfigure(indice % 2, weight=1)
            tk.Label(bloque, text=etiqueta, font=("Segoe UI", 10, "bold"), bg=BLANCO, fg=NEGRO).pack(anchor="w", pady=(0, 5))
            entrada = tk.Entry(bloque, font=("Segoe UI", 11), bg=CAMPO, fg=NEGRO, insertbackground=VINO, relief="flat", bd=0)
            entrada.pack(fill="x", padx=12, pady=8)
            entradas[nombre] = entrada

    def calcular():
        try:
            valores = {nombre: leer_numero(entrada) for nombre, entrada in entradas.items()}
            for nombre in ("tasa", "crecimiento"):
                if nombre in valores:
                    valores[nombre] /= 100
            valores["periodos"] = int(valores["periodos"])
            nombre_resultado, valor, datos = operaciones[seleccion.get()]["calcular"](valores)
            resultado.config(text=f"{nombre_resultado}: ${valor:,.2f}")
            presente, flujos = calcular_gradiente_geometrico(
                datos["pago"],
                datos["tasa"],
                datos.get("crecimiento", datos["tasa"]),
                datos["periodos"],
            )
            mostrar_grafica(grafica_gradiente_geometrico(flujos, presente))
        except (ValueError, ZeroDivisionError):
            messagebox.showerror("Datos inválidos", "Ingrese valores numéricos válidos.")

    selector.bind("<<ComboboxSelected>>", cargar_campos)
    cargar_campos()
    botones_formulario(VINO, calcular)


if __name__ == "__main__":
    crear_ventana()
    ventana.mainloop()
