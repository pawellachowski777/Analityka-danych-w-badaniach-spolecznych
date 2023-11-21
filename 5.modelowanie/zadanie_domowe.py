import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import warnings
sns.set()
warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")

# dane o zdrowiu psychicznym uczniów
# https://www.kaggle.com/datasets/rxnach/student-stress-factors-a-comprehensive-analysis
df = pd.read_csv('StressLevelDataset.csv')
# tabela zawiera 1100 obserwacji (bez braków), autorzy podzielili czynniki powodujące strs na 5 głównych faktorów,
# na który składają się 4 parametry
# Psychological Factors => 'anxiety_level', 'self_esteem', 'mental_health_history', 'depression',
# Physiological Factors => 'headache', 'blood_pressure', 'sleep_quality', 'breathing_problem
# Environmental Factors => 'noise_level', 'living_conditions', 'safety', 'basic_needs',
# Academic Factors => 'academic_performance', 'study_load', 'teacher_student_relationship', 'future_career_concerns',
# Social Factor => 'social_support', 'peer_pressure', 'extracurricular_activities', 'bullying'

print(df.info())

# Chciałbym zbadać zależność między jakością kształcenia (academic_performance) a obawami o przyszłą karierę
# (future_career_concerns)



df = df[['academic_performance', 'future_career_concerns']]
print(df.describe())
# Oceny uczniów mieszczą się w zakresie od 0 do 5
# Na stronie nie ma dokładnych opisów co oznaczają poszczególne oceny, przyjmuję więc, że

# dla jakości kształcenia - academic_performance:
# 0 - bardzo źle
# 1 - źle
# 2 - trochę źle
# 3 - trochę dobrze
# 4 - dobrze
# 5 - bardzo dobrze

# dla obaw o przyszłość zawodową - future_career_concerns:
# 0 - bardzo niskie
# 1 - niskie
# 2 - neutralnie ze wskazaniem na obawę
# 3 - neutralnie ze wskazaniem na brak obaw
# 4 - wysokie
# 5 - bardzo wysokie

# Teza: im uczniowie gorzej oceniają jakość kształcenia, tym bardziej obawiają się przyszłości
# Uważam, że rozkłady 2 zmiennych będą zbliżone do rozkładu normalnego



plt.hist(df['academic_performance'], bins=[0,1,2,3,4,5,6], alpha=0.7, align='left', color='blue')
plt.hist(df['future_career_concerns'], bins=[0,1,2,3,4,5,6], alpha=0.7, align='left', color='green')
plt.show()

# zmienne mają podobny układ, bardzo mało odpowiedzi na 0, 3,4,5 niemal się pokrywają, różnica pojawia się w ocenach 1 i 2
# jakość nauczania najczęściej była oceniana na 2 (trochę źle)
# większość uczniów ma umiarkowane obawy wobec przyszłości



print(df.corr())
# Występuje silna korelacja ujemna, co może potwierdzać tezę
sns.heatmap(pd.crosstab(df['future_career_concerns'], df['academic_performance']), annot=True, fmt='d')
plt.show()



# W obu zmiennych obserwacji z wynikiem 0 jest bardzo mało, usunę je, żeby nie robiły niepotrzebnego szumu
df = df.loc[df['academic_performance'] != 0]
df = df.loc[df['future_career_concerns'] != 0]

# odpowiedzi 4 i 5 mają bardzo podobny rozkład, połączę je w jedną wartość
df.loc[(df['future_career_concerns'] == 4) | (df['future_career_concerns'] == 5), 'future_career_concerns'] = 4
df.loc[(df['academic_performance'] == 4) | (df['academic_performance'] == 5), 'academic_performance'] = 4



# Stworzenie modelu regresji
X = df[['academic_performance']]
y = df[['future_career_concerns']]

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())



df['future_career_concerns_pred'] = model.predict().round()
plt.hist(df['future_career_concerns_pred'], bins=[1,2,3,4,5,6], alpha=0.7, align='left', color='red')
plt.hist(df['future_career_concerns'], bins=[1,2,3,4,5,6], alpha=0.7, align='left', color='blue')
plt.show()

# Model ma problemy z rozróżnieniem odpowiedzi 3 (postawa neutralna wobec przyszłości ze wskazaniem na brak obaw) a 4
# (duża lub bardzo duża obawa o przyszłość zawodową).
# Dobrze natomiast radzi sobie z rozpoznawaniem odpowiedzi 1 i 2 (mała lub umiarkowana obawa)



# Symulacja nowej tabeli na podstawie rozkładu istniejących danych

np.random.seed(42)
df['academic_performance_random'] = np.random.choice(df['academic_performance'], size=len(df['academic_performance']))

plt.hist(df['academic_performance'], bins=[0,1,2,3,4,5,6], alpha=0.7, align='left', color='blue')
plt.hist(df['academic_performance_random'], bins=[0,1,2,3,4,5,6], alpha=0.7, align='left', color='green')
plt.plot()
# Symulacja działa prawidłowo


# predykcja na podstawie zasymulowanych danych z rozkładu
df['future_career_concerns_pred_random'] = round(model.params['const'] + df['academic_performance_random'] * model.params['academic_performance'])