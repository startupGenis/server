# manager_server.py
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
class Config:
    AUTH_KEY = os.getenv('AUTH_KEY', 'chave_secreta')  # Better to use environment variable
    PORT = int(os.getenv('PORT', 5000))
    HOST = '0.0.0.0'

# State management
class DNSState:
    def __init__(self):
        self.client_ip = None
        self.client_port = None
        self.last_update = None

    def update(self, ip, port):
        self.client_ip = ip
        self.client_port = port
        self.last_update = datetime.now()

dns_state = DNSState()

# Middleware for authentication
def require_auth(f):
    def decorated(*args, **kwargs):
        auth_key = request.headers.get('X-Auth-Key')
        if auth_key != Config.AUTH_KEY:
            logging.warning("Invalid authentication attempt")
            return jsonify({'error': 'Invalid authentication key'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/api/update-dns', methods=['POST'])
@require_auth
def update_dns():
    try:
        data = request.get_json()
        ip = data.get('ip')
        port = data.get('port')

        if not ip or not port:
            return jsonify({'error': 'Missing IP or port'}), 400

        dns_state.update(ip, port)
        logging.info(f"DNS updated: {ip}:{port}")
        
        return jsonify({
            'status': 'success',
            'ip': ip,
            'port': port,
            'timestamp': dns_state.last_update.isoformat()
        })

    except Exception as e:
        logging.error(f"Error updating DNS: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    if dns_state.client_ip and dns_state.client_port:
        target_url = f"http://{dns_state.client_ip}:{dns_state.client_port}"
        logging.info(f"Redirecting to: {target_url}")
        return redirect(target_url)
    return "No active client registered", 404

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    logging.info("Starting DNS Manager Server")
    app.run(host=Config.HOST, port=Config.PORT)

