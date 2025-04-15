from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

bp = Blueprint('api', __name__)

@bp.route('/search', methods=['GET'])
def search():
    search_value = request.args.get('query')

    if not search_value:
        return jsonify({"error": "No search value provided" }), 400

    book_data = scrape_books_list(search_value)

    if book_data:
        return jsonify(book_data), 200
    else:
        return jsonify({"error": "Book not found" }), 400

@bp.route('/book', methods=['GET'])
def get_book():
    book_url = request.args.get('query')
    if not book_url:
        return jsonify({"error": "No book url provided" }), 400

    book_data = scrape_book(book_url)

    if book_data:
        return jsonify(book_data), 200
    else:
        return jsonify({"error": "Book not found" }), 400


# --- Functions for scraping ---
def scrape_books_list(search_value):
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
            book_info = {
                'title': book_div.find('a', {'class': 'titre1'}).text.strip(),
                'author': book_div.find('a', {'class': 'libelle'}).text.strip(),
                'img': img_true_path,
                'book_url': book_div.find('a', {'class': 'titre1'}).get('href'),
            }
            books.append(book_info)
        except AttributeError:
            continue

    return books

def scrape_book(book_url):
    true_url = f"https://www.babelio.com{book_url}"
    response = requests.get(true_url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    book = {}

    try:
        img_src = soup.find('img', {'itemprop': 'image'}).get('src')
        book_resume = soup.find('div', {'class': 'livre_resume'}).text.strip()
        livre_refs_div = soup.find('div', {'class': 'livre_refs grey_light'}) ## field with EAN and pages infos
        if livre_refs_div:
            text = livre_refs_div.text ## for correct split (bug for EAN with space etc
            book['ean'] = text.split('EAN :')[1].split('<br>')[0].strip().split()[0] ## split the string for EAN only
            book['pages'] = livre_refs_div.text.split('pages')[0].split()[-1].strip() ## split the string for pages number only
        book['title'] = soup.find('h1', {'itemprop': 'name'}).find('a').text.strip()
        book['author'] = soup.find('span', {'itemprop': 'name'}).text.strip()
        book['img'] = f"https://www.babelio.com{img_src}" ##full path to save the img
        book['resume'] = book_resume.replace(">Voir plus", "").strip() ##removing the button after long resume
    except AttributeError:
        return None

    return book
