import json
import logging
import os
from redis import Redis
from quart import Quart, request, render_template, redirect

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

app = Quart(__name__)
app.redis = Redis(host='redis', decode_responses = True)

@app.route('/geo_code', methods=['POST'])
async def geo_code():
    form = await request.form
    address = request.args.get('address') or form.get('address')
    pubsub = app.redis.pubsub()
    if address:
        app.redis.rpush('queue', json.dumps({'address': address}))
        logging.info(f'Pushed {address} onto queue')
        pubsub.subscribe('response:'+address)
    else:
        return {'Error': 'No valid request received. Pass parameters as form- or URL-parameters.'}
    for item in filter(lambda payload: payload.get('type') == 'message', pubsub.listen()):
        data = json.loads(item['data'])['response']
        logging.info(f'Returning {data} to client')
        return {'response': data}

@app.route('/', methods=['GET'])
def get_index_page():
    """Redirect to the orders page"""
    return redirect('/index')

@app.route('/index', methods=['GET'])
async def page():
    return await render_template('/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
