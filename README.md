# restmessier

## Demostration of RESTful Web API for Messier Objects

This is a simple RESTful Web API for CRUD operations on a collection of Messier celestial targets based on MongoDB. Also, the Geospatial api of MongoDB is used which provides the functionlity of quering the API for objects that are nearby another Messier object or a set of WGS84 coordinates. This API is also a WSGI application with allows for easy scaling.

What is a Messier object? https://en.wikipedia.org/wiki/Messier_object


## Requirements

1. PyMongo
2. jsonschema
3. flask
4. python 2.7+

### Start up the API with the development server of Flask

```
$ ./astrocat.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
```

### Get a list of Messier objects

```
$ curl -i http://localhost:5000/astronomy/messier/

Content-Type: application/json
Content-Length: 37214
Server: Werkzeug/0.10.4 Python/2.7.9
Date: Fri, 10 Jul 2015 10:16:19 GMT

{
  "messierobjects": [
    {
      "_id": "559bacd8e5e7103b9611f3f2", 
      "constellation": "LEPUS", 
      "loc": {
        "coordinates": [
          5.2212, 
          -24.34
        ], 
        "type": "Point"
      }, 
      "mid": "M79", 
      "ngcid": "NGC 1904", 
      "remarks": "Globular cluster", 
      "url": "/astronomy/messier/M79"
    }, 
...
```

### Get a single Messier object

```
$ curl -i http://localhost:5000/astronomy/messier/m82
curl: (6) Could not resolve host: GET
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 369
Server: Werkzeug/0.10.4 Python/2.7.9
Date: Fri, 10 Jul 2015 10:20:19 GMT

{
  "object": {
    "_id": "559bacd8e5e7103b9611f3f5", 
    "constellation": "URSA MAJOR", 
    "loc": {
      "coordinates": [
        9.5154, 
        69.56
      ], 
      "type": "Point"
    }, 
    "mid": "M82", 
    "ngcid": "NGC 3034", 
    "remarks": "Galaxy   irregular Radio source", 
    "url": "/astronomy/messier/M82"
  }, 
  "responded": 1436523619.1128
```
