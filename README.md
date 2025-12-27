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
- Debe contener una columna `age` con la edad del evaluado

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

1. **Portada** con título del test
2. **Introducción** personalizada con el nombre del evaluado
3. **Descripción de la prueba** y variables técnicas
4. **Tabla de resultados** con puntuaciones directas y clasificaciones
5. **Interpretación detallada** de cada índice:
   - Variabilidad del rendimiento (VAR)
   - Velocidad de procesamiento (TR)
   - Errores de omisión (O)
   - Errores de comisión (C)
   - Concentración (CON)
6. **Síntesis del perfil atencional** con interpretación integrada

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
