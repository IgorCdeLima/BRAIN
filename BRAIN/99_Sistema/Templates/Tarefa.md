---
tipo: tarefa
id: T-####
status: backlog
projeto:
papel:
interface: nao
seguranca: nao
tamanho: normal
criado: {{date:YYYY-MM-DD}}
tags: []
---
# T-#### - {{title}}

<!-- Status: backlog -> pronta -> em-andamento -> revisao -> (correcao -> em-andamento -> revisao) -> aprovada -> concluida (ou bloqueada).
     aguardando-humano: o agente parou esperando uma decisao do humano (ex.: escolha da direcao visual).
     aguardando-pesquisa: o agente parou esperando um SEARCH-#### bloqueante (Fluxo de pesquisa).
     interface: sim quando a tarefa muda a tela -> o Designer faz a revisao visual antes do Revisor fechar.
     seguranca: sim quando toca upload, autenticacao, dados pessoais, segredos, rede ou novas dependencias
     -> a Seguranca faz a revisao antes do Revisor fechar. Criterios no Fluxo de tarefa. -->
<!--
     Tamanho: trivial | normal | grande. Arquivo: operacao/tarefas/T-####.md
     Worktree no Orca: T-####-descricao-curta -->

## Objetivo

## Contexto

<!-- Links para docs do projeto, notas do Brain, bugs relacionados. -->

## Criterios de aceite

- [ ]

## Restricoes / o que NAO fazer

-

## Verificacoes obrigatorias

<!-- Da Matriz de verificacao, conforme o tipo e o tamanho da tarefa. -->

- [ ] Testes automaticos passam
- [ ] Criterios de aceite atendidos
- [ ] Revisao de codigo

---

## Entrega

<!-- Preenchido pelo executor ao terminar. -->

- **Worktree / branch:**
- **Commits:**
- **Decisoes tomadas:**
- **Duvidas em aberto:**
- **Verificacoes feitas:**
- **Verificacoes NAO feitas (e por que):**
- **Candidatos a conhecimento:**

## Pedidos ao Coordenador

<!-- So referencias: "- [ ] COORD-#### - resumo". O pedido (comando exato, pasta, motivo, ou o erro inesperado)
     fica em operacao/coordenador/COORD-####.md (ADR-0021).
     O Coordenador marca [x] ao executar (com a aprovacao do humano) ou "-> ADM-####" ao escalar ao Administrador. -->

- [ ]

## Passos do humano

<!-- So decisoes (escolher direcao visual, aceitar ADR, responder duvida) e acoes que so o humano pode
     fazer (Orca, lancador papel, senha, sudo, criar .env com segredo). Comandos vao em "Pedidos ao Coordenador". -->

- [ ]

## Revisao visual

<!-- So se interface: sim. Preenchido pelo Designer antes do Revisor fechar. Nao muda o status. -->

- **UX:**
- **Commit avaliado:**
- **Bloqueantes:**

## Revisao de seguranca

<!-- So se seguranca: sim. Preenchido pela Seguranca antes do Revisor fechar. Nao muda o status. -->

- **SEC:**
- **Commit avaliado:**
- **Bloqueantes (severidade media ou maior):**
- **NAO verificado:**

## Revisao

<!-- Preenchido pelo Revisor. Um VER por commit verificado. Considera os UX e SEC bloqueantes. -->

- **VER:**
- **Commit verificado:**
- **Resultado:**
- **Correcoes pedidas (se status correcao):**
- **Merge (humano):**
