import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modulos.interes_simple import calcular_interes_simple
from modulos.interes_compuesto import calcular_futuro
from modulos.gradiente_geometrico import calcular_gradiente_geometrico
from interfaz.interes_compuesto_ui import mostrar_interes_compuesto_ui
from interfaz.gradiente_aritmetico_ui import mostrar_gradiente_aritmetico_ui

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
    entradas = crear_formulario(
        "Interés Simple",
        "Cálculo del interés generado y del valor futuro.",
        VERDE_CLARO,
        [
            ("capital", "Capital"),
            ("tasa", "Tasa de interés (%)"),
            ("periodos", "Número de períodos")
        ]
    )

    resultado = panel_resultado(VERDE_CLARO)

    def calcular():
        try:
            capital = leer_numero(entradas["capital"])
            tasa = leer_numero(entradas["tasa"]) / 100
            periodos = int(entradas["periodos"].get())

            if capital <= 0 or tasa < 0 or periodos <= 0:
                raise ValueError

            interes, futuro = calcular_interes_simple(
                capital,
                tasa,
                periodos
            )

            resultado.config(
                text=(
                    f"Interés generado: ${interes:,.2f}\n"
                    f"Valor futuro: ${futuro:,.2f}"
                )
            )

            fig = grafica_interes_simple(
                capital,
                futuro,
                periodos
            )
            mostrar_grafica(fig)

        except ValueError:
            messagebox.showerror(
                "Datos inválidos",
                "Ingrese valores numéricos válidos."
            )

    botones_formulario(
        VERDE_CLARO,
        calcular
    )


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
    entradas = crear_formulario(
        "Gradiente Geométrico",
        "Cálculo del valor presente de una serie con crecimiento porcentual.",
        VINO,
        [
            ("pago", "Pago inicial"),
            ("tasa", "Tasa de interés (%)"),
            ("crecimiento", "Crecimiento (%)"),
            ("periodos", "Número de períodos")
        ]
    )

    resultado = panel_resultado(VINO)

    def calcular():
        try:
            pago = leer_numero(entradas["pago"])
            tasa = leer_numero(entradas["tasa"]) / 100
            crecimiento = leer_numero(entradas["crecimiento"]) / 100
            periodos = int(entradas["periodos"].get())

            if (
                pago <= 0
                or tasa < 0
                or crecimiento < 0
                or periodos <= 0
            ):
                raise ValueError

            presente, flujos = calcular_gradiente_geometrico(
                pago,
                tasa,
                crecimiento,
                periodos
            )

            fig = grafica_gradiente_geometrico(
                flujos,
                presente
            )
            mostrar_grafica(fig)

        except (ValueError, ZeroDivisionError):
            messagebox.showerror(
                "Datos inválidos",
                "Ingrese valores numéricos válidos."
            )

    botones_formulario(
        VINO,
        calcular
    )


if __name__ == "__main__":
    crear_ventana()
    ventana.mainloop()
