from flask import Blueprint, request, jsonify
from scraper import scrape_books_list, scrape_book

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