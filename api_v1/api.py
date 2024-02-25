from flask import request, jsonify, Flask
import sqlite3
import csv
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config["DEBUG"] = True

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # Our API url 
fake_API_KEY = "kajpazn494JEJDkajbd24kjbzbdhv344"

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,
    config={  
        'app_name': "API RESTful"
    },
)

app.register_blueprint(swaggerui_blueprint)

########## Endpoints ##########
@app.route('/', methods=['GET'])
def home():
    return '''<h1>API REST</h1>
<p>A prototype API for play with items and files</p>''', 200


@app.route('/api/v1/resources/items', methods=['GET'])
def get_All_Items():
    conn = sqlite3.connect('database.db')

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    items = cur.execute('SELECT * FROM article;').fetchall()

    # Convert object Row () into dict python
    items_dict = [dict(row) for row in items]

    return jsonify(items_dict)


@app.route('/api/v1/resources/items', methods=['POST'])
def add_Items():
    try :
        id = request.json['id_article']
        reference = request.json['reference']
        code = request.json['code_article']
        name = request.json['article_nom']

        # Return Object row which seems dict (tuple by default)
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        items = cur.execute('INSERT INTO article \
            (id_article, reference, code_article, article_nom) VALUES (?, ?, ?, ?)', 
                (id, reference, code, name))
        
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': "New items created", "id" : id}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    

@app.route('/api/v1/resources/items/<int:id_article>', methods=['GET', 'PUT', 'DELETE'])
def handle_Items_By_Id(id_article):
    conn = sqlite3.connect('database.db')

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    item = cur.execute('SELECT * FROM article WHERE id_article=?',[id_article]).fetchall()

    if not item:
        conn.close()
        return jsonify({'success': False, 'message': 'item not found'}), 404
    
    if request.method == "GET":
        # Convert object Row () into dict python
        item_dict = [dict(row) for row in item]

        conn.close()
        return jsonify(item_dict[0])
    elif request.method == "PUT":
        reference = request.json['reference']
        code = request.json['code_article']
        name = request.json['article_nom']

        item = cur.execute('UPDATE article SET reference=?, \
            code_article=?, article_nom=? WHERE id_article=?',[reference, code, name, id_article])

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': "item update"}), 200
    elif request.method == "DELETE":
        item = cur.execute('DELETE FROM article WHERE id_article=?',[id_article])

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': "item delete"}), 200
    else :
        conn.close()
        return jsonify({'success': False, 'message': 'method used unknown'}), 404
    

@app.route('/api/v1/resources/files', methods=['GET'])
def get_All_Files():
    conn = sqlite3.connect('database.db')

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    items = cur.execute('SELECT * FROM dossier;').fetchall()

    # Convert object Row () into dict python
    items_dict = [dict(row) for row in items]

    return jsonify(items_dict)


@app.route('/api/v1/resources/files/<int:id_dossier>', methods=['GET'])
def get_Files_By_Id(id_dossier):
    conn = sqlite3.connect('database.db')

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    item = cur.execute('SELECT * FROM dossier WHERE id_dossier=?',[id_dossier]).fetchall()

    if not item:
        conn.close()
        return jsonify({'success': False, 'message': 'item not found'}), 404

    # Convert object Row () into dict python
    items_dict = [dict(row) for row in item]

    return jsonify(items_dict[0])


@app.route('/api/v1/resources/files/<int:id_dossier>', methods=['DELETE'])
def delete_Files_By_Id(id_dossier):
    conn = sqlite3.connect('database.db')

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    item = cur.execute('SELECT * FROM dossier WHERE id_dossier=?',[id_dossier]).fetchall()

    if not item:
        conn.close()
        return jsonify({'success': False, 'message': 'file not found'}), 404

    item = cur.execute('DELETE FROM dossier WHERE id_dossier=?',[id_dossier])

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': "file delete"}), 200


@app.route('/api/v1/resources/files/<int:id_dossier>', methods=['PUT'])
def update_Files_By_Id(id_dossier):

    auth_header = request.headers.get('X-API-KEY')

    if auth_header != fake_API_KEY:
        return jsonify({'success': False, 'message': 'API key invalid'}), 401

    conn = sqlite3.connect('database.db')

    id_article = request.json['id_article']
    num_dossier = request.json['num_dossier']
    date = request.json['date']

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    item = cur.execute('SELECT * FROM dossier WHERE id_dossier=?',[id_dossier]).fetchall()

    if not item:
        conn.close()
        return jsonify({'success': False, 'message': 'file not found'}), 404

    item = cur.execute('UPDATE dossier SET num_dossier=?, \
            date=?, id_article=? WHERE id_dossier=?',[num_dossier, date, id_article, id_dossier])

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': "file update"}), 200


@app.route('/api/v1/resources/items/<int:id_article>/files', methods=['GET'])
def get_Files_By_ItemId(id_article):
    conn = sqlite3.connect('database.db')

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    item = cur.execute('SELECT * FROM dossier WHERE id_article=?',[id_article]).fetchall()

    if not item:
        conn.close()
        return jsonify({'success': False, 'message': 'item not found'}), 404

    # Convert object Row () into dict python
    items_dict = [dict(row) for row in item]

    return jsonify(items_dict)


@app.route('/api/v1/resources/items/<int:id_article>/files', methods=['POST'])
def add_Files_By_ItemId(id_article):
    conn = sqlite3.connect('database.db')

    id = request.json['id_dossier']
    num_dossier = request.json['num_dossier']
    date = request.json['date']

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    item = cur.execute('SELECT * FROM article WHERE id_article=?',[id_article]).fetchall()

    if not item:
        conn.close()
        return jsonify({'success': False, 'message': 'item not found'}), 404

    item = cur.execute('INSERT INTO dossier \
            (id_dossier, num_dossier, date, id_article) VALUES (?, ?, ?, ?)', 
                (id, num_dossier, date, id_article))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': "New file created"}), 200


@app.route('/api/v1/resources/items/<int:id_article>/files/<int:id_dossier>', methods=['PUT'])
def update_Files_By_ItemId(id_article, id_dossier):
    conn = sqlite3.connect('database.db')

    num_dossier = request.json['num_dossier']
    date = request.json['date']

    # Return Object row which seems dict (tuple by default)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    item = cur.execute('SELECT * FROM article WHERE id_article=?',[id_article]).fetchall()

    if not item:
        conn.close()
        return jsonify({'success': False, 'message': 'item not found'}), 404
    
    item = cur.execute('SELECT * FROM dossier WHERE id_dossier=?',[id_dossier]).fetchall()

    if not item:
        conn.close()
        return jsonify({'success': False, 'message': 'file not found'}), 404

    item = cur.execute('UPDATE dossier SET num_dossier=?, \
            date=? WHERE id_dossier=?',[num_dossier, date, id_dossier])

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': "file update"}), 200

app.run()