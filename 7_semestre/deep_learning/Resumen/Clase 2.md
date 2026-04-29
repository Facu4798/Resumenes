<p align="center" style="font-size: 40px; font-weight: bold;">
Clase 2 — Unidad II: Red Perceptrón Multicapa
</p>


## 1. Redes Neuronales y MLP

Una **red neuronal** es un sistema de procesamiento paralelo, masivo y distribuido formado por unidades simples que adquieren conocimiento mediante entrenamiento y lo almacenan en sus pesos.

Tipos principales: MLP, Redes Convolucionales (CNN), Redes Recurrentes (RNN), Transformers.

### Red Perceptrón Multicapa (RPMC / MLP)

También llamadas **Feedforward** o **Redes Densas**. Sus características:

- Constituidas por capas de perceptrones conectadas secuencialmente.
- Dos capas consecutivas están **completamente conectadas** (fully connected):
- Tres tipos de capas:
  1. **Capa de entrada:** recibe el vector de entrada.
  2. **Capas ocultas:** una o más capas intermedias; aquí ocurre el procesamiento.
  3. **Capa de salida:** produce el vector de salida de la red.(probabilidades)

Una **red shallow** tiene exactamente una capa oculta entre la entrada y la salida.


## 2. El Perceptrón

Recibe varias entradas, las combina linealmente con sus pesos y aplica una función de activación:

$$y = f\!\left(\sum_{i=0}^{n} w_i x_i\right) = f(\mathbf{w}^T \mathbf{x})$$

donde $x_0 = 1$ es el término de bias, $w_0$ su peso, y $f$ es la **función de activación**.

> La función de activación **debe ser no lineal**. Si fuera lineal, toda la red —sin importar cuántas capas tenga— sería una transformación lineal. La no linealidad permite aprender relaciones complejas.



## 3. Funciones de Activación

La elección de la función de activación ha sido uno de los factores más determinantes en la evolución del Deep Learning.

### 3.1 Sigmoide

- Rango: $(0, 1)$ — gradiente máximo de solo $0.25$ en $x=0$.
- Históricamente fue la primera función diferenciable usada en redes profundas.

**Problemas en redes profundas:**
1. **Vanishing gradient:** la derivada se aplana rápidamente para  $|x|>3$. Al encadenar muchas capas, el gradiente se multiplica en cada una y desaparece exponencialmente — las capas iniciales casi no aprenden (actualización minima) → todo el aprendizaje se concentra en las capas finales. 
2. **Salida no centrada en 0:** al ser positiva, los gradientes de los pesos de la capa siguiente tienen el mismo signo. Hace que los parametros avancen en *zigzag*.
3. **Costo computacional:** es mas costosa que ReLU.

**Cuándo se usa aún:** capa de salida para clasificación binaria, *gates* de LSTMs, *attention weights*.



### 3.2 Tangente Hiperbólica (tanh)

- Rango: $(-1, 1)$ — **centrada en 0**, a diferencia de la sigmoide. evita *zigzag*
- Gradiente máximo de $1.0$ en $x=0$ — mayor que el de la sigmoide, entrena más rápido.

**Problema que comparte con la sigmoide:** sigue saturando para $|x| > 2$ — hay vanishing gradient en redes muy profundas, aunque menos grave que con la sigmoide.

**Uso actual:** *cell state* y *output gate* en LSTMs/GRUs; redes shallow con salida en $(-1, 1)$.



### 3.3 ReLU (Rectified Linear Unit)

$$\text{ReLU}(x) = \max(0, x)$$


**Ventajas:**
- **No satura para $x > 0$:** la derivada es  1 en la zona activa — el gradiente no se encoge en backpropagation.
- **Sparse activation:** cada sample activa neuronas distintas. Esto separa mejor los conceptos en el espacio de activaciones.
- **Eficiencia computacional:** solo una comparación — es trivial en GPU.

**Problema: neuronas muertas.** Una neurona queda "muerta" cuando su preactivación es negativa para *todas* las muestras. En ese caso su salida es siempre 0 y su gradiente es siempre 0 → los pesos nunca se actualizan.

**Causas comunes:** learning rate muy alto, inicialización incorrecta de pesos, datos con alta varianza sin normalizar.
- Un 10–50% de neuronas inactivas es normal y hasta útil.
- Si >80% están muertas se produce un *capacity collapse*: la red ya no puede representar adecuadamente los datos.

**Soluciones:**
- **Leaky ReLU:** permite una pequeña pendiente para $x < 0$.
- **ELU:** curva exponencial para $x < 0$. Inicialización cuidadosa para mantener $\hat{y} \approx 0$.
- **Batch Normalization:** mantiene las activaciones en rango activo.

### 3.6 GELU (Gaussian Error Linear Unit)

Multiplica la entrada $x$ por la probabilidad de que $x$ sea mayor que una variable aleatoria normal — de ahí el nombre "Gaussian Error".


### ¿Por qué GELU y SiLU superan a ReLU?

1. **Suavidad ($C^\infty$):** gradientes suaves en toda la recta real. 
2. **No monotonía:** el pequeño valle negativo añade curvatura extra — la red puede representar más funciones sin necesitar más parámetros.
3. **Gradiente siempre no nulo:** no hay zona donde el gradiente sea exactamente 0 (excepto $x \to -\infty$), eliminando el problema de neuronas muertas.
4. **Derivada puede superar 1:** alrededor de $x \approx 1.5$, la derivada es $\approx 1.1$, lo que facilita el flujo de gradientes en redes muy profundas. Esto contrasta con la sigmoide (máximo 0.25) o la tanh (máximo 1.0).



### Tabla Comparativa de Funciones de Activación

| Función | Rango | Centrada en 0 | Satura | Grad. máx. | Uso principal |
|---|---|---|---|---|---|
| Sigmoide | $(0,1)$ | No | Ambos lados | $0.25$ | Clasificación binaria, LSTM gates |
| Tanh | $(-1,1)$ | Sí | Ambos lados | $1.0$ | LSTM/GRU, redes shallow |
| ReLU | $[0,\infty)$ | No | $x<0$ muerto | $1.0$ ($x>0$) | CNNs, MLPs clásicos |
| Leaky ReLU | $(-\infty,\infty)$ | $\approx$ Sí | No | $1.0$ | Alternativa a ReLU |
| ELU | $(-\alpha,\infty)$ | $\approx$ Sí | $x\to-\infty$ | $1.0$ | Redes medianas, tabular |
| GELU | $\approx(-0.17,\infty)$ | $\approx$ Sí | $x\to-\infty$ | $\sim 1.1$ | Transformers (BERT, GPT) |
| SiLU/Swish | $\approx(-0.28,\infty)$ | $\approx$ Sí | $x\to-\infty$ | $\sim 1.1$ | YOLO, EfficientNet |

**Sobre la saturación:** una función satura cuando su derivada tiende a 0 para $|x|$ grande. La saturación frena el aprendizaje porque los gradientes desaparecen.

**Sobre el centrado en 0:** si la función produce siempre valores positivos los gradientes, se produce *zigzag*. La solución práctica es usar **Batch Normalization** después de cada capa, que normaliza las activaciones a media ≈ 0 — esta es la razón por la que ReLU funciona bien en la práctica pese a no estar centrada.

**Sobre el costo computacional:** En todas las funciones son despreciables comparadas con el costo de multiplicar matrices. < 5% del tiempo de foward pass.

### Vanishing Gradients — Soluciones Modernas

| Solución | Cómo ayuda |
|---|---|
| ReLU y variantes | Derivada = 1 en zona activa, no se encoge al propagarse |
| Residual connections (ResNet) | Camino alternativo (*bypass*) que preserva el gradiente intacto |
| Batch Normalization | Mantiene las activaciones en la zona donde la función no satura (hacer Z sobre cada feature)|



## 4. Teorema de Aproximación Universal

> **(Cybenko, 1989; Hornik, 1991):** Una red neuronal *shallow* con suficientes neuronas ocultas y una función de activación no lineal continua puede aproximar cualquier función continua.


**Implicación práctica:** en principio, una sola capa oculta es *suficiente* para representar cualquier función (si tiene suficientes neuronas). Para algunas funciones, una red shallow necesita exponencialmente más neuronas que una red profunda para la misma precisión. El teorema garantiza **existencia**, no **eficiencia**.



## 5. Entrenamiento: Funciones de Pérdida

El entrenamiento consiste en ajustar todos los pesos de la red para que sus predicciones se acerquen lo más posible a los valores reales del dataset. La **función de pérdida** mide la diferencia entre las predicciones y los valores reales - guía el entrenamiento.


### Binary Cross-Entropy (BCE)
Se usa en clasificación binaria junto con función sigmoide.

- **Penaliza fuertemente las predicciones *seguras pero incorrectas*:** los terminos logarítmicos hacen que la pérdida tienda a infinito cuando el modelo asigna probabilidad baja a la clase correcta.
- **Continua y diferenciable:** compatible con optimización por gradiente.
- **Interpretación probabilística:** equivale al negativo del logaritmo de la probabilidad asignada a la clase correcta.
- **Sensible al desbalance de clases**


### Categorical Cross-Entropy (CCE)

Extensión de BCE para múltiples clases. Se usa junto con función **softmax**.

- Las etiquetas deben estar en formato **one-hot encoding**
- Solo el término correspondiente a la **clase correcta** contribuye a la pérdida¿
- **Penaliza fuertemente las predicciones incorrectas y seguras.**
- **Continua y diferenciable:** compatible con optimización por gradiente.

### Regresión — MSE, MAE y Huber


**Mean Squared Error (MSE / Pérdida L2):**
- Penaliza los errores grandes de forma cuadrática → **muy sensible a outliers**
- Continua, diferenciable y convexa → optimización estable.
- La magnitud depende de las unidades de la variable objetivo.

**Mean Absolute Error (MAE / Pérdida L1):**
- Usa el valor absoluto de la diferencia → penalización **lineal**. Mas robusta a outliers.
- No es diferenciable en 0 (gradiente indefinido) — en la práctica se usan subgradientes.
- Dependiente de la escala.

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



## 6. Gradient Descent

El descenso por gradiente es el método que se usa para minimizar la función de pérdida. El gradiente de una función en un punto apunta en la dirección de mayor crecimiento; para minimizar, se avanza en la dirección opuesta al gradiente.

### Variantes según el tamaño del batch

| Variante | Cómo calcula el gradiente | Ventaja | Desventaja |
|---|----|----|----|
| **Batch GD** | Todo el dataset a la vez | Gradiente exacto, convergencia estable | Muy lento y costoso en memoria para datasets grandes |
| **Mini-batch GD** | Un subconjunto (ej. 32, 64, 128 muestras) | Balance entre velocidad y estabilidad | Hiperparámetro extra (tamaño del batch) |
| **SGD** (Stochastic GD) | Una sola muestra a la vez | Muy rápido por iteración; puede escapar mínimos locales | Gradiente ruidoso, convergencia errática |

## 7. Backpropagation

Algoritmo para calcular eficientemente el gradiente de la pérdida respecto a *todos* los pesos de la red, aplicando la **regla de la cadena** hacia atrás desde la capa de salida hasta la capa de entrada.

### Idea Central

La red hace dos pasadas:

1. **Forward pass:** se propagan las entradas capa por capa hacia adelante, calculando la salida de cada neurona. Al final se calcula la pérdida.
2. **Backward pass:** se propaga el error hacia atrás, calculando la contribución de cada peso a la pérdida. Se usa la regla de la cadena para descomponer gradientes complejos en productos de derivadas locales.

### Cálculo de los Pesos — Capa de Salida

El peso $w_{oh}$ que conecta la unidad $h$ de la capa oculta con la unidad $o$ de la capa de salida se actualiza como:

$$w_{oh}^{(k+1)} = w_{oh}^{(k)} - \eta \cdot \frac{\partial L}{\partial w_{oh}}$$

donde $\frac{\partial L}{\partial w_{oh}}$ se calcula usando la regla de la cadena y $L$ es la función de pérdida.

### Cálculo de los Pesos — Capa Oculta

El peso $w_{hi}$ que conecta la entrada $i$ con la unidad $h$ de la capa oculta se actualiza como:

$$w_{hi}^{(k+1)} = w_{hi}^{(k)} - \eta \cdot \frac{\partial L}{\partial w_{hi}}$$

Donde $\frac{\partial L}{\partial w_{hi}}$ se calcula usando la regla de la cadena, teniendo en cuenta que el error de la neurona oculta $h$ depende de los errores de todas las neuronas de salida a las que está conectada:

El error de una neurona oculta es la suma de los errores de todas las neuronas de salida a las que está conectada, ponderada por los pesos de esas conexiones, multiplicada por la derivada local de su función de activación. El error "fluye hacia atrás" a través de los pesos.

Las ecuaciones se implementan en forma **matricial** para mayor eficiencia computacional. Los pesos se pueden actualizar:
- Después de presentar **todo** el dataset (batch).
- Después de un **subconjunto** del dataset (mini-batch).
- Después de **cada ejemplo** individual (SGD).



## 8. Shallow vs. Deep: Capacidad de Representación

### ¿Qué mide la "capacidad" de una red?

- **¿Cuantas regiones lineales puede crear?** (con ReLU) H + 1 en 1D, pero exponencial en profundidad.
- **Número de parámetros vs capacidad**: una red con $P$ parámetros puede generar $O(P)$ regiones lineales si es shallow, pero $O(2^P)$ si es profunda.

### Limitaciones de las Redes Shallow

1. **Ineficiencia de parámetros:** para representar funciones compuestas una red shallow necesita exponencialmente más neuronas que una red profunda.
2. **No captura estructura jerárquica:** el mundo real tiene estructura de composición. Una sola capa no puede explotar esta jerarquía; todas las relaciones deben aprenderse simultáneamente. Las redes profundas aprenden estructuras de forma natural.
3. **Generalización:** redes muy anchas con pocos datos tienden a sobreajustar. La profundidad actúa como un regularizador implícito.

### Motivación para la Profundidad

- **Composición de funciones simples:** cada capa aprende una transformación del espacio de representación. Las capas sucesivas construyen abstracciones progresivamente más complejas
- **Evidencia empírica en visión por computadora:**
  - Capa 1 → bordes y gradientes de color
  - Capa 2 → texturas y esquinas
  - Capa 3 → partes de objetos
  - Capa 4+ → objetos completos y conceptos
- La profundidad transforma representaciones **no linealmente separables** en **linealmente separables** 
