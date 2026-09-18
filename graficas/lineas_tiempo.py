import matplotlib.pyplot as plt


def grafica_interes_simple(capital, valor_futuro, periodos):
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.axhline(0, linewidth=1)

    for periodo in range(periodos + 1):
        ax.plot(periodo, 0, "o")
        ax.text(periodo, -0.08, str(periodo), ha="center")

    ax.annotate(
        f"${capital:,.2f}",
        xy=(0, 0),
        xytext=(0, 0.25),
        ha="center",
        arrowprops=dict(arrowstyle="->")
    )

    ax.annotate(
        f"${valor_futuro:,.2f}",
        xy=(periodos, 0),
        xytext=(periodos, 0.25),
        ha="center",
        arrowprops=dict(arrowstyle="->")
    )

    ax.text(0, -0.15, "P", ha="center", fontweight="bold")
    ax.text(periodos, -0.15, "F", ha="center", fontweight="bold")

    ax.set_xlim(-1, periodos + 1)
    ax.set_ylim(-0.25, 0.4)
    ax.set_yticks([])
    ax.set_xlabel("Períodos")
    ax.set_title("Línea de Tiempo - Interés Simple")
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.show()


def grafica_gradiente_geometrico(flujos):
    periodos = len(flujos)

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.axhline(0, linewidth=1)

    for periodo, flujo in enumerate(flujos, start=1):
        ax.plot(periodo, 0, "o")

        ax.annotate(
            f"${flujo:,.2f}",
            xy=(periodo, 0),
            xytext=(periodo, 0.25),
            ha="center",
            arrowprops=dict(arrowstyle="->")
        )

        ax.text(periodo, -0.12, f"P{periodo}", ha="center")

    ax.set_xlim(0, periodos + 1)
    ax.set_ylim(-0.2, 0.4)
    ax.set_yticks([])
    ax.set_xticks(range(1, periodos + 1))
    ax.set_xlabel("Períodos")
    ax.set_title("Línea de Tiempo - Gradiente Geométrico")
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.show()