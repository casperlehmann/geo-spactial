# Geo-spatial demo

```
docker-compose up --build
```

api hosted on localhost:5000

redis running on localhost:6379

worker running on localhost:5001

```
Notice: Issues whis running on Windows.
https://github.com/docker/for-win/issues/1804
```

## Tests
```
>>> requests.post('http://localhost:5000/geo_code', {'address': 'New York City'}).json()
{'latlng': [40.7127281, -74.0060152]}
```

```
>>> requests.post('http://localhost:5000/geo_code', {'address': ''}).json()
{'Error': 'No valid request received. Pass parameters as form- or URL-parameters.'}
```

```
>>> requests.post('http://localhost:5000/geo_code', {'latlng':'[40.7127281,-74.0060152]'}).json()
{'address': 'New York City Hall, 260, Broadway, Civic Center, Manhattan Community Board 1, Manhattan, New York County, NYC, New York, 10000, USA'}
```
