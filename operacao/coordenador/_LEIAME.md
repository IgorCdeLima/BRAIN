# coordenador

Caixa de pedidos ao Coordenador `COORD-####.md` (template `BRAIN/99_Sistema/Templates/Pedido ao Coordenador.md`). Decisao: [[ADR-0020 Cadeia de pedidos de comando]].

Cadeia: **agente -> Coordenador -> Administrador -> humano.** O humano aprova cada comando com um clique, mas so digita o que so ele pode fazer (Orca, lancador `papel`, senha, `sudo`).

- **Pedido ligado a uma tarefa:** vai no cartao, secao "Pedidos ao Coordenador". Nao use esta pasta.
- **Pedido sem tarefa** (Pesquisador, Bibliotecario, ambiente): qualquer papel cria um `COORD-####` aqui (proximo numero livre), com o comando exato, a pasta e o motivo.
- O **Coordenador** le os pedidos `aberto` no panorama e executa com a aprovacao do humano. Se nao tiver permissao, abre um `ADM-####` em `operacao/administrador` e registra a referencia aqui.
- Status: `aberto` -> `concluido` | `escalado` (virou ADM) | `recusado`.
- Nada e apagado: pedidos antigos ficam como historico.
