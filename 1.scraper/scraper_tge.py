import pandas as pd
from bs4 import BeautifulSoup
import requests
from pytz import timezone
import datetime
import urllib3

urllib3.disable_warnings()

# pobieramy dane z https://tge.pl/gaz-rdn

def _call_tge(day):
    path = rf"https://tge.pl/gaz-rdb?dateShow={day.strftime('%d-%m-%Y')}&dateAction=prev"
    page = requests.get(path, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def download_data(soup):
    row_soup_mean = soup.find('div', class_=['table-responsive']).find_all('td', 'footable-visible')
    row_soup = soup.find_all('div', class_=['wyniki-footable-kontrakty_blokowe-0'])[0].find_all('td',
                                                                                                'footable-visible')

    contract = row_soup[0].text.strip()
    mean_ = float(row_soup_mean[1].text.replace(',', '.'))
    min_ = float(row_soup[1].text.replace(',', '.'))
    max_ = float(row_soup[2].text.replace(',', '.'))
    volume = float(row_soup[3].text.replace(',', '.'))

    df = pd.DataFrame([{
        'kontrakt': contract,
        'gaz_rdb[PLN/MWh]': mean_,
        'gaz_rdb_min[PLN/MWh]': min_,
        'gaz_rdb_max[PLN/MWh]': max_,
        'wolumen[MWh]': volume
    }])

    return df


def prepare_dataframe(df, date):
    df.insert(0, 'date_cet', date)
    df['date_cet'] = pd.to_datetime(df['kontrakt'].iloc[0][-8:], format='%d-%m-%y')
    # df['date_cet'] = pd.to_datetime(df['date_cet'])
    df['date_cet'] = df['date_cet'].dt.date
    df['date_cet'] = pd.to_datetime(df['date_cet'])

    df['date_cet'] = df['date_cet'].astype(str)

    return df


def import_dataset(day):
    soup = _call_tge(day)
    df = download_data(soup)
    df = prepare_dataframe(df, day)
    return df


config = {
    'DATE_DOWNLOAD': datetime.datetime.now(timezone('Europe/Warsaw')) + pd.Timedelta(days=0),
    'DAYS_BACK': 9,
}

# lista dni od dziś - DAYS_BACK do dziś
date_list = [config['DATE_DOWNLOAD'] - datetime.timedelta(days=x) for x in range(config['DAYS_BACK'])]
date_list.reverse()

df_all = pd.DataFrame()
empty_dates = []
not_empty_dates = []

for day in date_list:
    print(day)
    df = import_dataset(day)
    if not df.empty:
        not_empty_dates.append(day)
        df_all = pd.concat([df_all, df])


df_all.to_csv('tge_gaz_rdn.csv', sep=';')
