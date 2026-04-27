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


<p style="font-size: 30px; text-align: center; font-weight: bold;">Clase 5</p>

# Patrones Estructurales
Patrones para manejar el límite de 16MB por documento, crecimiento ilimitado de arrays y datos dispersos.

## 1. Subset Pattern
**Problema:** Embeber aumenta el tamaño de documento.

**Solución:** Dividir los datos en dos partes:
- **Documento principal:** Contiene solo un subconjunto de los datos (mas rapido)
- **Colección overflow:** El resto vive en documentos en una colección aparte, consultados solo cuando el usuario pide "cargar más".


## 2. Continuation Document Pattern (Bucket Pattern)
Extensión del Subset Pattern para datasets masivos donde incluso el referencing estándar se vuelve costoso. En vez de una sola colección overflow, se estructura la data como una **linked list de documentos**: cada documento contiene un chunk de datos y un campo `next_page` que apunta al siguiente documento de continuación.


- **Índice reducido:** Solo se indexan los documentos "página", no millones de lecturas individuales.
- **Agregación más rápida:** Obtener un día entero = leer 1 documento en vez de 1440.
- **Paginación integrada:** La app navega el historial siguiendo el puntero `next_page`.

## 3. Attribute Pattern
**Problema:** En catálogos de e-commerce, cada categoría tiene atributos distintos (laptops tienen `ram` y `cpu`; ropa tiene `size` y `fabric`). Si se crean campos explícitos para todos los posibles atributos, se generan cientos de claves `null` en cada documento (datos *sparse*). Crear un índice separado por cada atributo posible destruye el rendimiento de escritura y devora RAM.

**Solución:** Convertir los atributos variables en un **array de pares clave-valor** con formato uniforme. Esto permite crear un único índice multikey que cubre absolutamente todos los atributos con una sola instrucción.

```json
// Esquema disperso (MAL: claves nulas desperdiciadas)
{ "name": "ThinkPad", "ram": "16GB", "cpu": "i7", "clothing_size": null, "color": null }

// Attribute Pattern (BIEN: solo atributos relevantes)
{
    "name": "ThinkPad",
    "specs": [
        { "k": "ram", "v": "16GB" },
        { "k": "cpu", "v": "i7" }
    ]
}
```

## 4. Manual Padding (Pre-allocation) Pattern
**Problema:** MongoDB ubica documentos secuencialmente en disco. Si un documento crece más allá del espacio que se le asignó al crearlo, el motor debe **mover físicamente el documento completo** a una nueva ubicación en disco, lo que degrada el rendimiento de escritura.

**Solución:** Al crear el documento, incluir un campo `_padding` con un string dummy del tamaño que se estima que el documento llegará a tener. En la primera actualización real, se elimina con `$unset`. El espacio que ocupaba ese padding queda pre-reservado en disco y el documento puede crecer sin relocalizarse.

```js
// Crear con padding pre-asignado
db.events.insertOne({ _id: "event_1", data: [], _padding: "x".repeat(1000) })

// Primera actualización: liberar el padding y usar ese espacio
db.events.updateOne({ _id: "event_1" }, { $unset: { _padding: "" }, $push: { data: newItem } })
```

---

# Patrones de Procesamiento Distribuido

## 1. Materialized Views
**Problema:** Las BDs documentales están optimizadas para leer una entidad a la vez. Calcular analytics sobre millones de documentos en tiempo real es insostenible (ej: sumar revenue sobre 50.000 órdenes tarda 5 segundos).

**Solución:** Pre-calcular la consulta costosa y guardar el resultado como un documento normal e indexable. En vez de recalcular, la vista se actualiza incrementalmente con cada operación de escritura.

```js
// Consulta pesada (inviable en tiempo real)
db.orders.aggregate([
    { $match: { date: "2026-04-23" } },
    { $group: { _id: null, total: { $sum: "$amount" } } }
])

// Vista materializada: se actualiza con cada nueva orden (1 ms de lectura)
db.daily_sales.updateOne(
    { _id: "2026-04-23" },
    { $inc: { total_revenue: 50 } },
    { upsert: true }
)
```
Las vistas se actualizan via **cron jobs** (batch diferido) o de forma **eager** (sincronamente con cada cambio de datos base).

## 2. Fan-Out-On-Write (Vista Materializada Eager)
**Problema:** En redes sociales, cargar el home feed implica consultar los posts de miles de usuarios seguidos. Ejecutar esa consulta en cada carga de página genera latencia insostenible.

**Solución:** Mover el trabajo del momento de la lectura al momento de la escritura. Cuando un usuario publica, el sistema distribuye ("fan-out") el nuevo post directamente en los arrays de timeline pre-computados de todos sus seguidores activos. Cuando el seguidor abre la app, su feed ya está armado: solo lee un documento → lectura en sub-milisegundos.

### El problema de las celebridades (Hybrid Fan-Out)
Fan-Out-On-Write funciona bien para usuarios con 500 seguidores, pero si Selena Gomez (400M seguidores) publica una foto, hacer 400 millones de escrituras instantáneas colapsa el cluster.

| Tipo de usuario | Estrategia | Mecanismo |
|----------------|------------|-----------|
| Usuario normal (99%) | **Push** (Fan-Out-On-Write) | Al publicar, el post se escribe en el timeline de cada seguidor en la BD |
| Celebridad | **Pull** (Fan-Out-On-Read) | El post NO se distribuye. Al abrir la app, el sistema hace un merge en memoria con los posts de las celebridades seguidas |

## 3. Scatter-Gather Pattern
Patrón para consultas que no pueden enrutarse a un único shard porque la clave de sharding no está en el filtro.

1. **Scatter:** La consulta se transmite (broadcast) a todos los shards del cluster.
2. **Local Execute:** Cada shard procesa la consulta en paralelo, sobre su propio subconjunto de datos.
3. **Gather:** La capa de enrutamiento recolecta los resultados parciales de todos los shards, los fusiona y devuelve un dataset unificado al cliente.

## 4. Map-Reduce Pattern
Patrón para procesar grandes datasets distribuidos. Funciona en tres fases:

1. **Map:** Corre localmente en cada nodo. Convierte los datos en pares clave-valor relevantes, minimizando tráfico de red.
2. **Combine (opcional):** Pre-reduce los datos localmente *antes* de transmitirlos por la red, reduciendo drásticamente el ancho de banda utilizado.
3. **Reduce:** Agrega todos los valores de una misma clave provenientes de todos los nodos, produciendo el resultado final.

**Ejemplo: contar palabras en 50TB de texto distribuidos en 100 servidores:**
```
Map    (nodo):    "the quick fox the" → {the:1},{quick:1},{fox:1},{the:1}
Combine(local):   → {the:2},{quick:1},{fox:1}      ← menos datos viajan por red
Reduce (global):  todos los nodos → {the:450k}, {quick:12k}
```

## 5. Incremental Map-Reduce
**Problema:** Map-Reduce sobre datasets históricos masivos puede tardar horas. Tirar la vista materializada y recalcular todo desde cero cada vez que llegan datos nuevos es ineficiente.

**Solución (Delta Merge):** Solo se computan los cambios nuevos (*deltas*) en la fase Map. Esos deltas pequeños se fusionan rápidamente con la vista materializada existente, obteniendo analytics en tiempo real sin el costo de un recálculo completo.

---

# Patrones de Arquitectura y Ciclo de Vida

## 1. Incremental Schema Migration (Lazy Migration)
**Problema:** En BDs schemaless, el esquema está implícito en el código de la aplicación. Correr un script masivo para migrar 10 millones de documentos al nuevo esquema de golpe genera locks severos y downtime del cluster.

**Solución:** Agregar un campo `schema_version` a cada documento. La migración vive en la lógica de la aplicación:
- Al leer un documento con versión vieja, se **transforma en memoria** al nuevo formato.
- Al guardarlo de vuelta en disco, se persiste ya en el formato nuevo con `schema_version` actualizado.
- La migración ocurre gradualmente a través del tráfico natural, **sin downtime** (*lazy execution*).

```js
function getUser(id) {
    let user = db.users.find(id);
    if (user.schema_version === 1) {
        // Migración lazy al leer: "name" → "first_name" + "last_name"
        let parts = user.name.split(' ');
        user.first_name = parts[0];
        user.last_name = parts[1];
        delete user.name;
        user.schema_version = 2;
        db.users.save(user);  // persiste el nuevo formato
    }
    return user;
}
```

## 2. Event Sourcing
**Problema:** En CRUD tradicional, actualizar el estado de un registro **destruye** el estado anterior. No queda registro de cuándo, por qué ni cómo cambió algo (ej: saldo bancario actualizado → historial de movimientos perdido).

**Solución:** En vez de guardar el estado actual, se persiste un **log append-only de todos los eventos** que ocurrieron. El estado actual se deriva reproduciendo (replaying) todos los eventos en orden. Como el log es inmutable se tiene:
- Audit trail perfecto.
- Capacidad de reconstruir el estado en cualquier punto del tiempo.
- Capacidad de reconstruir la base de datos completa desde cero.

```json
// CRUD (destructivo): no hay historia de por qué el balance es 50
{ "account_id": "991", "balance": 50 }

// Event Sourcing (inmutable): el balance se calcula reproduciendo los eventos: 100 - 50 = 50
[
    { "type": "ACCOUNT_CREATED", "time": "10:00" },
    { "type": "DEPOSITED",  "amount": 100, "time": "10:05" },
    { "type": "WITHDRAWN",  "amount": 50,  "time": "11:00" }
]
```

## 3. CQRS (Command Query Responsibility Segregation)
Separa física y lógicamente el sistema que **escribe datos** (Command) del que los **lee** (Query). Cada lado puede tener tecnología, esquema e índices optimizados para su rol específico.

**Cómo funciona:** El sistema de escritura emite eventos ante cada cambio. Los nodos de lectura consumen esos eventos y mantienen sus propias estructuras optimizadas para su caso de uso. Se suele combinar con Event Sourcing.

**Ejemplo - E-Commerce:**
- **Command (escribe):** PostgreSQL con ACID para inventario. Al actualizar precio, emite evento `PRICE_UPDATED`.
- **Query (lee):** MongoDB con un documento desnormalizado por producto. Al recibir el evento, actualiza su documento. El frontend lee en milisegundos sin JOINs.

```
Frontend -> API Gateway -> Microservice -> MongoDB  (lectura instantánea)
                                          ↑ consume eventos
Warehouse -> API -> Microservice -> PostgreSQL       (escrituras ACID)
```

---

# Arquitecturas Polyglot

No existe una base de datos óptima para todos los casos de uso. Una aplicación moderna puede usar múltiples tecnologías de almacenamiento especializadas, encapsuladas detrás de microservicios con API para que cada capa sea intercambiable.

## Polyglot Persistence Design

| Tecnología | Ejemplo | Casos de uso |
|-----------|---------|-------------|
| Document Store | MongoDB | Órdenes completas, perfiles de usuario, catálogos polimórficos |
| Graph Store | Neo4j | Traversals de relaciones profundas, motores de recomendación |
| Key-Value Cache | Redis | Estado de sesión, rate limiters, carritos de compra volátiles |

**Anti-patrón (Spaghetti):** Múltiples apps consultando directamente la misma BD crean acoplamiento fuerte. Un cambio de schema rompe todas las apps simultáneamente.

**Solución (Service Encapsulation):** Cada BD está detrás de su propio microservicio. El frontend habla con una API Gateway. Si se cambia la BD subyacente, el frontend no lo nota.

```
// Anti-patrón: acoplamiento directo
App_A -> Query(MongoDB_Prod)
App_B -> Query(MongoDB_Prod)   // un schema change rompe ambas

// Encapsulación correcta
Frontend -> API Gateway -> Microservice -> Database
```

## Redis: Caché de Alta Velocidad y Concurrencia Avanzada
Redis opera completamente en RAM, lo que lo hace mucho más que un caché simple. Provee:

- **Distributed Locking:** Redis puede lockear datos finos en RAM, previniendo race conditions antes de que lleguen al tier de BD principal.
- **Counting Semaphores:** A diferencia de locks binarios (bloqueado/libre), los semáforos restringen el acceso concurrente a un número exacto de operaciones simultáneas (ej: máximo 5 requests de API concurrentes por usuario).
- **Sharded Structures:** Redis usa representaciones compactas en RAM (ziplists, intsets). Fragmentar datos en miles de Hashes pequeños en vez de un Hash masivo reduce drásticamente el footprint de memoria.
- **Rich Data Types:** Listas, Sets, Hashes y Sorted Sets (ZSETs) nativos en memoria permiten computar analytics complejos a velocidades sub-milisegundo.