import matplotlib.pyplot as plt


def _estilo_grafica(ax):
    ax.set_facecolor("#F8FBF9")
    ax.grid(True, axis="x", color="#D5E2DD", linestyle="--", linewidth=0.8, alpha=0.8)
    ax.grid(True, axis="y", color="#E9F1EE", linestyle="-", linewidth=0.5, alpha=0.6)
    for spine in ax.spines.values():
        spine.set_color("#BFCFC8")
        spine.set_linewidth(1)
    ax.tick_params(axis="both", colors="#3B4F4A", labelsize=8)


def _flecha_flujo(ax, periodo, destino, etiqueta, tipo, color, posicion_texto):
    ax.annotate(
        "",
        xy=(periodo, destino),
        xytext=(periodo, 0),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            linewidth=2.2,
            mutation_scale=16,
            shrinkA=0,
            shrinkB=0,
        ),
        zorder=4,
    )
    ax.text(
        periodo,
        posicion_texto,
        f"{tipo}\n{etiqueta}",
        ha="center",
        va="center",
        fontsize=9,
        color=color,
        bbox=dict(
            boxstyle="round,pad=0.28",
            facecolor="#FFFFFF",
            edgecolor=color,
            linewidth=1,
        ),
        zorder=5,
    )


def grafica_interes_simple(capital, valor_futuro, periodos):
    fig, ax = plt.subplots(figsize=(12.5, 4.6), facecolor="#F3F7F5")
    _estilo_grafica(ax)

    ax.plot([0, periodos], [0, 0], color="#173A31", linewidth=2.2, zorder=2)

    for p in range(periodos + 1):
        ax.text(p, -0.14, f"P{p}", ha="center", va="top", fontsize=8, color="#173A31")

    _flecha_flujo(ax, 0, -0.52, f"${capital:,.2f}", "EGRESO", "#A67C18", -0.72)
    _flecha_flujo(ax, periodos, 0.52, f"${valor_futuro:,.2f}", "INGRESO", "#0B5D4B", 0.72)

    for p in range(1, periodos):
        ax.text(
            p,
            0.15,
            "SIN FLUJO",
            ha="center",
            va="bottom",
            fontsize=7,
            color="#9AAEA7",
        )

    ax.text(0, 0.13, "Hoy", ha="center", va="bottom", fontsize=8, color="#60766E")
    ax.text(periodos, 0.13, f"Período {periodos}", ha="center", va="bottom", fontsize=8, color="#60766E")
    ax.set_xlim(-0.55, periodos + 0.55)
    ax.set_ylim(-0.9, 0.9)
    ax.set_yticks([])
    ax.set_xticks(range(periodos + 1))
    ax.set_xlabel("Tiempo", fontsize=9, color="#2B4B45", labelpad=8)
    ax.set_title("Diagrama de flujo de caja - Interés simple", fontsize=11, color="#173A31", pad=12)
    ax.text(
        0.5,
        0.98,
        "Convención: egreso ↓  |  ingreso ↑",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8,
        color="#60766E",
    )

    fig.tight_layout()
    return fig


def grafica_interes_compuesto(capital, valor_futuro, periodos):
    fig, ax = plt.subplots(figsize=(12.5, 4.6), facecolor="#F3F7F5")
    _estilo_grafica(ax)

    ax.plot([0, periodos], [0, 0], color="#173A31", linewidth=2.2, zorder=2)

    for periodo in range(periodos + 1):
        ax.text(
            periodo,
            -0.14,
            f"P{periodo}",
            ha="center",
            va="top",
            fontsize=8,
            color="#173A31",
        )

    _flecha_flujo(ax, 0, -0.52, f"${capital:,.2f}", "EGRESO", "#A67C18", -0.72)
    _flecha_flujo(ax, periodos, 0.52, f"${valor_futuro:,.2f}", "INGRESO", "#0B5D4B", 0.72)

    for periodo in range(1, periodos):
        ax.text(
            periodo,
            0.15,
            "SIN FLUJO",
            ha="center",
            va="bottom",
            fontsize=7,
            color="#9AAEA7",
        )

    ax.text(0, 0.13, "Hoy", ha="center", va="bottom", fontsize=8, color="#60766E")
    ax.text(periodos, 0.13, f"Período {periodos}", ha="center", va="bottom", fontsize=8, color="#60766E")
    ax.set_xlim(-0.55, periodos + 0.55)
    ax.set_ylim(-0.9, 0.9)
    ax.set_yticks([])
    ax.set_xticks(range(periodos + 1))
    ax.set_xlabel("Tiempo", fontsize=9, color="#2B4B45", labelpad=8)
    ax.set_title("Diagrama de flujo de caja - Interés compuesto", fontsize=11, color="#173A31", pad=12)
    ax.text(
        0.5,
        0.98,
        "Convención: egreso ↓  |  ingreso ↑  |  capitalización sin flujo",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8,
        color="#60766E",
    )

    fig.tight_layout()
    return fig


def grafica_gradiente_aritmetico(pago, gradiente, periodos):
    fig, ax = plt.subplots(figsize=(12.5, 4.6), facecolor="#F3F7F5")
    _estilo_grafica(ax)

    ax.plot([0, periodos], [0, 0], color="#173A31", linewidth=2.2, zorder=2)
    ax.text(0, 0.13, "Hoy", ha="center", va="bottom", fontsize=8, color="#60766E")
    ax.text(
        0,
        0.72,
        "VP equivalente se muestra en el resultado",
        ha="center",
        va="center",
        fontsize=8,
        color="#A67C18",
    )

    for periodo in range(1, periodos + 1):
        flujo = pago + gradiente * (periodo - 1)
        ax.text(periodo, -0.14, f"P{periodo}", ha="center", va="top", fontsize=8, color="#173A31")
        _flecha_flujo(ax, periodo, -0.52, f"${flujo:,.2f}", "EGRESO", "#A67C18", -0.72)

    ax.set_xlim(-0.55, periodos + 0.55)
    ax.set_ylim(-0.9, 0.9)
    ax.set_yticks([])
    ax.set_xticks(range(periodos + 1))
    ax.set_xlabel("Tiempo", fontsize=9, color="#2B4B45", labelpad=8)
    ax.set_title("Diagrama de flujo de caja - Gradiente aritmético", fontsize=11, color="#173A31", pad=12)
    ax.text(
        0.5,
        0.98,
        "Convención: pagos/egresos ↓  |  gradiente positivo aumenta  |  gradiente negativo disminuye",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8,
        color="#60766E",
    )

    fig.tight_layout()
    return fig


def grafica_gradiente_geometrico(flujos, valor_presente=None):
    periodos = len(flujos)

    fig, ax = plt.subplots(figsize=(12.5, 4.6), facecolor="#F3F7F5")
    _estilo_grafica(ax)

    x = list(range(1, periodos + 1))
    ax.plot([0.5, periodos + 0.5], [0, 0], color="#173A31", linewidth=2.2, zorder=2)

    for periodo, flujo in zip(x, flujos):
        ax.text(periodo, -0.14, f"P{periodo}", ha="center", va="top", fontsize=8, color="#173A31")
        _flecha_flujo(ax, periodo, -0.52, f"${flujo:,.2f}", "EGRESO", "#244F45", -0.72)

    ax.text(0.5, 0.13, "Inicio", ha="center", va="bottom", fontsize=8, color="#60766E")
    ax.text(periodos + 0.5, 0.13, "Fin", ha="center", va="bottom", fontsize=8, color="#60766E")
    if valor_presente is not None:
        ax.text(
            0.5,
            0.72,
            f"VP equivalente: ${valor_presente:,.2f}",
            ha="center",
            va="center",
            fontsize=8,
            color="#244F45",
        )
    ax.set_xlim(0.2, periodos + 0.8)
    ax.set_ylim(-0.9, 0.9)
    ax.set_yticks([])
    ax.set_xticks(x)
    ax.set_xlabel("Tiempo", fontsize=9, color="#2B4B45", labelpad=8)
    ax.set_title("Diagrama de flujo de caja - Gradiente geométrico", fontsize=11, color="#173A31", pad=12)
    ax.text(
        0.5,
        0.98,
        "Convención: pagos/egresos ↓  |  crecimiento según la tasa indicada",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8,
        color="#60766E",
    )

    fig.tight_layout()
    return fig
