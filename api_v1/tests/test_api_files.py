import requests

SERVEUR = "http://127.0.0.1:5000"
ENDPOINT = SERVEUR + "/api/v1/resources"

def test_api_call():
    response = requests.get(SERVEUR)
    assert response.status_code == 200

def test_create_file():
    id_file = 21
    num_dossier = "ref 30"
    date = "03/03/2024"
    id_item = 1
    payload = new_file_payload(id_item, id_file, num_dossier, date)
  
    create_item_response = create_file(payload, id_item)
    assert create_item_response.status_code == 200

    get_item_response = get_file(id_file)
    assert get_item_response.status_code == 200

    get_item_data =  get_item_response.json()
    assert get_item_data["id"] == id_file
    assert get_item_data["num_file"] == num_dossier
    assert get_item_data["date"] == date
    assert get_item_data["id_item"] == id_item

def test_update_file():
    id_file = 22
    num_dossier = "ref 30"
    date = "03/03/2024"
    id_item = 1
    payload = new_file_payload(id_item, id_file, num_dossier, date)
  
    create_item_response = create_file(payload, id_item)
    assert create_item_response.status_code == 200

    new_data = new_file_payload(id_item, id_file, "new num dossier", "00/00/0000", )

    update_item_response = update_file(id_item, id_file, new_data)
    assert update_item_response.status_code == 200

    get_item_response = get_file(id_file)
    assert get_item_response.status_code == 200

    get_item_data =  get_item_response.json()
    assert get_item_data["num_file"] == "new num dossier"
    assert get_item_data["date"] == "00/00/0000"

def test_update_file_auth():
    id_file = 23
    num_dossier = "test"
    date = "03/03/2024"
    id_item = 1
    payload = new_file_payload(id_item, id_file, num_dossier, date)
  
    create_item_response = create_file(payload, id_item)
    assert create_item_response.status_code == 200

    new_data = new_file_payload(20, id_file, "new num dossier", "00/00/0000")
    headers = { 'X-API-KEY' : 'kajpazn494JEJDkajbd24kjbzbdhv344' }

    update_item_response = update_file_auth(id_file, headers ,new_data)
    assert update_item_response.status_code == 200

    get_item_response = get_file(id_file)
    assert get_item_response.status_code == 200

    get_item_data =  get_item_response.json()
    assert get_item_data["num_file"] == "new num dossier"
    assert get_item_data["date"] == "00/00/0000"
    assert get_item_data["id_item"] == 20

def test_delete_file():
    # create item
    # delete the item
    # get the item and check that it's not found
    id_file = 24
    num_dossier = "ref 30"
    date = "03/03/2024"
    id_item = 1
    payload = new_file_payload(id_item, id_file, num_dossier, date)
  
    create_item_response = create_file(payload, id_item)
    assert create_item_response.status_code == 200
    
    delete_item_response = delete_file(id_file)
    assert delete_item_response.status_code == 200

    get_item_response = get_file(id_file)
    assert get_item_response.status_code == 404

def test_list_files_for_item():
    # Create item
    # Create 2 files for this item
    # Get files for this item and see if 2 items are returned
    id_item = 24
    reference = "ref 100"
    code = "code 100"
    nom = "item 100"
    payload = new_item_payload(id_item, reference, code, nom)
  
    create_item_response = create_item(payload)
    assert create_item_response.status_code == 200

    id_file = 25
    num_dossier = "ref 84"
    date = "12/12/1084"
    payload = new_file_payload(id_item, id_file, num_dossier, date)
  
    create_item_response = create_file(payload, id_item)
    assert create_item_response.status_code == 200

    id_file = 26
    num_dossier = "ref 85"
    date = "12/12/1085"
    payload = new_file_payload(id_item, id_file, num_dossier, date)
  
    create_item_response = create_file(payload, id_item)
    assert create_item_response.status_code == 200

    get_files_response = get_files_for_item(id_item)
    assert get_files_response.status_code == 200

    data = get_files_response.json()
    assert len(data) == 2

def create_file(payload, id_item):
    return requests.post(ENDPOINT + f"/items/{id_item}/files", json=payload)

def get_file(id_file):
    return requests.get(ENDPOINT + f"/files/{id_file}")

def get_files_for_item(id_item):
    return requests.get(ENDPOINT + f"/items/{id_item}/files")

def update_file(id_item, id_file, payload):
    return requests.put(ENDPOINT + f"/items/{id_item}/files/{id_file}", json=payload)

def update_file_auth(id_file, headers, payload):
    return requests.put(ENDPOINT + f"/files/{id_file}",json=payload, headers=headers)

def delete_file(id_file):
    return requests.delete(ENDPOINT + f"/files/{id_file}")

def new_file_payload(id_item, id_file, num_dossier, date):
    return {
        "id_item": id_item,
        "id": id_file,
        "num_file": num_dossier,
        "date": date
    }

def new_item_payload(id_item, reference, item_code, item_name):
    return {
        "id": id_item,
        "reference": reference,
        "item_code": item_code,
        "item_name": item_name
    }

def create_item(payload):
    return requests.post(ENDPOINT + "/items", json=payload)