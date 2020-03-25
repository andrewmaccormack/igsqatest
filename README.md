# igsqatest
##IGS QA Test

### Artifacts:
- [Original instructions](from_IGS/README.md)
- [Testing Logbook](Log.md)
- [12 Open Issues](https://github.com/andrewmaccormack/igsqatest/issues)
- Automated tests, 22 pass, 7 fail, covering happy path and error cases for each endpoint

### Automated tests
These are run with pytest, results as below:
```
=========================== short test summary info ===========================
FAILED test_01_product_get.py::test_product_get_at_startup[3-expected2] - Ass...
FAILED test_01_product_get.py::test_product_get_malformed[] - assert 405 == 400
FAILED test_02_product_post_delete.py::test_product_post_after_delete - Asser...
FAILED test_03_product_put.py::test_product_put - AssertionError: assert {'id...
FAILED test_03_product_put.py::test_product_put_nonexistent[-1] - assert 426 ...
FAILED test_03_product_put.py::test_product_put_nonexistent[0] - assert 426 =...
FAILED test_03_product_put.py::test_product_put_nonexistent[9999] - assert 42...
======================== 7 failed, 22 passed in 1.16s =========================
```
[Full log](pytest_output.log) 
#### Traceability of automated test failures to issues
- `test_product_get_at_startup` fail corresponds to [Issue #9](https://github.com/andrewmaccormack/igsqatest/issues/9)
- `test_product_get_malformed` fail corresponds to [Issue #10](https://github.com/andrewmaccormack/igsqatest/issues/10)
- `test_product_post_after_delete` fail corresponds to [Issue #3](https://github.com/andrewmaccormack/igsqatest/issues/3)
- `test_product_put` fail corresponds to [Issue #7](https://github.com/andrewmaccormack/igsqatest/issues/7)
- `test_product_put_nonexistent` fails correspond to [Issue #8](https://github.com/andrewmaccormack/igsqatest/issues/8)
- Other issues were noticed during [exploratory testing](Log.md)

