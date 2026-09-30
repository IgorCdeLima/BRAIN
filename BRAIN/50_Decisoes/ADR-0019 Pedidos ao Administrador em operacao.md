---
tipo: decisao
status: aceita
decidido_em: 2026-09-30
decidido_por: Igor
substituida_por:
criado: 2026-09-30
tags: [ambiente, agentes, administracao, operacao]
---
# ADR-0019 Pedidos ao Administrador em operacao

## Contexto

- O [[ADR-0018 Papel Administrador com senha e aprovacao a cada mudanca]] criou a escalacao Coordenador -> Administrador, mas nao disse onde o pedido fica.
- Na T-0005 o Coordenador improvisou uma secao "Notas para o Administrador" dentro do cartao. O Administrador so achou porque o humano avisou; pedidos espalhados em cartoes se perdem.
- O humano propos uma pasta propria para o que precisa da avaliacao do Administrador.

## Decisao

1. **Pasta `operacao/administrador/`**, com um arquivo por pedido `ADM-####.md` (template `BRAIN/99_Sistema/Templates/Pedido ao Administrador.md`). Status: `aberto` -> `em-andamento` -> `concluido` | `recusado`.
2. Fica em `operacao/`, e nao no `BRAIN/`: pedido pendente e estado de trabalho, como os `SEARCH-####` em `operacao/pesquisas`; o Brain guarda conhecimento e so o Bibliotecario escreve nele.
3. **So o Coordenador cria** pedidos (hook de escrita e perfil liberam a pasta so para ele). Os demais papeis escalam ao Coordenador pelo cartao. No cartao fica so a referencia `ADM-####`.
4. O **Administrador** le os pedidos `aberto` no inicio de toda sessao (pedido inicial do lancador), apresenta ao humano e executa cada item com a aprovacao dele, registrando a decisao e os commits no proprio pedido.

## Alternativas consideradas

| Alternativa | Por que nao |
|---|---|
| Secao no cartao da tarefa | Espalha os pedidos; pedido de ambiente sem tarefa nao tem onde ficar |
| Pasta no `BRAIN/` (ex.: `80_Administrador`) | Mistura estado de trabalho com conhecimento; exigiria liberar escrita no Brain fora do Inbox |
| Proposta no `BRAIN/00_Inbox` | O Inbox e do Bibliotecario (candidatos a conhecimento), nao fila de trabalho |
| Todos os papeis criam pedidos | Mais caminhos de escrita; o Coordenador ja filtra e ve o contexto da tarefa |

## Consequencias

- Um lugar unico para o Administrador procurar; o panorama do Coordenador mostra os ADM abertos.
- Mais uma pasta que o hook de escrita do Coordenador libera.
- O pendente da T-0005 (push de BRAIN e lab, worktree) continua no cartao; pedidos novos ja usam a pasta.
