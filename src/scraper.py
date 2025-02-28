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
            img_src = book_div.find('img', {'class': 'cr_image'}).get('src')
            img_true_path = f"https://www.babelio.com{img_src}"
            book_href = book_div.find('a', {'class': 'titre1'}).get('href')
            book_true_path = f"https://www.babelio.com{book_href}"
            book_info = {
                'title': book_div.find('a', {'class': 'titre1'}).text.strip(),
                'author': book_div.find('a', {'class': 'libelle'}).text.strip(),
                'img': img_true_path,
                'book_url': book_true_path,
            }
            books.append(book_info)
        except AttributeError:
            continue

    return books