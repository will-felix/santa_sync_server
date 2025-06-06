from flask import Flask, request, jsonify

app = Flask(__name__)

#BANCO DE DADOS FALSO (EM MEMORIA)
known_devices = {
    "DEAFE33453R4": [
        {
            "rule_type": "BINARY",
            "policy": "ALLOWLIST",
            "identifier": "hjkdgfjkdsdafdasfd"
        },
        {
            "rule_type": "BINARY",
            "policy": "BLOCKLIST",
            "identifier": "liouuihlkijjkjhjkh"
        }
    ]
}

@app.route('/')
def hello():
    return 'Servidor de sincronização funcionando!'

# ENDPOINT PREFLIGHT
@app.route('/preflight', methods=['POST'])
def preflight():
    data = request.get_json()
    serial_num = data.get('serial_num')

    print(f"Recebido preflight do serial: {serial_num}")

    # BUSCA REGRAS PARA O SERIAL NUMBER SE EXISTIR 
    rules = known_devices.get(serial_num, [])
    
    #RESPOSTA QUE O SANTA ESPERA
    response = {
        "client_mode": 1,
        "blacklist_regex": [],
        "whitelist_regex": [],
        "transitive_whitelist_regex": True,
        "batch_size": 20,
        "rules": rules
    }

    return jsonify(response)

import json

EVENTS_FILE = 'eventos.json' # <-- ARQUIVO ONDE GUARDA OS EVENTOS

# ENDPOINT POSTFLIGHT
@app.route('/postflight', methods=['POST'])
def postflight():
    data = request.get_json()

    print(f"Recebido postflight: {json.dumps(data, indent=2)}")
    
    with open(EVENTS_FILE, 'a') as f:
        
            for event in data.get('events', []):
                registro = {
                    "serial_num": data.get('serian_num'),
                    "event": event
                }     
                f.write(json.dumps(registro) + '\n')

    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

