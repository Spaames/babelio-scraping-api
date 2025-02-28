from flask import Blueprint, request, jsonify
from scraper import scrape_books_data

bp = Blueprint('api', __name__)

@bp.route('/search', methods=['GET'])
def search():
    search_value = request.args.get('query')

    if not search_value:
        return jsonify({"error": "No search value provided" }), 400

    book_data = scrape_books_data(search_value)

    if book_data:
        return jsonify(book_data), 200
    else:
        return jsonify({"error": "Book not found" }), 400

