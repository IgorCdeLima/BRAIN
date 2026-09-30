# operacao — estado do trabalho do ambiente

Dados operacionais: mudam muito e não são conhecimento. Por isso ficam fora do Brain.

- `tarefas/` — cartões de tarefa e handoffs entre agentes.
- `pesquisas/` - pedidos de pesquisa `SEARCH-####`.
- `coordenador/` - pedidos de comando ao Coordenador `COORD-####` sem tarefa (qualquer papel cria).
- `administrador/` - pedidos ao Administrador `ADM-####` (so o Coordenador cria).

Os logs automáticos ficam em `01_IA/logs`, fora do Git (ver `logs/_LEIAME.md`).
- `qualidade/` — verificações, bugs e achados de segurança **do próprio ambiente 01_IA**.
  Os de cada projeto ficam no repositório do projeto, em `qualidade/`.
