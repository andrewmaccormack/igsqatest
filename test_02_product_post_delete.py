from common import api_url
import requests
import pytest

from test_01_product_get import get_product

# Get initial data from products endpoint to compare with one-by-one
from test_00_products import get_products

def post_product(data):
    return requests.post(f"{api_url}product", data)

def delete_product(id):
    return requests.delete(f"{api_url}product/{id}")

@pytest.mark.parametrize("test_input", [{"Id": "4"}, {"Name": "Five"}, {"Price": 6.0}, {"Id": "7", "Name": "Seven", "Price": -7.0}, {}])
def test_product_post(test_input):
    initial_state=get_products().json()
    resp = post_product(test_input)
    assert resp.status_code == 200
    #resp_body = resp.json()
    # Check we got id back
    #assert "id" in resp_body
    # Check there is one more entry in products
    assert len(get_products().json()) == len(initial_state)+1

def no_duplicate_fields(list_of_dicts, field="id"):
    ids=[x[field] for x in list_of_dicts]
    return len(ids) == len(set(ids))

def test_product_delete(id=1):
    initial_state = get_products().json()
    resp=delete_product(id)
    assert resp.status_code == 200
    assert len(get_products().json()) == len(initial_state)-1

def test_product_post_after_delete():
    initial_state = get_products().json()
    #Check before we start
    assert no_duplicate_fields(initial_state)
    test_product_delete(2)
    resp=post_product({"Name": "Nine"})
    new_state=get_products().json()
    # Back to original size
    assert len(new_state) == len(initial_state)
    assert no_duplicate_fields(new_state)

@pytest.mark.parametrize("test_input", [-1, 0, 9999])
def test_product_delete_nonexistent(test_input):
    resp = delete_product(test_input)
    # Assume 404 is correct for non-existent entries
    assert resp.status_code == 404
