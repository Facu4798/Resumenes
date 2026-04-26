<p style="font-size: 30px; text-align: center; font-weight: bold;">Clase 1</p>

# Modelo tradicional - relacional
- Estructura de tablas y filas
- Los valores en una tupla relacional deben ser simples => no se permiten valores anidados.
- Requieren un esquema rigido predefinido

## El problema de la impedancia
"impedance mismatch" se refiere a la diferencia entre los modelos de datos relacionales simples y las estructuras de datos en memoria (como OOP). 

- **Discrepancia estructural**: Un objeto moderno tiene que ser dividido en varias filas y tables, requiriendo ser traducido constantemente.
- **Costos de productividad:** Se desperdicia esfuerzo haciendo aplicaciones para traducir objeto y RDBMS. aumenta la complejidad y baja el rendimiento y productividad.



|Caracteristica|Relacional|No Relacional(documentos)|
|-----------|------------|---------------------|
| Esquema   | Rigido, predefinido | No estructurado, flexible |
| Escalabilidad | Vertical (UP) | Horizontal (OUT) |
| Consistencia | Fuerte (ACID) | Eventual (BASE) | 
|Relaciones(joins)| Excelete para multiples joins | Se debe embeber datos. joins caros | 


|Caracteristica|Relacional|No Relacional(objetos)|
|-----------|------------|---------------------|
Modelo de datos|Tablas con filas y columnas|Objetos que soportan encapsulamiento, herencia y polimorfismo|
Lenguaje de consulta|SQL|Lenguajes de consulta propietarios|
Manejo de datos|Bueno para datos estructurados, consistencia y consultas ad-hoc|Bueno para datos complejos y relaciones intrinsecas|
Integración|Requiere una capa de traducción->impedance mismatch|Integración con OOP |
Popularidad|Gran adopción y herramientas|Menos popular y herramientas limitadas|

## Escalado
**Vertical: UP**
- Mas costoso 
- Aumentos de CPU, RAM, etc. en un solo servidor
- Eventualmente se llega a un límite físico

**Horizontal: OUT**
- Menos costoso
- Agregar más servidores para distribuir segun demanda
- Capacidad infinita de crecimiento
- Requiere que el sistema pueda manejar la distribución de datos

### Problemas de los RDBMS
Fueron diseñados para escalar verticalmente. Hacer consultas complejas en un sistema distribuido puede resultar en:
- Single point of failure: falla en un nodo puede afectar a todo el sistema
- Requerimiento de sharding manual: dividir datos en partes para distribuir, lo que puede ser complejo y propenso a errores
- Perdida de consultas entre shards
- Perdida de la integridad referencial: no se pueden garantizar relaciones entre datos distribuidos

### Bases de datos NoSQL
- Diseñadas para escalar horizontalmente
- Transacciones con consistencia eventual:(BASE)
- Teorema CAP: solo se pueden garantizar dos de las tres propiedades: Consistencia, Disponibilidad y Tolerancia a particiones

# NoSQL (Not Only SQL)
- Flexible / Schema-less: estructuras dinamicas con campos añadidos sobre la marcha
- Horizontalmente escalable
- Performante: Optimizaciones para casos de uso (patrones) específicos
- Arquitectura distribuida: clusters en la nube con tolerancia a fallos

# Teorema CAP
- Consistencia: cada lectura devuelve el valor mas reciente o un error(mismos datos en todos los nodos)
- Disponibilidad: cada solicitud recibe una respuesta sin garantía de que sea la mas reciente (sin error)
- Tolerancia a particiones: el sistema sigue funcionando a pesar de la pérdida o encolamiento de mensajes entre nodos

*MongoDB es CP. puede ocurrir un "split brain" cuando la red se divide y los nodos pierden contacto. en este caso el nodo primario se aisla y no puede aceptar escrituras, protegiendo la consistencia hasta que se elija un nuevo primario.*

*en bases de datos en memoria, se realizan flushes como checkpoints en disco. la consistencia se garantiza al escribir en disco*


**Parametros ajustables:**
- $R$(Responses required) = número de réplicas que deben responder para una lectura exitosa
- $W$(Acks required) = número de réplicas que deben confirmar una escritura exitosa
- $N$ = factor de replicación
- $R/W$ = numero de nodos que deben responder para una lectura/escritura exitosa

Se debe cumplir:
- para la escritura: $W > N/2$ para garantizar que la mayoría de los nodos tengan la escritura
- para la lectura: $R + W > N$ 
- 
# Bases de datos documentales
Usa documentos: Estructura de datos jerarquicos que contienen mapas, colleciones y valores escalares que son similares entre si pero no necesariamente iguales.

# Bases de datos clave-valor
El modelo NoSQL mas simple. datos almacenados como un blob asociado a una clave unica. Operaciones ultrarrapidas(GET, PUT, DELETE).


# Bases de datos de grafos
Almacenan datos como nodos y conexiones entre ellos (Relaciones persistidas fisicamente). 


# Bases de datos de familias de columnas
Almacenan datos en grupos relacionados que se acceden juntos. Cada fila puede tener un número variable de columnas y un uuid.
*supercolumna: mapa de columnas*

<p style="font-size: 30px; text-align: center; font-weight: bold;">Clase 2</p>

# Conceptos
- **Base de datos:** contenedor fisico para las colecciones con sus propios archivos en disco
- **Colección:** grupo de documentos relacionados, similar a una tabla
- **Documento:** unidad basica de datos. requiere un campo de id unico.

## Anatomía BSON (Binary JSON)
Json es excelente para humanos pero lento para maquinas. aporta:
- **Velocidad de parseo:** salto rapido entre campos
- **Tipos de datos ricos:** fechas, decimales, objectids.
- **Limite de tamaño:** 16MB por documento

## Objectid
proporcionado o generado automaticamente. funciona como pk. pesa 12 bytes. los primeros 4 bytes representan la marca de tiempo unix. *ordenar por id ordena por fecha de creación*

# Operaciones
- **Create:** `insertOne()`, `insertMany()`
- **Read:** `find()`, `findOne()`
- **Update:** `updateOne({field:equals},{$set:{field:value}})`
- **Delete:** `deleteOne({field:equals})`, `deleteMany()`

## Logicos
- **Comparación:** `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`
- **Lógicos:** `$and`, `$or`, `$not`, `$exists`,`$all`
- **Actualización:** `$set`,`$unset`, `$inc`, `$push`, `$pull`

# Tipos de datos
- Numberint(32 bits), NumberLong(64 bits), Decimal128(128 bits)
- Date objects: soportado por bson, es mas eficiente que strings de fecha
- ObjectId: 12 bytes _id


<p style="font-size: 30px; text-align: center; font-weight: bold;">Clase 3</p>

NoSQL permite documentos con diferentes estructuras y tipos de datos en la misma colección(Polymorfismo).

**Buneas prácticas de organización de colecciones:**
- Aplicar indices para agrupar documentos relacionados
- Agrupar documentos relacionados fisicamente (particionamiento).
- Evitar mezclar tipos de documentos en la misma colección

# Relaciones
Al tener un limite de 16MB por documento, se aplican relaciones:
### One-to-Few: 
un usuario a sus direcciones. Se aplica embedding, que aumenta la velocidad pero puede resultar en documentos grandes.
```json
{
    "username": "johndoe",
    "addresses":[
        {"type":"home", "address":"123 Main St"},
        {"type":"work", "address":"456 Office Rd"}
    ]
}
```

### One-to-Many: 
un posteo a sus comentarios. Se aplica referencing, que almacena el id del objeto padre. Requiere consultas de lookup intensas pero mantiene documentos pequeños.
```json
{
    "_id": ObjectId("post_id"),
    "title": "My Post",
    "content": "This is a post."
}
```
```json
{
    "_id": ObjectId("comment_id"),
    "post_id": ObjectId("post_id"),
    "author": "Jane",
    "text": "Great post!"
}
```

### One-to-Squillions:
un servicio a sus logs. Se aplica referencing

# Aggregation framework
Salir del simple `find()` para hacer consultas mas complejas. 

**Pipeline de agregación:**
```
COLLECTION ->  $match  ->    $group    ->   resultados
 (input)      (filtro)    (agrupación)    (output final)
```
- `$match`: filtra documentos según condiciones. va primero por predicate pushdown
- `$group`: agrupa documentos por un campo y aplica operaciones de agregación.
- `$project`: transforma documentos, seleccionando o creando campos.

*MongoDB añadió $lookup que hace un left outer join hacia una colección sin sharding. hace el match como un embedding en el output.*

<p style="font-size: 30px; text-align: center; font-weight: bold;">Clase 4</p>

# Conflictos entre escrituras
| Acercamiento pesimista | Acercamiento optimista |
|-----------------------|-----------------------|
|bloquea el recurso durante la escritura| Permite escrituras concurrentes y resuelve conflictos después|
|previene conflictos pero puede causar bloqueos| Mejora el rendimiento pero requiere logica compleja de resolución de conflictos|

En entornos distribuidos, teniendo un enfoque optimista, se utiliza la consistencia eventual, donde los cambios se propagan a través del sistema con el tiempo, pero permitiendo gran volumen de operaciones concurrentes.

# Conflictos entre escrituras y lecturas
|Read-your-writes|Domain specific stale reads|
|-----------------|-------------------------|
|garantiza que un usuario vea sus propias escrituras inmediatamente| Permite lecturas obsoletas para mejorar el rendimiento en casos donde la frescura de los datos no es crítica|
|se hace desde el mismo nodo | - |
| - | Depende del caso de uso que tanta tolerancia|

# Modelos de distruibución
- **Master-slave:** un nodo primario maneja todas las escrituras y replicas secundarias manejan lecturas. Elimina practicamente conflictos de escritura pero puede causar cuellos de botella y single point of failure.
- **Peer-to-peer:** todos los nodos son iguales y pueden manejar escrituras y lecturas y se sincronizan entre si. Elimina el single point of failure pero requiere mecanismos complejos de consistencia eventual porque aumentan los conflictos de escritura.


´<p style="font-size: 30px; text-align: center; font-weight: bold;">Clase 5</p>


bucket pattern= continuation pattern

incremental schema migration se hace con lazy execution, a medida que los nodos se liberan.