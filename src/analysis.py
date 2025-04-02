#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
df_wtt = pd.read_csv("wtt-stats.csv")
df_wtt.drop("Unnamed: 0", axis=1, inplace=True)
df_wtt.reset_index(inplace=True, drop=True)
df_wtt.head()

# %%
# Percentual por Genero
df_wtt.value_counts("Gender", normalize=True)

# %%
# Distribuição das Idades
df_wtt.Age.plot(kind='hist', title="Age distribution")

#%%
# Distribuição das partidas
df_wtt.Matches.plot(kind='hist', title='Matches distribution')

#%%
# Top 5 Jogadores com mais partidas odenados por Win Rate
df_wtt.nlargest(5,"Matches").sort_values("Win Rate %", ascending=False)

# %%
# Win Rate por Genero
df_wtt.groupby('Gender').agg({'Win Rate %': 'mean'})

#%%
# Media da Idade por Genero
df_wtt.groupby('Gender').agg({'Age': 'mean'})

# %%
# Partidas por Genero
df_wtt.groupby('Gender').agg({'Matches': 'mean'})

# %%
# Criando a coluna Country
df_wtt['country'] = df_wtt['Name'].str.extract('(\(\w*\))')[0].str.replace('\(|\)','', regex=True)


#%%
# Partidas por Nacionalidade
df_wtt.groupby('country').agg({'Matches':'mean'})\
    .rename({'Matches':'Matches per Country'}, axis = 1)\
    .nlargest(5, 'Matches per Country')\
    .sort_values('Matches per Country', ascending=False)
#%%
# Win Rate por Pais
df_wtt.groupby('country').agg({'Win Rate %':'mean'})\
    .rename({'Win Rate %':'Win Rate % per Country'}, axis = 1)\
    .nlargest(5, 'Win Rate % per Country')\
    .sort_values('Win Rate % per Country', ascending=False)
