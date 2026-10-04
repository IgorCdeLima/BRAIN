# administrador

Pedidos ao Administrador `ADM-####.md` (template `BRAIN/99_Sistema/Templates/Pedido ao Administrador.md`). Decisao: [[ADR-0019 Pedidos ao Administrador em operacao]].

Serve para o que exige area N4 (regras, perfis, lancador, hooks, `CLAUDE.md` do ambiente ou de projeto, lista de fontes) ou decisao de ambiente, e para o que so o Administrador faz (push, merge de ambiente).

- **Quem cria** (proximo numero livre):
  - o **Coordenador**, ao escalar (`pedido_por: coordenador`). Os demais papeis escalam ao Coordenador pelo cartao da tarefa;
  - o **Administrador**, para todo pedido direto do humano que altere algo: edicao, commit, merge, push, Docker (`pedido_por: humano`). Consultas e leituras nao geram ADM. Ele abre o ADM no inicio do trabalho, com o pedido nas palavras do humano.
- No cartao, deixe so a referencia: "Escalado ao Administrador: ADM-####".
- O **Administrador** le os pedidos com `status: aberto` no inicio da sessao, apresenta ao humano, executa com a aprovacao dele e preenche "Decisao do humano" e "Execucao".
- Status: `aberto` -> `em-andamento` -> `concluido` | `recusado`.
- Nada e apagado: pedidos antigos ficam como historico das mudancas de ambiente.
- **Citacao em notas do cofre (`BRAIN/`):** escreva pedidos `ADM-`, `COORD-`, `SEARCH-` e cartoes `T-` como codigo (`` `ADM-0011` ``), nunca como `[[link]]`. Esses arquivos ficam fora do cofre e o link quebra. Dentro de `operacao/` o `[[ADM-####]]` pode continuar (`ADM-0024`).
