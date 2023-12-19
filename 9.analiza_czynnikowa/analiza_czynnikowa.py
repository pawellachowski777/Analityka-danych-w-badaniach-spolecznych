import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_kmo
# pip install factor_analyzer
from sklearn.decomposition import PCA

# Wczytanie danych
dane = pd.read_csv("DS_2000-2009_IND_SAV.tab", sep="\t")

# Wybór kolumn od ep56_1 do ep56_27
dane_wybrane = dane.filter(like="ep56_")

# Zastąpienie wartości spoza zakresu 1-7 przez NaN
dane_wybrane = dane_wybrane.applymap(lambda x: x if x in range(1, 8) else np.nan)

# Usunięcie wierszy, które mają tylko wartości NaN
dane_czyste = dane_wybrane.dropna()

# Standaryzacja danych
dane_standard = (dane_czyste - dane_czyste.mean()) / dane_czyste.std()

# Ustalenie liczby czynników do ekstrakcji
eigenvalues = np.linalg.eigvals(dane_standard.corr())
factors_to_extract = np.sum(eigenvalues > 1)

# Przeprowadzenie analizy czynnikowej
fa = FactorAnalyzer(n_factors=factors_to_extract, rotation="varimax")
fa.fit(dane_standard)

# Wyświetlenie wyników analizy czynnikowej
loadings = pd.DataFrame(fa.loadings_, index=dane_standard.columns, columns=[f'Factor_{i}' for i in range(1, factors_to_extract + 1)])
print(loadings[abs(loadings) > 0.3].dropna(how='all'))

communality = pd.DataFrame(fa.get_communalities(), index=dane_standard.columns, columns=['Communality'])
print(communality)

# Przeprowadzenie analizy składowych głównych (PCA)
pca = PCA()
pca_results = pca.fit_transform(dane_standard)

# Wyświetlenie wyjaśnionej wariancji przez każdą składową
print(pca.explained_variance_ratio_)

# Obciążenia składowych głównych nie są bezpośrednio dostępne w sklearn, ale można je obliczyć
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

# KMO test
kmo_all, kmo_model = calculate_kmo(dane_standard)

# Jeśli KMO test jest odpowiedni, możemy kontynuować z analizą czynnikową
if kmo_model < 0.6:
    raise ValueError("KMO test wynosi mniej niż 0.6, analiza czynnikowa może nie być odpowiednia.")

# Ustalenie liczby czynników do ekstrakcji
fa = FactorAnalyzer(rotation='varimax')
fa.fit(dane_standard)
# Wyświetlenie obciążeń czynnikowych
print(fa.loadings_)
