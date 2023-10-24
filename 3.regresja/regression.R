# Instalacja i załadowanie potrzebnych pakietów
library(tidyverse)
library(caret)

# Wczytanie danych
df <- read.csv("C:\\UKSW\\Analityka-danych-w-badaniach-spolecznych\\3.regresja\\dane_regresja.csv", sep=';', dec=',')

# Skopiowanie i usunięcie wczorajszej daty z danych dla prognozy
df_today <- df[df$Data == '2023-10-24', ]
df <- df[df$Data != '2023-10-24', ]

# Dane objaśniające: Zapotrzebowanie, Wiatr, PV, Rezerwa
X <- df[c('Zapotrzebowanie', 'Wiatr', 'PV', 'Rezerwa')]
# Dane objaśniane: Cena
y <- df$'RCE'

# Dopasowanie modelu regresji liniowej
reg <- lm(y ~ ., data = cbind(y, X))

# R kwadrat
cat("R kwadrat:", summary(reg)$adj.r.squared, "\n")

# Predykcja cen na jutro
today_predict <- predict(reg, newdata = df_today[c('Zapotrzebowanie', 'Wiatr', 'PV', 'Rezerwa')])
today_predict <- data.frame(RCE_actual = df_today$`RCE`, RCE_pred = today_predict)

# Wykres prognozy regresji liniowej a wykonania z dnia 2023-10-24
with(today_predict, plot(RCE_actual, type = "l", col = "blue", lwd = 2, ylim = range(c(RCE_actual, RCE_pred)), main = "Prognoza regresji liniowej vs wykonanie z dnia 2023-10-24"))
lines(today_predict$RCE_pred, col = "red", lwd = 2)
legend("topright", legend = c("RCE_actual", "RCE_pred"), col = c("blue", "red"), lty = 1, lwd = 2)