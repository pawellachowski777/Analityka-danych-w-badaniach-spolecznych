import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp

# Read the data
file_path = "DS_2000-2009_IND_SAV.tab"
dane = pd.read_csv(file_path, sep="\t")

# Select columns for the index of satisfaction indicators
zadowolenie = dane[["ep64_1", "ep64_2", "ep64_3", "ep64_4", "ep64_5", "ep64_6", "ep64_7", "ep64_8", "ep64_9", "ep64_10", "ep64_11", "ep64_12", "ep64_13", "ep64_14", "ep64_15", "ep64_16", "ep64_17", "ep64_18", "ep64_19", "ep64_20"]].dropna()

# Plot histogram of the sum of satisfaction indicators for each row
import matplotlib.pyplot as plt
plt.hist(zadowolenie.sum(axis=1))
plt.show()

# Calculate the sum of satisfaction indicators for each row
suma_zadowolenie = zadowolenie.sum(axis=1)

# Calculate the mean of the sum of satisfaction indicators
srednia_zadowolenie = np.mean(suma_zadowolenie)

# Perform one-sample t-test and calculate confidence interval for empirical data
wynik_t_testu_empiryczne = ttest_1samp(suma_zadowolenie, popmean=srednia_zadowolenie)
conf_interval_empiryczne = (np.mean(suma_zadowolenie) - wynik_t_testu_empiryczne.statistic * np.std(suma_zadowolenie) / np.sqrt(len(suma_zadowolenie)),
                            np.mean(suma_zadowolenie) + wynik_t_testu_empiryczne.statistic * np.std(suma_zadowolenie) / np.sqrt(len(suma_zadowolenie)))
print(conf_interval_empiryczne)

# Simulate data based on the same distribution
odchylenie_std_empiryczne = np.std(suma_zadowolenie)
symulowane_dane = np.random.normal(loc=srednia_zadowolenie, scale=odchylenie_std_empiryczne, size=len(suma_zadowolenie))

# Perform one-sample t-test and calculate confidence interval for simulated data
wynik_t_testu_symulowane = ttest_1samp(symulowane_dane, popmean=srednia_zadowolenie)
conf_interval_symulowane = (np.mean(symulowane_dane) - wynik_t_testu_symulowane.statistic * np.std(symulowane_dane) / np.sqrt(len(symulowane_dane)),
                            np.mean(symulowane_dane) + wynik_t_testu_symulowane.statistic * np.std(symulowane_dane) / np.sqrt(len(symulowane_dane)))
print(conf_interval_symulowane)