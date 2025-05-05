from flask import Flask, request, jsonify
from requests_oauthlib import OAuth1
import requests

app = Flask(__name__)

# Credenciales NetSuite
CONSUMER_KEY = 'aad3d730f2ad5f5ca143f72ba5e4a45b915567603b35d9bc72f731fcd649e577'
CONSUMER_SECRET = '83e6815536254f601b72e1d1a245fd86b48b23105346566dfe24d63128e8972b'
ACCESS_TOKEN = '6d11bc2f242721fe2745f34dd7a0502168c25d79b95b29505dc8d740e3194211'
ACCESS_SECRET = 'f80bb6e21b54e6c927faab11dadfae633bf31b3f845e27400f50ef581bf11986'
REALM = '7768258'

BASE_URL = 'https://7768258.restlets.api.netsuite.com/app/site/hosting/restlet.nl'
SCRIPT_ID = '2383'
DEPLOY_ID = '1'

@app.route('/netsuite-data', methods=['GET'])
def get_netsuite_data():
    fecha_desde = request.args.get('fechaDesde')
    fecha_hasta = request.args.get('fechaHasta')

    if not fecha_desde or not fecha_hasta:
        return jsonify({'error': 'Debe incluir los parámetros fechaDesde y fechaHasta'}), 400

    params = {
        'script': SCRIPT_ID,
        'deploy': DEPLOY_ID,
        'fechaDesde': fecha_desde,
        'fechaHasta': fecha_hasta
    }

    auth = OAuth1(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_SECRET,
        realm=REALM,
        signature_method='HMAC-SHA256'
    )

    response = requests.get(BASE_URL, auth=auth, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            'error': 'Error al conectarse a NetSuite',
            'status': response.status_code,
            'body': response.text
        }), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
