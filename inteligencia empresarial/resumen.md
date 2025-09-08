<style>
/* GitHub-like Markdown heading styles */

h1 {
  padding-bottom: 0.1em;
  font-size: 2em;
  border-bottom: 1px solid #50555aff;
  font-weight: 700;
  line-height: 1.25;
}

h2 {
  padding-bottom: 0.1em;
  font-size: 1.5em;
  border-bottom: 1px solid #8f959bff;
  font-weight: 600;
  line-height: 1.25;
}

h3 {
  font-size: 1.25em;
  font-weight: 600;
}

h4 {
  font-size: 1em;
  font-weight: 600;
}

h5 {
  font-size: 0.875em;
  font-weight: 600;
}

h6 {
  font-size: 0.85em;
  color: #57606a;
}


/* Alternating row colors for markdown tables */
table {
  border-collapse: collapse;
  width: 100%;
  text-align: center;
}

table th, table td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: center;
}

table th {
  background-color: #202429ff;
}

table tr:nth-child(even) {
  background-color: #202429ff;
  text-align: center; 
}

table tr:nth-child(odd) {
  background-color: #2b3136ff;
  text-align: center;
}

body {
  background-color: #24292e;
}


</style>



<div style="text-align: center; font-size: 40px;font-weight: 800">
  Inteligencia empresarial
</div>


# Clase 1:

## OLAP vs OLTP

OLTP: (On Line Transaction Processing)
- Inserts, deletes, updates rápidos y consistentes
- Aplicaciones criticas de negocio
- Sistemas fuente de datos estructurados para BI.
- Generalmente normalizado
- Procesamiento en tiempo real

OLAP: (On Line Analytical Processing)
- Analizan el negocio. Análisis de datos descriptivos, predictivos.=> toma de decisiones
- orientado a lograr una mayor performance en las consultas. => desnormalizado y con información agregada
- Tipos 
    - Relational OLAP
    - Multidimensional OLAP: no relacional. qbot(datacube)
    - Hybrid OLAP: MOLAP + ROLAP

<div style="text-align: center;">
<img src ="image-9.png"/>
</div>



## Data Warehouse

<div style="text-align: center;">
    <img src="image-3.png" alt="Data Warehouse diagram" />
</div>

<div style="text-align: center;">
    <img src="image-2.png" alt="Data Warehouse structure" />
</div>


- Un data warehouse es un repositorio central, corporativo, compuesto por datos históricos y actuales. - Son usados por BI para ejecutar consultas analíticas -> se comunican con sistemas OLAP para soportar consultas analíticas
- Periódicamente extraen datos de otras fuentes para consolidarlas en una única base de datos, con lo cual crecen y aumenta el tiempo de respuesta.

<div style="text-align: center;">
    <img src="image-4.png" alt="Data Warehouse implementation" />
</div>

- Los DWs usualmente se implementan en bases de 
datos optimizadas para soportar reporting y tareas de 
análisis de datos
- A veces una base analítica (OLAP) puede existir
 separada de la base de datos. 
- Tuning: índices, vistas materializadas, compresión (antes de las nubes)



## Beneficios de DW + Data Marts

Beneficios del Data warehousing
- Integración de datos históricos
- Mejora en la calidad de la información
- Baselistapara analítica avanzada y BI

**Data Mart:** porción de un DW para análisis de un departamento específico, generalmente no tiene tanto nivel de granularidad como el DW. $\sum datamarts=DWH$

## Enfoques de implementación de DW
Inmon:enfoque descendente (DW corporativo primero)

<div style="text-align: center;">
    <img src="image.png" alt="Inmon approach" />
</div>

+Lento +Completo

Kimball: enfoque ascendente (Data Marts integrados forman el DW)

<div style="text-align: center;">
    <img src="image-1.png" alt="Kimball approach" />
</div>

+Rapido +Retrabajo

## Arquitectura típica de un DW
Puede incluir los siguientes elementos/capas:
- Sistemas fuente, OLTPs
- Staging Area (opcional)
- ETL/ELT
- Repositorio de datos central (**Data Warehouse**)
- Data Marts
- Cubos
- Herramienta de Reporting (reportes, tableros, consultas ad-hoc)
- Data Mining (DDZ)

<div style="text-align: center;">
    <img src="image-5.png" alt="Arquitectura típica de un DW" />
</div>

### Ejemplos

**Data Warehouse virtual:**

Para resolver cada pedido de los usuarios, el personal de IT (área de Data) genera distintos procesos/queries para poder extraer la  información de los sistemas operacionales necesarios.

<div style="text-align: center;">
    <img src="image-6.png" alt="Data Warehouse virtual" />
</div>

falta de integridad, el excesivo esfuerzo de extracción y de control de la información

**Data Marts independientes**
Se construyen distintos data marts o cubos a medida que se demandan para que puedan resolver los distintos pedidos de los usuarios más rápidamente.

<div style="text-align: center;">
    <img src="image-7.png" alt="Data Marts independientes" />
</div>

falta de integridad entre los distintos data marts y la duplicidad de los procesos de ETL.

**Data Warehouse**
Se construye un data warehouse completo para que se puedan resolver todos los distintos pedidos analíticos de los usuarios. Luego desde el DW se pueden construir cubos multidimensionales (OLAP) para acceder a la 
información más rápidamente

<div style="text-align: center;">
    <img src="image-8.png" alt="Data Warehouse completo" />
</div>

El tiempo que demanda construir el DW suele ser mayor al tiempo que las áreas usuarias están dispuestas a esperar.

## ETL
ETL es la operación principal para cargar los Data wahouse / Data marts

Los datos requeridos primero son obtenidos (extracted) desde las fuentes, y luego de ser extraídos son modificados (transformed) aplicando ciertas reglas,para luego ser insertados (loaded) en el sistema destino

**Herramientas (ADF / AWS Glue)**
- Desarrollar los procesos de ETL en forma visual
- Orquestar la ejecución de los procesos
- Antes se hacia con stored procedures

# Clase 2

## proposito del bi
**definición**: Conjunto de procesos y herramientas orientadas al análisis de información con 
el objetivo de hacer uso de datos reales en el proceso de toma de decisiones
- **alcence estrategico**: informacion confiable para planificación
- **objetivo principal**: datos dispersos -> conocimiento util

**BI como ventaja competitiva:**
- Identificación de tendencias de mercado
- Mejora en la relación con los clientes
- Optimización de procesos internos

| BI operativo | BI estrategico |
|----|-----|
|Reportes diarios, monitoreo de procesos internos| Análisis para visión a largo plazo|


## Arquitectura

### Arquitecturas clasicas vs modernas

**On Premise**(Costos mas altos, Alto control)
- Costos de infra
- Menejo de infra y seguridasd depende de la empresa
- Uso intensivo de recursos
- Local

**Cloud**(Costos mas bajos, Menos control)
- Baja inversion inicial
- Mantenimiento y updates a cargo del provedoor
- Bajo control de infra
- Global y escalable

**Hardware outsourcing**

**Hibridas**

## Big Data
Surge de necesidades de negocio e innovaciones tecnologicas

**definición:**: Volumen masivo de datos variados muy grandes y difíciles de procesar con las 
bases de datos y el software tradicionales.

**Las 5 Vs**:
- Volumen: Muchos datos
- Velocidad: generación y procesamiento rapido
- Variedad: Distintos formatos y tipos
- Veracidad: datos de calidad 
- Valor: datos utiles para la organización.

**Data Lakes:** fepositorio central para almacenar muchos datos crudos en varios formatos
- Pros: Almacenamiento cost-effective, escalabilidad, esquema flexible
- Cons: Desafíos de gobierno de datos, issues de calidad de datos
- **Si es:** gestion de datos flexible, con autoservicio, que soporta whatifs(escenarios) y desechables y promueve la culñtura del retry.
- **No es:** Un reemplazo del DWH o ODS, ni con performance transacional ni analitico.


<div style="text-align: center;">
  <img src="image-10.png" alt="alt text" />
  <img src="image-11.png" alt="alt text" />
</div>

**Usos del data lake**
- Staging: para carga al DWH
- Datos historicos: dado el bajo costo y capacidad para consultas grandes.
- Integración con datos externos: Igual que staging pero con datos externos (suplementing data)

- **Datos maestros** Datos core como nombres de clientes

## Asistencia a la toma de decisiones
|Tipos de decisiones |Rol del BI |
|-----|------|
|Estrategicas: largo plazo| definir planes de crecimiento, ROI |
|Tacticas: mediano plazo. ajuste de estrategia|Seguimiento de areas especificas|
|Operativas: dia a dia| monitoreo y optimizacion NRT |



## KPIs

**Métricas:** medidas cuantitativas y cualitativas para cuantificar el rendimiento/progreso
- tomar decisiones informadas
- evaluar efectividad
- establecer objetivos

**KPI(key performance indicator):**  medida del rendimiento de un proceso (%). relacionado con un objetivo 
- Reflejar estado actual y alineación y ajuste con estrategia
- Identificar areas con problemas
- Es importante establecer:
  - Niveles de rendimiento aceptables que sean expuestos por las métricas
  - Método de los informes, la forma, la frecuencia y distribución 

**Tipos de KPI**
- estrategico: cuota de mercado, clientes
- financieros: rentabilidad, utilidad
- tacticos: cantidad de ordenes, clientes satisfechos
- operativos: tiempos de entrega, eficiencia, nivel de servicio

## Objetivos smart (framework)
- Specific: dirigidos al area especifica
- Measurable: datos completos y precisos para medirlos
- Achievable: realistas
- Relevant: medir solo lo necesario para comprender el estado
- Time bound: los resultados deben estar disponibles cuando se necesiten. deben tener marco temporal

## Balanced scorecard
- método para medir el desempeño organizacional de manera integral.
- Herramienta (tableros) que permite convertir misión y visión en KPIs de actuación.
- Perspectivas:
  - Financiera: rentabilidad
  - Clientes: Satisfacción
  - Procesos internos: eficiencia y calidad
  - Aprendizaje y crecimiento: Capacitación, innovación
  - Cultura organizacional


# Clase 3

## BAM (bussiness activity monitoring)

**definicion:** monitoreo en tiempo real de actividades, operaciones y procesos 
clave del negocio

**proposito:** identificar eventos criticos al instante para reaccionar

*nota: se combina coin BPM historico*

**beneficios**
- Causa raiz $\Rightarrow$ reaccion en tiempo real
- Adaptacion rapida
- Solucionar cuellos de botellas
- Visibilidad continua de KPIs y SLAs
- Reducción de costos


## BPM (bussiness process management)
**definición:** Disciplina que modela, automatiza y optimiza procesos de negocio

**Propósito:** alinear procesos con la estrategia y mejorar continuamente. + Eficiencia - Costos

**Ciclo de vida**
1. Diseñar (hitos, tareas, responsables)
2. Modelar (visualmente, con detalle)
3. Ejecutar/Implementar (POC primero)
4. Monitorear
5. Optimizar

**Beneficios**
- Procesos más escalables, con una mejor ejecución de procesos y automatización del flujo de trabajo
- Mayor transparencia, por la automatización de procesos, se definen claramente a los dueños de las tareas a lo largo del proceso
- Menos dependencia de los equipos de desarrollo. Low code solutions

## BI, BAM & BPM
BAMcombina tanto la recolección de datos y la visualización de BI como la fortaleza analítica de BPM para crear un enfoque holístico de todas las actividades comerciales.

BPMpermite a los líderes construir sobre el trabajo de BI al analizar grandes cantidades de datos recopilados de diversas fuentes.

## Balanced scorecard

**definicion:** metodo para medir el desempeño organizacional de manera integral
- Herramienta para convertir misión y visión en objetivos y KPIs con retroalimentación
- Perspectivas:
  - Financiera: rentabilidad, reducción de costos.
  - Clientes: satisfacción, fidelización
  - Procesos internos: eficiencia, calidad
  - Aprendizaje y crecimiento: capacitación, innovación, cultura organizacional

![alt text](image-12.png)

**beneficios**
- Sistema de gestion que transforma estrategia $\Rightarrow$ KPIs
- Alinear los objetivos de toda la organización
- Permitir comunicar fácilmente la visión y la estrategia
- Priorizar los procesos más decisivos
 • Identificar ldonde se deben alocar mas recursos
 • Medir el impacto de las decisiones estratégicas


## dashboards
**definicion:** Interfaces visuales que resumen KPIs y datos globales, de areas o proyectos
- Personalizables a cada area
- Flexibles

**porposito:** ofrecer una visión global de los datos de forma resumida NRT para decisiones

**Tipos:**
- Estratégicos: visión general
- Tácticos: áreas específicas
- Operativos: NRT procesos diarios  

Características de un buen dashboard
- Claridad y jerarquía visual
- Interactividad
- Elección del gráfico más adecuado
- Filtros
- Actualización automática

## Herramientas
**Tradicionales:** SAP bussiness objects, Oracle BI, Strategy, IBM Cognos

**Modernas(Self Service y Nube):** Power BI, Tableau, Qlik Sense, Google Looker studio
- Integración con data lakes y big data tools
- IA y ML
- Visualizacion interactiva en multiples dispositivos
- Automatización

![alt text](image-13.png)

# Clase 4

## Diseño dimensional
- Modelos de datos tradicionales (entidad-relación, 3NF) terminan 
siendo muy complejos y difíciles de ser entendidos por los 
usuarios finales
- Joins de múltiples tablas, frecuentemente grandes, son lentos y 
consumen muchos recursos del sistema para consultas

Surgen modelos orientados a OLAP, no OLTP

**Caracteristicas**
- Predecible
- Facil de administrar
- Facil de entender (para it y bussines)

**Cubos N-dimensionales**
- se querea con slicing.
- basicamente un tensor

## Dimensiones
- Punto de entrada del modelo
- Indican las distintas formas que tenemos para de ver la información almacenada en un hecho. Le dan contexto
- Contienen atributos/campos descriptivos
- Contienen una clave única asignada en el ETL (surrogate key)
- Tienden a ser discretas y a menudo jerárquicas

**Conformed dimensions**
Dimensión que tiene el mismo significado en cada fact table en la que está interviniendo

**Conformed facts**
Métricas que pueden aparecer en distintos data marts. Misma unidad de medida y nombre a menos que no sean comparables (si no tienen el mismo significado)

**Granularidad de un hecho**
Nivel de detalle en el que encontrará la información almacenada de un hecho en una fact table


## Tablas de hechos
- Tabla central
- Contiene metricas que reoresentan *"los numeros de la empresa"*
- contiene atributos FK
- Cada conjunto de hechos esta basado en la interseccion de cada combinacion de los atributos dimensionales(granularidad del hecho)

**Tipos de tablas de hechos**
- Transaccional (ventas,pedidos)
- Snapshot (saldos, stock)
- Factless solo tiene FKs (Eventos, difusión)
- Agregaciones

**Tipos de hechos**
- Aditivos: Se suman en todas las dimensiones
- SemiAditivos: se pueden sumar en algunas dimesniones pero no en todas (!= dimension tiempo)
- No aditivos: no se pueden sumar en ninguna dimensión (porcentajes)

## Star Schema
- Unica tabla por dimension
- Desnormalización al menor nivel de detalle de cada dimension
- Facil de entender
- Minimiza los joins

## Snow Flake
- Una o mas tabas por dimension
- Totalmente normalizado -> se separan las tablas de baja cardinalidad
- Mas joins posibles (si la consulta se va al outer rim)

| Star | Snowflake|
|------|----------|
|Pocos joins|Mayor complejidad de consultas|
|Acceso rapido|Menos performance|
|Redundancia|Espacio optimo|
|Facil de entender| No recomendable para DWH|

## Slowly changed dimensions
- Tipo 1: Nos se registra el cambio (overwrite)
- Tipo 2: Append con nueva surrogate key
- Tipo 3: Un nuevo campo por cada hecho historico para esa PK

## Degenerate dimensions
Cuando se quiere almacenar los números de los documentos de las transacciones que se encuentran en el hecho y no tiene sentido tenerlos en una dimensión
- evitamos la creación de una dimensión con gran cantidad de registros

## Junk dimensions
Cuando en el sistema operacional existen campos tipo flag o texto junto con los campos que se utilizarán para asociar la transacción a la dimensión
- Estos campos deberían ser agrupados con algún criterio, generando una dimensión con los distintos valores que pueden tomar los campos de las distintas agrupaciones

## Agregaciones
Sumarizaciones de otros hechos realizadas con anterioridad al momento de la consulta para acelerar la performance
- segun biz o distribucion de los datos
- se hace durante o despues del etl de forma total o incremental

**implicancias**
- DBA: mas espacio, mas tareas de mantenimiento
- ETL: agrega tiempo de computo y carga. requiere sincronizacion entre datos detallados y agregados
- OLAP y reportes: ver como herramientas manejan las agregaciones

**Diseño de agregaciones**
- Se generan nuevas tablas agregadas
- Nuevas tablas dimensionales (mas chicas relacionadas a la agg table)
- Manejo de agregaciones (reportes/dbms). El usuario solo debe saber que existe la tabla de mayor detalle





