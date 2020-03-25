from common import api_url
import requests

def get_products():
    return requests.get(api_url + "products")

def test_products_at_startup():
    resp = get_products()
    assert resp.status_code == 200
    resp_body = resp.json()
    assert len(resp_body) == 3