---
tipo: pedido-coordenador
id: COORD-0020
status: concluido
urgencia: nao-bloqueante
pedido_por: administrador
tarefa: T-0015
criado: 2026-10-02
atendido_em: 2026-10-04
adm: ADM-0015, ADM-0025
tags: [ambiente, hooks, scratchpad, verificacao, revisor, seguranca]
---
# COORD-0020 - Verificar o hook restringir_escrita na revisao da T-0015

## Pedido

- [x] Quando a T-0015 chegar a `revisao`, incluir no pedido ao humano a verificacao real do [[ADM-0015]] (hook `restringir_escrita.py` com `@scratchpad` e prefixos ancorados na pasta da sessao). Na sessao `papel revisor` (ou `papel seguranca`) do worktree da T-0015, o humano pede ao agente, **antes ou depois da revisao, como teste de ambiente**:
  1. Gravar `x.py` no scratchpad da propria sessao -> deve ser **permitido**.
  2. `cd` para outra pasta (ex.: `$IA_RAIZ/operacao`) e gravar `<worktree>/qualidade/verificacoes/teste-adm15.md` -> deve ser **permitido** (prova que `CLAUDE_PROJECT_DIR` chega ao hook).
  3. Apagar o arquivo do passo 2 (nao commitar).
  4. Gravar `<worktree>/app/x.py` -> deve ser **negado**.
- [x] -> ADM-0025 Registrar o resultado dos 4 passos no ADM-0015 (secao Execucao) por um ADM ou avisando o Administrador. Se o passo 2 for negado: `CLAUDE_PROJECT_DIR` nao chega ao hook; o Administrador passa para a alternativa (`IA_PASTA_SESSAO` exportada pelo lancador).

Deixar a referencia "- [ ] COORD-0020 - verificar hook do ADM-0015 na revisao" na secao "Pedidos ao Coordenador" do cartao T-0015.

## Motivo

O teste na T-0012 nao foi possivel: o cartao esta `concluida` e o lancador so abre o Revisor com `status: revisao` (protecao correta, nao contornada). O merge foi feito antes do teste por decisao do humano (2026-10-02); se a variavel nao chegar, o hook volta ao comportamento antigo (falha fechada).

---

## Atendimento

Coordenador, 2026-10-03: o teste nao foi feito na revisao da T-0015. A tarefa passou por `revisao` sem que o roteiro fosse levado ao humano, e o cartao agora esta `concluida`, entao o lancador nao abre mais o Revisor nela. O pedido continua `aberto` e **passa para a revisao da T-0013**: quando ela chegar a `revisao`, levar ao humano os 4 passos acima, na sessao `papel seguranca` ou `papel revisor` do worktree da T-0013. A referencia entra no cartao da T-0013.
- **Causa:** o Coordenador nao estava em sessao quando a T-0015 entrou em `revisao`, e nada lembrou o humano.
- **Melhoria:** citar o COORD no proprio cartao, em "Pedidos ao Coordenador", e no topo da secao "Revisao", para o Revisor ver.

## Execucao do roteiro (seguranca, T-0013, 2026-10-04)

Sessao `papel seguranca` no worktree `/home/igor/orca/workspaces/lab/T-0013` (revisao de seguranca da T-0013). Resultado dos 4 passos:

1. Gravar `x.py` no scratchpad da sessao (Write) -> **permitido**.
2. `cd /home/igor/Documentos/01.GITHUB/BRAIN/operacao/tarefas` (o ambiente confirmou a troca do diretorio principal) e gravar `<worktree>/qualidade/seguranca/teste-adm15.md` (Write) -> **permitido**. Adaptacao: o roteiro cita `qualidade/verificacoes/`, que e do Revisor; usei a pasta liberada para a Seguranca. Prova que `CLAUDE_PROJECT_DIR` (pasta de inicio da sessao) chega ao hook: a mensagem do hook diz "Prefixos relativos valem a partir da pasta em que a sessao comecou (/home/igor/orca/workspaces/lab/T-0013)".
3. Arquivos dos passos 1 e 2 apagados (`rm`), nada commitado; `git status` limpo.
4. Gravar `<worktree>/app/x.py` (Write) -> **negado** pelo `PreToolUse:Write` com a lista de caminhos do papel e "Escrita ... negada. Nao tente outro caminho". Nao contornado.

Conclusao: o hook se comporta como o ADM-0015 previu. Falta registrar no ADM-0015 (secao Execucao), que a Seguranca nao pode escrever: fica para o Coordenador/Administrador.

Coordenador, 2026-10-04: **concluido.** Teste real feito, com o resultado esperado nos 4 passos. O registro no ADM-0015 (area N4) e o fechamento dele foram escalados ao ADM-0025, item 1, com o texto exato e a aprovacao do humano. A melhoria do atendimento anterior funcionou: com a referencia no cartao, a Seguranca viu o pedido e rodou o roteiro.
