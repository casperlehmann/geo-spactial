import pytest
import fakeredis
import json

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.api import app
from worker.worker import consume

@pytest.mark.asyncio
async def test_client_root_redirects():
    client = app.test_client()
    response = await client.get('/')
    assert response.status_code == 302

@pytest.mark.asyncio
async def test_client_index_loads():
    client = app.test_client()
    response = await client.get('/index')
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_client_geo_code_loads():
    client = app.test_client()
    response = await client.post('/geo_code', json=None)
    assert response.status_code == 400
    return_data = json.loads(response.response.data)
    assert list(return_data.keys())[0] == 'Error'
    assert return_data['Error'] == 'No valid request received. Pass parameters as form- or URL-parameters.'


class fake_pubsub:
    """Fakeredis does not support subscription. We manually mock the methods used.

    Source: https://pypi.org/project/fakeredis/
    """
    def __init__(self, redis):
        self.parent = redis
        self.data = None

    def listen(self):
        yield {'type': 'message', 'data': json.dumps({'response': f'Mocked response for subscription {self.data}'})}

    def __call__(self):
        return self

    def subscribe(self, *args, **kwargs):
        self.data = args[0]

@pytest.mark.asyncio
async def test_client_geo_code_accepts_data():
    client = app.test_client()
    app.redis = fakeredis.FakeStrictRedis()
    app.redis.pubsub = fake_pubsub(app.redis)
    data = {'address': 'New York City'}
    response = await client.post('/geo_code', form=data)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_client_geo_code_with_address_yields_from_subscribed_channel():
    client = app.test_client()
    app.redis = fakeredis.FakeStrictRedis()
    app.redis.pubsub = fake_pubsub(app.redis)
    data = {'address': 'New York City'}
    response = await client.post('/geo_code', form=data)
    return_data = json.loads(response.response.data)
    assert response.status_code == 200
    assert list(return_data.keys())[0] == 'latlng'
    assert return_data['latlng'] == 'Mocked response for subscription response:New York City'

@pytest.mark.asyncio
async def test_client_geo_code_with_latlng_yields_from_subscribed_channel():
    client = app.test_client()
    app.redis = fakeredis.FakeStrictRedis()
    app.redis.pubsub = fake_pubsub(app.redis)
    data = {'latlng': '["35.6828387", "139.7594549"]'}
    response = await client.post('/geo_code', form=data)
    return_data = json.loads(response.response.data)
    assert response.status_code == 200
    assert list(return_data.keys())[0] == 'address'
    assert return_data['address'] == 'Mocked response for subscription response:["35.6828387", "139.7594549"]'

@pytest.mark.asyncio
async def test_client_geo_code_with_lat_and_lng_yields_from_subscribed_channel():
    client = app.test_client()
    app.redis = fakeredis.FakeStrictRedis()
    app.redis.pubsub = fake_pubsub(app.redis)
    data = {'lat': '35.6828387', 'lng': '139.7594549'}
    response = await client.post('/geo_code', form=data)
    return_data = json.loads(response.response.data)
    assert response.status_code == 200
    assert list(return_data.keys())[0] == 'address'
    assert return_data['address'] == 'Mocked response for subscription response:["35.6828387", "139.7594549"]'

@pytest.mark.asyncio
async def test_client_geo_code_with_lat_only_yields_from_subscribed_channel():
    client = app.test_client()
    app.redis = fakeredis.FakeStrictRedis()
    app.redis.pubsub = fake_pubsub(app.redis)
    data = {'lat': '35.6828387'}
    response = await client.post('/geo_code', form=data)
    return_data = json.loads(response.response.data)
    assert response.status_code == 400
    assert list(return_data.keys())[0] == 'Error'
    assert return_data['Error'] == 'Both lat and lng must be set'

@pytest.mark.asyncio
async def test_client_geo_code_with_lng_yields_from_subscribed_channel():
    client = app.test_client()
    app.redis = fakeredis.FakeStrictRedis()
    app.redis.pubsub = fake_pubsub(app.redis)
    data = {'lng': '139.7594549'}
    response = await client.post('/geo_code', form=data)
    return_data = json.loads(response.response.data)
    assert response.status_code == 400
    assert list(return_data.keys())[0] == 'Error'
    assert return_data['Error'] == 'Both lat and lng must be set'

class FakeOpenStreetMap():
    def __init__(self, query, method=None):
        self.query = query
        self.method = method

    @property
    def lat(self):
        return f'Mocked response for {self.query}'

    @property
    def lng(self):
        return f'Mocked response for {self.query}'

    @property
    def address(self):
        return f'Mocked address response for {self.query}'

def test_consume_takes_latlng():
    redis = fakeredis.FakeStrictRedis()
    redis.pubsub = fake_pubsub(redis)
    latlng_data = json.dumps(['35.6828387', '139.7594549'])
    redis.pubsub.subscribe(latlng_data)
    redis.rpush('queue', json.dumps({'latlng': latlng_data}))
    consume(redis, ['queue'], FakeOpenStreetMap)
    queue = list(redis.pubsub.listen())
    assert json.loads(queue[0]['data'])['response'] == 'Mocked response for subscription ["35.6828387", "139.7594549"]'

def test_consume_takes_address():
    redis = fakeredis.FakeStrictRedis()
    redis.pubsub = fake_pubsub(redis)
    address_data = 'New York City'
    redis.pubsub.subscribe(address_data)
    redis.rpush('queue', json.dumps({'address': address_data}))
    consume(redis, ['queue'], FakeOpenStreetMap)
    queue = list(redis.pubsub.listen())
    assert json.loads(queue[0]['data'])['response'] == 'Mocked response for subscription New York City'
