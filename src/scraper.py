import requests
from bs4 import BeautifulSoup

def scrape_books_data(search_value):
    url = "https://www.babelio.com/recherche.php"
    data = {"Recherche": search_value}

    response = requests.post(url, data=data)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for book_div in soup.find_all('div', {'class': 'cr_carte'}):
        try:
            book_info = {
                'title': book_div.find('a', {'class': 'titre1'}).text.strip()
            }
            books.append(book_info)
        except AttributeError:
            continue

    return books