import pandas as pd
import enviar_reporte

df = pd.read_csv('ingestion_log.csv')
df['fecha'] = pd.to_datetime(df['fecha'])

# FILTRO POR FECHA PARA SIMULAR EL "LUNES NEGRO"
fecha_filtro = pd.Timestamp('2024-09-16')
df_dia = df[df['fecha'] == fecha_filtro].copy()

# METRICAS

# % datos faltantes = 1 - (registros_recibidos / registros_esperados)
df_dia['%_datos_faltantes'] = ((1 - df_dia['registros_recibidos'] / df_dia['registros_esperados']) * 100).fillna(0).round(2)

# % nulos campos críticos = nulos_campos_criticos / registros_recibidos
df_dia['%_nulos_campos_criticos'] = (df_dia['nulos_campos_criticos'] / df_dia['registros_recibidos'] * 100).fillna(0).round(2)

# % duplicados = duplicados / registros_recibidos
df_dia['%_duplicados'] = (df_dia['duplicados'] / df_dia['registros_recibidos'] * 100).fillna(0).round(2)

# prom_latencia = promedio de latencia_minutos por tabla
prom_lat = df_dia.groupby('tabla')['latencia_minutos'].mean()
df_dia['prom_latencia'] = df_dia['tabla'].map(prom_lat)

# UMBRALES PARA CADA DOMINIO
umbrales_dominio = {
    'banco_creditos': 10,
    'retail_ventas':  30,
    'rrhh_novedades': 40,
}
umbral_latencia = 35  #LATENCIA APLICA PARA TODOS LOS DOMINIOS

df_dia['umbral_dominio'] = df_dia['dominio'].map(umbrales_dominio)

df_alertas = df_dia[
    (df_dia['%_datos_faltantes']       >= df_dia['umbral_dominio']) |
    (df_dia['%_duplicados']            >= df_dia['umbral_dominio']) |
    (df_dia['%_nulos_campos_criticos'] >= df_dia['umbral_dominio']) |
    (df_dia['prom_latencia']           >= umbral_latencia)
]

df_reporte = df_alertas.drop(columns=['umbral_dominio'])
df_reporte.to_csv('reporte_alertas.csv', index=False)
print('Reporte generado')

if not df_alertas.empty:
    enviar_reporte.enviar()
else:
    print('Sin alertas. No se envía mail.')
