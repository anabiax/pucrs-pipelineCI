import pytest

from app.tarefas import GerenciadorTarefas


@pytest.fixture
def gerenciador():
    return GerenciadorTarefas()


def test_adicionar_tarefa(gerenciador):
    tarefa = gerenciador.adicionar("Estudar CI/CD")
    assert tarefa.id == 1
    assert tarefa.titulo == "Estudar CI/CD"
    assert tarefa.concluida is False


def test_adicionar_titulo_vazio_gera_erro(gerenciador):
    with pytest.raises(ValueError):
        gerenciador.adicionar("   ")


def test_listar_retorna_todas(gerenciador):
    gerenciador.adicionar("A")
    gerenciador.adicionar("B")
    assert [t.titulo for t in gerenciador.listar()] == ["A", "B"]


def test_ids_sao_sequenciais(gerenciador):
    assert gerenciador.adicionar("A").id == 1
    assert gerenciador.adicionar("B").id == 2


def test_concluir_tarefa(gerenciador):
    tarefa = gerenciador.adicionar("A")
    gerenciador.concluir(tarefa.id)
    assert gerenciador.listar()[0].concluida is True


def test_remover_tarefa(gerenciador):
    tarefa = gerenciador.adicionar("A")
    gerenciador.remover(tarefa.id)
    assert gerenciador.listar() == []


def test_concluir_inexistente_gera_erro(gerenciador):
    with pytest.raises(KeyError):
        gerenciador.concluir(99)


def test_remover_inexistente_gera_erro(gerenciador):
    with pytest.raises(KeyError):
        gerenciador.remover(99)
