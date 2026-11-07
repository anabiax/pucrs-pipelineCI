"""Gerenciador de tarefas em memória (aplicação de exemplo para o pipeline de CI)."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Tarefa:
    id: int
    titulo: str
    concluida: bool = False


@dataclass
class GerenciadorTarefas:
    _tarefas: List[Tarefa] = field(default_factory=list)
    _proximo_id: int = 1

    def adicionar(self, titulo: str) -> Tarefa:
        titulo = (titulo or "").strip()
        if not titulo:
            raise ValueError("O título da tarefa não pode ser vazio.")
        tarefa = Tarefa(id=self._proximo_id, titulo=titulo)
        self._tarefas.append(tarefa)
        self._proximo_id += 1
        return tarefa

    def listar(self) -> List[Tarefa]:
        return list(self._tarefas)

    def concluir(self, tarefa_id: int) -> Tarefa:
        tarefa = self._buscar(tarefa_id)
        tarefa.concluida = True
        return tarefa

    def remover(self, tarefa_id: int) -> None:
        self._tarefas.remove(self._buscar(tarefa_id))

    def _buscar(self, tarefa_id: int) -> Tarefa:
        for tarefa in self._tarefas:
            if tarefa.id == tarefa_id:
                return tarefa
        raise KeyError(f"Tarefa {tarefa_id} não encontrada.")
