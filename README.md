# igsqatest
IGS QA Test

* Download instructions, notice a markdown file, this is probably the first test!
* Not actually got development set up on home computer, so download git, Pycharm community, python  
* Thought I'd set up github project to record progress, keep code, track issues
* Followed instructions in downloaded readme.md
* Able to install dot net core and unpack file
* ran command from powershell: 
```
PS C:\Users\amac> cd C:\Users\amac\Downloads\QATest-Project\QATest
PS C:\Users\amac\Downloads\QATest-Project\QATest> dotnet QATest.dll
Hosting environment: Production
Content root path: C:\Users\amac\Downloads\QATest-Project\QATest
Now listening on: http://localhost:5000
Application started. Press Ctrl+C to shut down.
warn: Microsoft.AspNetCore.HttpsPolicy.HttpsRedirectionMiddleware[3]
      Failed to determine the https port for redirect.
``` 
* Visited http://localhost:5000/swagger/index.html got swagger interface
* Visited https://localhost:5001/swagger/index.html got localhost refused to connect
* Assuming that this is related to warning on console, maybe deliberate as part of test?
* **Must remember to file an issue for missing https and really http should be off too for security**
* **Should need some kind of authentication too**
* Also, this test example is very waterfall! Doesn't the definition of done include something on test?
* Lets try a quick explore through swagger, what is preloaded in this instance?

```
curl -X GET "http://localhost:5000/api/products" -H "accept: text/plain"

[
  {
    "id": 1,
    "name": "Lavender heart",
    "price": "9.25"
  },
  {
    "id": 2,
    "name": "Personalised cufflinks",
    "price": "45.00"
  },
  {
    "id": 3,
    "name": "Kids T-shirt Kids T-shirt",
    "price": "19.95"
  }
]
```
* Response code was 200
* OK, so we know we are getting responses and there's some preloaded data
* Lets see if we can get an error:
```
http://localhost:5000/api/product/5
http://localhost:5000/api/product/0
http://localhost:5000/api/product/-1
```
* All give a 404

## Try some automated swagger testing
* Installed swagger_tester python module
* Created autoswagger.py and after some trial and error pointed at swagger URL
```
Traceback (most recent call last):
  File "C:\Users\amac\PycharmProjects\igsqatest\venv\lib\site-packages\swagger_parser\swagger_parser.py", line 71, in __init__
    validate_spec(self.specification, '')
  File "C:\Users\amac\PycharmProjects\igsqatest\venv\lib\site-packages\swagger_spec_validator\validator20.py", line 170, in validate_spec
    validate_apis(apis, bound_deref)
  File "C:\Users\amac\PycharmProjects\igsqatest\venv\lib\site-packages\swagger_spec_validator\validator20.py", line 367, in validate_apis
    "Duplicate operationId: {}".format(operation_id)
swagger_spec_validator.common.SwaggerValidationError: Duplicate operationId: Get
```
* **Double checked swagger definitions and see that *operationId* is supposed to be unique across all endpoints and Get is used twice in the json supplied**
* Hacked json to fix that problem then got :
```buildoutcfg
INFO:swagger_tester.swagger_tester:TESTING PUT /api/product/42?
... stack trace...
requests.exceptions.MissingSchema: Invalid URL '/api/product/42?': No schema supplied. Perhaps you meant http:///api/product/42??
Starting testrun against None or http://localhost:5000/swagger/v1 using examples: True

Process finished with exit code 1
```
* re-run with dry-run=True to see what it would have tried to do:
```
Starting testrun against None or http://localhost:5000/swagger/v1 using examples: True
INFO:swagger_tester.swagger_tester:TESTING PUT /api/product/42?
INFO:swagger_tester.swagger_tester:
Would send PUT to /api/product/42? with body {'Id': 42, 'Name': 'string', 'Price': 5.5} and headers []
INFO:swagger_tester.swagger_tester:TESTING POST /api/product?
INFO:swagger_tester.swagger_tester:
Would send POST to /api/product? with body {'Id': 42, 'Name': 'string', 'Price': 5.5} and headers []
INFO:swagger_tester.swagger_tester:TESTING GET /api/products?
INFO:swagger_tester.swagger_tester:
Would send GET to /api/products? with body None and headers [('Content-Type', 'application/json')]
INFO:swagger_tester.swagger_tester:TESTING GET /api/product/42?
INFO:swagger_tester.swagger_tester:
Would send GET to /api/product/42? with body None and headers [('Content-Type', 'application/json')]
INFO:swagger_tester.swagger_tester:TESTING DELETE /api/product/42?
INFO:swagger_tester.swagger_tester:
Would send DELETE to /api/product/42? with body None and headers [('Content-Type', 'application/json')]
```
* OK lets try those manually through http://localhost:5000/swagger/index.html
* Response to PUT  /api/product/42? with body {'Id': 42, 'Name': 'string', 'Price': 5.5} and headers []
* 426 error with blank type, no text and no trace, and 426 should mean "upgrade required"
* GET on /api/product/42 gives 404 as might be expected
* POST on /api/product/ with body {'Id': 42, 'Name': 'string', 'Price': 5.5} gives 200
* GET  on /api/product/42 still gives 404
* GET on /api/products now lists:
```buildoutcfg
[
  {
    "id": 1,
    "name": "Lavender heart",
    "price": "9.25"
  },
  {
    "id": 2,
    "name": "Personalised cufflinks",
    "price": "45.00"
  },
  {
    "id": 3,
    "name": "Kids T-shirt Kids T-shirt",
    "price": "19.95"
  },
  {
    "id": 4,
    "name": "abcd",
    "price": "5.50"
  }
]
```
* DELETE on 42 gives 404
* DELETE of 4 gives 200
* GET products again returns 3 items
* PUT on existing entry 2 and then GET products does seem to update name and price fields
* POST a new entry goes in as id 4
* DELETE entry 1 and 2
* **POST a new entry, goes in as id 3!** 
* NB also noticed can enter negative prices, assume thats a bad thing
* **POST another new entry, goes in as id 3**
* POST another, goes in as id 5
* DELETE item 3 only deletes first item 3 in  list
* **POST another new entry, goes in as item 5**
* Appears that new item id is based on list length
* Delete all  entries
* POST entry, goes in as item 1
* **Id (not id) field is not in model for POST and seems to disappear into ether**
* No responses other than 200 are documented
* **PUT on non-existing entry, gives 426 too**
* If PUT/POST non-required fields are left blank get null/0.0 as defaults. Not documented.

## Automation

* Sticking with what I know, use requests and pytest

* **Just noticed price is a string in model and get, but a float in put/post, exactly how is conversion supposed to go?**

* Automated GET for product and products, assumed that get products was good initial data and then compared with get product one by one and found that **name is duplicated for item 3 for products but not product** indicates something odd in internal datat structure perhaps?
* Above might have been missed by manual/exploratory test

 * Added negative test cases for GET product, unexpected 405 result from a blank ID, but others OK. Anyway, 400 response is an assumption.
 
 * **Creating with POST, no id returned in any way, so how do you know what new ID is?**
 
 * Ideally, RESTful should return location URI to the POST, not just id
 
 * **Handling the capitalisation (initial caps when passing in, lowercase coming out) is an unnecessary faff in automation**
 
 * Finished writing automated tests, could also cover some other boundaries: unicode, etc.
 * NB Tests need to run on freshly initialised instance for handling of initial data
 ```buildoutcfg
=========================== short test summary info ===========================
FAILED test_01_product_get.py::test_product_get_at_startup[3-expected2] - Ass...
FAILED test_01_product_get.py::test_product_get_malformed[] - assert 405 == 400
FAILED test_02_product_post_delete.py::test_product_post_after_delete - Asser...
FAILED test_03_product_put.py::test_product_put - AssertionError: assert {'id...
FAILED test_03_product_put.py::test_product_put_nonexistent[-1] - assert 426 ...
FAILED test_03_product_put.py::test_product_put_nonexistent[0] - assert 426 =...
FAILED test_03_product_put.py::test_product_put_nonexistent[9999] - assert 42...
======================== 7 failed, 19 passed in 1.22s =========================
```