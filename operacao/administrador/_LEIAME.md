# administrador

Pedidos ao Administrador `ADM-####.md` (template `BRAIN/99_Sistema/Templates/Pedido ao Administrador.md`). Decisao: [[ADR-0019 Pedidos ao Administrador em operacao]].

Serve para o que exige area N4 (regras, perfis, lancador, hooks, `CLAUDE.md` do ambiente ou de projeto, lista de fontes) ou decisao de ambiente, e para o que so o Administrador faz (push, merge de ambiente).

- **So o Coordenador cria** um pedido (proximo numero livre). Os demais papeis escalam ao Coordenador pelo cartao da tarefa.
- No cartao, deixe so a referencia: "Escalado ao Administrador: ADM-####".
- O **Administrador** le os pedidos com `status: aberto` no inicio da sessao, apresenta ao humano, executa com a aprovacao dele e preenche "Decisao do humano" e "Execucao".
- Status: `aberto` -> `em-andamento` -> `concluido` | `recusado`.
- Nada e apagado: pedidos antigos ficam como historico das mudancas de ambiente.
