import pandas as pd
import os
from datetime import datetime

def analyze_times():
    # Directorios
    input_dir = './TiemposEjecucion/'
    output_dir = './AnalisisTiempos/'
    
    # Crear directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Análisis de tiempos por iteración
        iter_df = pd.read_csv(os.path.join(input_dir, 'iteration_times.csv'))
        iter_grouped = iter_df.groupby(['metaheuristic', 'instance'])
        
        iter_stats = iter_grouped['iteration_time'].agg([
            ('mean_iter_time', 'mean'),
            ('median_iter_time', 'median'),
            ('min_iter_time', 'min'),
            ('max_iter_time', 'max'),
            ('std_iter_time', 'std'),
            ('total_iterations', 'count')
        ]).round(3)
        
        # Análisis de fitness por iteración
        fitness_stats = iter_grouped['best_fitness'].agg([
            ('best_fitness', 'min'),
            ('mean_fitness', 'mean'),
            ('std_fitness', 'std')
        ]).round(3)
        
        # Combinar estadísticas de iteraciones
        iter_stats = pd.concat([iter_stats, fitness_stats], axis=1)
        
        # Análisis de tiempos totales
        total_df = pd.read_csv(os.path.join(input_dir, 'total_times.csv'))
        total_grouped = total_df.groupby(['metaheuristic', 'instance'])
        
        total_stats = total_grouped.agg({
            'total_time': ['mean', 'median', 'min', 'max', 'std', 'count'],
            'final_fitness': ['min', 'mean', 'std'],
            'population': 'mean',
            'max_iterations': 'mean'
        }).round(3)
        
        # Renombrar columnas para más claridad
        total_stats.columns = [
            'mean_total_time', 'median_total_time', 'min_total_time', 
            'max_total_time', 'std_total_time', 'num_executions',
            'best_final_fitness', 'mean_final_fitness', 'std_final_fitness',
            'avg_population', 'avg_max_iterations'
        ]
        
        # Agregar timestamp al nombre de los archivos
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Guardar resultados
        iter_stats.to_csv(os.path.join(output_dir, f'iteration_analysis_{timestamp}.csv'))
        total_stats.to_csv(os.path.join(output_dir, f'total_analysis_{timestamp}.csv'))
        
        print("Análisis completado. Resultados guardados en:")
        print(f"- Análisis por iteración: iteration_analysis_{timestamp}.csv")
        print(f"- Análisis de tiempos totales: total_analysis_{timestamp}.csv")
        
        print("\nResumen de estadísticas por iteración:")
        print(iter_stats)
        print("\nResumen de estadísticas totales:")
        print(total_stats)
        
    except FileNotFoundError as e:
        print(f"Error: No se encontró alguno de los archivos de tiempos en {input_dir}")
        print(f"Detalle del error: {str(e)}")
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")

if __name__ == "__main__":
    analyze_times()