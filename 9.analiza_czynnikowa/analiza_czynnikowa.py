import pandas as pd
import numpy as np
# pip install factor_analyzer
from factor_analyzer import FactorAnalyzer


df = pd.read_csv('DS_2000-2009_IND_SAV.tab', sep='\t')

# 56.1. Podziwiam ludzi, którzy mają drogie domy, samochody i ubrania
# 56.27. Bez kar fizycznych nie da się dobrze wychować dzieci.
df = df[['ep56_1', 'ep56_27']].copy()

df.loc[~df['ep56_1'].isin([1, 2, 3, 4, 5, 6, 7]), 'ep56_1'] = np.nan
df.loc[~df['ep56_27'].isin([1, 2, 3, 4, 5, 6, 7]), 'ep56_27'] = np.nan

df = df.dropna()

fa = FactorAnalyzer(n_factors=3, rotation='varimax')

# Dopasuj model analizy czynnikowej do danych
fa.fit(df)

# Wyświetl wyniki analizy czynnikowej
loadings = pd.DataFrame(fa.loadings_, index=df.columns, columns=[f'Factor{i}' for i in range(1, 3)])
print("Wyniki analizy czynnikowej:")
print(loadings)
