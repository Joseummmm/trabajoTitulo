import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Cargar datos
data = pd.read_csv("./TiemposEjecucion/total_times.csv")
output_folder = "./GraficosTiempo"
os.makedirs(output_folder, exist_ok=True)

data = data[(data["metaheuristic"].isin(["AOA", "GWO"])) & (data["total_time"] >= 1)]


def setup_limited_yticks(ax, data, column, max_ticks=10):
    """Configura el eje Y para mostrar una cantidad limitada de valores."""
    min_value = int(np.floor(data[column].min()))
    max_value = int(np.ceil(data[column].max()))
    step = max(1, (max_value - min_value) // max_ticks)
    ax.set_yticks(np.arange(min_value, max_value + 1, step))


def create_plot(
    data, instance, output_folder, plot_func, title, y_label, filename_suffix
):
    """Genera y guarda un gráfico específico basado en la función de trazado proporcionada."""
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    plot_func(data, ax)
    setup_limited_yticks(
        ax, data, "total_time"
    )  # Limitar la cantidad de ticks en el eje Y
    plt.title(f"{title}: AOA vs GWO - {instance}")
    plt.xlabel("Metaheurística")
    plt.ylabel(y_label)
    plt.tight_layout()

    # Crear subcarpetas jerarquizadas
    plot_folder = os.path.join(output_folder, instance, filename_suffix)
    os.makedirs(plot_folder, exist_ok=True)

    # Guardar el gráfico en la subcarpeta correspondiente
    plt.savefig(os.path.join(plot_folder, f"{filename_suffix}_{instance}.png"))
    plt.close()


# Funciones específicas de cada tipo de gráfico
def violin_plot(data, ax):
    sns.violinplot(data=data, x="metaheuristic", y="total_time", inner="quartile")


def box_plot(data, ax):
    sns.boxplot(data=data, x="metaheuristic", y="total_time")


def strip_plot(data, ax):
    sns.boxplot(data=data, x="metaheuristic", y="total_time", color="white")
    sns.stripplot(data=data, x="metaheuristic", y="total_time", color="0.3", alpha=0.5)


def ecdf_plot(data, ax):
    for algo in data["metaheuristic"].unique():
        sorted_data = np.sort(data[data["metaheuristic"] == algo]["total_time"])
        ecdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        ax.step(sorted_data, ecdf, label=algo)
    ax.legend()


def kde_plot(data, ax):
    for algo in data["metaheuristic"].unique():
        sns.kdeplot(data=data[data["metaheuristic"] == algo]["total_time"], label=algo)
    ax.legend()


def histogram_plot(data, ax):
    for algo in data["metaheuristic"].unique():
        ax.hist(
            data[data["metaheuristic"] == algo]["total_time"],
            alpha=0.5,
            density=True,
            label=algo,
        )
    ax.legend()


def error_bar_plot(data, ax):
    stats = data.groupby("metaheuristic")["total_time"].agg(["mean", "std"])
    ax.errorbar(stats.index, stats["mean"], yerr=stats["std"], fmt="o", capsize=5)


def violin_points_plot(data, ax):
    sns.violinplot(data=data, x="metaheuristic", y="total_time", color="0.8")
    sns.stripplot(
        data=data,
        x="metaheuristic",
        y="total_time",
        color="0.3",
        alpha=0.5,
        jitter=0.2,
        size=4,
    )


def swarm_plot(data, ax):
    sns.swarmplot(data=data, x="metaheuristic", y="total_time")


# Generación de gráficos
def generate_plots_for_instance(data, instance, output_folder):
    plot_funcs = [
        (violin_plot, "Gráfico de Violín", "Tiempo Total (Segundos)", "violin_plot"),
        (box_plot, "Gráfico de Caja", "Tiempo Total (Segundos)", "box_plot"),
        (
            strip_plot,
            "Gráfico de Puntos y Caja",
            "Tiempo Total (Segundos)",
            "strip_box_plot",
        ),
        (
            ecdf_plot,
            "Función de Distribución Acumulada",
            "Proporción Acumulada",
            "ecdf_plot",
        ),
        (kde_plot, "Gráfico de Densidad (KDE)", "Densidad", "kde_plot"),
        (histogram_plot, "Histograma", "Frecuencia Relativa", "histogram_plot"),
        (
            error_bar_plot,
            "Gráfico de Barras de Error",
            "Tiempo Total (Segundos) (Media ± Desv. Est.)",
            "error_bar_plot",
        ),
        (
            violin_points_plot,
            "Gráfico de Violín con Puntos",
            "Tiempo Total (Segundos)",
            "violin_points_plot",
        ),
        (swarm_plot, "Gráfico de Enjambre", "Tiempo Total (Segundos)", "swarm_plot"),
    ]
    for plot_func, title, y_label, filename_suffix in plot_funcs:
        create_plot(
            data, instance, output_folder, plot_func, title, y_label, filename_suffix
        )


# Generar gráficos para cada instancia
for instance in data["instance"].unique():
    instance_data = data[data["instance"] == instance]
    generate_plots_for_instance(instance_data, instance, output_folder)

print("Gráficos de tiempo generados y guardados en la carpeta:", output_folder)
