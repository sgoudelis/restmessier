# restmessier

## Demostration of RESTful Web API for Messier Objects

This is a simple RESTful Web API for CRUD operations on a collection of Messier celestial targets based on MongoDB. Also, the Geospatial api of MongoDB is used which provides the functionlity of quering the API for objects that are nearby another Messier object or a set of WGS84 coordinates. This API is also a WSGI application with allows for easy scaling.

What is a Messier object? https://en.wikipedia.org/wiki/Messier_object


## Todo

1. Proper caching headers

## Requirements

1. PyMongo
2. jsonschema
3. flask
4. python 2.7+

### Setup

Create a virtual enviroment with virtualenv.

```
$ virtualenv  env
Running virtualenv with interpreter /usr/bin/python2
New python executable in env/bin/python2
Also creating executable in env/bin/python
Installing setuptools, pip...done.

$ env/bin/pip install pymongo jsonschema flask 
```

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
$ curl -i -X GET http://localhost:5000/astronomy/messier/m82
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
}
```


### Delete an object

```
$ curl -X DELETE http://localhost:5000/astronomy/messier/m02
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 378
Server: Werkzeug/0.10.4 Python/2.7.9
Date: Thu, 16 Jul 2015 09:04:47 GMT

{
  "object": {
    "_id": "559bacd8e5e7103b9611f3a9", 
    "constellation": "SCORPIO", 
    "loc": {
      "coordinates": [
        16.2036, 
        -26.24
      ], 
      "type": "Point"
    }, 
    "mid": "M04", 
    "ncgid": "NGC 6121", 
    "remarks": "Globular cluster", 
    "status": "deleted"
  }, 
  "responded": 1437036051.36044
}
```

### Update an object

```
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"ngcid":"xyz"}'  http://localhost:5000/astronomy/messier/m06
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 383
Server: Werkzeug/0.10.4 Python/2.7.9
Date: Thu, 16 Jul 2015 08:58:56 GMT

{
  "object": {
    "_id": "559bacd8e5e7103b9611f3ab", 
    "constellation": "SCORPIO", 
    "loc": {
      "coordinates": [
        17.3648, 
        -32.11
      ], 
      "type": "Point"
    }, 
    "mid": "M06", 
    "ngcid": "xyz", 
    "remarks": "Open cluster   naked-eye Superb cluster", 
  }, 
  "responded": 1437037136.738732
}
```

### Get nearby objects

Query the API to get objects that are no further away than 3 degrees.

```
$ curl -i -X GET  http://localhost:5000/astronomy/messier/m01/nearby/3
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 1128
Server: Werkzeug/0.10.4 Python/2.7.9
Date: Thu, 16 Jul 2015 09:06:24 GMT

{
  "centerobject": {
    "_id": "559bacd8e5e7103b9611f3a6", 
    "constellation": "TAURUS", 
    "loc": {
      "coordinates": [
        5.313, 
        21.59
      ], 
      "type": "Point"
    }, 
    "mid": "M01", 
    "ncgid": "NGC 1952", 
    "pipes": "nai", 
    "remarks": "Supernova remnant   Crab Nebula", 
    "url": "/astronomy/messier/M01"
  }, 
  "nearbyobjects": [
    {
      "_id": "559bacd8e5e7103b9611f3d1", 
      "constellation": "TAURUS", 
      "loc": {
        "coordinates": [
          3.4406, 
          23.58
        ], 
        "type": "Point"
      }, 
      "mid": "M45", 
      "ncgid": "NGCMEL", 
      "remarks": "Open cluster   The Pleiades \u2013 Seven Sisters", 
      "url": "/astronomy/messier/M45"
    }, 
    {
      "_id": "559bacd8e5e7103b9611f3c8", 
      "constellation": "GEMINI", 
      "loc": {
        "coordinates": [
          6.0548, 
          24.21
        ], 
        "type": "Point"
      }, 
      "mid": "M35", 
      "ncgid": "NGC 2168", 
      "remarks": "Open cluster   naked eye", 
      "url": "/astronomy/messier/M35"
    }
  ], 
  "responded": 1437037584.890835
}
```

### Query the API to get nearby objects within a circle (of N degrees) with a RA and DEC coordinates given. 

```
$ curl -i -X GET http://localhost:5000/astronomy/messier/nearby/18.45/22.12/5
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 853
Server: Werkzeug/0.10.4 Python/2.7.9
Date: Thu, 16 Jul 2015 09:11:01 GMT

{
  "nearbyobjects": [
    {
      "_id": "559bacd8e5e7103b9611f3eb", 
      "constellation": "SAGITTA", 
      "loc": {
        "coordinates": [
          19.513, 
          18.39
        ], 
        "type": "Point"
      }, 
      "mid": "M71", 
      "ncgid": "NGC 6838", 
      "remarks": "Open cluster   very distant", 
      "url": "/astronomy/messier/M71"
    }, 
    {
      "_id": "559bacd8e5e7103b9611f3c0", 
      "constellation": "VULPECULA", 
      "loc": {
        "coordinates": [
          19.5724, 
          22.35
        ], 
        "type": "Point"
      }, 
      "mid": "M27", 
      "ncgid": "NGC 6853", 
      "remarks": "Planetary   Dumb-Bell Nebula", 
      "url": "/astronomy/messier/M27"
    }
  ], 
  "responded": 1437037861.534802, 
  "target": {
    "coordinates": [
      18.45, 
      22.12
    ], 
    "degrees": 5
  }
}

```

