import pandas as pd

start = '20230924'
end = '20231024'

path_rce = f"https://www.pse.pl/getcsv/-/export/csv/PL_CENY_RYN_EN/data_od/{start}/data_do/{end}"
df_rce = pd.read_csv(path_rce, sep=';', decimal=',')


def prepare_time(df, data, godzina, format_time):
    # obróbka czasu, polecam chat GPT ;)
    df[data] = pd.to_datetime(df[data], format=format_time)
    df['Data_godzina'] = df[data] + pd.to_timedelta(df[godzina], unit='h')

    return df


# używam wczeniej napisaną funkcję
df_rce = prepare_time(df_rce, 'Data', 'Godzina', '%Y%m%d')

# warto dodawać jednostki dla jasności
# df_rce.rename(columns={'RCE': 'RCE[PLN/MWh]'}, inplace=True)

path_pk5 = f"https://www.pse.pl/getcsv/-/export/csv/PL_PD_GO_BILANS/data_od/{start}/data_do/{end}"
# tu był problem z kodowaniem trzeba było zmienić domyślną wartość, pomógł internet
df_pk5 = pd.read_csv(path_pk5, encoding="cp1250", sep=';')

# zostawiamy tylko potrzebne kolumny
df_pk5 = df_pk5[['Doba', 'Godzina', 'Prognozowane zapotrzebowanie sieci', 'Prognozowana sumaryczna generacja źródeł wiatrowych',
                 'Prognozowana sumaryczna generacja źródeł fotowoltaicznych', 'Wymagana rezerwa mocy OSP']].copy()

df_pk5 = prepare_time(df_pk5, 'Doba', 'Godzina', '%Y-%m-%d')
df_pk5.rename(columns={
    'Doba': 'Data',
    'Prognozowane zapotrzebowanie sieci': 'Zapotrzebowanie',
    'Prognozowana sumaryczna generacja źródeł wiatrowych': 'Wiatr',
    'Prognozowana sumaryczna generacja źródeł fotowoltaicznych': 'PV',
    'Wymagana rezerwa mocy OSP': 'Rezerwa'
}, inplace=True)

# wykonanie inner joina
df = pd.merge(df_pk5, df_rce, on=['Data_godzina', 'Data', 'Godzina'], how='inner').reset_index(drop=True)
df.to_csv('dane_regresja.csv', sep=';', decimal=',', index=False)
