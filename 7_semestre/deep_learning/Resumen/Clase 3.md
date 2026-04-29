<p align="center" style="font-size: 40px; font-weight: bold;">
Clase 3 (Unidad 2 — Diapositiva 76 a 118)
</p>


## 1. Backpropagation

**Observación práctica:** una red más profunda y estrecha suele generalizar mejor que una más ancha y shallow con el mismo número de parámetros distribuido en más capas.

**Objetivo:** actualizar los parámetros de una red para reducir la función de pérdidas.

### ¿Cómo calcular el gradiente para cada capa?

- La pérdida depende de la salida, que depende de la última capa, que depende de la penúltima, y así sucesivamente.
- Se aplica la **regla de la cadena** al grafo computacional para propagar la señal de error desde la salida hacia los pesos de las primeras capas.
- **Complejidad computacional:** $O(\text{parámetros})$ — igual que un forward pass.

### Dos operaciones principales

1. **Forward pass:** calcular y guardar las activaciones de cada capa.
2. **Backward pass:** propagar gradientes desde la salida hacia la entrada.

### Backpropagación Vectorizada

En la práctica se trabaja con matrices (batches de muestras). La notación estándar usa:

- $A^l$ — activaciones de la capa $l$ para el batch.
- $W^l$ — pesos de la capa $l$.
- $\delta^l$ — gradiente de la pérdida respecto a las preactivaciones de la capa $l$.

**Forward pass** (guardar activaciones):

$$Z^l = W^l A^{l-1} + b^l, \qquad A^l = f(Z^l)$$

**Backward pass** (propagar gradientes):

- Propagación del error hacia la capa anterior ($\odot$ = Hadamard):

$$\delta^l = (W^{l+1})^T \delta^{l+1} \odot f'(Z^l)$$

- Gradiente respecto a pesos y bias:

$$\frac{\partial L}{\partial W^l} = \delta^l (A^{l-1})^T, \qquad \frac{\partial L}{\partial b^l} = \sum_{\text{batch}} \delta^l$$

**Actualización (Gradient Descent):**

$$W^l \leftarrow W^l - \eta \frac{\partial L}{\partial W^l}, \qquad b^l \leftarrow b^l - \eta \frac{\partial L}{\partial b^l}$$



## 2. Implementación de un MLP en PyTorch

### `nn.Module` — La Base de PyTorch DL

`nn.Module` es la clase base para todos los modelos en PyTorch. Responsabilidades:

- Contiene los parámetros del modelo (`nn.Parameter`).
- Define el grafo computacional en `forward()`.
- Gestiona sub-módulos jerárquicamente (`.children()`, `.modules()`).
- Permite mover el modelo entre dispositivos (`.to(device)`, `.cuda()`).
- Alternancia entre modos entrenamiento y evaluación (`.train()`, `.eval()`).
- Serialización: guardar y cargar pesos (`.state_dict()`, `.load_state_dict()`).

### Capas predefinidas más comunes

- `nn.Linear(in, out)`: capa completamente conectada.
- `nn.ReLU()`, `nn.GELU()`, `nn.SiLU()`: funciones de activación.
- `nn.BatchNorm1d(features)`: batch normalization.
- `nn.Dropout(p)`: dropout.
- `nn.Sequential`: apila capas en orden secuencial.



## 3. Regularización

Las redes profundas tienen millones de parámetros → alto riesgo de **overfitting**.

### Trade-off Bias-Varianza en DL

- **Underfitting (alto bias):** modelo demasiado simple, error alto en train y test.
- **Overfitting (alta varianza):** memoriza el training set, falla en test.

**Señales de overfitting:**
- Brecha grande entre train loss y validation loss.
- Validation loss sube mientras train loss sigue bajando.
- Alta accuracy en train, baja en validation.

**Estrategias de regularización:**
- Restricción de parámetros: L1/L2 weight decay.
- Ruido durante entrenamiento: Dropout.
- Normalización de activaciones: Batch Norm, Layer Norm.
- Data augmentation.
- Early stopping: parar cuando `val_loss` deja de mejorar.

### 3.1 Regularización L2 — Weight Decay

Se añade un término $\frac{\lambda}{2}\|W\|_F^2$ a la función de pérdida, donde $\lambda$ es el coeficiente de regularización (hiperparámetro).

El gradiente regularizado produce un factor multiplicativo $(1 - \eta\lambda)$ en la actualización — de ahí el nombre **weight decay**: los pesos se reducen ligeramente en cada paso.

**Interpretación:** penaliza pesos grandes, fuerza soluciones suaves y generalizables.

### 3.2 Regularización L1 — Sparsity

Se añade el término $\lambda \|W\|_1$ a la pérdida. El gradiente L1 es constante (no depende del tamaño del peso), lo que empuja los pesos **exactamente a cero** → soluciones **sparse**.

En contraste, L2 reduce los pesos pero rara vez los lleva a exactamente cero.

### 3.3 Comparativa L1 vs L2

| | L1 | L2 |
|---|---|---|
| Efecto sobre los pesos | Exactamente a 0 (sparse) | Pequeños pero no nulos |
| Estabilidad con SGD | Menos estable | Más estable |
| Uso en DL | Poco frecuente (más común en Lasso) | Estándar en casi todos los modelos |



## 4. Dropout (Srivastava et al., 2014)

### Mecanismo

- **Durante entrenamiento:** cada neurona se desactiva independientemente con probabilidad $p$. Las neuronas activas se escalan por $\frac{1}{1-p}$ para mantener la esperanza.
- **Durante evaluación:** todas las neuronas activas — no hay dropout.

```python
model.train()  # activa el dropout
model.eval()   # desactiva el dropout — ¡no olvidarlo!
```

### ¿Por qué funciona? — Interpretaciones

1. **Ensemble:** entrena simultáneamente $2^n$ sub-redes — la evaluación es el promedio implícito.
2. **Ruido:** añade ruido aleatorio que previene la co-adaptación de neuronas.
3. **Robustez:** la red aprende a no depender de ninguna neurona específica.

**Tasas típicas:** capas densas $p \approx 0.5$, capas de entrada $p \approx 0.2$.



## 5. Batch Normalization (Ioffe & Szegedy, 2015)

### Problema que resuelve: Internal Covariate Shift

La distribución de activaciones de cada capa cambia durante el entrenamiento → las capas posteriores deben adaptarse constantemente → frena el entrenamiento y requiere learning rates pequeños.

### Beneficios

- Permite learning rates más grandes → entrenamiento más rápido.
- Regularización implícita → menos necesidad de dropout.
- Reduce sensibilidad a la inicialización.

**¿Antes o después de la activación?**
- **Original (Ioffe & Szegedy):** BN antes de la activación.
- **Pre-Norm (práctica moderna):** BN antes de cada bloque, activación después.

### Algoritmo — por batch y por feature

1. Media del mini-batch ($N$ muestras): $\mu_B = \frac{1}{N}\sum x_i$
2. Varianza del mini-batch: $\sigma^2_B = \frac{1}{N}\sum (x_i - \mu_B)^2$
3. Normalización ($\varepsilon$ para estabilidad numérica): $\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma^2_B + \varepsilon}}$
4. Escalado y desplazamiento con parámetros aprendibles $\gamma, \beta$: $y_i = \gamma \hat{x}_i + \beta$

### Detalles importantes

- **Durante entrenamiento:** $\mu$ y $\sigma^2$ se calculan sobre el mini-batch actual; se acumula un *running mean* y *running var* (media exponencial móvil).
- **Durante evaluación (`model.eval()`):** se usan los *running* acumulados. Si se olvida llamar a `model.eval()`, BN usa las stats del batch de test → resultados incorrectos.
- $\gamma$ y $\beta$ se inicializan en 1 y 0 respectivamente.

**Limitación principal:** depende del tamaño del batch — batch pequeño → estimaciones ruidosas. Con `batch_size=1` es totalmente inestable. Alternativa: **Layer Normalization**.



## 6. Layer Normalization (Ba et al., 2016)

### Diferencia clave con Batch Norm

- **BN** normaliza a través del batch (dim=0): calcula $\mu, \sigma$ sobre las $N$ muestras.
- **LN** normaliza a través de los features (dim=-1): calcula $\mu, \sigma$ **por cada muestra**.

### Ventajas sobre Batch Norm

- Independiente del tamaño del batch — funciona con `batch_size=1`.
- Idéntico en training y evaluation — sin modo dual.
- Estándar en todos los Transformers (BERT, GPT, ViT).

### ¿Cuándo usar cuál?

| | Batch Norm | Layer Norm |
|---|---|---|
| Arquitectura | CNNs, MLPs con batch grande | Transformers, RNNs, NLP |
| Depende del batch | Sí | No |
| Modo dual train/eval | Sí | No |



## 7. Gradient Descent — Optimizadores

### 7.1 SGD básico — Limitaciones

- Muy sensible al learning rate.
- Misma LR para todos los parámetros — ineficiente.
- Oscila en valles alargados.

**Problemas:**
- **Saddle points:** más comunes que mínimos locales en alta dimensión.
- **Ravines:** curvatura alta en una dirección, baja en otra → zigzag lento.
- **Plateaus:** gradientes casi nulos durante largas regiones.

### 7.2 SGD con Momentum

**Velocidad** — media exponencial móvil del gradiente:

$$v_t = \beta v_{t-1} + (1-\beta)\nabla L$$

**Actualización:**

$$\theta \leftarrow \theta - \eta v_t$$

**Intuición:** la pelota acumula velocidad cuesta abajo. En direcciones consistentes, la velocidad aumenta; en direcciones oscilantes, se cancela → reduce el zigzag.

- $\beta = 0.9$ es el valor estándar.
- Permite usar un LR mayor que sin momentum.

### 7.3 RMSprop (Hinton, 2012)

Media exponencial del cuadrado del gradiente ($\rho \approx 0.9$):

$$E[g^2]_t = \rho E[g^2]_{t-1} + (1-\rho) g_t^2$$

$$\theta \leftarrow \theta - \frac{\eta}{\sqrt{E[g^2]_t + \varepsilon}} g_t$$

**Efecto:** LR grande para parámetros con gradientes pequeños y viceversa → LR adaptativa por parámetro.

**Cuándo usar:** útil para RNNs (gradientes muy variables en el tiempo). En la práctica, Adam (que combina momentum + RMSprop) es más popular.

### 7.4 Adam — Adaptive Moment Estimation (Kingma & Ba, 2014)

El optimizador más usado en DL. Combina momentum (primer momento) con RMSprop (segundo momento).

**Algoritmo:**

- Primer momento: $m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t$ — ($\beta_1 = 0.9$)
- Segundo momento: $v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$ — ($\beta_2 = 0.999$)
- Corrección de bias (importante al inicio): $\hat{m}_t = \frac{m_t}{1-\beta_1^t}$, $\hat{v}_t = \frac{v_t}{1-\beta_2^t}$
- Actualización: $\theta \leftarrow \theta - \frac{\eta}{\sqrt{\hat{v}_t} + \varepsilon}\hat{m}_t$

**Hiperparámetros por defecto** (rara vez se cambian): $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\varepsilon = 10^{-8}$, $\eta = 10^{-3}$.

### 7.5 AdamW — Adam con Weight Decay Correcto (Loshchilov & Hutter, 2019)

**El problema con Adam + L2:** añadir $\lambda\|W\|^2$ a la pérdida e incluirlo en el gradiente no equivale a weight decay puro — el L2 queda amortiguado por $\sqrt{\hat{v}_t}$, por lo que distintos parámetros reciben decay diferente.

**La corrección:** separar el weight decay de la actualización de Adam:

$$\theta \leftarrow \theta - \eta\left(\frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \varepsilon} + \lambda\theta\right)$$

El weight decay actúa directamente sobre $\theta$, independientemente de la escala adaptativa.

**Impacto práctico:** AdamW generaliza significativamente mejor que Adam con L2. Es el estándar en GPT, BERT, ViT, ResNet modernos, YOLO.

**Guía de uso:**
- Empezar siempre con AdamW.
- `weight_decay`: 0.01–0.1 para modelos grandes; 1e-4 para modelos pequeños.

### 7.6 Comparativa de Optimizadores

| Optimizador | LR adaptativa | Momentum | Weight Decay | Uso típico |
|---|---|---|---|---|
| SGD | No | Opcional | Vía L2 | CNNs clásicas, ImageNet |
| SGD+Nesterov | No | Sí | Vía L2 | CV con batch grande |
| RMSprop | Sí | No | Vía L2 | RNNs, RL |
| Adam | Sí | Sí | Problemático | NLP, atención, prototipos |
| **AdamW** | Sí | Sí | ✓ Correcto | **Estándar moderno** |

**Recomendación práctica:** AdamW como punto de partida en prácticamente todos los proyectos. SGD+momentum para CNNs en visión con LR scheduling agresivo (OneCycle, Cosine).



## 8. Learning Rate Scheduling

**¿Por qué no usar un LR fijo?**
- LR grande al inicio → converge rápido pero oscila cerca del mínimo.
- LR pequeño al inicio → muy lento, puede quedarse atrapado en plateaus.
- **Solución:** LR grande al inicio, reducir progresivamente al acercarse al mínimo.

### Estrategias principales

- **Step decay:** reducir LR por un factor cada $k$ épocas.
- **Cosine Annealing:** LR sigue un coseno de $\eta_{max}$ a $\eta_{min}$.
- **OneCycleLR:** aumentar hasta $\eta_{max}$ y luego bajar (Smith, 2019).
- **Warmup lineal:** LR crece linealmente de 0 a $\eta_{max}$ en los primeros steps.
- **ReduceLROnPlateau:** reduce LR cuando la `val_loss` no mejora.

### Warmup + Cosine Decay (estándar en Transformers y ViT)

- **Fase 1 (warmup):** LR crece linealmente de 0 a $\eta_{max}$ en $T_\text{warmup}$ steps.
- **Fase 2:** LR sigue coseno decreciente hasta $\eta_{min}$.

> Evita inestabilidad al inicio cuando los pesos aún son aleatorios.



## 9. Inicialización de Pesos

### ¿Por qué importa?

- **Pesos demasiado grandes:** activaciones explotan → saturación o gradientes explosivos.
- **Pesos demasiado pequeños:** activaciones se desvanecen → vanishing gradients.
- Redes de 10+ capas con pesos aleatorios $\mathcal{N}(0,1)$: entrenamiento imposible sin BN.

**Objetivo:** la varianza de las activaciones (y de los gradientes) debe mantenerse aproximadamente constante capa a capa.

### Inicialización He / Kaiming (He et al., 2015)

Diseñada específicamente para ReLU y variantes. Compensa el factor $\frac{1}{2}$ de ReLU (≈ 50% de neuronas desactivadas):

$$\text{Var}(W) = \frac{2}{fan\_in}$$

- **Distribución normal He:** $W \sim \mathcal{N}\!\left(0,\, \sqrt{\tfrac{2}{fan\_in}}\right)$
- **Distribución uniforme He:** $W \sim \mathcal{U}\!\left(-\sqrt{\tfrac{6}{fan\_in}},\, \sqrt{\tfrac{6}{fan\_in}}\right)$



## 10. Gradient Flow — Diagnóstico y Sanity Checks

### 10.1 Diagnóstico del Flujo de Gradientes

**¿Qué monitorear?**
- Norma del gradiente por capa.
- Histograma de gradientes: distribución por capa y por época.
- Ratio gradiente/peso: debe ser $\approx 10^{-3}$.

**Señales de vanishing gradient:**
- Las primeras capas tienen gradientes órdenes de magnitud menores que las últimas.
- La pérdida no disminuye aunque el modelo tenga capacidad suficiente.
- Los pesos de las primeras capas no cambian entre épocas.

**Señales de exploding gradient:**
- La pérdida diverge (NaN o Inf).
- Los pesos crecen sin control entre épocas.
- **Solución:** gradient clipping — $g_t \leftarrow g_t \cdot \frac{\text{max\_norm}}{\|g_t\|}$

**Herramienta:** W&B tiene gradient histograms en tiempo real durante el entrenamiento.

### 10.2 Sanity Checks — Antes de Entrenar

Antes de lanzar un entrenamiento largo, verificar que todo funciona correctamente:

| Check | Qué hacer | Resultado esperado |
|---|---|---|
| **1. Pérdida inicial** | Verificar valor inicial con softmax | $\approx \log(K)$ para $K$ clases (ej. MNIST: ≈2.30) |
| **2. Overfit en batch pequeño** | Entrenar solo en 5–20 muestras muchas épocas | `training_loss ≈ 0` — si no, hay un bug |
| **3. Verificar shapes** | Imprimir shapes de X, y, logits, loss en primer batch | Forward produce la shape esperada |
| **4. Gradient check numérico** | `torch.autograd.gradcheck()` | Gradientes analíticos = diferencias finitas |
| **5. Monitorear primera época** | Observar curva de pérdida en primer batch | Pérdida baja monotónicamente si el LR es correcto |

### 10.3 Diagnóstico — Problemas Comunes

**La pérdida no baja:**
- LR demasiado pequeño → aumentar 10× y ver si hay movimiento.
- Gradientes cercanos a 0 → revisar funciones de activación e inicialización.
- Bug en la pérdida → sanity check con batch pequeño.

**La pérdida diverge o sale NaN:**
- LR demasiado grande → reducir 10×.
- Gradientes exploding → aplicar gradient clipping (`max_norm=1.0`).
- Overflow en `exp()` → usar log-sum-exp trick, revisar softmax con `LogSoftmax`.

**Overfitting:**
- Aumentar dropout, añadir weight decay, reducir capacidad del modelo.
- Data augmentation, más datos.

**Underfitting:**
- Aumentar capacidad: más capas, más neuronas.
- Reducir regularización, entrenar más épocas.
- Revisar si hay bug en el preprocesamiento de datos.

**Entrenamiento lento:**
- Verificar que los datos están en GPU, no solo el modelo.
- Aumentar `batch_size` si la VRAM lo permite.
