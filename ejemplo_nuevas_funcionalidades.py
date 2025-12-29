"""
Ejemplo de uso de las nuevas funcionalidades de lector_datos.py

Este script demuestra las mejoras implementadas:
1. Estructura explícita para celdas seleccionadas
2. Estructura explícita para índices por fila
3. Funciones de utilidad para consultar datos
"""

from lector_datos import (
    leer_datos_excel,
    calcular_puntuaciones_directas,
    esta_celda_seleccionada,
    obtener_indices_fila,
    obtener_celdas_seleccionadas,
    obtener_celdas_no_seleccionadas,
    obtener_resumen_indices
)

# Ruta al archivo Excel (ajustar según tu ubicación)
RUTA_EXCEL = r"C:\Users\Pablo\OneDrive\Escritorio\data\pablo prada_1.xlsx"


def ejemplo_uso_completo():
    """
    Ejemplo completo de uso de las nuevas funcionalidades
    """
    print("=" * 70)
    print("EJEMPLO: NUEVAS FUNCIONALIDADES DE LECTOR_DATOS")
    print("=" * 70)
    
    # 1. Leer datos del Excel
    print("\n1. Leyendo datos del Excel...")
    datos = leer_datos_excel(RUTA_EXCEL)
    print(f"   ✓ Edad: {datos['edad']} años")
    print(f"   ✓ Nombre: {datos['nombre_completo']}")
    
    # 2. Calcular puntuaciones con estructuras mejoradas
    print("\n2. Calculando puntuaciones con estructuras explícitas...")
    resultados = calcular_puntuaciones_directas(datos)
    print(f"   ✓ Cálculos completados")
    
    # 3. Usar la estructura explícita de celdas seleccionadas
    print("\n3. Consultando celdas seleccionadas (estructura explícita):")
    
    # 3.1 Obtener todas las celdas seleccionadas
    celdas_sel = obtener_celdas_seleccionadas(resultados)
    print(f"   ✓ Total de celdas seleccionadas: {len(celdas_sel)}")
    print(f"   ✓ Primeras 5 celdas seleccionadas: {list(celdas_sel)[:5]}")
    
    # 3.2 Obtener todas las celdas no seleccionadas
    celdas_no_sel = obtener_celdas_no_seleccionadas(resultados)
    print(f"   ✓ Total de celdas no seleccionadas: {len(celdas_no_sel)}")
    
    # 3.3 Consultar celdas específicas
    print("\n   Consultando celdas específicas:")
    for row, col in [(1, 1), (1, 30), (5, 20), (14, 45)]:
        seleccionada = esta_celda_seleccionada(resultados, row, col)
        estado = "✓ SELECCIONADA" if seleccionada else "✗ NO SELECCIONADA"
        print(f"     - Celda (fila {row}, columna {col}): {estado}")
    
    # 4. Usar la estructura explícita de índices por fila
    print("\n4. Consultando índices por fila (estructura explícita):")
    
    # 4.1 Acceso directo por número de fila
    print("\n   Acceso directo a índices de filas específicas:")
    for row in [1, 5, 10, 14]:
        indices = obtener_indices_fila(resultados, row)
        print(f"     - Fila {row:2d}: TR={indices['TR']:2d}, TA={indices['TA']:2d}, "
              f"O={indices['O']:2d}, C={indices['C']:2d}")
    
    # 4.2 También disponible mediante la estructura indices_por_fila
    print("\n   Iterando sobre todos los índices por fila:")
    for row, indices in sorted(resultados['indices_por_fila'].items()):
        if row in [1, 7, 14]:  # Mostrar solo algunas filas como ejemplo
            print(f"     - Fila {row:2d}: {indices}")
    
    # 5. Índices globales (ya calculados)
    print("\n5. Índices globales calculados:")
    print(f"   ✓ TR_total: {resultados['TR_total']}")
    print(f"   ✓ TA_total: {resultados['TA_total']}")
    print(f"   ✓ O_total: {resultados['O_total']}")
    print(f"   ✓ C_total: {resultados['C_total']}")
    print(f"   ✓ E_total: {resultados['E_total']} (O + C)")
    print(f"   ✓ TOT: {resultados['TOT']} (TR - E)")
    print(f"   ✓ CON: {resultados['CON']} (TA - C)")
    print(f"   ✓ VAR: {resultados['VAR']} (TR_max - TR_min)")
    print(f"   ✓ TR_max: {resultados['TR_max']}")
    print(f"   ✓ TR_min: {resultados['TR_min']}")
    
    # 6. Resumen completo
    print("\n6. Generando resumen completo:")
    print(obtener_resumen_indices(resultados))
    
    # 7. Compatibilidad hacia atrás
    print("\n7. Verificando compatibilidad hacia atrás:")
    print(f"   ✓ TR_por_fila (lista): {resultados['TR_por_fila'][:3]}... (primeras 3 filas)")
    print(f"   ✓ datos_d2 (DataFrame): {len(resultados['datos_d2'])} filas")
    
    print("\n" + "=" * 70)
    print("EJEMPLO COMPLETADO ✓")
    print("=" * 70)


def ejemplo_uso_imagen():
    """
    Ejemplo de generación de imagen usando las nuevas estructuras
    """
    from generador_imagen_final import generar_imagen_final
    import os
    
    print("\n" + "=" * 70)
    print("EJEMPLO: GENERACIÓN DE IMAGEN CON NUEVAS ESTRUCTURAS")
    print("=" * 70)
    
    # Leer y calcular
    datos = leer_datos_excel(RUTA_EXCEL)
    resultados = calcular_puntuaciones_directas(datos)
    
    # Generar imagen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_base = os.path.join(script_dir, 'grafico_D2.png')
    ruta_salida = os.path.join(script_dir, 'grafico_D2_final.png')
    
    print("\n✓ Generando imagen con estructura explícita de celdas seleccionadas...")
    exito = generar_imagen_final(resultados, resultados['datos_d2'], ruta_base, ruta_salida)
    
    if exito:
        print(f"✓ Imagen generada: {ruta_salida}")
        print(f"  - Puntos dibujados: {len(obtener_celdas_seleccionadas(resultados))} celdas")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Ejecutar ejemplos
    try:
        ejemplo_uso_completo()
        ejemplo_uso_imagen()
    except FileNotFoundError:
        print("\n⚠ Archivo Excel no encontrado.")
        print("   Ajustar RUTA_EXCEL al inicio del script.")
