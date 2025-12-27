# Generador de Informes Test D2 - Atención

Este programa procesa los datos del Test D2 de Atención y genera un informe profesional en formato Word (.docx).

## 📋 Requisitos

- Python 3.7 o superior
- Las siguientes bibliotecas de Python:
  - pandas
  - openpyxl
  - python-docx

## 🚀 Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
proyecto_d2/
│
├── main.py                    # Programa principal
├── lector_datos.py           # Lee datos del Excel
├── reglas_psicometricas.py   # Aplica baremos según edad
├── textos.py                 # Textos del informe
├── generador_docx.py         # Genera el documento Word
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
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
RUTA_SALIDA = r"C:\Users\Pablo\OneDrive\Escritorio\data\Informe_D2_Resultado.docx"
NOMBRE_CASO = "caso"  # Cambiar por el nombre real del evaluado
```

### Paso 2: Ejecutar el programa

```bash
python main.py
```

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

El informe generado incluye:

1. **Portada** (Primera página)
   - Título del test: "D2, TEST DE ATENCIÓN"
   - Nombre completo del encuestado (extraído de `sub_num`)
   - Edad del evaluado
   - Fecha de aplicación (si está disponible)
   - Fecha del informe (generada automáticamente)
   - Nota de confidencialidad
2. **Introducción** personalizada con el nombre del evaluado
3. **Descripción de la prueba** y variables técnicas (TR, TA, O, C, E, TOT, CON, VAR)
4. **GRÁFICO D2** (Página 3)
   - Imagen escalada para ocupar verticalmente toda la página
   - Mantiene proporción sin deformación
   - Cuadros de texto rotados verticalmente con puntuaciones (TR, TA, O, C)
   - Posiciones de cuadros configurables desde el código Python
5. **Tabla de resultados** con puntuaciones directas y clasificaciones
6. **Interpretación detallada** de cada índice:
   - Variabilidad del rendimiento (VAR)
   - Velocidad de procesamiento (TR)
   - Errores de omisión (O)
   - Errores de comisión (C)
   - Concentración (CON)
7. **Síntesis del perfil atencional** con interpretación integrada

## 🔧 Configuración Avanzada

### Personalización de Posiciones de Cuadros de Texto en el Gráfico

Las posiciones de los cuadros de texto sobre el gráfico D2 pueden ajustarse editando el diccionario `textbox_positions` en `generador_docx.py` (línea ~310):

```python
textbox_positions = {
    'TR': {'x': Inches(0.5), 'y': Inches(2.0)},   # Posición para TR
    'TA': {'x': Inches(1.5), 'y': Inches(2.5)},   # Posición para TA
    'O': {'x': Inches(2.5), 'y': Inches(3.0)},    # Posición para O
    'C': {'x': Inches(3.5), 'y': Inches(3.5)},    # Posición para C
}
```

Los valores se especifican en pulgadas desde el borde de la página. Ajuste estos valores para alinear los cuadros con las líneas correspondientes del gráfico.

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
