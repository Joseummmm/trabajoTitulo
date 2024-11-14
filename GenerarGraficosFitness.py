import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import re


def extract_scp_instance(filename):
    """Extrae el identificador de instancia SCP del nombre del archivo."""
    match = re.search(r"scp([a-zA-Z0-9]+)", filename)
    return match.group(1) if match else None


def read_fitness_data(folder_path):
    """Lee y organiza los datos de los archivos CSV para su visualización."""
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith("_best_fitness.csv"):
            algorithm = filename.split("_")[0]
            scp_instance = extract_scp_instance(filename)
            if scp_instance:
                df = pd.read_csv(os.path.join(folder_path, filename))
                df["Algorithm"] = algorithm
                df["SCP_Instance"] = f"SCP{scp_instance}"
                all_data.append(df[["Algorithm", "SCP_Instance", "best_fitness"]])
    return pd.concat(all_data, ignore_index=True)


def setup_limited_yticks(ax, data, column, max_ticks=10):
    """Configura el eje Y para mostrar una cantidad limitada de valores."""
    min_value = int(np.floor(data[column].min()))
    max_value = int(np.ceil(data[column].max()))
    step = max(
        1, (max_value - min_value) // max_ticks
    )  # Calcula el paso para limitar los ticks
    ax.set_yticks(np.arange(min_value, max_value + 1, step))


def create_plot(
    data, instance, output_folder, plot_func, title, y_label, filename_suffix
):
    """Genera y guarda un gráfico específico basado en la función de trazado proporcionada."""
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    plot_func(data, ax)
    setup_limited_yticks(
        ax, data, "best_fitness"
    )  # Limitar la cantidad de ticks en el eje Y
    plt.title(f"{title}: AOA vs GWO - {instance}")
    plt.xlabel("Algoritmo")
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
    sns.violinplot(data=data, x="Algorithm", y="best_fitness", inner="quartile")


def box_plot(data, ax):
    sns.boxplot(data=data, x="Algorithm", y="best_fitness")


def strip_plot(data, ax):
    sns.boxplot(data=data, x="Algorithm", y="best_fitness", color="white")
    sns.stripplot(data=data, x="Algorithm", y="best_fitness", color="0.3", alpha=0.4)


def ecdf_plot(data, ax):
    for algorithm in data["Algorithm"].unique():
        sorted_data = np.sort(data[data["Algorithm"] == algorithm]["best_fitness"])
        ecdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        ax.step(sorted_data, ecdf, label=algorithm)
    ax.legend()


def kde_plot(data, ax):
    for algorithm in data["Algorithm"].unique():
        sns.kdeplot(
            data=data[data["Algorithm"] == algorithm]["best_fitness"], label=algorithm
        )
    ax.legend()


def histogram_plot(data, ax):
    for algorithm in data["Algorithm"].unique():
        ax.hist(
            data[data["Algorithm"] == algorithm]["best_fitness"],
            alpha=0.5,
            density=True,
            label=algorithm,
        )
    ax.legend()


def error_bar_plot(data, ax):
    stats = data.groupby("Algorithm")["best_fitness"].agg(["mean", "std"])
    ax.errorbar(stats.index, stats["mean"], yerr=stats["std"], fmt="o", capsize=5)


def violin_points_plot(data, ax):
    sns.violinplot(data=data, x="Algorithm", y="best_fitness", color="0.8")
    sns.stripplot(
        data=data,
        x="Algorithm",
        y="best_fitness",
        color="0.3",
        alpha=0.4,
        jitter=0.2,
        size=4,
    )


def swarm_plot(data, ax):
    sns.swarmplot(data=data, x="Algorithm", y="best_fitness")


# Generación de gráficos
def generate_plots_for_instance(data, instance, output_folder):
    plot_funcs = [
        (violin_plot, "Gráfico de Violín", "Mejor Fitness", "violin_plot"),
        (box_plot, "Gráfico de Caja", "Mejor Fitness", "box_plot"),
        (strip_plot, "Gráfico de Puntos y Caja", "Mejor Fitness", "strip_box_plot"),
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
            "Mejor Fitness (Media ± Desv. Est.)",
            "error_bar_plot",
        ),
        (
            violin_points_plot,
            "Gráfico de Violín con Puntos",
            "Mejor Fitness",
            "violin_points_plot",
        ),
        (swarm_plot, "Gráfico de Enjambre", "Mejor Fitness", "swarm_plot"),
    ]
    for plot_func, title, y_label, filename_suffix in plot_funcs:
        create_plot(
            data, instance, output_folder, plot_func, title, y_label, filename_suffix
        )


# Función principal
def main():
    # Ruta absoluta a la carpeta de entrada y de salida
    input_folder = "./MejoresFitness"  # Carpeta donde se encuentran los archivos CSV
    output_folder = (
        "./GraficosFitness"  # Carpeta para guardar los gráficos en la raíz del proyecto
    )

    # Leer los datos
    data = read_fitness_data(input_folder)

    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Generar gráficos para cada instancia
    for instance in data["SCP_Instance"].unique():
        instance_data = data[data["SCP_Instance"] == instance]
        generate_plots_for_instance(instance_data, instance, output_folder)
    print("Gráficos generados y guardados en la carpeta:", output_folder)


# Ejecución del script
if __name__ == "__main__":
    main()
