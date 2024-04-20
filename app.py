from flask import Flask, request
from waitress import serve
import  jsonpickle
import os

PORT = 3000
DEBUG = False
DEVELOPMENT = False
app = Flask(__name__)
codes = {}

# Usage
# 1. Start the server
# 2. Hit startup endpoint
# 3. Hit oauth_callback endpoint
# 4. Hit get_code endpoint with the state to get the code

@app.route('/startup', methods=['GET'])
def startup():
    # App will stay up for 5 minutes on glitch
    return jsonpickle.encode({ 'status': True })

@app.route('/oauth/callback')
def oauth_callback(methods=['POST']):
    auth_code = request.args.get('code')
    state = request.args.get('state')
    codes[state] = auth_code
    return jsonpickle.encode({ 'status': 'good' })

@app.route('/get_code/<state>', methods=['GET'])
def get_code(state):
    code = codes.get(state)
    if code:
        return jsonpickle.encode({ 'code': code })
    return jsonpickle.encode({ 'error': 'Code not found' })

if __name__ == '__main__':
    if DEVELOPMENT:
        app.run(debug=DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', PORT)))
    else:
        serve(app, host="0.0.0.0", port=PORT)
