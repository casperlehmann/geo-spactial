import json
import logging
import os
from redis import Redis
from quart import Quart, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

app = Quart(__name__)
app.redis = Redis(host='redis', decode_responses = True)

@app.route('/geo_code', methods=['POST'])
async def geo_code():
    form = await request.form
    address = request.args.get('address') or form.get('address')
    logging.info(f'Pushed {address} onto queue')
    app.redis.rpush('queue', json.dumps({'address': address}))
    return {'message': 'I come in peace'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
