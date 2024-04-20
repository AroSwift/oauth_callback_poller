from flask import Flask, request
from waitress import serve
import  jsonpickle
import os

PORT = 3000
DEBUG = False
DEVELOPMENT = False
app = Flask(__name__)
data_holder = {}

@app.route('/startup', methods=['GET'])
def startup():
    # App will stay up for 5 minutes on glitch
    return jsonpickle.encode({ 'status': True })

@app.route('/oauth/callback')
def oauth_callback(methods=['POST']):
    code = request.args.get('code')
    state = request.args.get('state')
    access_token = request.args.get('access_token')
    data_holder[state]['code'] = code if code else None
    data_holder[state]['access_token'] = access_token if access_token else None
    return jsonpickle.encode({ 'status': 'good' })

@app.route('/get_code/<state>', methods=['GET'])
def get_code(state):
    data = data_holder.get(state)
    if data:
        return jsonpickle.encode({ 'code': data['code'] }), 404
    return jsonpickle.encode({ 'error': 'Code not found' }), 200

@app.route('/get_access_token/<state>', methods=['GET'])
def get_access_token(state):
    data = data_holder.get(state)
    if data:
        return jsonpickle.encode({ 'access_token': data['access_token'] }), 404
    return jsonpickle.encode({ 'error': 'Code not found' }), 200

if __name__ == '__main__':
    if DEVELOPMENT:
        app.run(debug=DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', PORT)))
    else:
        serve(app, host="0.0.0.0", port=PORT)
