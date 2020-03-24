from common import api_url
import requests

def test_product_get():
    resp = requests.get(api_url + "product")
    assert resp.status_code == 200
    resp_body = resp.json()
