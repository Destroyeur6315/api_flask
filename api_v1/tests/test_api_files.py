import requests

SERVEUR = "http://127.0.0.1:5000"
ENDPOINT = SERVEUR + "/api/v1/resources"

def test_api_call():
    response = requests.get(SERVEUR)
    assert response.status_code == 200

def test_create_file():
    id_dossier = 90
    num_dossier = "ref 30"
    date = "03/03/2024"
    id_article = 1
    payload = new_file_payload(id_article, id_dossier, num_dossier, date)
  
    create_item_response = create_file(payload, id_article)
    assert create_item_response.status_code == 200

    get_item_response = get_file(id_dossier)
    assert get_item_response.status_code == 200

    get_item_data =  get_item_response.json()
    assert get_item_data["id_dossier"] == id_dossier
    assert get_item_data["num_dossier"] == num_dossier
    assert get_item_data["date"] == date
    assert get_item_data["id_article"] == id_article

def test_update_file():
    id_dossier = 91
    num_dossier = "ref 30"
    date = "03/03/2024"
    id_article = 1
    payload = new_file_payload(id_article, id_dossier, num_dossier, date)
  
    create_item_response = create_file(payload, id_article)
    assert create_item_response.status_code == 200

    new_data = new_file_payload(id_article, id_dossier, "new num dossier", "00/00/0000", )

    update_item_response = update_file(id_article, id_dossier, new_data)
    assert update_item_response.status_code == 200

    get_item_response = get_file(id_dossier)
    assert get_item_response.status_code == 200

    get_item_data =  get_item_response.json()
    assert get_item_data["num_dossier"] == "new num dossier"
    assert get_item_data["date"] == "00/00/0000"

def test_update_file_auth():
    id_dossier = 92
    num_dossier = "test"
    date = "03/03/2024"
    id_article = 1
    payload = new_file_payload(id_article, id_dossier, num_dossier, date)
  
    create_item_response = create_file(payload, id_article)
    assert create_item_response.status_code == 200

    new_data = new_file_payload(20, id_dossier, "new num dossier", "00/00/0000")
    headers = { 'X-API-KEY' : 'kajpazn494JEJDkajbd24kjbzbdhv344' }

    update_item_response = update_file_auth(id_dossier, headers ,new_data)
    assert update_item_response.status_code == 200

    get_item_response = get_file(id_dossier)
    assert get_item_response.status_code == 200

    get_item_data =  get_item_response.json()
    assert get_item_data["num_dossier"] == "new num dossier"
    assert get_item_data["date"] == "00/00/0000"
    assert get_item_data["id_article"] == 20

def test_delete_file():
    # create item
    # delete the item
    # get the item and check that it's not found
    id_dossier = 93
    num_dossier = "ref 30"
    date = "03/03/2024"
    id_article = 1
    payload = new_file_payload(id_article, id_dossier, num_dossier, date)
  
    create_item_response = create_file(payload, id_article)
    assert create_item_response.status_code == 200
    
    delete_item_response = delete_file(id_dossier)
    assert delete_item_response.status_code == 200

    get_item_response = get_file(id_dossier)
    assert get_item_response.status_code == 404

def test_list_files_for_item():
    # Create item
    # Create 2 files for this item
    # Get files for this item and see if 2 items are returned
    id_article = 110
    reference = "ref 100"
    code = "code 100"
    nom = "item 100"
    payload = new_item_payload(id_article, reference, code, nom)
  
    create_item_response = create_item(payload)
    assert create_item_response.status_code == 200

    id_dossier = 120
    num_dossier = "ref 84"
    date = "12/12/1084"
    payload = new_file_payload(id_article, id_dossier, num_dossier, date)
  
    create_item_response = create_file(payload, id_article)
    assert create_item_response.status_code == 200

    id_dossier = 121
    num_dossier = "ref 85"
    date = "12/12/1085"
    payload = new_file_payload(id_article, id_dossier, num_dossier, date)
  
    create_item_response = create_file(payload, id_article)
    assert create_item_response.status_code == 200

    get_files_response = get_files_for_item(id_article)
    assert get_files_response.status_code == 200

    data = get_files_response.json()
    assert len(data) == 2

def create_file(payload, id_article):
    return requests.post(ENDPOINT + f"/items/{id_article}/files", json=payload)

def get_file(id_dossier):
    return requests.get(ENDPOINT + f"/files/{id_dossier}")

def get_files_for_item(id_article):
    return requests.get(ENDPOINT + f"/items/{id_article}/files")

def update_file(id_article, id_dossier, payload):
    return requests.put(ENDPOINT + f"/items/{id_article}/files/{id_dossier}", json=payload)

def update_file_auth(id_dossier, headers, payload):
    return requests.put(ENDPOINT + f"/files/{id_dossier}",json=payload, headers=headers)

def delete_file(id_dossier):
    return requests.delete(ENDPOINT + f"/files/{id_dossier}")

def new_file_payload(id_article, id_dossier, num_dossier, date):
    return {
        "id_article": id_article,
        "id_dossier": id_dossier,
        "num_dossier": num_dossier,
        "date": date
    }

def new_item_payload(id_article, reference, code_article, article_nom):
    return {
        "id_article": id_article,
        "reference": reference,
        "code_article": code_article,
        "article_nom": article_nom
    }

def create_item(payload):
    return requests.post(ENDPOINT + "/items", json=payload)