# Cars
Cars REST API

The API allows a user to add an existing car to a database, rate it with a number 1-5 and show the most popular cars.

## Try it out!

### Play with the API on heroku:
```
http https://shrouded-tor-45074.herokuapp.com/api/cars
```
### Or use a docker image:
```
docker run \
-e CARS_SECRET_KEY=$CARS_SECRET_KEY \
-e CARS_DEBUG=False \
kol478/cars-api -dp 8000:8000
```


# Usage

Examples use [httpie](https://httpie.io) to perform http requests.
You can download it using your favorite packet manager:

```$ brew install httpie```




### Showing all existing cars:
```
$ http http://127.0.0.1:8000/api/cars
```

### Showing the most popular cars:
You can show the most popular cars (based on number of rates)

```
$ http http://127.0.0.1:8000/api/popular
```

### Adding a new car:
```
$ http http://127.0.0.1:8000/api/cars make='Tesla' model='Model 3'
```

### Rating a car:

You can rate an existing car with number ranging from 1 to 5

```
$ http http://127.0.0.1:8000/api/rate car_id=1, rating=5
```

### Deleting a car:

You can delete a car with the http delete method

```
$ http DELETE http://127.0.0.1:8000/api/cars/1
```

# Setup and installation

Clone the repo:
```
$ git clone https://github.com/Miszo97/Cars-API
$ cd Cars
```

Create a virtual environment and activate it:
```
$ python3 -m venv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```

Apply migrations:
```
$ python manage.py migrate
```
Export enviroment variables

```
export CARS_SECRET_KEY='your-secret-key' \
export CARS_DEBUG=True
```

Finally run the server:
```
$ python manage.py runserver
```

Start playing with the API 🙌🏻
