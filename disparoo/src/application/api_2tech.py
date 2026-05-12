import subprocess
import json
import sys
from pathlib import Path

from flask import Flask, jsonify, request


app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYTHON_PATH = sys.executable


@app.route("/disparo-2", methods=["GET", "POST"])
def get_stats():
    try:
        body = request.get_json(silent=True) or {}

        processo = subprocess.run(
            [PYTHON_PATH, "-m", "src.application.main"],
            input=json.dumps(body),
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(PROJECT_ROOT)
        )

        linhas = processo.stdout.strip().splitlines()
        resultado_json = None

        for linha in reversed(linhas):
            linha = linha.strip()

            if linha.startswith("{") and linha.endswith("}"):
                try:
                    resultado_json = json.loads(linha)
                    break
                except json.JSONDecodeError:
                    pass

        if processo.returncode != 0:
            return jsonify({
                "status": "erro",
                "mensagem": "Erro ao rodar script Selenium",
                "returncode": processo.returncode,
                "resultado": resultado_json,
                "stdout": processo.stdout,
                "stderr": processo.stderr
            }), 500

        if not resultado_json:
            return jsonify({
                "status": "erro",
                "mensagem": "Nenhum JSON válido retornado pelo script",
                "stdout": processo.stdout,
                "stderr": processo.stderr
            }), 500

        if "error" in resultado_json:
            return jsonify({
                "status": "erro",
                "mensagem": "Script retornou erro",
                "resultado": resultado_json,
                "stdout": processo.stdout,
                "stderr": processo.stderr
            }), 500

        return jsonify({
            "status": "ok",
            "dados": resultado_json
        }), 200

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5090)