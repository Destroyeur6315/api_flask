import flask
from flask import request, jsonify
import sqlite3
import csv

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def setup_bdd():
    # data_article = pd.read_csv('./data/data_article.csv', sep=";")
    # data_dossier = pd.read_csv('./data/data_dossier.csv', sep=";")
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    with open('./data/data_dossier.csv') as f:
        reader = csv.reader(f, delimiter=";")
        data = list(reader)

    print(data)
    # penser à supprimer la première ligne

    i = 0

    for row in data:
        print("*******$")
        print(row)
        print("*******$")
        # cur.execute("INSERT INTO article \
        #             (id_article, reference, code_article, article_nom) VALUES (?, ?, ?, ?)", row)
        cur.execute("INSERT INTO dossier \
                    (id_dossier, num_dossier, date, id_article) VALUES (?, ?, ?, ?)", (i, row[0], row[1], row[2]))
        i += 1

    conn.commit()
    conn.close()

    return data

# setup_bdd()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/article/all', methods=['GET'])
def api_all_article():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM article;').fetchall()

    return jsonify(all_books)

@app.route('/api/v1/resources/dossier/all', methods=['GET'])
def api_all_dossier():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM dossier;').fetchall()

    return jsonify(all_books)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()