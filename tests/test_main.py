import json
import threading
from http.server import HTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from app import main


@pytest.fixture
def url():
    main.gerenciador.__init__()
    servidor = HTTPServer(("127.0.0.1", 0), main.Handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{servidor.server_port}"
    servidor.shutdown()
    servidor.server_close()


def _post(url, corpo):
    cabecalho = {"Content-Type": "application/json"}
    return urlopen(Request(url + "/tarefas", json.dumps(corpo).encode(), cabecalho))


def test_health(url):
    assert json.load(urlopen(url + "/health")) == {"status": "ok"}


def test_criar_e_listar(url):
    assert _post(url, {"titulo": "A"}).status == 201
    assert json.load(urlopen(url + "/tarefas"))[0]["titulo"] == "A"


def test_titulo_vazio_retorna_400(url):
    with pytest.raises(HTTPError) as erro:
        _post(url, {"titulo": " "})
    assert erro.value.code == 400


def test_rota_inexistente_retorna_404(url):
    with pytest.raises(HTTPError) as erro:
        urlopen(url + "/x")
    assert erro.value.code == 404
    with pytest.raises(HTTPError) as erro:
        urlopen(Request(url + "/x", b"{}"))
    assert erro.value.code == 404
