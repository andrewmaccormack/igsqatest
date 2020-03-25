from common import api_url
from common import initial_data
import requests

import pytest

def get_product(id):
    return requests.get(api_url + f"product/{id}")

@pytest.mark.parametrize("test_input,expected", [(x["id"], x) for x in initial_data])
def test_product_get_at_startup(test_input, expected):
    resp = get_product(test_input)
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body == expected
