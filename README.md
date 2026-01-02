# Generador de Informes Test D2 - Atención

Este programa procesa los datos del Test D2 Raven y genera un informe profesional en formato Word (.docx).

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
proyecto_raven/
│
├── main.py                      # Programa principal
├── lector_datos.py              # Lee datos del Excel
├── reglas_psicometricas.py      # Aplica baremos según edad
├── textos.py                    # Textos del informe
├── generador_docx.py            # Genera el documento Word
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

### Hoja "Ravens Matrices"
Debe contener las siguientes columnas:
- `Ensayo`: 5 series: A, B, C, D y E con 12 filas por serie: A1, A2..., A12, B1...
- `Respuesta correcta`: Indica si es estímulo relevante ('si' o 'no')
- `Respuesta dada`: Indica que número indico el participante como respuesta (un valor discreto entre 1 y 8)

## 🎯 Cómo Usar el Programa

### Paso 1: Configurar las rutas

Editar el archivo `main.py` y modificar las siguientes variables:

```python
RUTA_EXCEL = r"C:\Users\Pablo\OneDrive\Escritorio\data\María"
RUTA_SALIDA = r"C:\Users\Pablo\OneDrive\Escritorio\data\Informe_Raven_Resultado.docx"
NOMBRE_CASO = "caso"  # Cambiar por el nombre real del evaluado
```

### Paso 2: Ejecutar el programa

```bash
python main.py
```

El programa ejecutará automáticamente los siguientes pasos:
1. Leer datos del archivo Excel
2. Calcular puntuaciones directas
3. Obtener puntuaciones típicas (baremos)
4. Generar informe en formato Word
5. Guardar el informe

## 📈 Puntuaciones Calculadas

El programa calcula las siguientes puntuaciones directas:

### Por cada fila (A, B, C, D, E):
- **PD de cada serie**: Número de aciertos por serie
- **Índice de discrepancia de cada serie**: Diferencia, resto entre la puntuación esperada y la puntuación dada

### Totales:
- **PD_total**: Total de aciertos
- **Discrepancia significativa o no significativa**: Si en alguna de las escalas este índice es mayor a 2

## 🎓 Interpretación de Puntuaciones Típicas

El programa clasifica automáticamente las puntuaciones según baremos por edad:

### PD:
- **bajo**: Por debajo del Pc25
- **normal**: Entre el Pc25 y el 75
- **alto**: Por encima del Pc75



## 📄 Contenido del Informe

El informe generado incluye:

1. **Portada** (Primera página)
   - Título del test: "Test de Matrices progresivas de Raven, un test de inteligencia"
   - Nombre completo del encuestado (extraído de `sub_num`)
   - Edad del evaluado
   - Fecha de aplicación (si está disponible)
   - Fecha del informe (generada automáticamente)
   - Nota de confidencialidad
2. **Introducción**  predeterminada y constante
3. **Descripción de la prueba** y variables técnicas PD e índice de discrepancia
5. **Tabla de resultados** con puntuaciones directas y clasificaciones
6. **Interpretación detallada** de los resultados del participante
7. **Síntesis del caso**


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

Los baremos están basados en el manual oficial del Test de Matrices Progresivas de Raven Escala General (SPM) 3ºEdición (Raven, Court and Raven, 2001):

## 📞 Contacto

Para dudas o sugerencias sobre el programa, contactar al desarrollador.

## 📝 Notas Importantes

- El programa está diseñado para generar informes profesionales automáticamente
- Se recomienda revisar el informe generado antes de su uso clínico
- Los baremos son aproximaciones basadas en el manual oficial
- Siempre verificar que los datos de entrada son correctos antes de ejecutar
