from common import api_url
import requests

def get_products():
    return requests.get(api_url + "products")

def test_products_at_startup():
    resp = get_products()
    assert resp.status_code == 200
    resp_body = resp.json()
    assert len(resp_body) == 3

def test_put_products():
    initial_count = len(get_products().json())
    resp=requests.put(api_url + "products", {"Name": "n/a"})
    # Any error, maybe 405?
    assert resp.status_code>=400
    assert len(get_products().json()) == initial_count

def test_post_products():
    initial_count = len(get_products().json())
    resp=requests.post(api_url + "products", {"Name": "n/a"})
    # Any error, maybe 405?
    assert resp.status_code>=400
    assert len(get_products().json()) == initial_count

def test_delete_products():
    initial_count = len(get_products().json())
    resp=requests.delete(api_url + "products")
    # Any error, maybe 405?
    assert resp.status_code>=400
    assert len(get_products().json()) == initial_count
