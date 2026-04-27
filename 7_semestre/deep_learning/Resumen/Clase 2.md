<p align="center" style="font-size: 40px; font-weight: bold;">
Clase 2 — Unidad II: Red Perceptrón Multicapa
</p>

---

## Contenido

1. [Redes Neuronales y MLP](#1-redes-neuronales-y-mlp)
2. [El Perceptrón](#2-el-perceptrón)
3. [Funciones de Activación](#3-funciones-de-activación)
4. [Teorema de Aproximación Universal](#4-teorema-de-aproximación-universal)
5. [Entrenamiento: Funciones de Pérdida](#5-entrenamiento-funciones-de-pérdida)
6. [Gradient Descent](#6-gradient-descent)
7. [Backpropagation](#7-backpropagation)
8. [Shallow vs. Deep: Capacidad de Representación](#8-shallow-vs-deep-capacidad-de-representación)

---

## 1. Redes Neuronales y MLP

Una **red neuronal** es un sistema de procesamiento paralelo, masivo y distribuido formado por unidades simples que adquieren conocimiento mediante entrenamiento y lo almacenan en sus pesos.

Tipos principales: MLP, Redes Convolucionales (CNN), Redes Recurrentes (RNN), Transformers.

### Red Perceptrón Multicapa (RPMC / MLP)

También llamadas **Feedforward** o **Redes Densas**. Sus características:

- Constituidas por capas de perceptrones conectadas secuencialmente.
- Dos capas consecutivas están **completamente conectadas** (fully connected): cada nodo de una capa se conecta con todos los nodos de la siguiente.
- Tres tipos de capas:
  1. **Capa de entrada:** recibe el vector de entrada.
  2. **Capas ocultas:** una o más capas intermedias; aquí ocurre el procesamiento.
  3. **Capa de salida:** produce el vector de salida de la red.

Una **red shallow** tiene exactamente una capa oculta entre la entrada y la salida.

> El número total de pesos de la red crece con el número de capas y el número de neuronas por capa, lo que determina la capacidad de la red.

---

## 2. El Perceptrón

Unidad computacional básica inspirada en la neurona biológica (McCulloch & Pitts, 1943). Recibe varias entradas, las combina linealmente con sus pesos y aplica una función de activación:

$$y = f\!\left(\sum_{i=0}^{n} w_i x_i\right) = f(\mathbf{w}^T \mathbf{x})$$

donde $x_0 = 1$ es el término de bias, $w_0$ su peso, y $f$ es la **función de activación**.

> La función de activación **debe ser no lineal**. Si fuera lineal, toda la red —sin importar cuántas capas tenga— colapsaría a una única transformación lineal, perdiendo toda capacidad de representar patrones complejos.

---

## 3. Funciones de Activación

La elección de la función de activación ha sido uno de los factores más determinantes en la evolución del Deep Learning.

**Cronología:**
- 1943 — McCulloch & Pitts: función escalón
- 1986 — Rumelhart et al.: backpropagation con Sigmoide (diferenciable)
- 2010 — Nair & Hinton: ReLU supera a Sigmoide/Tanh en CNNs
- 2012 — AlexNet: ReLU + Dropout → revolución en ImageNet
- 2016 — Hendrycks & Gimpel: GELU (adoptada por BERT, GPT y todos los Transformers)
- 2017 — Ramachandran et al.: SiLU/Swish vía búsqueda automática

---

### 3.1 Sigmoide

$$\sigma(x) = \frac{1}{1 + e^{-x}}, \qquad \sigma'(x) = \sigma(x)\,(1-\sigma(x))$$

- Rango: $(0, 1)$ — gradiente máximo de solo $0.25$ en $x=0$.
- Históricamente fue la primera función diferenciable usada en redes profundas.

**Problemas en redes profundas:**
1. **Vanishing gradient:** la derivada se aplana rápidamente para valores grandes de $|x|$. Al encadenar muchas capas, el gradiente se multiplica en cada una y desaparece exponencialmente — las capas iniciales casi no aprenden.
2. **Salida no centrada en 0:** siempre produce valores positivos, por lo que los gradientes de los pesos de la capa siguiente siempre tienen el mismo signo. Esto provoca que el optimizador avance en *zigzag* en lugar de ir directo al mínimo.
3. **Costo computacional:** el cálculo de $e^x$ es significativamente más costoso que operaciones como `max(0,x)`.

**Cuándo se usa aún:** capa de salida para clasificación binaria, *gates* de LSTMs, *attention weights*.

---

### 3.2 Tangente Hiperbólica (tanh)

$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}, \qquad \tanh'(x) = 1 - \tanh^2(x)$$

- Rango: $(-1, 1)$ — **centrada en 0**, a diferencia de la sigmoide.
- Gradiente máximo de $1.0$ en $x=0$ — mayor que el de la sigmoide, entrena más rápido.
- Al estar centrada en 0, los gradientes no tienen sesgo de signo, lo que evita el problema del *zigzag*.

**Problema que comparte con la sigmoide:** sigue saturando para $|x| > 2$ — hay vanishing gradient en redes muy profundas, aunque menos grave que con la sigmoide.

**Uso actual:** *cell state* y *output gate* en LSTMs/GRUs; redes shallow con salida en $(-1, 1)$.

---

### 3.3 ReLU (Rectified Linear Unit)

$$\text{ReLU}(x) = \max(0, x)$$

Devuelve $x$ si es positivo, $0$ si es negativo. Su derivada es $1$ para $x>0$ y $0$ para $x\leq 0$.

**Ventajas:**
- **No satura para $x > 0$:** la derivada es exactamente 1 en la zona activa — el gradiente no se encoge al propagarse hacia atrás.
- **Sparse activation:** en redes bien entrenadas, ~50% de las neuronas están inactivas para una muestra dada. Esto separa mejor los conceptos en el espacio de activaciones.
- **Eficiencia computacional:** solo una comparación — es trivial en GPU.

**Problema: neuronas muertas.** Una neurona queda "muerta" cuando su entrada ponderada es negativa para *todas* las muestras del dataset. En ese caso su salida es siempre 0 y su gradiente es siempre 0 → los pesos nunca se actualizan. Es una condición irreversible durante el entrenamiento.

- Causas comunes: learning rate muy alto, inicialización incorrecta de pesos, datos sin normalizar.
- Un 10–50% de neuronas inactivas es normal y hasta útil.
- Si >80% están muertas se produce un *capacity collapse*: la red ya no puede representar adecuadamente los datos.

---

### 3.4 Leaky ReLU

$$f(x) = \max(\alpha x,\; x), \quad \alpha = 0.01$$

Igual a ReLU para $x > 0$, pero para $x < 0$ tiene una pequeña pendiente $\alpha$ en lugar de ser exactamente 0. Esto garantiza un gradiente mínimo siempre presente → elimina el problema de neuronas muertas.

---

### 3.5 ELU (Exponential Linear Unit)

$$f(x) = \begin{cases} x & x \geq 0 \\ \alpha(e^x - 1) & x < 0 \end{cases}$$

Para $x < 0$ usa una curva exponencial en lugar de una línea recta, lo que la hace **suave y continua** en $x=0$. Con buena inicialización, la media de sus salidas es cercana a 0 — reduce el sesgo interno. Costo mayor que Leaky ReLU por el cálculo exponencial.

---

### 3.6 GELU (Gaussian Error Linear Unit)

$$\text{GELU}(x) = x \cdot \Phi(x) = x \cdot \frac{1}{2}\left[1 + \text{erf}\!\left(\frac{x}{\sqrt{2}}\right)\right]$$

Aproximación usada en PyTorch (menos costosa):

$$\text{GELU}(x) \approx 0.5x\left(1 + \tanh\!\left(\sqrt{\frac{2}{\pi}}\,(x + 0.044715\,x^3)\right)\right)$$

Multiplica la entrada $x$ por la probabilidad de que $x$ sea mayor que una variable aleatoria normal — de ahí el nombre "Gaussian Error". Tiene un pequeño valle negativo para valores levemente negativos ($x \approx -0.17$), lo que le da mayor curvatura y capacidad expresiva.

---

### 3.7 SiLU / Swish

$$\text{SiLU}(x) = x \cdot \sigma(x) = \frac{x}{1+e^{-x}}$$

Multiplica la entrada por su propia sigmoide — una forma de "auto-compuerta". Tiene un pequeño valle negativo similar al GELU (mínimo cerca de $x \approx -0.28$).

---

### ¿Por qué GELU y SiLU superan a ReLU?

La ventaja clave es que son **suaves y no monótonas**: tienen un pequeño "valle" para valores levemente negativos. Esto mejora empíricamente la capacidad expresiva de la red y el flujo de gradientes.

1. **Suavidad ($C^\infty$):** gradientes suaves en toda la recta real. ReLU no es diferenciable en $x=0$, lo que puede crear inestabilidades en la optimización.
2. **No monotonía:** el pequeño valle negativo añade curvatura extra — la red puede representar más funciones sin necesitar más parámetros.
3. **Gradiente siempre no nulo:** no hay zona donde el gradiente sea exactamente 0 (excepto $x \to -\infty$), eliminando completamente el problema de neuronas muertas.
4. **Derivada puede superar 1:** alrededor de $x \approx 1.5$, la derivada es $\approx 1.1$, lo que facilita el flujo de gradientes en redes muy profundas. Esto contrasta con la sigmoide (máximo 0.25) o la tanh (máximo 1.0).

---

### Tabla Comparativa de Funciones de Activación

| Función | Rango | Centrada en 0 | Satura | Grad. máx. | Uso principal |
|---|---|---|---|---|---|
| Sigmoide | $(0,1)$ | No | Ambos lados | $0.25$ | Clasificación binaria, LSTM gates |
| Tanh | $(-1,1)$ | Sí | Ambos lados | $1.0$ | LSTM/GRU, redes shallow |
| ReLU | $[0,\infty)$ | No | $x<0$ muerto | $1.0$ ($x>0$) | CNNs, MLPs clásicos |
| Leaky ReLU | $(-\infty,\infty)$ | $\approx$Sí | No | $1.0$ | Alternativa a ReLU |
| ELU | $(-\alpha,\infty)$ | $\approx$Sí | $x\to-\infty$ | $1.0$ | Redes medianas, tabular |
| GELU | $\approx(-0.17,\infty)$ | $\approx$Sí | $x\to-\infty$ | $\sim 1.1$ | Transformers (BERT, GPT) |
| SiLU/Swish | $\approx(-0.28,\infty)$ | $\approx$Sí | $x\to-\infty$ | $\sim 1.1$ | YOLO, EfficientNet |

**Sobre la saturación:** una función satura cuando su derivada tiende a 0 para $|x|$ grande. La saturación frena el aprendizaje porque los gradientes desaparecen. Sigmoide y tanh saturan en ambos extremos; ReLU solo satura (con gradiente nulo) para $x < 0$; GELU y SiLU solo saturan hacia $-\infty$.

**Sobre el centrado en 0:** si la función produce siempre valores positivos (como sigmoide o ReLU), los gradientes de la capa siguiente siempre tienen el mismo signo, lo que provoca oscilaciones en la optimización (*zigzag*). La solución práctica es usar **Batch Normalization** después de cada capa, que normaliza las activaciones a media ≈ 0 — esta es la razón por la que ReLU funciona bien en la práctica pese a no estar centrada.

**Sobre el costo computacional:** la diferencia es despreciable comparada con las multiplicaciones matriciales que dominan el cómputo de la red. ReLU sigue siendo preferida cuando el cómputo es muy limitado; GELU/SiLU cuando la precisión importa más (NLP, visión de alta capacidad).

---

### Vanishing Gradients — Soluciones Modernas

| Solución | Cómo ayuda |
|---|---|
| ReLU y variantes | Derivada = 1 en zona activa, no se encoge al propagarse |
| Residual connections (ResNet) | Camino alternativo (*bypass*) que preserva el gradiente intacto |
| Batch Normalization | Mantiene las activaciones en la zona donde la función no satura |

---

## 4. Teorema de Aproximación Universal

> **(Cybenko, 1989; Hornik, 1991):** Una red neuronal *shallow* con suficientes neuronas ocultas y una función de activación no lineal continua puede aproximar cualquier función continua con precisión arbitraria sobre un dominio compacto.

- Cybenko (1989): demostrado para activaciones sigmoidales.
- Hornik (1991): generalizado a cualquier activación no constante, acotada y continua.
- Leshno et al. (1993): condición mínima — la activación no sea polinomial.

**Implicación práctica:** en principio, una sola capa oculta es *suficiente* para representar cualquier función. El problema no es *qué* puede representar, sino *cuántas neuronas* necesita. Para algunas funciones, una red shallow necesita exponencialmente más neuronas que una red profunda para la misma precisión. El teorema garantiza **existencia**, no **eficiencia**.

---

## 5. Entrenamiento: Funciones de Pérdida

El entrenamiento consiste en ajustar todos los pesos de la red para que sus predicciones se acerquen lo más posible a los valores reales del dataset. La **función de pérdida** (o *loss function*) es la métrica que cuantifica esa discrepancia — es la función que el optimizador intenta minimizar.

### Clasificación Binaria — Binary Cross-Entropy (BCE)

Mide qué tan lejos está la probabilidad predicha de la etiqueta real (0 o 1). Se usa junto con función de activación sigmoide en la capa de salida.

- Penaliza fuertemente las predicciones *seguras pero incorrectas*: si el modelo asigna 99% de probabilidad a la clase equivocada, la pérdida es muy alta.
- Interpretación probabilística: equivale al negativo del logaritmo de la probabilidad asignada a la clase correcta.
- Sensible al desbalance de clases: si una clase tiene muchos más ejemplos que la otra, el modelo puede aprender a ignorar la clase minoritaria. Se puede usar una variante ponderada.
- Continua y diferenciable → compatible con optimización por gradiente.

### Clasificación Multiclase — Categorical Cross-Entropy (CCE)

Extensión de BCE para múltiples clases. Se usa junto con función **softmax** en la capa de salida, que convierte los valores de salida en una distribución de probabilidad (suman 1).

- Las etiquetas deben estar en formato **one-hot encoding** (vector de ceros con un 1 en la posición de la clase correcta).
- Solo el término correspondiente a la clase correcta contribuye a la pérdida — penaliza cuando el modelo asigna baja probabilidad a la clase verdadera.
- Penaliza fuertemente las predicciones incorrectas y seguras.
- Continua y diferenciable → compatible con optimización por gradiente.

### Regresión — MSE, MAE y Huber

Para problemas donde la salida es un valor continuo.

**Mean Squared Error (MSE / Pérdida L2):**
- Eleva al cuadrado la diferencia entre predicción y valor real, luego promedia.
- Penaliza los errores grandes de forma cuadrática → **muy sensible a outliers**: un solo dato muy alejado puede dominar la pérdida y sesgar el entrenamiento.
- Continua, diferenciable y convexa → optimización estable.
- La magnitud depende de las unidades de la variable objetivo.
- Estándar en regresión; más fácil de minimizar que RMSE.

**Mean Absolute Error (MAE / Pérdida L1):**
- Usa el valor absoluto de la diferencia → penalización **lineal**, no cuadrática.
- **Robusta a outliers:** un dato muy alejado no domina la pérdida.
- No es diferenciable en 0 (gradiente indefinido) — en la práctica se usan subgradientes.
- El gradiente es constante (no disminuye cerca del mínimo) → puede oscilar alrededor del mínimo en lugar de converger suavemente.
- Muy interpretable: la pérdida está en las mismas unidades que la variable objetivo.

**Huber:**
- Combina lo mejor de MSE y MAE mediante un umbral $\delta$ (hiperparámetro elegido por validación cruzada).
- Para errores pequeños ($|r| \leq \delta$): se comporta como MSE → convergencia suave.
- Para errores grandes ($|r| > \delta$): se comporta como MAE → robusta a outliers.
- Diferenciable en todo el dominio (a diferencia de MAE).

| | MSE | MAE | Huber |
|---|---|---|---|
| Sensibilidad a outliers | Alta | Baja | Configurable con $\delta$ |
| Diferenciabilidad | Sí | No en $r=0$ | Sí |
| Gradiente cerca del mínimo | Suave (→0) | Constante | Suave (→0) |

---

## 6. Gradient Descent

El descenso por gradiente es el método iterativo que se usa para minimizar la función de pérdida. La idea central: el gradiente de una función en un punto apunta en la dirección de mayor crecimiento; para minimizar, se avanza en la dirección *opuesta*.

$$\boldsymbol{\theta}_{k+1} = \boldsymbol{\theta}_k - \eta \, \nabla_{\boldsymbol{\theta}} L(\boldsymbol{\theta}_k)$$

donde $\eta$ es el **learning rate** (tasa de aprendizaje), un hiperparámetro crítico:
- **$\eta$ muy pequeño:** convergencia lenta, pero estable.
- **$\eta$ muy grande:** los pasos son demasiado grandes y el algoritmo puede divergir o oscilar.

El algoritmo parte de un punto inicial $\boldsymbol{\theta}_0$ (aleatorio) y actualiza iterativamente los pesos en la dirección que reduce la pérdida.

### Variantes según el tamaño del batch

| Variante | Cómo calcula el gradiente | Ventaja | Desventaja |
|---|---|---|---|
| **Batch GD** | Todo el dataset a la vez | Gradiente exacto, convergencia estable | Muy lento y costoso en memoria para datasets grandes |
| **Mini-batch GD** | Un subconjunto (ej. 32, 64, 128 muestras) | Balance entre velocidad y estabilidad | Hiperparámetro extra (tamaño del batch) |
| **SGD** (Stochastic GD) | Una sola muestra a la vez | Muy rápido por iteración; puede escapar mínimos locales | Gradiente ruidoso, convergencia errática |

En la práctica se usa **mini-batch** casi siempre.

---

## 7. Backpropagation

Algoritmo para calcular eficientemente el gradiente de la pérdida respecto a *todos* los pesos de la red, aplicando la **regla de la cadena** hacia atrás desde la capa de salida hasta la capa de entrada.

Desarrollado por Rumelhart, Hinton y Williams (*Nature*, 1986). Paul Werbos (1974) lo describió primero en su tesis doctoral, pero el trabajo pasó desapercibido durante años.

### Idea Central

La red hace dos pasadas:

1. **Forward pass:** se propagan las entradas capa por capa hacia adelante, calculando la salida de cada neurona. Al final se calcula la pérdida.
2. **Backward pass:** se propaga el error hacia atrás, calculando la contribución de cada peso a la pérdida. Se usa la regla de la cadena para descomponer gradientes complejos en productos de derivadas locales.

### Cálculo de los Pesos — Capa de Salida

El peso $w_{oh}$ que conecta la unidad $h$ de la capa oculta con la unidad $o$ de la capa de salida se actualiza como:

$$w_{oh}^{(k+1)} = w_{oh}^{(k)} - \eta \cdot \delta_o^W \cdot v_h$$

donde:
- $v_h$ es la activación de la neurona oculta $h$ (calculada en el forward pass).
- $\delta_o^W = g'(z_o)\,(\hat{y}_o - y_o)$ es la **señal de error de la capa de salida**: producto entre la derivada de la función de activación de salida y el error de predicción.

### Cálculo de los Pesos — Capa Oculta

El peso $w_{hi}$ que conecta la entrada $i$ con la unidad $h$ de la capa oculta se actualiza como:

$$w_{hi}^{(k+1)} = w_{hi}^{(k)} - \eta \cdot \delta_h^V \cdot x_i$$

donde $\delta_h^V$ es la **señal de error retropropagada** (aquí entra la regla de la cadena):

$$\delta_h^V = f'(z_h) \sum_{o=1}^{O} w_{oh}^W \cdot \delta_o^W$$

Es decir: el error de una neurona oculta es la suma de los errores de todas las neuronas de salida a las que está conectada, ponderada por los pesos de esas conexiones, multiplicada por la derivada local de su función de activación. El error "fluye hacia atrás" a través de los pesos.

> **Intuición:** cada peso contribuye a la pérdida en proporción a (1) cuánto activó a la neurona que lo usó y (2) cuánto error generó esa neurona. Backprop distribuye la responsabilidad del error a cada peso de la red.

Las ecuaciones se implementan en forma **matricial** para mayor eficiencia computacional. Los pesos se pueden actualizar:
- Después de presentar **todo** el dataset (batch).
- Después de un **subconjunto** del dataset (mini-batch).
- Después de **cada ejemplo** individual (SGD).

---

## 8. Shallow vs. Deep: Capacidad de Representación

### ¿Qué mide la "capacidad" de una red?

Con funciones de activación ReLU, una red divide el espacio de entrada en **regiones lineales** — piezas donde la función que implementa es lineal. Más regiones → puede representar funciones más complejas.

- Una red **shallow** con $n$ neuronas crea hasta $n$ regiones lineales en 1D.
- Una red **deep** con $L$ capas y $n$ neuronas por capa puede crear hasta $n^L$ regiones.

La profundidad aumenta la capacidad **exponencialmente** con el número de capas, mientras que añadir más neuronas a una sola capa solo la aumenta linealmente. Con el mismo número total de parámetros, una red profunda tiene una capacidad expresiva enormemente mayor.

### Limitaciones de las Redes Shallow

1. **Ineficiencia de parámetros:** para representar funciones compuestas (como $f = g \circ h$), una red shallow necesita exponencialmente más neuronas que una red profunda equivalente.
2. **No captura estructura jerárquica:** el mundo real tiene estructura de composición — un objeto está formado por partes, que están formadas por formas más simples. Una sola capa no puede explotar esta jerarquía; todas las relaciones deben aprenderse simultáneamente.
3. **Generalización:** redes muy anchas con pocos datos tienden a sobreajustar. La profundidad actúa como un regularizador implícito.

### Motivación para la Profundidad

- **Composición de funciones simples:** cada capa aprende una transformación del espacio de representación. Las capas sucesivas construyen abstracciones progresivamente más complejas — análogo al razonamiento humano: de lo concreto a lo abstracto.
- **Evidencia empírica en visión por computadora:**
  - Capa 1 → bordes y gradientes de color
  - Capa 2 → texturas y esquinas
  - Capa 3 → partes de objetos
  - Capa 4+ → objetos completos y conceptos
- La profundidad transforma representaciones **no linealmente separables** en **linealmente separables** — la capa de salida solo necesita hacer una separación lineal final.
