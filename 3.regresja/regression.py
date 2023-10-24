import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd

df = pd.read_csv("dane_regresja.csv", sep=';', decimal=',')

# kopiuje i wycinam wczorajszą datę z danych, aby zrobić na niej prognozę
df_today = df[df['Data'] == '2023-10-24'].copy()
df.drop(index=df_today.index, inplace=True)

df_today = df_today.reset_index(drop=True)

# dane objaśniające: zapo, wiat, PV
X = df[['Zapotrzebowanie', 'Wiatr', 'PV', 'Rezerwa']]
# dane onjaśniane: cena
y = df['RCE']

reg = LinearRegression().fit(X, y)
# R kwadrat
print("R kwadrat:", reg.score(X, y))

# predykcja cen na jutro
today_predict = reg.predict(df_today[['Zapotrzebowanie', 'Wiatr', 'PV', 'Rezerwa']])
today_predict = pd.Series(today_predict, name='RCE_pred')
today_predict = pd.merge(df_today['RCE'], today_predict, left_index=True, right_index=True)
print(today_predict)
sns.lineplot(today_predict[['RCE', 'RCE_pred']])
plt.title("Prognoza regresji liniowej vs wykonanie z dnia 2023-10-24")
plt.show()
