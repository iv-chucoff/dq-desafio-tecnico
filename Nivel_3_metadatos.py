# ===========================================================================
# NOTA IMPORTANTE – DATOS AGREGADOS
#
# Este script trabaja con los datos ya agregados del ingestion_log.csv.
# Eso significa que los % de nulos, duplicados y faltantes se calculan sobre
# los totales que el sistema de ingesta ya consolidó, NO sobre el archivo crudo.
#
# En un entorno de producción, la validación debería ocurrir en dos capas:
#
# CAPA 1 – A nivel de columna (sobre el archivo crudo):
#   - Verificar que cada campo tenga el tipo de dato correcto (DATE, FLOAT, INTEGER, STRING)
#   - Verificar que las fechas respeten el formato YYYY-MM-DD
#   - Verificar que los campos con dominio cerrado (estado, tipo_licencia, canal, etc.)
#     contengan únicamente los valores permitidos declarados en el contrato
#   - Detectar valores fuera de rango (montos negativos)
#
# CAPA 2 – A nivel de entrega (lo que hace este script):
#   - Verificar que el archivo llegó (frecuencia)
#   - Verificar volumen, duplicados, nulos en críticos y latencia
#
# ===========================================================================

import pandas as pd
import json


# ---------------------------------------------------------------------------
# #FECHA DE PROCESAMIENTO
# ---------------------------------------------------------------------------
fecha_procesamiento = '2024-09-16'
fecha_procesamiento = pd.Timestamp(fecha_procesamiento)
alertas = []


# ---------------------------------------------------------------------------
# # METADATOS – Contratos por tabla
# Derivados del catálogo definido en Nivel_3_metadatos.md
# ---------------------------------------------------------------------------
contratos = [
    {
        "dominio": "banco_creditos", 
        "tabla": "otorgamientos",
        "owner": "Ivana Chucoff",
        "frecuencia": "diaria",
        "umbral_faltantes_pct": 10,
        "umbral_duplicados_pct": 10,
        "umbral_nulos_pct": 10,
        "latencia_max_min": 35,
    },
    {
        "dominio": "banco_creditos",
        "tabla": "cobranzas",
        "owner": "Ivana Chucoff",
        "frecuencia": "diaria",
        "umbral_faltantes_pct": 10,
        "umbral_duplicados_pct": 10,
        "umbral_nulos_pct": 10,
        "latencia_max_min": 35,
    },
    {
        "dominio": "retail_ventas",
        "tabla": "tickets",
        "owner": "Laura Rodriguez",
        "frecuencia": "diaria",
        "umbral_faltantes_pct": 30,
        "umbral_duplicados_pct": 30,
        "umbral_nulos_pct": 30,
        "latencia_max_min": 35,
    },
    {
        "dominio": "rrhh_novedades",
        "tabla": "empleados",
        "owner": "Juan Figueroa",
        "frecuencia": "diaria",
        "umbral_faltantes_pct": 40,
        "umbral_duplicados_pct": 40,
        "umbral_nulos_pct": 40,
        "latencia_max_min": 35,
    },
]   

# ---------------------------------------------------------------------------
# LECTURA DE LA TABLA ingestion_log.csv
# ---------------------------------------------------------------------------
df = pd.read_csv('ingestion_log.csv')
df['fecha'] = pd.to_datetime(df['fecha'])

df_dia = df[df['fecha'] == fecha_procesamiento]


# ---------------------------------------------------------------------------
# CÁLCULO DE MÉTRICAS
# ---------------------------------------------------------------------------
# % datos faltantes: qué proporción del volumen comprometido no llegó
df_dia['%_datos_faltantes'] = (
    (1 - df_dia['registros_recibidos'] / df_dia['registros_esperados']) * 100
).fillna(0).round(2)

# % nulos en campos críticos sobre registros recibidos
df_dia['%_nulos_campos_criticos'] = (
    df_dia['nulos_campos_criticos'] / df_dia['registros_recibidos'] * 100
).fillna(0).round(2)

# % duplicados sobre registros recibidos
df_dia['%_duplicados'] = (
    df_dia['duplicados'] / df_dia['registros_recibidos'] * 100
).fillna(0).round(2)


# ---------------------------------------------------------------------------
# VALIDACIONES
# ---------------------------------------------------------------------------

# VERIFICACIÓN DE FRECUENCIA + VALIDACIÓN DE UMBRALES Y LATENCIA
tablas_frecuencia = [c for c in contratos if c['frecuencia'] == 'diaria']
tablas_en_log     = set(zip(df_dia['dominio'], df_dia['tabla']))

for contrato in tablas_frecuencia:
    dominio = contrato['dominio']
    tabla   = contrato['tabla']
    owner   = contrato['owner']

    # 1. Valido que haya llegado el archivo
    if (dominio, tabla) not in tablas_en_log:
        alertas.append({
            "dominio":   dominio,
            "tabla":     tabla,
            "owner":     owner,
            "severidad": "CRITICA",
            "tipo":      "Archivo no entregado",
            "detalle":   f"{dominio}.{tabla} no está registrada en el log del {fecha_procesamiento}.",
        })
        continue

    # Buscar la fila del df para esta tabla
    row = df_dia[(df_dia['dominio'] == dominio) & (df_dia['tabla'] == tabla)].iloc[0]

    # 2. Datos faltantes
    if row['%_datos_faltantes'] >= contrato['umbral_faltantes_pct']:
        alertas.append({
            "dominio":   dominio,
            "tabla":     tabla,
            "owner":     owner,
            "severidad": "ALTA",
            "tipo":      "Datos faltantes",
            "detalle":   f"{dominio}.{tabla}: {row['%_datos_faltantes']}% faltantes (umbral: < {contrato['umbral_faltantes_pct']}%). Recibidos: {int(row['registros_recibidos'])} / Esperados: {int(row['registros_esperados'])}.",
        })

    # 3. Nulos en campos críticos
    if row['%_nulos_campos_criticos'] >= contrato['umbral_nulos_pct']:
        alertas.append({
            "dominio":   dominio,
            "tabla":     tabla,
            "owner":     owner,
            "severidad": "ALTA",
            "tipo":      "Nulos en campos críticos",
            "detalle":   f"{dominio}.{tabla}: {row['%_nulos_campos_criticos']}% de nulos en campos obligatorios (umbral: < {contrato['umbral_nulos_pct']}%).",
        })

    # 4. Duplicados
    if row['%_duplicados'] >= contrato['umbral_duplicados_pct']:
        alertas.append({
            "dominio":   dominio,
            "tabla":     tabla,
            "owner":     owner,
            "severidad": "MEDIA",
            "tipo":      "Datos duplicados",
            "detalle":   f"{dominio}.{tabla}: {row['%_duplicados']}% duplicados (umbral: < {contrato['umbral_duplicados_pct']}%). Duplicados detectados: {int(row['duplicados'])}.",
        })

    # 5. Latencia
    if row['latencia_minutos'] >= contrato['latencia_max_min']:
        alertas.append({
            "dominio":   dominio,
            "tabla":     tabla,
            "owner":     owner,
            "severidad": "MEDIA",
            "tipo":      "Latencia excedida",
            "detalle":   f"{dominio}.{tabla}: latencia de {int(row['latencia_minutos'])} min (máximo: {contrato['latencia_max_min']} min).",
        })


# ---------------------------------------------------------------------------
# GENERACIÓN DEL JSON
# ---------------------------------------------------------------------------

# Agrupar por owner
alertas_por_owner = {}
for alerta in alertas:
    owner = alerta['owner']
    if owner not in alertas_por_owner:
        alertas_por_owner[owner] = []
    alertas_por_owner[owner].append(alerta)

# Imprimir por consola
for owner, lista in alertas_por_owner.items():
    print(f"\n=== {owner} ({len(lista)} alerta/s) ===")
    for a in lista:
        print(f"  [{a['severidad']}] {a['dominio']}.{a['tabla']} – {a['tipo']}")

# Guardar en archivo
with open('alertas.json', 'w', encoding='utf-8') as f:
    json.dump(alertas_por_owner, f, ensure_ascii=False, indent=2)

print("\nAlertas guardadas en alertas.json")