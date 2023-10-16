import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Link to the page
link = "https://pl.wikipedia.org/wiki/Pochowani_na_Cmentarzu_Wojskowym_na_Pow%C4%85zkach"
# Request the content of the page
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')

# Extracting places with names and surnames of deputies and extracting text
html = soup.select("li:not([class])")

# # Searching for the appropriate selectors
names = [a.get('title') for li in html for a in li.select("a")]
# if a and a.get('title') is not None
links = [a.get('href') for li in html for a in li.select("a")]
#
# Eliminacja stron nieodnoszących się do haseł
not_wiki = [not re.search("https", href) for href in links]
names = [im for i, im in enumerate(names) if not_wiki[i]]
links = [odn for odn in links if not re.search("https", odn)]

# Creating a DataFrame
df = pd.DataFrame({'imie_nazwisko': names, 'odnosniki': links})
df = df.dropna()


# Function to download pages
def sciaganie(x):
    x = "https://pl.wikipedia.org" + x
    linkx = requests.get(x)
    stronax = BeautifulSoup(linkx.content, 'html.parser').select(".mw-parser-output p")
    return [strona.get_text() for strona in stronax]


# Downloading pages
# tu ograniczam tabelkę do 10 pierwszych wierszy, żeby skrypt wykonywał się szybciej
# df = df.loc[0:200]
stronywiki = [sciaganie(odn) for odn in df['odnosniki']]
df['stronywiki'] = stronywiki
df = df[df['stronywiki'].str.len() != 0].copy()


# Saving as CSV
# df.to_csv('powazki.csv', encoding='utf-8', index=False)


def regex_operation(df, pattern, line_to_serach_in, new_column_name):
    df[new_column_name] = [re.findall(pattern, strony[line_to_serach_in]) for strony in df['stronywiki']]
    # usuwam puste
    df = df[df[new_column_name].str.len() != 0].copy()

    return df


# dodaje polskie znaki, tworzę kolumny ur i zm z danymi do dalszego procesowania
df = regex_operation(df, r'\d+ [A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ, ]+ \d{4} [A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ, ]+', 0, 'ur')
df = regex_operation(df, r'\d+ [A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ, ]+ \d{4} [A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ, ]+', 1, 'zm')

# wyciągnięcie dat i miejsca z kolumn ur i zm
for index, row in df['ur'].items():
    row_list = row[0].split(' ')
    df.loc[index, 'data_urodzenia'] = ' '.join(row_list[0:3])
    df.loc[index, 'miejsce_urodzenia'] = ' '.join(row_list[3:])

for index, row in df['zm'].items():
    row_list = row[0].split(' ')
    df.loc[index, 'data_smierci'] = ' '.join(row_list[0:3])
    df.loc[index, 'miejsce_smierci'] = ' '.join(row_list[3:])

df.drop(columns=['ur', 'zm'], inplace=True)

# usunięcie nawisów z imienia i nazwiska
pattern = r'\([^)]*\)'
df['imie_nazwisko'] = df['imie_nazwisko'].str.replace(pattern, '', regex=True).str.strip()
print(df)