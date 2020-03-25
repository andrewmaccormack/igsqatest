from common import api_url
import requests
import pytest

from test_00_products import get_products
from test_01_product_get import get_product

def put_product(id, data):
    return requests.put(f"{api_url}product/{id}", data)

def test_product_put():
    initial_count=len(get_products().json())
    id=3
    initial_data=get_product(id).json()
    new_data={"Id": id, "Name": initial_data["name"]+"_newname", "Price": 3.14159}
    # Handle the different capitalization in responses to data passed in, and convert price to string as in spec
    expected_data={k.lower(): v for k,v in new_data.items()}
    expected_data["price"]=str(expected_data["price"])

    resp=put_product(id, new_data)
    assert resp.status_code == 200
    # Still same number of products overall
    assert len(get_products().json()) == initial_count
    actual_data=get_product(id).json()
    assert actual_data != initial_data
    assert actual_data == expected_data

def test_product_put_other_fields():
    id=3
    initial_data=get_product(id).json()
    new_data={"Id": id, "Name": initial_data["name"], "Price": initial_data["price"], "spurious": "garbage"}
    resp=put_product(id, new_data)
    # Assume it ignores bad fields and keeps existing data as is
    assert resp.status_code == 200
    actual_data = get_product(id).json()
    assert actual_data == initial_data

@pytest.mark.parametrize("test_input", [-1, 0, 9999])
def test_product_put_nonexistent(test_input):
    resp = put_product(test_input, {"Id": test_input, "Name": "nullname", "Price": 9.99})
    # Assume 404 is correct for non-existent entries
    assert resp.status_code == 404