import pandas as pd
import os
from datetime import datetime
import glob

def analyze_best_fitness():
    # Directorio de entrada y salida
    input_dir = './MejoresFitness/'
    output_dir = './AnalisisFitness/'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Obtener todos los archivos de fitness
        fitness_files = glob.glob(os.path.join(input_dir, '*_best_fitness.csv'))
        
        # Lista para almacenar resultados
        results = []
        
        for file in fitness_files:
            # Extraer metaheurística e instancia del nombre del archivo
            filename = os.path.basename(file)
            # Dividir el nombre del archivo y tomar solo las dos primeras partes
            parts = filename.split('_')
            if len(parts) >= 2:
                mh = parts[0]  # Primera parte es la metaheurística
                instance = parts[1]  # Segunda parte es la instancia
            else:
                print(f"Advertencia: Formato de nombre de archivo inesperado: {filename}")
                continue
            
            # Leer archivo
            df = pd.read_csv(file)
            
            # Calcular estadísticas
            stats = {
                'metaheuristic': mh,
                'instance': instance,
                'num_executions': len(df),
                'mean_fitness': df['best_fitness'].mean(),
                'median_fitness': df['best_fitness'].median(),
                'min_fitness': df['best_fitness'].min(),
                'max_fitness': df['best_fitness'].max(),
                'range_fitness': df['best_fitness'].max() - df['best_fitness'].min(),
                'std_fitness': df['best_fitness'].std(),
                'mean_time': df['total_time'].mean(),
                'std_time': df['total_time'].std()
            }
            
            results.append(stats)
        
        # Crear DataFrame con resultados
        results_df = pd.DataFrame(results)
        
        # Redondear valores numéricos
        numeric_columns = results_df.select_dtypes(include=['float64']).columns
        results_df[numeric_columns] = results_df[numeric_columns].round(3)
        
        # Guardar resultados con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, f'fitness_analysis_{timestamp}.csv')
        results_df.to_csv(output_file, index=False)
        
        print(f"Análisis completado. Resultados guardados en: {output_file}")
        print("\nResumen de estadísticas:")
        print(results_df.to_string())
        
        # Identificar mejores resultados por instancia
        best_results = results_df.loc[results_df.groupby('instance')['min_fitness'].idxmin()]
        
        print("\nMejores resultados por instancia:")
        for _, row in best_results.iterrows():
            print(f"Instancia: {row['instance']}")
            print(f"Mejor metaheurística: {row['metaheuristic']}")
            print(f"Mejor fitness: {row['min_fitness']}")
            print(f"Tiempo medio: {row['mean_time']}")
            print("---")
        
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")

if __name__ == "__main__":
    analyze_best_fitness()