# Guía Detallada: Generador de Diagrama de Gantt Optimizado

Este documento es una guía paso a paso para usar y entender el script de Python `generar_gantt_optimizado.py`.

## 1. ¿Qué Hace Este Script?

El script lee un archivo CSV específico llamado `Plan de trabajo _Summan.xlsx - Summan.csv`, procesa los datos del plan de trabajo y genera dos archivos:

- **Diagrama de Gantt interactivo (archivo .html):** Puedes abrirlo en tu navegador, pasar el ratón sobre las tareas para ver detalles, y hacer zoom.
- **Diagrama de Gantt estático (archivo .png):** Una imagen de alta resolución que puedes usar en reportes, presentaciones o correos electrónicos.

La característica principal es que este script lee el progreso de tus tareas (por ejemplo, 80% completado) y lo dibuja en las barras del diagrama, dándote una visión clara del avance del proyecto.

## 2. Requisitos (Qué necesitas antes de empezar)

Para que el script funcione, necesitas tener:

- **Python 3:** Puedes descargarlo desde [python.org](https://www.python.org/).
- **Librerías de Python:** `pandas` (para leer datos), `plotly` (para crear gráficos) y `kaleido` (para guardar la imagen .png).

Instalación de librerías:

```bash
pip install pandas plotly kaleido
```

## 3. Archivos Necesarios

Asegúrate de tener los siguientes archivos en la misma carpeta:

```
TuCarpetaDeProyecto/
├── generar_gantt_optimizado.py     (El script de Python)
└── Plan de trabajo _Summan.xlsx - Summan.csv  (Tu archivo de datos)
```

## 4. Paso a Paso: Cómo Ejecutar el Script

### Abrir tu Terminal:
- **Windows:** Tecla de Windows → escribir `cmd` o `PowerShell` → Enter
- **Mac:** Abrir la aplicación "Terminal"
- **Linux:** Abrir tu terminal preferida

### Navegar a tu Carpeta:

```bash
cd C:\Usuarios\TuNombre\Documentos\MiProyectoGantt
```
(Reemplaza con la ruta real de tu carpeta)

### Ejecutar el Script:

```bash
python generar_gantt_optimizado.py
```

### Revisar los Resultados

Si todo salió bien, verás un mensaje de "¡Éxito!". En tu carpeta se crearán dos archivos:

- `gantt_optimizado_interactivo.html`
- `gantt_optimizado_estatico.png`

Haz doble clic en el archivo `.html` para abrir el gráfico interactivo en tu navegador.

## 5. Explicación Detallada del Código

### Importaciones
```python
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import plotly.io as pio
import sys
```

### Sección 1: Limpieza y Preparación de Datos
```python
pio.templates.default = "plotly_white"

try:
    df = pd.read_csv(csv_path)

    if 'Unnamed: 8' in df.columns:
        df = df.rename(columns={'Unnamed: 8': 'Progreso_Num'})
    
    if 'NOMBRE DE TAREA' in df.columns:
         df = df[df['NOMBRE DE TAREA'] != 'Summan'].copy()
    
    if 'FECHA INICIO' not in df.columns or 'FECHA FIN' not in df.columns:
        print(f"Error:...", file=sys.stderr)
        return

    df['FECHA INICIO'] = pd.to_datetime(df['FECHA INICIO'], errors='coerce')
    df['FECHA FIN'] = pd.to_datetime(df['FECHA FIN'], errors='coerce')

    df = df.dropna(subset=['FECHA INICIO', 'FECHA FIN'])
    df['Progreso_Num'] = pd.to_numeric(df['Progreso_Num'], errors='coerce').fillna(0)
    df['Progreso_Num'] = df['Progreso_Num'].clip(0, 1)

    if 'RESPONSABLE' not in df.columns:
        df['RESPONSABLE'] = 'No asignado'
    else:
        df['RESPONSABLE'] = df['RESPONSABLE'].fillna('No asignado')
```

### Sección 2: Transformación para el Gráfico
```python
df_gantt = pd.DataFrame({
    'Task': df['NOMBRE DE TAREA'],
    'Start': df['FECHA INICIO'],
    'Finish': df['FECHA FIN'],
    'Resource': df['RESPONSABLE'],
    'Complete': (df['Progreso_Num'] * 100).round(0)
})
```

### Sección 3: Creación del Gráfico
```python
resources = df_gantt['Resource'].unique()
colors = px.colors.qualitative.Plotly
color_map = {res: colors[i % len(colors)] for i, res in enumerate(resources)}

fig = ff.create_gantt(
    df_gantt,
    colors=color_map,
    index_col='Resource',
    show_colorbar=True,
    group_tasks=True,
    title='Diagrama de Gantt del Proyecto (Optimizado con Progreso)'
)

fig.update_layout(
    title_x=0.5,
    yaxis_autorange="reversed",
    hovermode="x unified"
)
```

### Sección 4: Guardar Archivos
```python
output_html = "gantt_optimizado_interactivo.html"
fig.write_html(output_html)

output_image = "gantt_optimizado_estatico.png"
try:
    fig.write_image(output_image, width=1200, height=800, scale=2)
    print(f"¡Éxito! Se generaron dos archivos:")
except Exception as e:
    print(f"¡Éxito! Se generó el archivo HTML interactivo: {output_html}")
    print(f"No se pudo generar la imagen estática: {e}", file=sys.stderr)
```

### Sección if __name__ == "__main__"
```python
if __name__ == "__main__":
    file_to_process = "Plan de trabajo _Summan.xlsx - Summan.csv"
    generar_gantt_optimizado(file_to_process)
```

## 6. Solución de Problemas Comunes

- **Error:** `FileNotFoundError: [Errno 2] No such file or directory`
  - **Significa:** No se encontró el archivo CSV.
  - **Solución:** Asegúrate de que el archivo esté en la misma carpeta y el nombre sea exacto.

- **Error:** `ModuleNotFoundError: No module named 'pandas'` o `plotly`
  - **Significa:** No tienes instalada la librería.
  - **Solución:** Ejecuta `pip install pandas plotly kaleido`

- **El script se ejecuta pero solo crea el HTML:**
  - **Significa:** `kaleido` no está instalado o falla.
  - **Solución:** Ejecuta `pip install --upgrade kaleido`

- **Error:** `KeyError: 'Unnamed: 8'` o `'FECHA INICIO'`
  - **Significa:** Los nombres de las columnas cambiaron.
  - **Solución:** Ajusta los nombres de columnas en la Sección 1 del script para que coincidan con tu CSV.

