from flask import Flask, request, jsonify, redirect
#from flask_cors import CORS  # Importando Flask-CORS
import logging

app = Flask(__name__)
#CORS(app)  # Habilitando CORS para o aplicativo Flask

# Configuração de autenticação
CHAVE_AUTENTICACAO = 'chave_secreta'

# Variáveis globais para armazenar o IP e a porta do servidor local
ip_atualizado = None
porta_atualizada = None

# Configuração de logging
logging.basicConfig(level=logging.INFO)

@app.route('/atualizar_dns', methods=['POST'])
def atualizar_dns():
    global ip_atualizado, porta_atualizada

    # Verifica a chave de autenticação
    chave = request.headers.get('X-Auth-Key')
    if chave != CHAVE_AUTENTICACAO:
        logging.warning("Tentativa de acesso com chave de autenticação inválida")
        return jsonify({'error': 'Chave de autenticação inválida'}), 403

    # Obtém o IP e porta do payload da solicitação
    dados = request.json
    ip_atualizado = dados.get('ip')
    porta_atualizada = dados.get('porta')

    # Logando a solicitação recebida
    if ip_atualizado and porta_atualizada:
        logging.info(f"Recebida solicitação de atualização de IP: {ip_atualizado}:{porta_atualizada}")
    else:
        logging.error("Dados inválidos recebidos. IP ou porta faltando.")
        return jsonify({'error': 'Dados inválidos. IP ou porta faltando.'}), 400

    return jsonify({'status': 'IP atualizado com sucesso', 'ip': ip_atualizado, 'porta': porta_atualizada})

@app.route('/')
def index():
    if ip_atualizado and porta_atualizada:
        # Redireciona o usuário para o servidor local
        logging.info(f"Redirecionando para o servidor local: http://{ip_atualizado}:{porta_atualizada}")
        return redirect(f"http://{ip_atualizado}:{porta_atualizada}")
    else:
        logging.warning("Nenhum IP atualizado encontrado para redirecionamento.")
        return "Nenhum IP atualizado encontrado.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)