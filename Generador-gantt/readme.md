Guía Detallada: Generador de Diagrama de Gantt Optimizado
Este documento es una guía paso a paso para usar y entender el script de Python generar_gantt_optimizado.py.
1. ¿Qué Hace Este Script?
El script lee un archivo CSV específico llamado Plan de trabajo _Summan.xlsx - Summan.csv, procesa los datos del plan de trabajo y genera dos archivos:
Un diagrama de Gantt interactivo (archivo .html): Puedes abrirlo en tu navegador, pasar el ratón sobre las tareas para ver detalles, y hacer zoom.
Un diagrama de Gantt estático (archivo .png): Una imagen de alta resolución que puedes usar en reportes, presentaciones o correos electrónicos.
La característica principal es que este script lee el progreso de tus tareas (por ejemplo, 80% completado) y lo dibuja en las barras del diagrama, dándote una visión clara del avance del proyecto.
2. Requisitos (Qué necesitas antes de empezar)
Para que el script funcione, necesitas tener dos cosas instaladas en tu computadora:
Python 3: Si no lo tienes, puedes descargarlo desde python.org.
Librerías de Python: El script depende de pandas (para leer datos) y plotly (para crear los gráficos). También necesitarás kaleido para guardar la imagen .png.
Puedes instalar todas las librerías necesarias abriendo tu terminal (CMD, PowerShell, o Terminal en Mac/Linux) y ejecutando el siguiente comando:
pip install pandas plotly kaleido


3. Archivos Necesarios
Asegúrate de tener los siguientes archivos en la misma carpeta:
TuCarpetaDeProyecto/
├── generar_gantt_optimizado.py     (El script de Python)
└── Plan de trabajo _Summan.xlsx - Summan.csv  (Tu archivo de datos)


4. Paso a Paso: Cómo Ejecutar el Script
Abre tu Terminal:
En Windows: Presiona la tecla de Windows, escribe cmd o PowerShell y presiona Enter.
En Mac: Abre la aplicación "Terminal".
En Linux: Abre tu terminal preferida.
Navega a tu Carpeta:
Usa el comando cd (change directory) para moverte a la carpeta donde guardaste tus archivos.
Ejemplo:
cd C:\Usuarios\TuNombre\Documentos\MiProyectoGantt

(Reemplaza esa ruta con la ruta real de tu carpeta)
Ejecuta el Script:
Una vez que estés en la carpeta correcta, simplemente ejecuta el script usando python:
python generar_gantt_optimizado.py


¡Revisa los Resultados!
Si todo salió bien, verás un mensaje de "¡Éxito!" en tu terminal. Ahora, en tu carpeta, habrán aparecido dos archivos nuevos:
gantt_optimizado_interactivo.html
gantt_optimizado_estatico.png
Simplemente haz doble clic en el archivo .html para abrir el gráfico interactivo en tu navegador.
5. Explicación Detallada del Código (Para Entenderlo)
Aquí desglosamos qué hace cada parte del script generar_gantt_optimizado.py.
Importaciones
import pandas as pd                 # Para leer y manipular los datos (tu CSV)
import plotly.figure_factory as ff  # Se usa para la función create_gantt (la avanzada)
import plotly.express as px         # Se usa para las paletas de colores
import plotly.io as pio             # Para configurar el tema y guardar los gráficos
import sys                          # Para mostrar mensajes de error


Sección 1: Limpieza y Preparación de Datos
Esta es la parte más importante. Los datos "crudos" de tu CSV no se pueden graficar directamente.
# Establece un fondo blanco por defecto para los gráficos
pio.templates.default = "plotly_white"

try:
    df = pd.read_csv(csv_path)

    # El progreso (ej. 0.81) estaba en una columna sin nombre.
    # Aquí la renombramos a 'Progreso_Num' para usarla fácilmente.
    if 'Unnamed: 8' in df.columns:
        df = df.rename(columns={'Unnamed: 8': 'Progreso_Num'})
    
    # La primera fila de tu CSV es un resumen general del proyecto ("Summan").
    # La quitamos para no graficarla como si fuera una tarea.
    if 'NOMBRE DE TAREA' in df.columns:
         df = df[df['NOMBRE DE TAREA'] != 'Summan'].copy()
    
    # Verificamos que las columnas de fecha existan
    if 'FECHA INICIO' not in df.columns or 'FECHA FIN' not in df.columns:
        print(f"Error:...", file=sys.stderr)
        return

    # Convertimos el TEXTO de las fechas (ej. "2025-10-06") a un formato
    # de FECHA real que Python entiende. 'errors='coerce'' convierte
    # cualquier fecha mala o vacía en 'NaT' (Not a Time).
    df['FECHA INICIO'] = pd.to_datetime(df['FECHA INICIO'], errors='coerce')
    df['FECHA FIN'] = pd.to_datetime(df['FECHA FIN'], errors='coerce')

    # Eliminamos cualquier fila donde la fecha de inicio o fin
    # no se pudo entender (era 'NaT'). Sin esto, Plotly daría un error.
    df = df.dropna(subset=['FECHA INICIO', 'FECHA FIN'])

    # Convertimos la columna de progreso (que puede tener texto como "Cerrado")
    # a un número. 'errors='coerce'' convierte "Cerrado" en 'NaN' (Not a Number).
    # .fillna(0) reemplaza todos los 'NaN' con 0.
    df['Progreso_Num'] = pd.to_numeric(df['Progreso_Num'], errors='coerce').fillna(0)
    
    # Nos aseguramos de que el progreso esté entre 0 y 1 (ej. 0.8)
    df['Progreso_Num'] = df['Progreso_Num'].clip(0, 1)

    # Rellenamos los 'RESPONSABLE' que estén vacíos con "No asignado".
    if 'RESPONSABLE' not in df.columns:
        df['RESPONSABLE'] = 'No asignado'
    else:
        df['RESPONSABLE'] = df['RESPONSABLE'].fillna('No asignado')


Sección 2: Transformación para el Gráfico
La función de Plotly create_gantt espera nombres de columna muy específicos (Task, Start, Finish, Resource, Complete). Creamos un nuevo DataFrame (tabla) que coincida exactamente con ese formato.
df_gantt = pd.DataFrame({
    'Task': df['NOMBRE DE TAREA'],
    'Start': df['FECHA INICIO'],
    'Finish': df['FECHA FIN'],
    'Resource': df['RESPONSABLE'],
    # Convertimos el progreso de 0.0-1.0 a 0-100 (ej. 0.8 -> 80)
    'Complete': (df['Progreso_Num'] * 100).round(0) 
})


Sección 3: Creación del Gráfico
Aquí es donde ocurre la magia.
# --- Esta es la mejora clave ---
# Usamos ff.create_gantt porque soporta la columna 'Complete'
# para dibujar el progreso. El px.timeline (versión simple) no lo hace.

# Obtenemos una lista de todos los responsables únicos (ej. "Summan", "Cliente")
resources = df_gantt['Resource'].unique()
# Creamos una paleta de colores
colors = px.colors.qualitative.Plotly
# Asignamos un color diferente a cada responsable
color_map = {res: colors[i % len(colors)] for i, res in enumerate(resources)}

# Creamos la figura del Gantt
fig = ff.create_gantt(
    df_gantt,               # Los datos que acabamos de transformar
    colors=color_map,       # El mapa de colores por responsable
    index_col='Resource',   # Le dice a Plotly que use nuestra columna 'Resource' para los colores
    show_colorbar=True,     # Muestra la leyenda de colores
    group_tasks=True,       # Agrupa las tareas por responsable en el gráfico
    title='Diagrama de Gantt del Proyecto (Optimizado con Progreso)'
)

# Ajustes finales para que se vea más limpio
fig.update_layout(
    title_x=0.5, # Centra el título
    yaxis_autorange="reversed", # Pone la primera tarea arriba (en lugar de abajo)
    hovermode="x unified"       # Mejora la info que aparece al pasar el ratón
)


Sección 4: Guardar Archivos
Finalmente, guardamos el gráfico que creamos.
# Guardar el diagrama interactivo como HTML
output_html = "gantt_optimizado_interactivo.html"
fig.write_html(output_html)

# Guardar el diagrama estático como imagen PNG
output_image = "gantt_optimizado_estatico.png"
try:
    # Esto requiere la librería 'kaleido'
    fig.write_image(output_image, width=1200, height=800, scale=2)
    print(f"¡Éxito! Se generaron dos archivos:")
    # ...
except Exception as e:
    # Si 'kaleido' no está instalado, esto fallará
    # pero el HTML sí se habrá creado.
    print(f"¡Éxito! Se generó el archivo HTML interactivo: {output_html}")
    print(f"No se pudo generar la imagen estática: {e}", file=sys.stderr)


Sección if __name__ == "__main__":
Esta es la parte que realmente ejecuta todo. Le dice a Python: "cuando ejecutes este archivo directamente (y no lo importes desde otro script), corre la función generar_gantt_optimizado con este archivo".
if __name__ == "__main__":
    # Aquí defines qué archivo CSV quieres procesar
    file_to_process = "Plan de trabajo _Summan.xlsx - Summan.csv"
    
    generar_gantt_optimizado(file_to_process)


6. Solución de Problemas Comunes
Error: FileNotFoundError: [Errno 2] No such file or directory
Significa: No encontró el archivo Plan de trabajo _Summan.xlsx - Summan.csv.
Solución: Asegúrate de que el archivo CSV esté exactamente en la misma carpeta que el script .py y que el nombre sea idéntico (mayúsculas y espacios importan).
Error: ModuleNotFoundError: No module named 'pandas' (o 'plotly')
Significa: No tienes instalada la librería.
Solución: Ejecuta pip install pandas plotly kaleido en tu terminal.
El script se ejecuta pero solo dice "¡Éxito! Se generó el archivo HTML..." y no crea el PNG.
Significa: La librería kaleido (para crear la imagen) no está instalada o falla.
Solución: Ejecuta pip install --upgrade kaleido en tu terminal para instalarla o actualizarla.
Error: KeyError: 'Unnamed: 8' (o 'FECHA INICIO')
Significa: Los nombres de las columnas en tu archivo CSV han cambiado.
Solución: Tendrás que abrir el script de Python y ajustar los nombres de las columnas en la "Sección 1: Limpieza de Datos" para que coincidan con tu nuevo CSV.
