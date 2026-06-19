# dq-desafio-tecnico
Data Quality - Desafío técnico

## Problema más critico detectado, ya que estos incidentes pertenecen al dominio "banco_creditos" y es un dominio con criticidad alta para el holding.

Al gerente de riesgos le comento:

"Se identificaron 14 días, entre agosto de 2024 y enero de 2025, en los que no se procesó ningún registro.
Como consecuencia de la falta de procesamiento del 16/09/2024, el 17/09/2024 se detectaron 576 registros con datos faltantes en campos críticos."

## Incidentes detactados por orden de prioridad

| Prioridad | Criticidad | Dominio | Incidente | Impacto Promedio | Días | Período | Observaciones |
|-----------|-----------|---------|-----------|-----------------|------|---------|---------------|
| 1 | ALTA | banco_creditos | Registros faltantes | 100% | 14 | Ago 2024 – Ene 2025 | Este dominio es crítico para el holding y por 14 días no se procesó ningún registro. |
| 2 | ALTA | banco_creditos | Nulos campos críticos | 18% | 1 | 17/9/2024 | Este dominio es crítico para el holding y de los registros que no se procesaron el 16/09/2026, el 17/02/2024 un 18% de registros en campos críticos no se procesaron. |
| 3 | MEDIA | retail_ventas | Latencia | 70 min | 19 | Ago 2024 – Ene 2025 | Este dominio tiene criticidad media. En un total de 19 días el procesamiento tuvo un promedio de 70 minutos. Esto es considerablemente alto para procesar 8.400 registros. Analizaría el proceso y me fijaría en el ETL si hay algún proceso que esté corriendo en paralelo y esté agotando los recursos. |
| 4 | MEDIA | retail_ventas | Registros faltantes | 7,31% | 23 | Ago 2024 – Ene 2025 | Este dominio tiene criticidad media. En un total de 23 días hubo un 7,31% de registros faltantes. |
| 5 | BAJA | rrhh_novedades | Nulos campos críticos | 1,10% | 15 | Ago 2024 – Ene 2025 | Este dominio tiene criticidad baja y la cantidad de incidentes no es representativa. |
| 6 | BAJA | retail_ventas | Duplicados | 0,54% | 23 | Ago 2024 – Ene 2025 | Este dominio tiene criticidad baja y el promedio de incidentes no supera el 1% por eso lo considero con prioridad baja. |
| 7 | BAJA | banco_creditos | Nulos campos críticos | 0,10% | 34 | Ago 2024 – Ene 2025 | La cantidad de incidentes no es representativa. |
| 8 | BAJA | retail_ventas | Nulos campos críticos | 0,03% | 19 | Ago 2024 – Ene 2025 | La cantidad de incidentes no es representativa. |
