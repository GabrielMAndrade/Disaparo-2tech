import subprocess
import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

PROJECT_ROOT = "/home/node/Ranking_2tech"
PYTHON_PATH = os.path.join(PROJECT_ROOT, ".venv", "bin", "python3")

@app.route("/ranking", methods=["GET"])
def get_stats():
    try:
        body = request.get_json(silent=True) or {}

        processo = subprocess.run(
            [PYTHON_PATH, "-m", "src.application.main"],
            input=json.dumps(body),
            capture_output=True,
            text=True,
            timeout=300,
            cwd=PROJECT_ROOT
        )

        if processo.returncode != 0:
            return jsonify({
                "status": "erro",
                "mensagem": "Erro ao rodar script Selenium",
                "stderr": processo.stderr,
                "stdout": processo.stdout
            }), 500

        linhas = processo.stdout.strip().splitlines()
        resultado_json = {}

        for linha in reversed(linhas):
            linha = linha.strip()
            if linha.startswith("{") and linha.endswith("}"):
                resultado_json = json.loads(linha)
                break

        if not resultado_json:
            return jsonify({
                "status": "erro",
                "mensagem": "Nenhum JSON válido retornado pelo script",
                "stdout": processo.stdout,
                "stderr": processo.stderr
            }), 500

        return jsonify(resultado_json)

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5090)