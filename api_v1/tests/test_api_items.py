import requests

SERVEUR = "http://127.0.0.1:5000"
ENDPOINT = SERVEUR + "/api/v1/resources"

def test_api_call():
    response = requests.get(SERVEUR)
    assert response.status_code == 200

def test_create_item():
    id_item = 21
    reference = "ref 30"
    code = "code 30"
    name = "item 30"
    payload = new_item_payload(id_item, reference, code, name)
  
    create_item_response = create_item(payload)
    assert create_item_response.status_code == 200

    get_item_response = get_item(id_item)
    assert get_item_response.status_code == 200

    get_item_data =  get_item_response.json()
    assert get_item_data["reference"] == reference
    assert get_item_data["item_code"] == code
    assert get_item_data["item_name"] == name

def test_update_item():
    # create item
    # update the item
    # get and validate the change
    id_item = 22
    reference = "ref 30"
    code = "code 30"
    name = "item 30"
    payload = new_item_payload(id_item, reference, code, name)
  
    create_item_response = create_item(payload)
    assert create_item_response.status_code == 200

    new_data = new_item_payload(id_item, "new ref", "new code", "new name")

    update_item_response = update_item(id_item, new_data)
    assert update_item_response.status_code == 200

    get_item_response = get_item(id_item)
    assert get_item_response.status_code == 200

    get_item_data =  get_item_response.json()
    assert get_item_data["reference"] == "new ref"
    assert get_item_data["item_code"] == "new code"
    assert get_item_data["item_name"] == "new name"

def test_delete_item():
    # create item
    # delete the item
    # get the item and check that it's not found
    id_item = 23
    reference = "ref 30"
    code = "code 30"
    name = "item 30"
    payload = new_item_payload(id_item, reference, code, name)
  
    create_item_response = create_item(payload)
    assert create_item_response.status_code == 200
    
    delete_item_response = delete_item(id_item)
    assert delete_item_response.status_code == 200

    get_item_response = get_item(id_item)
    assert get_item_response.status_code == 404

def create_item(payload):
    return requests.post(ENDPOINT + "/items", json=payload)

def get_item(id_item):
    return requests.get(ENDPOINT + f"/items/{id_item}")

def update_item(id_item, payload):
    return requests.put(ENDPOINT + f"/items/{id_item}", json=payload)

def delete_item(id_item):
    return requests.delete(ENDPOINT + f"/items/{id_item}")

def new_item_payload(id_item, reference, item_code, item_name):
    return {
        "id": id_item,
        "reference": reference,
        "item_code": item_code,
        "item_name": item_name
    }