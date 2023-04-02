import pandas as pd
from bycep import distancia_metros_entre_ceps


df = pd.DataFrame()
df['cep_origem'] = ['24934610', '24220031', '24754210']
df['cep_destino'] = ['24230102', '24230102', '24230102']

distancias = []
for iloc, row in df.iterrows():
    distancias.append(distancia_metros_entre_ceps(row['cep_origem'], row['cep_destino']))

df['distancias'] = distancias

print(df)