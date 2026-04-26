<p align="center" style="font-size: 40px; font-weight: bold;">
Clase 4 (Unidad 3 - Diapositiva 1 a ??)
</p>


*problema: en una MLP cada pixel se trata como una entrada, no capturan estructuras -> muchos parametros -> entrenamiento lento*

**Motivación:**
- Que se compartan pesos: el mismo detector de bordes se puede usar en toda la imagen
- Localidad: cada neurona procesa solo una región (receptive field)
- Invariancia traslacional: un gato es un gato esté donde esté
**Solución´:**
- Aplicar el mismo filtro deslizando sobre toda la imagen
- Parámetros: solo el filtro (3x3 = 9 pesos) reutilizado
- CNN: parámetros independientes del tamaño de la imagen


# Redes Convolucionales
Especializada en el procesamiento de datos con estructura de cuadrícula
- Series de tiempo (1D sigue siendo una cuadrícula)
- Imágenes (2D)

# Convolución
$$A^{rXc} \cdot F^{kXk} = B^{(r-k+1)X(c-k+1)}$$

Esto reduce los tamaños de las imagenes, quitando bordes, ya que los pixeles de las esquinas se suelen utilizar menos.

## Padding
Agrega ceros alrededor de la imagen para mantener el tamaño después de la convolución. Esto se hace para que la imagen no se reduzca después de cada capa convolucional.

- **Valido(valid)**: sin padding, la imagen se reduce
- **Igual(same)**: padding para mantener el mismo tamaño

**Tipos de relleno:**
- Ceros (zero-padding): el más común, rellena con ceros
- Reflejo (reflect): rellena con una reflexión de la imagen

## Stride
Determina el paso del filtro al deslizarse sobre la imagen. 

$A^{rXc} \cdot F^{kXk}_s = B^{\left\lfloor \frac{r-k+2p}{s} + 1 \right\rfloor \times \left\lfloor \frac{c-k+2p}{s} + 1 \right\rfloor}$

Donde $p$ es el padding.

Stride = 1 da la maxima resolución posible, stride = 2 reduce a la mitad el tamaño de la imagen, etc. El stride asimetrico (2,1) se puede usar para reducir solo una dimensión (utl en audio/series).

# Pooling

- Hace las representaciones más compactas y manejables.
- Ayuda a reducir el sobreajuste
- Trabaja de forma independiente sobre cada feature map.(el feature map es un cubo con cada salida de aplicar cada filtro a la imagen. queda $r\times c\times F$)
- Debe especificarse el teamaño del filtro y el stride, pero no el padding.

## Max Pooling
Divide la feature map en regiones no solapadas y toma el valor máximo (operación fija sin parametros aprendibles).
- Preserva la activación mas fuerte -> "hay un borde aquí"

*Max pool 2X2, stride=2 el el mas comun. reduce r y c a la mitad. el máximo no cambia con pequeñas traslaciones. las dimensiones quedan como convolución sin padding.*

**Actualidad**: esta siendo reemplazado por Conv(stride=2)

## Average Pooling
Calcula el promedio de cada región. Mas suave pero diluye las activaciones fuertes (menos agresivo que max pooling).
- Usado en LeNet-t y GoggleNet

## Global Average Pooling
Caso especial: ventana = tamaño de la feature map. 

(N,F,r,c) -> (N,F,1,1) -> (N,F).

**Ventaja:** 
- Elimina la capa FC(fully connected - densa) final.
- Independiente de la resolución de entrada.
- Regularización implicita: no puede hacer overfit espacialmente.

**Actualidad** ResNet y eficientNet

# Propiedades de la Convolución

## Pesos compartidos
El mismo filtro se aplica en toda la imagen. 
- Parametros de una capa convolucional = $C_{out} \times C_{in} \times k \times k + C_{out}$ (si se incluye bias).
- Parametros de una capa densa = $C_{in} \times h_{in} \times w_{in} \times h_{out} \times w_{out} + C_{out} \times h_{out} \times w_{out}$ (si se incluye bias).

## Localidad
Cada neurona en la feature map esta conectada solo a una región $k \times k$ de la entrada. Cada valor en el feature map de salida se calcula aplicando el filtro a una región.
- En una capa densa, cada neurona esta conectada a toda la entrada.

**Consecuencias prácticas:** Menos parámetros. El modelo aprende detectores locales en vez de depender de pixeles arbitrariamente distantes.

## Equivarianza traslacional
Si la entrada se traslada, la feature map se traslada en la misma cantidad. $f(T(x)) = T(f(x))$.

## Composición jerarquica
- Capas tempranas detectan características simples (bordes, gradientes).
- Capas profundas combinan patrones simples -> detectores de objetos complejos.
- Esto sale automáticamente del entrenamiento.

# Entrada multicanal
**Filtros:**
- Un filtro tiene forma $C_{in} \times k \times k$. Para una imagen RGB, $C_{in}=3$. El filtro se aplica a todos los canales a la vez.
- Con $C_{out}$ filtros, el tensor de pesos es $C_{out} \times C_{in} \times k \times k$.
- Salida: $(N, C_{out}, r_{out}, c_{out})$

**Feature maps:**
- Cada $C_{out}$ canales de salida es un feature map
- Representa la respuesta de un filtro en cada posición.
- Alta activación = el patrón del filtro está presente en esa región.

**Visualización**
- Primeras capa: feature maps $\approx$ imagenes en escala de grises filtradas.
- Capas profundas: feature maps son abstractos, difíciles de interpretar 

# Receptive field(RF)
Región de la entrada original que afecta a una neurona.
- En la práctica solo el centro del RF tiene influencia fuerte
- Las neuronas en el borde tienen gradientes casi nulos

**¿Por qué cada capa suma k-1 al RF?**
explicar despues

## ¿Por qué filtros pequeños?
- 2 Capas Conv(3x3) tienen RF de 5x5, igual que una capa Conv(5x5), pero con menos parametros y mas no linealidades.
- Todos los modelos modernos siguien este principio excepto "stem" con Conv(7x7, stride=2) en la primera capa y despues Conv(3x3).

## Convoluciones dilatadas
**Motivación:** Produce RF grande sin reducir la resolución y sin mas parametros.

**Mecanismo:** 
Inserta $d-1$ ceros entre elementos adyacentes del filtro.
- Con $k=3$ el RF es $2d + 1$. el estandar es $d=1$ (sin dilatación)

**Aplicaciones:** DeepLab usa multiples tasas de dilatación en paralelo. Segmentación semantica preserva resolución mientras amplia RF.

## Convoluciones depthwise separables
**Motivación:** Una Conv($C_{in}\to C_{out}, k\times k$) opera en espacio y canales a la vez. Separar estas operaciones puede reducir drásticamente los parametros y el costo computacional.

**Depthwise convolution:** 
- Un filtro $k\times k$ por cada canal de entrada
- Parámetros: $C_{in} \times k^2$ (en lugar de  $C_{in} \times C_{out} \times k^2$)

**Pointwise convolution:**
- Conv(1x1) para mezclar canales (equivalente a aplicar una capa FC a cada posición espacial independientemente)
- Parámetros: $C_{in} \times C_{out}$

**Uso de la Conv(1x1) "network in network"**
- Cambiar el numero de canales sin costo espacial
- Reduce el cuello de botella
- Agrega no linealidades entre capas sin aumentar RF
- Parametros = $C_{in} \times C_{out}$ 


# Batch Normalization
*Posición en la red: Estandar: entre Conv y ReLU. Alternativa moderna: Antes de la convolución.*

Para cada canal $C$: normalizar sobre batch y posiciones espaciales:
- Parámetros: $\gamma$ (escala) y $\beta$ (desplazamiento). uno por canal.


# Entrenamiento
Se entrena de extremo a extremo con un conjunto de datos etiquetados.

**Función de pérdida:**
Promedio de la pérdida individual sobre las n muestras.

$$J = \frac{1}{n} \sum_{i=1}^{n} L(\hat{y}^{(i)}, y^{(i)})$$

- Función de perdida(i): entropía cruzada para clasificación, MSE para regresión.
- Optimización con descenso por gradiente(SGd,Adam,AdamW). Backpropagation fluye a travez de todas las capas, con la misma regla de la cadena.

*Imagenet: base de datos para entrenar modelos de visión. 1000 clases, 1.2 millones de imágenes de train, 50k de validación, 100k de test.*