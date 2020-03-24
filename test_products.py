from common import api_url
import requests

def test_products_at_startup():
    resp = requests.get(api_url + "products")
    assert resp.status_code == 200
    resp_body = resp.json()
    assert len(resp_body) == 3