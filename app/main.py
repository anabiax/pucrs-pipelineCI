"""Interface HTTP mínima do gerenciador de tarefas, usada como ponto de entrada do container."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from app.tarefas import GerenciadorTarefas

gerenciador = GerenciadorTarefas()


class Handler(BaseHTTPRequestHandler):
    def _responder(self, status, corpo):
        dados = json.dumps(corpo).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        if self.path == "/health":
            self._responder(200, {"status": "ok"})
        elif self.path == "/tarefas":
            self._responder(200, [vars(t) for t in gerenciador.listar()])
        else:
            self._responder(404, {"erro": "não encontrado"})

    def do_POST(self):
        if self.path != "/tarefas":
            return self._responder(404, {"erro": "não encontrado"})
        tamanho = int(self.headers.get("Content-Length", 0))
        try:
            titulo = json.loads(self.rfile.read(tamanho)).get("titulo")
            self._responder(201, vars(gerenciador.adicionar(titulo)))
        except (ValueError, AttributeError) as erro:
            self._responder(400, {"erro": str(erro)})


def main():
    porta = int(os.environ.get("PORT", "8000"))
    HTTPServer(("0.0.0.0", porta), Handler).serve_forever()


if __name__ == "__main__":  # pragma: no cover
    main()
