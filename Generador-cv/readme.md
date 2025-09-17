# 📄 Guía Paso a Paso — CV en Blanco con Python  

Este proyecto genera un archivo de **Currículum Vitae (CV)** en Word usando un script en Python.  
Está diseñado para personas que **no saben programar** y quieren un tutorial muy básico, claro y detallado.  

---

## 🖥️ Requisitos previos
1. **Una computadora** con Windows, macOS o Linux.  
2. **Python 3.9 o superior** instalado.  
3. El archivo del script: cv-general.py.  

---

## 🔎 Paso 1: Verificar si tienes Python
### En Windows
1. Haz clic en el botón de inicio.  
2. Escribe cmd y abre la aplicación llamada **Símbolo del sistema** (una ventana negra).  
3. Escribe este comando y presiona Enter:  
   python --version
4. Si aparece algo como Python 3.11.5, ¡ya lo tienes instalado! 🎉  

👉 Si aparece un error como “python no se reconoce”, significa que no está instalado.  

**Solución:** descarga Python en https://www.python.org/downloads/ e instala la última versión.  
Durante la instalación marca la casilla “Add Python to PATH”.  

---

### En macOS o Linux
1. Abre la aplicación Terminal.  
2. Escribe:  
   python3 --version
3. Si ves algo como Python 3.10.12, está listo.  

👉 Si no aparece, instala Python desde https://www.python.org/downloads/.  

---

## 📦 Paso 2: Instalar la librería necesaria
Nuestro script necesita una librería que permite crear documentos Word: python-docx.  

1. Abre tu terminal o ventana de comandos.  
2. Escribe:  
   pip install python-docx
3. Presiona Enter y espera.  
4. Si todo va bien, verás algo como:  
   Successfully installed python-docx-0.8.11

👉 Errores comunes:  
- “pip no se reconoce”: puede que necesites usar pip3 en lugar de pip.  
  pip3 install python-docx
- Si nada funciona, prueba reinstalar Python marcando la opción pip durante la instalación.  

---

## 📂 Paso 3: Guardar el script
1. Abre un editor de texto:  
   - En Windows: Bloc de notas.  
   - En macOS: TextEdit (en modo texto plano).  
2. Copia el contenido de cv_template_blank.py.  
3. Guarda el archivo en tu carpeta de documentos con este nombre:  
   cv_template_blank.py

⚠️ Importante: asegúrate de que el archivo termine en .py y no en .txt.  

---

## ▶️ Paso 4: Ejecutar el script
1. Abre la terminal o el símbolo del sistema.  
2. Navega hasta la carpeta donde guardaste el archivo. Ejemplo en Windows:  
   cd C:\Users\TuNombre\Documents
3. Ejecuta el script:  
   python cv_template_blank.py

👉 En macOS/Linux puede ser:  
   python3 cv_template_blank.py  

---

## 📄 Paso 5: Ver tu CV en blanco
Si todo salió bien, en la misma carpeta aparecerá un archivo nuevo:  
CV_Plantilla_Blanco.docx  

- Haz doble clic y ábrelo con Microsoft Word, Google Docs (subiéndolo) o LibreOffice Writer.  
- Verás la estructura de un CV lista para que la completes:  
  - Nombre completo y contacto.  
  - Perfil Profesional.  
  - Experiencia Profesional.  
  - Educación.  
  - Certificaciones.  
  - Habilidades.  

---

## 📝 Paso 6: Personalizar tu CV
1. Completa los campos con tu información real.  
2. Ejemplo:  
   - Perfil Profesional: “Ingeniera de Telecomunicaciones con 5 años de experiencia en proyectos de software y telecomunicaciones…”  
   - Experiencia: añade cargo, empresa, fechas, responsabilidades y logros.  
3. Guarda el archivo.  

---

## 📑 Paso 7: Exportar a PDF
Los reclutadores prefieren recibir CVs en PDF.  

- En Word:  
  Archivo > Guardar como > PDF  
- En Google Docs:  
  Archivo > Descargar > PDF  
- En LibreOffice Writer:  
  Archivo > Exportar como > PDF  

---

## ⚠️ Problemas frecuentes y soluciones
- El comando python no funciona → Prueba con python3.  
- No aparece el archivo CV_Plantilla_Blanco.docx → Revisa que ejecutaste el script en la carpeta correcta.  
- El archivo se guarda como cv_template_blank.py.txt → Cambia la extensión a .py quitando .txt.  
- Word no abre el archivo → Usa Google Docs o instala LibreOffice (es gratuito).  

---

## 🎉 ¡Listo!
Acabas de crear tu primer CV en blanco con Python.  
Ahora solo necesitas llenarlo con tu historia profesional y exportarlo en PDF.  

---

## 📬 Contacto
Si necesitas ayuda extra:  
- Autoría: Ana María Ochoa Patiño  
- Email: 8a.anamaria@gmail.com  
- LinkedIn: linkedin.com/in/8aanamaria  

---

"Un CV en blanco no es vacío: es un lienzo para tu historia profesional." ✨
