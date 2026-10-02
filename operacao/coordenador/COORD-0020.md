---
tipo: pedido-coordenador
id: COORD-0020
status: aberto
urgencia: nao-bloqueante
pedido_por: administrador
tarefa: T-0015
criado: 2026-10-02
atendido_em:
adm: ADM-0015
tags: [ambiente, hooks, scratchpad, verificacao, revisor, seguranca]
---
# COORD-0020 - Verificar o hook restringir_escrita na revisao da T-0015

## Pedido

- [ ] Quando a T-0015 chegar a `revisao`, incluir no pedido ao humano a verificacao real do [[ADM-0015]] (hook `restringir_escrita.py` com `@scratchpad` e prefixos ancorados na pasta da sessao). Na sessao `papel revisor` (ou `papel seguranca`) do worktree da T-0015, o humano pede ao agente, **antes ou depois da revisao, como teste de ambiente**:
  1. Gravar `x.py` no scratchpad da propria sessao -> deve ser **permitido**.
  2. `cd` para outra pasta (ex.: `$IA_RAIZ/operacao`) e gravar `<worktree>/qualidade/verificacoes/teste-adm15.md` -> deve ser **permitido** (prova que `CLAUDE_PROJECT_DIR` chega ao hook).
  3. Apagar o arquivo do passo 2 (nao commitar).
  4. Gravar `<worktree>/app/x.py` -> deve ser **negado**.
- [ ] Registrar o resultado dos 4 passos no ADM-0015 (secao Execucao) por um ADM ou avisando o Administrador. Se o passo 2 for negado: `CLAUDE_PROJECT_DIR` nao chega ao hook; o Administrador passa para a alternativa (`IA_PASTA_SESSAO` exportada pelo lancador).

Deixar a referencia "- [ ] COORD-0020 - verificar hook do ADM-0015 na revisao" na secao "Pedidos ao Coordenador" do cartao T-0015.

## Motivo

O teste na T-0012 nao foi possivel: o cartao esta `concluida` e o lancador so abre o Revisor com `status: revisao` (protecao correta, nao contornada). O merge foi feito antes do teste por decisao do humano (2026-10-02); se a variavel nao chegar, o hook volta ao comportamento antigo (falha fechada).

---

## Atendimento
