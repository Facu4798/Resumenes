# Preparación respuestas para el final

## Defensa del TP

**1. En no más de dos parrafos describa el problema de negocio seleccionado para el TAF (logística, staffing, cartera, etc.) e identifiquen al usuario final de la herramienta desarrollada.**

**2. En un parrafo explique las conclusiones obtenidas. ¿Cual fue el valor agregado real de la optimización respecto a una solución manual o heurística?**

**3. Describa la naturaleza de los datos de entradas (inputs). ¿Cómo evitó el "hardcoding" y que formato de ingesta de datos utilizó (CSV, API, etc.)?**

**4. Explique el proceso de validación. ¿Cómo verificaron que la solución matemática fuese factible en la realidad operativa?**

**5. Enumere las 3 principales dificultades encontradas, ya sea en el modelado matemático o en la implementación del prototipo en Python.**

## Elementos detallados del modelo y deployment

**Formulación matemática (Modelo conceptual):**
- **Objetivo general: ¿Que se busca optimizar? (Max/Min)**
- **Función objetivo: Expresión matemática de Z**
- **Variables de decisión: Definición, tipo (Continuas, Enteras, Binarias) y que representan en la realidad**

**Restricciones y lógica de negocio:**
- **Restricciones "duras" (Hard constraints): Ecuaciones clave que limitan la región factible (ej. capacidad, balance)**
- **Manejo de Infactibilidad: ¿Cómo responde el modelo si no existe solución posible con los recursos dados?**

**Analisis de sensibilidad y robustez:**
- **Análisis post-óptimo: Interpretación de precios sombra (duales) o análisis de rangos si aplica**
- **Escenarios: ¿Que parámetros clave variaron para probar la robustez?**

**Arquitectura del prototipo (deployment):**
- **Stack tecnológico: librería de modelado utilizada (pyomo, pulp.+, or-tools) y solver seleccionado (CBC,gurobi,GLPK)**
- **Interfaz de usuario: Tipo de implementación (Streamlit, API, Notebook Interactivo)**
- **Flujo de la solución: Input $\rightarrow$ Solver $\rightarrow$ Output accionable que les correspondería** 
