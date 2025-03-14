from flask import Flask, request, redirect

app = Flask(__name__)

# Senha para autenticação
SENHA_CORRETA = "genis789"

# Armazena o IP e a porta do servidor local
ip_atual = None
porta_atual = None

@app.route("/update_ip", methods=["POST"])
def update_ip():
    global ip_atual, porta_atual

    senha = request.form.get("senha")
    if senha != SENHA_CORRETA:
        return "Acesso negado! Senha incorreta.", 403

    ip_atual = request.form.get("ip")
    porta_atual = request.form.get("porta")

    print(f"IP e porta atualizados para: {ip_atual}:{porta_atual}")
    return "IP e porta atualizados com sucesso", 200

@app.route("/")
def home():
    if ip_atual and porta_atual:
        redirecionamento_url = f"http://{ip_atual}:{porta_atual}"
        return redirect(redirecionamento_url, code=302)
    else:
        return "Aguardando dados do servidor local...", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
