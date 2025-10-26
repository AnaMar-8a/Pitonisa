import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import plotly.io as pio
import sys

def generar_gantt_optimizado(csv_path):
    """
    Genera un diagrama de Gantt interactivo y estático a partir de un archivo CSV
    específico del plan de trabajo, mostrando el progreso de las tareas.
    """
    
    # Establecer un tema visual más limpio para el gráfico
    pio.templates.default = "plotly_white"

    try:
        df = pd.read_csv(csv_path)

        # --- 1. Limpieza y Preparación de Datos (Optimización) ---

        # Basado en la inspección, la columna 'Unnamed: 8' contiene el progreso numérico
        if 'Unnamed: 8' in df.columns:
            df = df.rename(columns={'Unnamed: 8': 'Progreso_Num'})
        else:
            print(f"Advertencia: No se encontró la columna 'Unnamed: 8'. El progreso no se mostrará.", file=sys.stderr)
            df['Progreso_Num'] = 0 # Crear columna vacía si no existe

        # Omitir la primera fila (índice 0) que es una tarea resumen ("Summan")
        if 'NOMBRE DE TAREA' in df.columns:
             df = df[df['NOMBRE DE TAREA'] != 'Summan'].copy()
        
        # Asegurarse de que las columnas de fecha existen
        if 'FECHA INICIO' not in df.columns or 'FECHA FIN' not in df.columns:
            print(f"Error: El archivo debe contener columnas 'FECHA INICIO' y 'FECHA FIN'.", file=sys.stderr)
            return

        # Convertir columnas de fecha a datetime. 'errors='coerce'' convierte fechas inválidas en NaT (Not a Time)
        df['FECHA INICIO'] = pd.to_datetime(df['FECHA INICIO'], errors='coerce')
        df['FECHA FIN'] = pd.to_datetime(df['FECHA FIN'], errors='coerce')

        # Eliminar filas donde las fechas de inicio o fin no pudieron ser interpretadas (son NaT)
        # Esto es crucial para que Plotly funcione
        df = df.dropna(subset=['FECHA INICIO', 'FECHA FIN'])

        # Convertir la columna de progreso numérico. 'errors='coerce'' convierte texto ("Cerrado") en NaN
        # .fillna(0) asegura que las tareas sin progreso numérico se traten como 0%
        df['Progreso_Num'] = pd.to_numeric(df['Progreso_Num'], errors='coerce').fillna(0)
        
        # Asegurar que el progreso esté entre 0 y 1 (Plotly espera 0-100 para 'Complete')
        df['Progreso_Num'] = df['Progreso_Num'].clip(0, 1)

        # Rellenar valores nulos en 'RESPONSABLE' para evitar errores en la agrupación
        if 'RESPONSABLE' not in df.columns:
            df['RESPONSABLE'] = 'No asignado'
        else:
            df['RESPONSABLE'] = df['RESPONSABLE'].fillna('No asignado')

        # --- 2. Transformación para el Diagrama de Gantt ---

        # plotly.figure_factory.create_gantt espera nombres de columna específicos.
        # También convertimos el progreso (0.0-1.0) a porcentaje (0-100).
        
        df_gantt = pd.DataFrame({
            'Task': df['NOMBRE DE TAREA'],
            'Start': df['FECHA INICIO'],
            'Finish': df['FECHA FIN'],
            'Resource': df['RESPONSABLE'],
            'Complete': (df['Progreso_Num'] * 100).round(0) # Convertir a porcentaje 0-100
        })
        
        # --- 3. Creación del Gráfico (Mejora) ---

        # Esta es una mejora clave: usamos create_gantt de figure_factory
        # en lugar de px.timeline, porque create_gantt soporta nativamente 
        # la columna 'Complete' para mostrar el progreso en las barras.

        # Crear un mapa de colores para los 'Recursos' (Responsables)
        resources = df_gantt['Resource'].unique()
        # Usamos una paleta de colores cualitativa de Plotly
        colors = px.colors.qualitative.Plotly
        color_map = {res: colors[i % len(colors)] for i, res in enumerate(resources)}

        fig = ff.create_gantt(
            df_gantt,
            colors=color_map,       # Aplicar el mapa de colores
            index_col='Resource',   # Agrupar y colorear por 'Resource' (RESPONSABLE)
            show_colorbar=True,     # Mostrar la leyenda de colores
            group_tasks=True,       # Agrupar visualmente las tareas por 'Resource'
            showgrid_x=True,        # Mostrar rejilla vertical
            showgrid_y=True,        # Mostrar rejilla horizontal
            title='Diagrama de Gantt del Proyecto (Optimizado con Progreso)'
        )

        # Ajustes finales del layout
        fig.update_layout(
            title_x=0.5, # Centrar el título
            yaxis_autorange="reversed", # Mostrar la primera tarea en la parte superior
            hovermode="x unified"       # Mejorar el tooltip al pasar el ratón
        )

        # --- 4. Guardar Archivos ---

        # Guardar el diagrama interactivo como HTML
        output_html = "gantt_optimizado_interactivo.html"
        fig.write_html(output_html)

        # Guardar el diagrama estático como imagen PNG
        # (Requiere la librería 'kaleido': pip install kaleido)
        output_image = "gantt_optimizado_estatico.png"
        try:
            # Configurar kaleido para una imagen de mayor resolución
            fig.write_image(output_image, width=1200, height=800, scale=2)
            print(f"¡Éxito! Se generaron dos archivos:")
            print(f"1. Diagrama interactivo: {output_html}")
            print(f"2. Imagen estática: {output_image}")
        except Exception as e:
            print(f"¡Éxito! Se generó el archivo HTML interactivo: {output_html}")
            print(f"No se pudo generar la imagen estática: {e}", file=sys.stderr)
            print("Asegúrate de tener 'kaleido' instalado ('pip install kaleido')")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{csv_path}'.", file=sys.stderr)
    except Exception as e:
        print(f"Ocurrió un error inesperado durante el procesamiento: {e}", file=sys.stderr)

# --- Punto de entrada para ejecutar el script ---
if __name__ == "__main__":
    # Define la ruta al archivo CSV que subiste
    # Asegúrate de que este archivo esté en la misma carpeta que el script
    # o proporciona la ruta completa.
    file_to_process = "Plan de trabajo _Summan.xlsx - Summan.csv"
    
    generar_gantt_optimizado(file_to_process)
