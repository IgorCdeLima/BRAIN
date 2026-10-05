# coordenador

Caixa de pedidos ao Coordenador `COORD-####.md` (template `BRAIN/99_Sistema/Templates/Pedido ao Coordenador.md`). Decisao: [[ADR-0020 Cadeia de pedidos de comando]].

Cadeia: **agente -> Coordenador -> Administrador -> humano.** O humano aprova cada comando com um clique, mas so digita o que so ele pode fazer (`tarefa aceitar`/`abrir`, lancador `papel`, senha, `sudo`).

- **Todo pedido**, com ou sem tarefa: qualquer papel cria um `COORD-####` aqui (proximo numero livre), com o comando exato, a pasta e o motivo, e diz ao humano so o numero. Com tarefa, preenche `tarefa:` e deixa a referencia na secao "Pedidos ao Coordenador" do cartao ([[ADR-0021 Pedidos ao Coordenador sempre em COORD e numeracao de qualidade por tarefa]]).
- **Erro inesperado** (ferramenta falhou, arquivo ausente, permissao negada, lancador recusou, conflito de merge): tambem vira `COORD-####`, com o erro exato, o que tentava fazer e a pasta. O Coordenador avalia a causa e registra a melhoria no Atendimento.
- O **Coordenador** le os pedidos `aberto` no panorama e executa com a aprovacao do humano. Se nao tiver permissao, abre um `ADM-####` em `operacao/administrador` e registra a referencia aqui.
- Status: `aberto` -> `concluido` | `escalado` (virou ADM) | `recusado`.
- Nada e apagado: pedidos antigos ficam como historico.
