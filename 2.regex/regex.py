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
names = [a.get('title') for li in html for a in li.select("a") ]
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
df = df.loc[0:10]
stronywiki = [sciaganie(odn) for odn in df['odnosniki']]
df['stronywiki'] = stronywiki

# Saving as CSV
df.to_csv('powazki.csv', encoding='utf-8', index=False)
#
# # Example for data extraction
df['miejsce_zm'] = [re.findall(r'\d{4} [A-Za-z, ]+', strony[1]) for strony in df['stronywiki']]
# df['miejsce_zm2'] = df['miejsce_zm'].apply(lambda x: re.sub(' \\\n', '', x))
# dane['miejsce_zm3'] = dane['miejsce_zm2'].apply(lambda x: re.sub(r'\d{4} |, [A-Za-z ]+', '', x))

# Display the DataFrame
# print(dane)
