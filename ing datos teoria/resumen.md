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
  Ingenieria de datos teoria
</div>

# Class 1

DE: collecting, processing, and managing data to support analytics and business decisions.

Lifecycle: ingestion, transformation, storage, and load


# Class 2

# Class 3

# Class 4

# Class 5

# Class 6

# Class 7

# Class 8: Silver & Gold layers
Single source of truth:
- sanidad de datos: no se que tengo en la capa de bronce

Limpia valida y enriquece los datos crudos

delta lake engine hace que la capa de silver funcione.
- transacciones acidas

Problemas de los datos crudos:
- data invalida: incompatible con el tipo de dato
- data no uniforme: datos no uniformer entre fuentes
- data duplicada:
  - cdc genera duplicados. sobre todo cuando no se guarda el timestamp
 
ssot:
- unification
- reliable
- consumption readiness

Standarization:
- casing, etc

Enrichment:
- data unificada

data preparada para agregación en capa de oro

validación => consistencia

## consumición de la capa de plata (oro)

seguridad:
- riesgos: no ecriptar

capa de oro: agregaciones

colaboración entre cliente e ingeniero de datos

agregaciones:
- bussiness reuirements
- data dependencies
- agreggation logic with sql or spark

la capa de oro se guarda como vistas materializadas

- consumidores diversos
- se debe hacer segun la arquitectura

se consume de plata y de oro
- silver: uso intermedio y analytics
- gold: bussiness ready optimized for reporting

problemas con la arquitectura medallion:
-
