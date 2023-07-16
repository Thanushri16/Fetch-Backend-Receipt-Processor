# Take home assessment for Fetch Backend Engineer position

## Receipt Processor Web Service - A Python Flask Application

A Receipt Processor web service built with Python and the Flask web framework that runs within a docker container and uses in-memory data storage. 

## Project setup and pre-requisites

* GitHub Account -> https://github.com/Thanushri16/Fetch-Backend-Receipt-Processor
* Docker or Docker desktop

## How to run the Python Receipt Processor application

Open a new terminal and type the following commands in the directory that consists the 'dockerfile' and 'app.py'. The first command builds a docker image of the application and the second command runs the tests in the docker image as a docker container. The third command runs the python application as a docker container after all the tests pass their execution.
```
docker build --tag receipt_processor .
docker run -p 5000:5000 receipt_processor
docker run -p 5000:5000 receipt_processor python app.py
```
* After running the commands, the Flask application would have started on the URL -> http://localhost:5000/
* Open a new terminal to use curl (in bash) or powershell (in windows) to test the GET and the POST requests. Alternatively, Postman can also be used for API testing.
* You can type "curl http://localhost:5000/" or go to "http://localhost:5000/" in your browser to check if you the get request to the main page of the web service works.
* To do a POST request in powershell, type the following commands
```
$headers = @{ "Content-Type" = "application/json" }
$response = Invoke-WebRequest -Uri "http://localhost:5000/receipts/process" -Method POST -Headers $headers -InFile example_receipt1.json
$response.RawContent
```
* To do a POST request in bash, type the following command
```
curl -X POST http://localhost:5000/receipts/process -H 'Content-Type: application/json' -d '{"retailer": "Target","purchaseDate": "2022-01-02","purchaseTime": "13:13","total": "1.25", "items": [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}]}'
``` 
* To view the response of a GET request i.e., to view the points associated with a receipt, type the following command with the receipt_id that is gotten as a JSON response after posting the receipt
```
curl http://localhost:5000/receipts/<receipt_id>/points
```

## How to stop the Python Receipt Processor application

Open a new terminal that is different from the one running the application and type the following commands. The first command helps you to find the container_id of the receipt_processor container which in turn can be used to stop the container using the docker stop command. 
```
docker ps
docker stop <container_id>
```

## Notes about the web service designed
* In order for the data to not persist when the application stops and to store information in memory without enabling data persistence, I relied on the concept of using python dictionaries to store data in the application without any database. When the application runs and receipts are posted, the receipts are stored in the dictionary with a unique receipt id which can be later retrieved to calculate the points associated with a receipt. However, when the application stops, the data stored in the dictionary also gets lost.
* In addition to the two POST and the GET endpoints that was required for the web service, I also implemented two other GET requests. The first GET request '/receipts' retrieves a list of all the receipts and the information associated with it in a list of JSON objects format. The second GET request '/receipts/id' retrieves all the information associated with a receipt having that id as its receipt_id.
* Additionally, for any production level code that has to be developed, it is important that testing be done for the API functionalities implemented. As a result, I have used the pytest module of python to test the web service functionalities.

## Assumptions
* In the points calculation associated with the length of the item description (5th rule), it is mentioned that price multiplied by 0.2 be rounded to the nearest integer. I assumed that it means using the math.ceil function to find the next highest and closest integer because in Example 1: 2.4 was rounded of to 3. 
* In my previous web application designs, I have always returned a 200 as the status code for GET requests and 201 for POST requests. However, this take home assessment had the api.yml file with the api specification that required 200 for any success responses (irrespective of GET or POST requests). So, I have proceeded with using 200 as status code for the '/receipts/process' endpoint with a successful POST request.