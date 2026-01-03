+"""
Módulo con los textos para generar el informe del test Raven Matrices
"""

# ============================================================================
# PÁRRAFOS FIJOS (siempre se incluyen)
# ============================================================================

PARRAFOS_FIJOS = {
    'titulo': "TEST DE MATRICES PROGRESIVAS DE RAVEN",
    
    'introduccion': """Este es un informe de evaluación cognitiva, obtenido a partir del rendimiento de {nombre} en la prueba Matrices Progresivas de Raven Escala Estándar.""",
    
    'descripcion_prueba': """1. DESCRIPCIÓN GENERAL DE LA PRUEBA.
     La prueba Matrices Progresivas de Raven es una prueba psicométrica no verbal estandarizada y diseñada para evaluar capacidad intelectual, especialmente el razonamiento deductivo, analógico o lógico-abstracto, independientemente del nivel cultural, educativo o del dominio del lenguaje del evaluado.
     La capacidad para analizar información visual, identificar relaciones, y deducir patrones o lógicas implícitas. Esta capacidad se considera un factor general y transversal de inteligencia y por tanto fundamentales para el aprendizaje, la adaptación a situaciones nuevas y el rendimiento académico general.
     Los resultados obtenidos en la prueba sirven de indicadores que son interpretados en comparación con los baremos normativos correspondientes, esto es, comparando el rendimiento de {nombre} con el rendimiento promedio de su grupo de referencia, personas de su misma edad y género. Más allá, para una interpretación más individualizada, cobra importancia la valoración cualitativa del contexto personal y situacional del evaluado.
     
     2. ¿EN QUÉ CONSISTE LA PRUEBA?
     La Escala General de Raven está compuesta por unas 5 series de 12 figuras incompletas organizadas en matrices. En cada ítem, el evaluado debe seleccionar, entre varias opciones, la figura que completa correctamente la matriz siguiendo una secuencia lógica. La dificultad de los ejercicios aumenta de manera progresiva, lo que permite evaluar cómo el sujeto afronta problemas cada vez más complejos. La prueba no requiere lectura ni expresión verbal compleja.

     3. El índice de discrepancia: para el control de efectos aleatorios.
     Esta prueba sigue un incremento progresivo en la dificultad de sus problemas. Es por ello que se espera un rendimiento mejor de los participantes en los primeros problemas frente los siguientes. Y si una persona acierta un problema avanzado habiendo errado problemas anteriores puede ser indicativo de 1) un acierto aleatorio en el problema actual, o 2) una baja atención en el problema anterior. Dado que esta prueba tiene como objetivo evaluar el razonamiento del encuestado, y no su suerte o atención, se presenta el índice de discrepancia. Este índice controla si los resultados del participante son demasiado inhóspitos, y por tanto considerados sesgados y poco fiables como medida de la capacidad de razonamiento del participante. Se calcula a partir de la diferencia entre la puntuación obtenida ante un ensayo avanzado y la puntuación esperada ante este mismo ensayo (esperado según la puntuación acumulada por el sujeto en el total de ensayos previos). Para que los resultados se consideren sesgados y no representativos, el valor absoluto del índice de discrepancia tiene que ser mayor de 2 en al menos una de las 5 escalas que conforman la prueba.
     """,
    
    'titulo_resultados': "Presentación de los resultados de {nombre}",
    
    'texto_imagen_baremos': "En esta siguiente tabla se muestra para cada puntuación total obtenida en la prueba posible, el número de problemas que se espera se acierten en cada escala.",
    'texto_tabla_discrepancia': "Finalmente, en base a esta puntuación esperada, y a la realmente obtenida por el sujeto se presenta a continuación, en forma de tabla, el cálculo del índice de discrepancia.""",
}

# ============================================================================
# PÁRRAFOS CONDICIONALES SEGÚN PUNTUACIONES
# ============================================================================

# VAR - Variabilidad del rendimiento
# Textos compartidos para evitar duplicación
TEXTO_DISCREPANCIA_SIGNIFICATIVA = """{Nombre} obtuvo un índice de discrepancia superior a 2 en la(s) escala(s): {escala_discrepante}. Esto señala que {Nombre} se ha beneficiado significativamente de aciertos aleatorios en problemas de escalas avanzadas. Esto indica cierta aleatoriedad en la respuesta de {Nombre} por lo que sus resultados en esta prueba y siguiente interpretación de su capacidad de razonamiento están distorsionados, más posiblemente siendo más positivos de los que realmente corresponde. Y por esto, hay que considerar con cautela los resultados a continuación expuestos."""

TEXTO_DISCREPANCIA_NO_SIGNIFICATIVA = """{Nombre} no obtuvo un índice de discrepancia significativo para ninguna de las escalas de la prueba. Esto es indicativo de que {Nombre} estuvo atento en la tarea y no respondió de manera aleatoria. Este índice es positivo y significa que los resultados a continuación expuestos son representativos del rendimiento típico de {Nombre}, al igual que la capacidad de razonamiento de {Nombre} que de estos resultados se infiere."""

# PD_Total - Según puntuación directa total y correspondiente percentil
PARRAFOS_PD = {
    'muy bajo': """El rendimiento obtenido por {Nombre} en la prueba se sitúa en un rango muy bajo (con resultados por debajo del 90% de las personas de su edad), lo que indica dificultades significativas en el razonamiento lógico y abstracto. Esto puede traducirse en una mayor complejidad para comprender relaciones entre elementos, resolver problemas nuevos o adaptarse a demandas cognitivas no estructuradas. En el contexto educativo, puede requerir apoyos específicos, adaptación de tareas y un seguimiento individualizado.""",
    
    'bajo': """{Nombre} presenta un nivel bajo de razonamiento abstracto, superando en resultados únicamente a entre un 10 y un 25% de las personas de su edad. Esto sugiere que puede experimentar ciertas dificultades al enfrentarse a tareas que requieren análisis lógico, identificación de patrones o resolución de problemas sin instrucciones claras. En orientación educativa, se recomienda reforzar estrategias de aprendizaje guiadas y estructuradas.""",

    'normal': """El resultado obtenido por {Nombre} se sitúa dentro del rango normal, indicando un nivel adecuado de razonamiento lógico y capacidad para comprender relaciones abstractas acordes a su edad. Esto sugiere que dispone de los recursos cognitivos necesarios para afrontar las demandas habituales del contexto educativo y beneficiarse de una enseñanza ordinaria.""",

    'alto': """{Nombre} obtiene una puntuación alta en la prueba, superando en resultados a entre un 75 y un 90% de los individuos de su edad. Esto refleja una buena capacidad de razonamiento abstracto, análisis de patrones y resolución de problemas. Este perfil cognitivo favorece el aprendizaje de contenidos complejos y la adaptación a situaciones nuevas, siendo un indicador positivo para el rendimiento académico y el aprovechamiento educativo.""",
    
    'muy alto': """El rendimiento de {Nombre} se sitúa en un rango muy alto, con resultados superiores a como mínimo el 90% de los individuos de su edad. Esto indica una capacidad superior de razonamiento lógico y pensamiento abstracto. Esto es, una gran facilidad para identificar relaciones complejas, aprender con rapidez y resolver problemas novedosos. En el ámbito educativo, puede beneficiarse de programas de enriquecimiento o ampliación curricular."""
}


