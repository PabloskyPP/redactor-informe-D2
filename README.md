# Generador de Informes Test D2 - Atención

Este programa procesa los datos del Test D2 de Atención y genera un informe profesional en formato PDF.

## 📋 Requisitos

- Python 3.7 o superior
- LibreOffice (para conversión de DOCX a PDF)
- Las siguientes bibliotecas de Python:
  - pandas
  - openpyxl
  - python-docx
  - pypdf
  - reportlab
  - Pillow

## 🚀 Instalación

1. Instalar LibreOffice (si no está instalado):
   - **Ubuntu/Debian**: `sudo apt-get install libreoffice-writer`
   - **Windows**: Descargar desde https://www.libreoffice.org/
   - **macOS**: `brew install --cask libreoffice`

2. Instalar las dependencias de Python:
```bash
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
proyecto_d2/
│
├── main.py                      # Programa principal
├── lector_datos.py              # Lee datos del Excel
├── reglas_psicometricas.py      # Aplica baremos según edad
├── textos.py                    # Textos del informe
├── generador_imagen_final.py    # Genera grafico_D2_final.png con overlays
├── generador_docx.py            # Genera el documento Word
├── generador_pdf.py             # Convierte DOCX a PDF e inserta imagen
├── grafico_D2.png               # Imagen base del gráfico D2
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

## 📊 Formato del Archivo Excel

El archivo Excel debe tener la siguiente estructura:

### Hoja "info"
- `age`: Edad del evaluado (obligatorio)
- `sub_num`: Nombre completo del encuestado (opcional pero recomendado)
  - Puede ser un identificador simple o nombre completo con apellidos
  - El programa extraerá automáticamente:
    - `nombre_completo`: valor completo de sub_num
    - `nombre`: solo el primer token (antes del primer espacio)

### Hoja "D2"
Debe contener las siguientes columnas:
- `row`: Número de fila (1-14)
- `letter_number`: Número de posición de la letra en la fila (1-47)
- `target`: Indica si es estímulo relevante ('si' o 'no')
- `selected`: Indica si fue seleccionado por el evaluado ('TRUE', 'FALSE' o vacío)

## 🎯 Cómo Usar el Programa

### Paso 1: Configurar las rutas

Editar el archivo `main.py` y modificar las siguientes variables:

```python
RUTA_EXCEL = r"C:\Users\Pablo\OneDrive\Escritorio\data\2312_21312.xlsx"
RUTA_SALIDA_PDF = r"C:\Users\Pablo\OneDrive\Escritorio\data\Informe_D2_Resultado.pdf"
NOMBRE_CASO = "caso"  # Cambiar por el nombre real del evaluado
```

### Paso 2: Ejecutar el programa

```bash
python main.py
```

El programa ejecutará automáticamente los siguientes pasos:
1. Leer datos del archivo Excel
2. Calcular puntuaciones directas
3. **Generar imagen final** `grafico_D2_final.png` con superposiciones
4. Obtener puntuaciones típicas (baremos)
5. Generar informe en formato Word (temporal)
6. Guardar el informe DOCX
7. **Convertir DOCX a PDF e insertar imagen como página 3**

**Nota**: La imagen `grafico_D2_final.png` se genera automáticamente en el mismo directorio del script.

## 📈 Puntuaciones Calculadas

El programa calcula las siguientes puntuaciones directas:

### Por cada fila (1-14):
- **TR**: Número del último elemento intentado en la fila
- **TA**: Total de aciertos (targets marcados correctamente)
- **O**: Errores de omisión (targets no marcados)
- **C**: Errores de comisión (no-targets marcados incorrectamente)

### Totales:
- **TR_total**: Suma de TR de todas las filas
- **TA_total**: Suma de TA de todas las filas
- **O_total**: Suma de O de todas las filas
- **C_total**: Suma de C de todas las filas
- **E_total**: Total de errores (O + C)
- **TOT**: TR_total - E_total
- **CON**: TA_total - C_total (índice de concentración)
- **TR_max**: TR más alto entre todas las filas
- **TR_min**: TR más bajo entre todas las filas
- **VAR**: Variabilidad (TR_max - TR_min)

## 🎓 Interpretación de Puntuaciones Típicas

El programa clasifica automáticamente las puntuaciones según baremos por edad:

### TR (Velocidad de procesamiento):
- **bajo**: Lento
- **normal**: Normal
- **alto**: Rápido

### O (Errores de omisión):
- **bajo**: Atento (pocos errores)
- **normal**: Atención normal
- **alto**: Despistado (muchos errores)

### C (Errores de comisión):
- **bajo**: Preciso (pocos errores)
- **normal**: Precisión normal
- **alto**: Impreciso (muchos errores)

### CON (Concentración):
- **bajo**: Desconcentrado
- **normal**: Concentración normal
- **alto**: Concentrado

### VAR (Variabilidad):
- **bajo**: Estable
- **normal**: Normal
- **alto**: Variable

## 📄 Contenido del Informe

El informe generado es un archivo PDF que incluye:

1. **Portada** (Primera página)
   - Título del test: "D2, TEST DE ATENCIÓN"
   - Nombre completo del encuestado (extraído de `sub_num`)
   - Edad del evaluado
   - Fecha de aplicación (si está disponible)
   - Fecha del informe (generada automáticamente)
   - Nota de confidencialidad
2. **Introducción y Descripción de la prueba** (Segunda página)
   - Introducción personalizada con el nombre del evaluado
   - Descripción de la prueba y variables técnicas (TR, TA, O, C, E, TOT, CON, VAR)
3. **GRÁFICO D2** (Tercera página) ⭐ **NUEVA UBICACIÓN**
   - Imagen final `grafico_D2_final.png` insertada como página completa
   - Incluye todas las superposiciones gráficas:
     - Textos rotados verticalmente con puntuaciones totales (TR, TA, O, C)
     - Cuadros de texto por fila con valores de cada índice
     - Puntos negros marcando respuestas seleccionadas
     - Líneas conectando puntos finales entre filas
   - Imagen centrada y escalada para ajustarse a la página
   - Mantiene proporción sin deformación
4. **Resultados e Interpretación** (Cuarta página en adelante)
   - Tabla de resultados con puntuaciones directas y clasificaciones
   - Interpretación detallada de cada índice:
     - Variabilidad del rendimiento (VAR)
     - Velocidad de procesamiento (TR)
     - Errores de omisión (O)
     - Errores de comisión (C)
     - Concentración (CON)
   - Síntesis del perfil atencional con interpretación integrada

## 🎨 Generación de Imagen Final

El programa genera automáticamente `grafico_D2_final.png` con superposiciones gráficas. Esta imagen se inserta como una página completa (página 3) en el PDF final. La imagen incluye:

### Elementos Superpuestos:
- **Textos rotados**: Puntuaciones totales (TR_total, TA_total, O_total, C_total) rotados verticalmente
- **Índices por fila**: Valores de TR, TA, O, C para cada una de las 14 filas
- **Puntos negros**: Marcan cada posición donde el evaluado seleccionó un ítem (selected != FALSE)
- **Líneas conectoras**: Unen el último punto de cada fila con el último punto de la fila siguiente

### Ventajas del nuevo formato PDF:
- ✅ Imagen como página completa e independiente (página 3)
- ✅ Mayor control sobre el posicionamiento gráfico
- ✅ No modifica el documento Word original
- ✅ Proceso reproducible y automatizado
- ✅ Imagen centrada y escalada correctamente en el PDF
- ✅ El documento Word queda limpio sin la imagen

## 📋 Nuevo Flujo de Generación

1. Se genera el documento Word (DOCX) **sin** la imagen del gráfico
2. El documento DOCX se convierte automáticamente a PDF usando LibreOffice
3. La imagen `grafico_D2_final.png` se inserta como página 3 del PDF
4. El resultado es un PDF con la estructura:
   - Páginas 1-2: Contenido original del DOCX
   - Página 3: Imagen del gráfico D2 (página completa)
   - Páginas 4+: Resto del contenido original del DOCX

## 🔧 Configuración Avanzada

### Personalización de Posiciones en la Imagen

Las posiciones de los elementos gráficos pueden ajustarse editando las constantes en `generador_imagen_final.py`:

```python
# Posiciones para textos rotados de totales (x, y en píxeles)
POSICIONES_TOTALES = {
    'TR_total': (20, 350),
    'TA_total': (50, 350),
    'O_total': (480, 350),
    'C_total': (510, 350),
}

# Márgenes del área útil del gráfico
MARGEN_SUPERIOR = 80    # Píxeles desde el top hasta la primera fila
MARGEN_INFERIOR = 40    # Píxeles desde la última fila hasta el bottom
MARGEN_IZQUIERDO = 40   # Píxeles desde el left hasta la primera columna
MARGEN_DERECHO = 40     # Píxeles desde la última columna hasta el right

# Configuración de puntos y líneas
RADIO_PUNTO = 4         # Radio de los puntos negros
GROSOR_LINEA = 2        # Grosor de las líneas conectoras
```

### Personalización de Fuentes y Colores

Puede ajustar los tamaños de fuente y colores en `generador_imagen_final.py`:

```python
# Tamaños de fuente
FUENTE_TOTALES_TAMANIO = 16
FUENTE_INDICES_TAMANIO = 12

# Colores (RGBA)
COLOR_PUNTO = (0, 0, 0, 255)  # Negro para puntos
COLOR_LINEA = (0, 0, 0, 255)  # Negro para líneas
```

## 🔧 Solución de Problemas

### Error: "No se encuentra el archivo Excel"
- Verificar que la ruta en `RUTA_EXCEL` es correcta
- Usar rutas absolutas o relativas correctas
- Verificar que el archivo existe

### Error: "Columna no encontrada"
- Verificar que la hoja "info" tiene la columna "age"
- Verificar que la hoja "D2" tiene todas las columnas requeridas

### Error al instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 📚 Baremos Utilizados

Los baremos están basados en el manual oficial del Test D2 (Brickenkamp & Zillmer):

- **Tabla A.1**: 8-10 años
- **Tabla A.2**: 11-12 años
- **Tabla A.3**: 13-14 años
- **Tabla A.4**: 15-16 años
- **Tabla A.5**: 17-18 años
- **Tabla A.6**: 19-23 años
- **Tabla A.7**: 24-29 años
- **Tabla A.8**: 30-39 años
- **Tabla A.9**: 40+ años

## 📞 Contacto

Para dudas o sugerencias sobre el programa, contactar al desarrollador.

## 📝 Notas Importantes

- El programa está diseñado para generar informes profesionales automáticamente
- Se recomienda revisar el informe generado antes de su uso clínico
- Los baremos son aproximaciones basadas en el manual oficial
- Siempre verificar que los datos de entrada son correctos antes de ejecutar