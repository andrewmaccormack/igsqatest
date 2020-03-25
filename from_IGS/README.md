## QA Engineer - Tech Test

### Instructions

The Software Development team at IGS have been tasked with building a simple back-end for an online marketplace. They have built a RESTful API to implement CRUD operations on this data. The endpoints are:

* GET /products - A list of products, names, and prices in JSON.
* POST /product - Create a new product using posted form data.
* GET /product/{product_id} - Return a single product in JSON format.
* PUT /product/{product_id} - Update a product's name or price by id.
* DELETE /product/{product_id} - Delete a product by id.

There is also a Swagger document which describes the API.

The software engineers have now finished their development and the application is ready to be tested. Your task is to take the project, run it and test it. The source code is not available, so use any testing tools that you think are appropriate for validating this black-box system. You will be evaluated on test coverage, readability and organisation of tests, and suggesting any improvements which could be made to the API.

So that the developers can review any bugs found in their application, a simple bug report should be produced as a result of the testing process. This can be in any format you feel is appropriate.

In order to run the application, you need to download .NET Core 2.2 runtime. This can be downloaded from:

https://dotnet.microsoft.com/download/thank-you/dotnet-runtime-2.2.7-windows-hosting-bundle-installer

A download for the project can be found at:

https://1drv.ms/u/s!AtYIQpme1WvliC00Dt3Ij2QVlA3H?e=L4nsth

Once downloaded, extract the zip file, and use Powershell or Command Prompt to open the extracted directory. Navigate into the "QATest" folder. The API can then be run using the following command:

```
dotnet QATest.dll 
```

You will then be able to open the swagger endpoints:

http://localhost:5000/swagger/index.html
https://localhost:5001/swagger/index.html

Bonus points for:
- Automating the running of the tests.
