from common import api_url
#from common import initial_data
import requests

import pytest

def get_product(id):
    return requests.get(api_url + f"product/{id}")

# Get initial data from products endpoint to compare with one-by-one
from test_products import get_products
compare_data=get_products().json()

@pytest.mark.parametrize("test_input,expected", [(x["id"], x) for x in compare_data])
def test_product_get_at_startup(test_input, expected):
    resp = get_product(test_input)
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body == expected

@pytest.mark.parametrize("test_input", [-1, 0, 4, 9999])
def test_product_get_nonexistent(test_input):
    resp = get_product(test_input)
    # Assume 404 is correct for non-existent entries
    assert resp.status_code == 404

@pytest.mark.parametrize("test_input", ["blargh", "", "null"])
def test_product_get_malformed(test_input):
    resp = get_product(test_input)
    # Assume 400 error is correct for malformed
    assert resp.status_code == 400