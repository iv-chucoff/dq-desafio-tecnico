# Nivel 3 – Metadatos de entrega de archivos

## Metadatos solicitados a los owners de cada tabla

Le solicito los siguientes metadatos a los owners de cada tabla:

### Columnas y Detalle
Nombre de cada campo y una descripción breve de su significado.
Permite entender qué representa cada dato y validar que el contenido tenga sentido de negocio.

### Tipo de dato
Tipo esperado para cada campo.
Permite detectar cuando el dato recibido no coincide con el tipo de dato esperado.

### Requerido
Indica si el campo es obligatorio u opcional.
Permite alertar cuando un campo crítico llega vacío o nulo.

### Formato
Formato esperado dentro del tipo de dato.
Permite validar que los valores sean consistentes.

### Valores permitidos
Lista de valores válidos para campos con dominio cerrado.
Permite detectar valores inesperados que no pertenecen al dominio definido.

### Frecuencia
Con qué periodicidad se espera recibir el archivo.
Permite detectar ausencias: si un día no llegan datos y la frecuencia es diaria, se genera una alerta.

### Owner
Nombre del responsable del dato.
Es el destinatario de las alertas en caso de incidente o incumplimiento.

### Umbral Datos Faltantes
Porcentaje máximo tolerable de registros faltantes respecto a los esperados.
Permite detectar entregas incompletas: si llegan menos registros de lo comprometido y la diferencia supera el umbral, se genera una alerta.

### Umbral Datos Duplicados
Porcentaje máximo tolerable de registros duplicados sobre el total recibido.
Permite detectar problemas de procesamiento.

### Umbral Campos Críticos Nulos
Porcentaje máximo tolerable de nulos en campos obligatorios.
Permite alertar cuando la tasa de datos faltantes en campos críticos supera lo aceptable para el negocio.

### Latencia
Tiempo de procesamiento.
Permite detectar entregas tardías que comprometen los procesos que dependen de esos datos.

---


## Ejemplo de catálogo de metadatos

| Dominio | Tabla | Columna | Detalle | Tipo | Requerido | Formato | Valores permitidos | Frecuencia | Owner | Umbral Datos Faltantes | Umbral Datos Duplicados | Umbral Campos Críticos Nulos | Latencia (min) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| banco_creditos | otorgamientos | fecha | Fecha de otorgamiento del crédito | DATE | Obligatorio | YYYY-MM-DD | | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | otorgamientos | monto | Monto otorgado | FLOAT | Obligatorio | 0.00 | | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | otorgamientos | plazo | Plazo del crédito en días | INTEGER | Obligatorio | 0 | | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | otorgamientos | cuotas | Cantidad de cuotas | INTEGER | Obligatorio | 0 | | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | otorgamientos | tasa_interes | Tasa de interés anual aplicada al crédito | FLOAT | Obligatorio | 0.00 | | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | cobranzas | fecha | Fecha en que se realizó el cobro | DATE | Obligatorio | YYYY-MM-DD | | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | cobranzas | monto | Monto cobrado | FLOAT | Obligatorio | 0.00 | | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | cobranzas | estado | Estado del cobro | STRING | Obligatorio | | pagado, pendiente, rechazado, en_mora, anulado | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | cobranzas | cuota_numero | Número de cuota | INTEGER | Obligatorio | 0 | | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| banco_creditos | cobranzas | canal | Canal por el que se realizó el cobro | STRING | Opcional | | debito automático, transferencia, ventanilla | Diaria | Ivana Chucoff | < 10% | < 10% | < 10% | < 35 |
| retail_ventas | tickets | fecha | Fecha de la transacción de venta | DATE | Obligatorio | YYYY-MM-DD | | Diaria | Laura Rodriguez | < 30% | < 30% | < 30% | < 35 |
| retail_ventas | tickets | cantidad_items | Cantidad de productos incluidos en el ticket | INTEGER | Obligatorio | 0 | | Diaria | Laura Rodriguez | < 30% | < 30% | < 30% | < 35 |
| retail_ventas | tickets | monto | Monto | FLOAT | Obligatorio | 0.00 | | Diaria | Laura Rodriguez | < 30% | < 30% | < 30% | < 35 |
| retail_ventas | tickets | medio_pago | Medio de pago | STRING | Opcional | | efectivo, tarjeta debito, tarjeta credito | Diaria | Laura Rodriguez | < 30% | < 30% | < 30% | < 35 |
| rrhh_novedades | empleados | primer_nombre | Primer nombre del empleado | STRING | Obligatorio | | | Diaria | Juan Figueroa | < 40% | < 40% | < 40% | < 35 |
| rrhh_novedades | empleados | segundo_nombre | Segundo nombre del empleado | STRING | Opcional | | | Diaria | Juan Figueroa | < 40% | < 40% | < 40% | < 35 |
| rrhh_novedades | empleados | apellido | Apellido del empleado | STRING | Obligatorio | | | Diaria | Juan Figueroa | < 40% | < 40% | < 40% | < 35 |
| rrhh_novedades | empleados | fecha_licencia | Fecha de inicio de la licencia | DATE | Obligatorio | YYYY-MM-DD | | Diaria | Juan Figueroa | < 40% | < 40% | < 40% | < 35 |
| rrhh_novedades | empleados | tipo_licencia | Tipo de licencia solicitada por el empleado | STRING | Obligatorio | | enfermedad, vacaciones, estudio, maternidad, paternidad | Diaria | Juan Figueroa | < 40% | < 40% | < 40% | < 35 |
