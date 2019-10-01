# Geo-spatial demo
Web-service frontend for geospatial transcoding via Open Street Map.

## Quickstart
```
docker-compose up --build
```
Access demo front-end at [localhost:5000](localhost:5000)

## Make commands
Install testing framework:
```
make install
```

Run pytest:
```
make unittest
```

Run pytest with coverage:
```
make coverage
```

Run app with docker-compose:
```
make dcup
```

## To-do
- [ ] Run unit-tests in container
- [ ] End-to-end integration tests
- [ ] To run in production switch away from Quart development server: https://pgjones.gitlab.io/quart/deployment.html
- [ ] Issues running on Windows: https://github.com/docker/for-win/issues/1804

## Run unittests
```
$ pytest --cov-report=term --cov-report=html --cov=api --cov=worker --cov-config=.coveragerc tests/tests.py
---------- coverage: platform darwin, python 3.7.2-final-0 -----------
Name               Stmts   Miss  Cover
--------------------------------------
api/api.py            41      0   100%
worker/worker.py      27      5    81%
--------------------------------------
TOTAL                 68      5    93%
```

## Manual tests
First, install requests:
```
pip install requests
```

```
>>> requests.post('http://localhost:5000/geo_code', {'address': 'New York City'}).json()
{'latlng': [40.7127281, -74.0060152]}
```

```
>>> requests.post('http://localhost:5000/geo_code', {'address': ''}).json()
{'Error': 'No valid request received. Pass parameters as form- or URL-parameters.'}
```

```
>>> requests.post('http://localhost:5000/geo_code', {'latlng': "[39.906217,116.3912757]"}).json()
{'address': '东长安街, 崇文, 北京市, 东城区, 北京市, 100010, 中国'}
```

```
>>> requests.post('http://localhost:5000/geo_code', {'lat':'[40.7127281]', 'lng':'[-74.0060152]'}).json()
{'address': 'New York City Hall, 260, Broadway, Civic Center, Manhattan Community Board 1, Manhattan, New York County, NYC, New York, 10000, USA'}
```

```
>>> requests.post('http://localhost:5000/geo_code', {'lat':'[40.7127281]'}).json()
{'Error': 'Both lat and lng must be set'}
```

```
>>> requests.post('http://localhost:5000/geo_code', {'lng':'[-74.0060152]'}).json()
{'Error': 'Both lat and lng must be set'}
```
