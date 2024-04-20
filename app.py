from flask import Flask, request
import os

PORT = 5022
app = Flask(__name__)
codes = {}

# Usage
# 1. Start the server
# 2. Hit startup endpoint
# 3. Hit oauth_callback endpoint
# 4. Hit get_code endpoint with the state to get the code

@app.route('/startup')
def startup():
    # App will stay up for 5 minutes on glitch
    return True

@app.route('/oauth/callback')
def oauth_callback():
    auth_code = request.args.get('code')
    state = request.args.get('state')
    codes[state] = auth_code
    return "Code received. You can close this page."

@app.route('/get_code/<state>')
def get_code(state):
    code = codes.get(state, None)
    if code:
        return {'code': code}
    return {'error': 'Code not found'}, 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', PORT)))
