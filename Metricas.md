# Métricas de Disponibilidad

## Métrica 1 — % de Datos Faltantes

**Qué mide:** La proporción de registros recibidos respecto a los esperados.

**Cómo se calcula:**

```
% faltantes = 1 - (registros_recibidos / registros_esperados)
```

**Umbrales por dominio:**

| Dominio | Criticidad | Umbral de alerta |
|---|---|---|
| banco_creditos | ALTA | > 10% |
| retail_ventas | MEDIA | > 30% |
| rrhh_novedades | BAJA | > 40% |

---

## Métrica 2 — % de Duplicados

**Qué mide:** La proporción de registros duplicados dentro del total de registros recibidos.

**Cómo se calcula:**

```
% duplicados = registros_duplicados / registros_recibidos
```

**Umbrales por dominio:**

| Dominio | Criticidad | Umbral de alerta |
|---|---|---|
| banco_creditos | ALTA | > 10% |
| retail_ventas | MEDIA | > 30% |
| rrhh_novedades | BAJA | > 40% |

---

## Métrica 3 — % de Nulos en Campos Críticos

**Qué mide:** La proporción de registros con valores nulos en campos definidos como críticos.

**Cómo se calcula:**

```
% nulos_criticos = nulos_campos_criticos / registros_recibidos
```

**Umbrales por dominio:**

| Dominio | Criticidad | Umbral de alerta |
|---|---|---|
| banco_creditos | ALTA | > 10% |
| retail_ventas | MEDIA | > 30% |
| rrhh_novedades | BAJA | > 40% |

---

## Métrica 4 — Latencia de Procesamiento

**Qué mide:** El tiempo promedio que tarda el pipeline en procesar los registros de cada dominio desde que los datos están disponibles hasta que finaliza la carga.

**Cómo se calcula:**

```
latencia = promedio(timestamp_fin_carga - timestamp_inicio_procesamiento)
```

**Umbral:** > 35 minutos para todos los dominios — alerta crítica independientemente de la criticidad del dominio.

Una latencia superior a 35 minutos indica alguno de los siguientes problemas:
- Partición mal configurada
- Script sin optimizar (filtros, joins ineficientes)
- Falta de caché
- Proceso paralelo agotando recursos del cluster

---

## Estrategia de Alertas

Todas las métricas se canalizan a través de Slack en el canal `#data-quality-alerts`, arrobando al owner del dominio afectado. El canal incluye a los owners de cada dominio y a los integrantes del equipo de Data Quality.

El mensaje de alerta incluye: dominio afectado, métrica que superó el umbral, valor observado vs umbral, y fecha/hora de detección.