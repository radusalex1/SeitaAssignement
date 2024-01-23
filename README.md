To run project:
1. clone the project
2. run command in vs code terminal: python -m venv venv
3. activate venv
4. pip install -r requirements.txt
5. to run the project: python rest_api.py
6. to test the endpoints, you can use postman or any other tool you wish.



Get /forecasts 
Has 2 parameters date time(iso format)
Returns the three kinds of forecasts for "then" that are the most recent, given the knowledge you can assume was available at "now".
http://127.0.0.1:5000/forecasts?now=2020-11-02T00:00:00Z&then=2020-11-02T00:00:00Z

Get /tomorrow
Has 1 parameter date time(iso format)
Return three booleans, telling if the next day (the one after "now") is expected to be "warm", "sunny" and "windy". 
http://127.0.0.1:5000/tomorrow?now=2020-11-02T00:00:00Z