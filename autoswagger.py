from swagger_tester import swagger_test

# Run the test
# An AssertionError will be raise in case of error.
swagger_test(app_url='http://localhost:5000/swagger/v1', dry_run=True)