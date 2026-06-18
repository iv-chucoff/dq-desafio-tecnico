import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
 
random.seed(42)
np.random.seed(42)
 
dominios = {
    "banco_creditos": {"tablas": ["otorgamientos", "cobranzas"], "esperados": [1500, 3200]},
    "retail_ventas":  {"tablas": ["tickets"],                    "esperados": [8400]},
    "rrhh_novedades": {"tablas": ["empleados"],                  "esperados": [200]},
}
 
rows = []
fecha_inicio = datetime(2024, 8, 1)
LUNES_NEGRO = datetime(2024, 9, 16).date()
MARTES_NEGRO = datetime(2024, 9, 17).date()
 
for i in range(180):
    fecha = (fecha_inicio + timedelta(days=i)).date()
    for dominio, config in dominios.items():
        for j, tabla in enumerate(config['tablas']):
            esperados = config['esperados'][j]
            # Lunes Negro: core bancario no transmite
            if dominio == 'banco_creditos' and fecha == LUNES_NEGRO:
                rows.append([fecha, dominio, tabla, esperados, 0, 0, 0, 0, 'MISSING'])
            # Martes: cobranzas llega con nulos y latencia
            elif dominio == 'banco_creditos' and tabla == 'cobranzas' and fecha == MARTES_NEGRO:
                rows.append([fecha, dominio, tabla, esperados,
                             int(esperados*0.97), int(esperados*0.18), 0, 94, 'WARNING'])
            elif dominio == 'banco_creditos' and random.random() < 0.04:
                rows.append([fecha, dominio, tabla, esperados, 0, 0, 0, 0, 'MISSING'])
            elif dominio == 'retail_ventas' and random.random() < 0.15:
                recibidos = int(esperados * random.uniform(0.88, 0.97))
                rows.append([fecha, dominio, tabla, esperados, recibidos,
                             0, random.randint(10,80), random.randint(30,90), 'WARNING'])
            else:
                roll = random.random()
                recibidos = int(esperados * random.uniform(0.995, 1.0))
                nulos = random.randint(0, 3) if roll < 0.1 else 0
                latencia = random.randint(8, 20)
                estado = 'WARNING' if nulos > 0 or latencia > 30 else 'OK'
                rows.append([fecha, dominio, tabla, esperados,
                             recibidos, nulos, 0, latencia, estado])
 
cols = ['fecha','dominio','tabla','registros_esperados',
        'registros_recibidos','nulos_campos_criticos','duplicados',
        'latencia_minutos','estado']
df = pd.DataFrame(rows, columns=cols)
df.to_csv('ingestion_log.csv', index=False)
print(f'Dataset generado: {len(df)} registros')
