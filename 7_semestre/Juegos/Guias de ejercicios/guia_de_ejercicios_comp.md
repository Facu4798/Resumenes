# Teoría de Juegos 2026 — Guía de Ejercitación 2: Modelos de Decisiones

Dificultad: ★ básico | ★★ intermedio | ★★★ avanzado

---

## Ejercicio 15 — Decisiones grupales ★

Una empresa está analizando el lanzamiento de un nuevo producto y las opiniones de los gerentes de marketing y de operaciones son antagónicas:

- **Gerente de marketing**: propone reducir el costo del producto para acceder a un mayor mercado.
- **Gerente de operaciones**: prefiere no realizar inversiones en la planta, aceptando un mayor costo.

**Preguntas:**
1. ¿Cómo puede resolverse la disputa?
2. ¿Es conveniente tomar las decisiones en forma grupal?
3. ¿Qué beneficios y desventajas pueden anticiparse?
4. ¿Qué métodos pueden emplearse para acordar la decisión?

---

## Ejercicio 16 — Compitiendo por el mercado ★

Dos compañías se reparten al **50%** el mercado consumidor de un determinado producto. Ambas empresas están analizando comenzar una campaña publicitaria para capturar mayor cuota de mercado.

**Reglas del juego:**
Si una empresa lanza una campaña, le quita clientes a la otra en la siguiente proporción según el medio elegido:

| Medio de publicidad | % de clientes quitados a la rival |
|---------------------|----------------------------------|
| Televisión          | 60%                              |
| Radio               | 30%                              |
| Diarios             | 10%                              |

> **Nota:** El juego es simétrico: ambas empresas tienen las mismas opciones de medios.

**Preguntas:**
a) Plantear la estrategia más conveniente para la publicidad.  
b) Usar el concepto de **estrategias dominadas** y encontrar el **punto minimax** y el **valor del juego**.  
c) Analizar qué sucede si se consideran **diferentes costos** según el medio utilizado.

**Ayuda:** Considerar que al tomar cada una de las demandas como la media de una distribución normal, deberá recalcularse las probabilidades en cada caso.

---

## Ejercicio 17 — El problema de LANZETTA ★★

### Contexto

LANZETTA estudia lanzar un nuevo modelo de moto. Su competidor es **MOTFRANCE**, el otro productor de motos del país.

### Opciones de LANZETTA

| Modelo | Precio ($/U) | Margen ($/U) | Demanda estimada (U/año) |
|--------|-------------|--------------|--------------------------|
| MP (monoplaza) | 2.000 | 1.000 | 500.000 |
| E (económico)  | 1.250 |   500 | 400.000 |

### Opciones de MOTFRANCE (reacciones posibles)

**Frente al modelo MP de LANZETTA:**

| Estrategia MOTFRANCE | Precio ($/U) | Costo ($/U) | Demanda capturada (U/año) |
|----------------------|-------------|-------------|---------------------------|
| Modelo importado (precio normal) | 2.500 | 1.500 | 200.000 |
| Precio agresivo                  | 2.000 | 1.500 | 400.000 |

**Frente al modelo E de LANZETTA:**
- MOTFRANCE compite mal → captura solo **100.000 U/año**.

### Matriz de pagos (Ganancia anual = Demanda × Margen)

|                          | MOTFRANCE: precio normal | MOTFRANCE: precio agresivo |
|--------------------------|--------------------------|----------------------------|
| **LANZETTA lanza MP**    | LANZETTA: 500k×1000 = 500M ; MOTFRANCE: 200k×1000 = 200M | LANZETTA: 500k×1000 = 500M ; MOTFRANCE: 400k×500 = 200M |
| **LANZETTA lanza E**     | LANZETTA: 400k×500 = 200M ; MOTFRANCE: 100k×? = ? | LANZETTA: 400k×500 = 200M ; MOTFRANCE: 100k×? = ? |

> Nota: Los márgenes de MOTFRANCE deben calcularse como Precio − Costo. Para precio normal: 2500−1500=1000 $/U. Para precio agresivo: 2000−1500=500 $/U.

**Matriz de pagos (ganancias anuales en millones $):**

|                          | MOTFRANCE: precio normal (margen 1000) | MOTFRANCE: precio agresivo (margen 500) |
|--------------------------|----------------------------------------|-----------------------------------------|
| **LANZETTA lanza MP**    | L: 500M, MF: 200M                     | L: 500M, MF: 200M                       |
| **LANZETTA lanza E**     | L: 200M, MF: 100M                     | L: 200M, MF: 50M                        |

> Aclaración: cuando LANZETTA lanza E, MOTFRANCE solo captura 100.000 U independientemente de su estrategia de precio, por lo que sus ganancias difieren según margen aplicado.

**Preguntas:**
a) ¿Qué hará MOTFRANCE?  
b) ¿Qué le conviene hacer a LANZETTA?

---

## Ejercicio 18 — Tateti ★★

**Preguntas:**
1. ¿Cómo podemos diseñar una estrategia para ganar, o al menos empatar en el **tateti** (tic-tac-toe 3×3)?
2. ¿Cómo podemos actuar si el juego se transforma en un **tatetitotu** (tic-tac-toe en 3D, 4×4×4)?

---

## Ejercicio 19 — Bluedeep ★

**Preguntas:**
1. ¿Cuáles son las dificultades para ganar al ajedrez?
2. ¿Cómo hizo **Deep Blue** para ganarle a **Kasparov**?

> Nota: El enunciado original dice "Bluedeep" y "Gasparov" pero se refiere a Deep Blue (IBM) y Garry Kasparov.

---

# Teoría de Juegos 2026 — Guía de Ejercitación 1: Modelos de Decisiones

---

## Ejercicio 1 — El problema del canillita ★

Un canillita debe decidir diariamente cuántos periódicos comprar sin conocer la demanda exacta.

**Datos:**
- Costo unitario: $4/diario
- Precio de venta: $5/diario
- Los diarios no vendidos no pueden devolverse
- Demanda posible: entre 50 y 100 unidades

**Distribución de probabilidades de demanda:**

| Demanda (unidades) | 50  | 60  | 70  | 80  | 90  | 100 |
|--------------------|-----|-----|-----|-----|-----|-----|
| Probabilidad       | 15% | 15% | 20% | 20% | 20% | 10% |

**Preguntas:**
a) ¿Cuántas unidades le conviene comprar?  
b) ¿Qué pasa si existe un valor de devolución de los diarios no vendidos?  
c) ¿Hasta qué valor máximo debería pagar por un informe que le pronosticara exactamente la demanda? (valor de la información perfecta)

---

## Ejercicio 2 — Perforando en Salta ★★

La empresa petrolera **PETRONORTE** prepara su programa de perforación 2010 en Salta.

**Datos generales:**

| Área     | Pozos disponibles | Inversión por pozo |
|----------|------------------|--------------------|
| Orán     | 30               | 10 MM$             |
| Tartagal | 40               | 5 MM$              |

**Presupuesto total disponible:** 300 MM$

**Clasificación de pozos y VAN (sin inversión, tasa descuento 10%):**

| Categoría | Descripción | VAN por pozo |
|-----------|-------------|--------------|
| A (Ace)   | Productivo alto | 50 MM$ |
| R (Regular) | Productivo medio | 12 MM$ |
| S (Seco)  | Improductivo | −10 MM$ (cierre) |

**Distribución por área:**

| Área     | % tipo A | % tipo R | % tipo S |
|----------|----------|----------|----------|
| Orán     | 40%      | 25%      | 35%      |
| Tartagal | 25%      | 50%      | 25%      |

**Preguntas:**
a) ¿Cuál es la estrategia óptima de perforación y el resultado esperado del programa?  
b) ¿Conviene asociar a un consultor especializado que cobra el **5% de las utilidades** y que, con sus estudios, puede identificar con total precisión el **20% de los pozos S** existentes en el área (que así pueden excluirse del programa)?

---

## Ejercicio 3 — Agrosur ★★

**AGROSUR** analiza instalar una línea de envasado de plaguicida para soja.

**Parámetros:** horizonte 5 años, tasa de interés nula, precio de venta: **1.200 $/T**, operación máxima: **300 días/año**, restricción: costos fijos ≤ **24.000 M$/año**.

**Opciones de capacidad:**

| Línea | Capacidad (T/día) | Costo Fijo (M$/mes) | Costo Variable ($/T) |
|-------|------------------|--------------------|--------------------|
| Slim  | 100              | 1.000              | 500                |
| Right | 150              | 2.000              | 400                |
| Top   | 300              | 2.500              | 300                |

> Los costos fijos incluyen el costo equivalente de la inversión. Los costos variables no incluyen materia prima.

**Escenarios de demanda:**

| Escenario | Demanda (T/año) |
|-----------|----------------|
| Alta      | 45.000         |
| Media     | 35.000         |
| Baja      | 25.000         |

**Objetivo:** Determinar la capacidad de planta que maximiza las utilidades.

---

## Ejercicio 4 — Savageando ★

**Preguntas:**
1. ¿En qué consiste el **criterio de decisión de Savage** (criterio minimax del arrepentimiento)?
2. ¿En qué situaciones es conveniente aplicarlo?
3. ¿Cómo puede reducirse el riesgo en el proceso decisional?

---

## Ejercicio 5 — Comprando la información ★★

Un comprador por Internet evalúa si realizar una compra riesgosa.

**Datos:**
- Precio ofertado del artículo: $300
- Precio de mercado: $400 → ganancia potencial: $100
- P(vendedor fraudulento) = 50%
- Si compra y es fraude: pierde $300

**Opción: contratar Credit Bureau por $8**
- P(informe negativo | vendedor fraudulento) = 85%
- P(informe positivo | vendedor confiable) = 75%

**Pregunta:** ¿Qué se le recomienda al comprador? ¿Debe contratar el Credit Bureau? ¿Debe comprar?

---

## Ejercicio 6 — Evaluando alternativas financieras ★★

Un fondo de inversiones dispone de **100 millones de pesos** e invertirá durante **2 años** en acciones **o** bonos (nunca ambos simultáneamente). Al final del año 1 puede cambiar de instrumento.

**Rendimientos según situación económica:**

| Situación económica | Bonos (%) | Acciones (%) |
|--------------------|-----------|--------------|
| Depresión          | 0         | −8           |
| Recesión           | 8         | 12           |
| Crecimiento        | 5         | 25           |

**Probabilidades:**

| Situación | Año 1 | Año 2 (si Año 1 = Crecimiento) | Año 2 (si Año 1 = Recesión) |
|-----------|-------|-------------------------------|------------------------------|
| Crecimiento | 70% | 70% | 20% |
| Recesión    | 30% | 30% | 70% |
| Depresión   | 0%  | 0%  | 10% |

**Objetivo:** Maximizar el valor del fondo al término del segundo año.

**Preguntas:**
a) Construir el árbol de decisión, establecer la política óptima de inversiones e indicar el resultado esperado.  
b) Reflexionar sobre el resultado.

---

## Ejercicio 7 — Riesgo geológico ★★

**NUCLEARSUR** debe decidir dónde construir una planta de procesamiento de combustibles nucleares.

**Opciones de localización:**

| Localización       | Costo construcción | Riesgo                                                        |
|--------------------|-------------------|---------------------------------------------------------------|
| Cañón del Diablo   | 10 MM$            | Si hay terremoto: pierde 10 MM$ y debe construir en Aguas Tranquilas igual |
| Aguas Tranquilas   | 20 MM$            | Sin riesgo                                                    |

**Datos de riesgo:**
- P(terremoto en próximos 5 años) = 20%

**Opción de contratar geólogo:** costo = 1 MM$
- P(predice terremoto | terremoto ocurre) = 95%
- P(predice no terremoto | no ocurre terremoto) = 90%

**Preguntas:**
1. ¿Debe contratarse el geólogo?
2. ¿Qué pasa si la decisión se demora un año y en ese año **no** ocurre un terremoto en Cañón del Diablo? ¿Cambia la recomendación?

---

## Ejercicio 8 — ¿Conviene la publicidad? ★★★

Una empresa evalúa incorporar un nuevo método de publicidad.

**Datos actuales:**
- Capacidad de producción: 100.000 u/mes
- Margen de venta: 100 $/u

**Distribución de demanda actual:**

| Demanda (miles de u) | 80  | 90  | 100 | 110 | 120 |
|----------------------|-----|-----|-----|-----|-----|
| Probabilidad (%)     | 15  | 35  | 25  | 20  | 5   |

**Opción publicidad:**
- Costo: 300.000 $/mes
- Incremento estimado de ventas: 10%

**Preguntas:**
a) ¿Es conveniente contratar la publicidad con el nuevo método?  
b) ¿Cómo analizar el problema si los valores de demanda (primera fila) pertenecieran a una **distribución normal con desvío del 5%**?

---

## Ejercicio 9 — Aceros a futuro ★★★

Una empresa comercializa aceros para la construcción y analiza ampliar su distribución en la región norte.

**Datos:**
- Margen: 100 $/T
- Horizonte: 3 años + operación posterior
- Costo financiero: nulo

**Opciones de centro de distribución:**

| Centro          | Capacidad (T/año) | Inversión |
|-----------------|------------------|-----------|
| Baja capacidad  | 100.000          | 10 MM$    |
| Alta capacidad  | 150.000          | 15 MM$    |

**Escenarios de demanda (primeros 3 años):**

| Escenario | Demanda (T/año) | Probabilidad |
|-----------|----------------|--------------|
| Media     | 80.000         | 40%          |
| Alta      | 125.000        | 60%          |

- En cada año existe un **10% de probabilidad de que cambie la tendencia** respecto al año anterior.
- Si se elige baja capacidad y la demanda resulta alta: se puede ampliar en una 2da etapa a **120.000 T/año** con inversión adicional de **10 MM$**.
- Luego de los 3 años: ventas se nivelan en **100.000 T/año** en ambas opciones.

**Preguntas:**
a) ¿Cuál es la inversión más conveniente y con qué ventaja económica?  
b) ¿Cuál es el valor máximo a pagar por un estudio de mercado de alta precisión (certeza ~100%)?  
c) ¿Cuál es la inversión máxima admisible en el centro de alta capacidad?

---

## Ejercicio 10 — Comprando equipos ★★

Seleccionar entre dos equipos alternativos para un proceso determinado.

**Datos:** vida útil técnica = 5 años, horizonte de planeamiento = 10 años, tasas de interés nulas, equipos no revendibles.

**Costos (miles de $):**

| Equipo | Inversión | Mant. Año 1 | Mant. Año 2 | Mant. Año 3 | Mant. Año 4 | Mant. Año 5 |
|--------|-----------|------------|------------|------------|------------|------------|
| A      | 1.000     | 100        | 200        | 700        | 800        | 900        |
| B      | 2.500     | 200        | 200        | 200        | 200        | 200        |

> Ambos equipos generan resultados operativos similares.

**Preguntas:**
1. ¿Qué equipo conviene seleccionar con tasas de interés nulas y horizonte de 10 años?
2. ¿Cómo se modifica la decisión si las tasas de interés son positivas?

---

## Ejercicio 11 — Localizando una nueva planta ★

**SOFTCOLAS** debe elegir entre dos áreas para instalar una nueva planta envasadora.

**Evaluación de factores** (escala de costos creciente de 0 a 10 — menor puntaje = mejor):

| Factor                       | Ponderación | Area A | Area B |
|------------------------------|-------------|--------|--------|
| Costos de construcción       | 10          | 8      | 5      |
| Servicios de infraestructura | 10          | 7      | 7      |
| Servicios de administración  | 10          | 4      | 7      |
| Valor inmobiliario           | 20          | 7      | 4      |
| Calidad de vida              | 20          | 4      | 8      |
| Transporte                   | 30          | 7      | 6      |

**Preguntas:**
1. ¿Cuál es la mejor área para establecer la nueva planta?
2. ¿Qué otras consideraciones pueden efectuarse?
3. ¿Qué preferiría el gerente comercial de SOFTCOLAS? ¿Y el gerente de operaciones?
4. ¿Cómo puede organizarse el proceso decisional?

---

## Ejercicio 12 — Decisiones personales ★

**Preguntas:**
1. Escribir tres decisiones importantes tomadas en los últimos años.
2. ¿Qué modelos de decisión se utilizaron?
3. ¿Qué estilo de decisión tiene el decisor?

---

## Ejercicio 13 — Vamos a la soja ★★

Un inversor analiza alquilar un campo de **1.000 Ha** por **20 años** a un costo de **$500.000** para sembrarlo de soja.

**Ganancias anuales posibles (miles de $) según zona y clima:**

|        | Cálido | Normal | Frío  |
|--------|--------|--------|-------|
| Sur    | 1.000  | 800    | 600   |
| Centro | 700    | 2.000  | 1.800 |
| Norte  | 400    | 1.700  | 3.000 |

**Probabilidades climáticas históricas:**

| Clima  | Probabilidad |
|--------|-------------|
| Cálido | 40%         |
| Normal | 40%         |
| Frío   | 20%         |

**Preguntas:**
1. ¿Conviene alquilar el campo? ¿En qué región?
2. ¿Qué conviene hacer si en los **primeros 5 años el clima resulta cálido** y se tiene la opción de **recuperar $300.000** (salir del contrato)?

---

## Ejercicio 14 — Malcomb Products ★★

El departamento de control de calidad debe decidir entre inspeccionar todos los ítems de un lote o ninguno.

**Datos:**
- Tamaño del lote: **N = 100 artículos**
- Costo de vender una pieza defectuosa: **$180**
- Costo de inspeccionar todo el lote: **$400**

**Categorías del lote:**

| Categoría | P(pertenecer a categoría) | P(ítem defectuoso \| categoría) |
|-----------|--------------------------|--------------------------------|
| I         | 0,90                     | p₁ = 0,01                     |
| II        | 0,05                     | p₂ = 0,02                     |
| III       | 0,05                     | p₃ = 0,20                     |

**Costo esperado de NO inspeccionar:** $180 \times p_j \times N$

**Preguntas:**
a) Realizar la **matriz de pagos**.  
b) ¿Qué decisión tomar usando el criterio de **valor esperado monetario**?  
c) ¿Cuál es el **valor esperado de la información perfecta (VEIP)**?  
d) Se considera una **tercera opción**: inspeccionar aleatoriamente **1 ítem** del lote ($20) y, según el resultado, decidir si inspeccionar los 99 restantes ($400) o no. El costo esperado de no inspeccionar los restantes sería $180 \times p_j \times N$. ¿Es conveniente esta nueva opción?
