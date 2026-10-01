---
tipo: decisao
status: aceita
decidido_em: 2026-10-01
decidido_por: Igor
substituida_por:
criado: 2026-10-01
tags: [ambiente, agentes, coordenacao, operacao, qualidade, rastreabilidade]
---
# ADR-0021 Pedidos ao Coordenador sempre em COORD e numeracao de qualidade por tarefa

## Contexto

- O [[ADR-0020 Cadeia de pedidos de comando]] mandava o pedido ligado a tarefa para a secao "Pedidos ao Coordenador" do cartao e so o pedido sem tarefa para `COORD-####`. Na T-0007 o humano pediu o merge ao Revisor, que respondeu com o comando para o humano rodar (COORD-0005); o pedido acabou virando o COORD-0004.
- A Seguranca tentou editar um candidato do Inbox ja promovido e recebeu "File does not exist"; nenhuma regra dizia o que fazer com um erro inesperado (COORD-0003).
- A T-0006 e a T-0007 criaram `VER-0011` e `VER-0012` no lab ao mesmo tempo, em worktrees paralelos; o merge da T-0007 deu conflito (adicionar/adicionar). Numerar pelo "proximo livre" so enxerga o proprio worktree.
- Para resolver esse conflito o Coordenador devolveu o cartao `aprovada` para `revisao` a mao, fora do fluxo.
- Pedido ao Administrador: ADM-0012.

## Decisao

1. **Todo pedido ao Coordenador e um `COORD-####`**, com ou sem tarefa (comando fora do perfil, merge, push, acao no Orca, qualquer coisa que so o humano faria). O cartao guarda so a referencia na secao "Pedidos ao Coordenador". Ao humano o agente diz so o numero do pedido. Decisoes (ADR, direcao visual, duvida de produto) continuam em "Passos do humano".
2. **Erro inesperado vira `COORD-####`** (ferramenta falhou, arquivo ausente ou movido, permissao negada, comando inexistente, lancador recusou, conflito de merge), com o erro exato, o que tentava fazer e a pasta. O Coordenador avalia a causa e propoe a melhoria (ajuste de regra via `ADM-####`, aviso ao papel afetado ou candidato a conhecimento), registrando no Atendimento.
3. **Numeracao de qualidade por tarefa:** `VER-T0007-01`, `BUG-T0007-01`, `SEC-T0007-01`, `UX-T0007-01`. O agente confere so os registros da mesma tarefa no worktree. Registro sem tarefa (copia principal) segue `PREFIXO-####`. Registros antigos nao sao renomeados.
4. **O Revisor nao volta depois de `aprovada`.** Problema no merge (ex.: conflito): o Coordenador aborta, registra um `COORD-####` e decide o proximo passo com o humano. O lancador continua iniciando o Revisor so com `revisao`.

## Alternativas consideradas

| Alternativa | Pros | Contras |
|---|---|---|
| Manter pedido de tarefa no cartao (ADR-0020) | Tudo da tarefa num arquivo | Dois lugares para pedir; o humano ja pediu COORD mesmo com tarefa |
| Numeracao: conferir `git log --all -- qualidade/` antes de numerar | Mantem `VER-####` | Gasta tokens a cada registro; nao ve arquivos ainda nao commitados em outro worktree |
| Numeracao: arquivo contador | Simples de ler | Dentro do Git cada worktree tem uma copia (mesmo conflito); fora do Git exige escrita fora do worktree e tem corrida |
| Numeracao: Coordenador reserva no cartao | Sem colisao | Passo manual a mais e mais tokens por tarefa |
| Lancador aceitar `aprovada` para o Revisor | Retrabalho rapido | Reabre revisao fora do fluxo; o humano preferiu escalar ao Coordenador |

## Consequencias

- **Positivas:** um so lugar para pedidos; erros viram melhoria do ambiente em vez de contorno silencioso; sem colisao de numero entre tarefas paralelas e sem consulta extra (menos tokens).
- **Negativas / riscos:** mais arquivos em `operacao/coordenador`; dois formatos de numero convivem (antigos `VER-####` e novos `VER-T####-##`); `COORD-####` pode colidir se dois papeis criarem ao mesmo tempo (a caixa fica na copia principal, entao o risco e baixo; se acontecer, vira COORD de erro).
- Emenda o item 3 do [[ADR-0020 Cadeia de pedidos de comando]] (pedido de tarefa no cartao).

## Relacionadas

- [[ADR-0020 Cadeia de pedidos de comando]]
- [[ADR-0009 Catalogo de qualidade]]
- [[Fluxo de tarefa]]
- [[Rastreabilidade]]
