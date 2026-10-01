---
tipo: pedido-coordenador
id: COORD-0010
status: escalado
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0012
criado: 2026-10-01
atendido_em: 2026-10-01
adm: ADM-0015
tags: [ambiente, permissoes, seguranca, scratchpad]
---
# COORD-0010 - Perfil da Seguranca bloqueia escrita no scratchpad da sessao

## Pedido

- [x] -> ADM-0015. Erro inesperado: avaliar se o perfil do papel Seguranca deve liberar escrita no scratchpad da sessao do Claude Code.
  - O que tentava: gravar um script de experimento (`exp.py`) no scratchpad indicado pelo sistema (`/tmp/claude-1000/<sessao>/scratchpad`), para medir o comportamento do Pillow em container antes de escrever a analise de ameacas.
  - Pasta: worktree `T-0012-ameacas-pillow` do lab.
  - Erro exato do hook PreToolUse:Write: "Este papel so pode escrever em: docs/seguranca, qualidade/seguranca, .../operacao/tarefas, .../operacao/pesquisas, .../operacao/coordenador, .../BRAIN/00_Inbox. Escrita em '/tmp/claude-1000/.../scratchpad/exp.py' negada."

## Motivo

As instrucoes de sistema da sessao mandam usar o scratchpad para arquivos temporarios, mas o hook do papel nega. Nao contornei: rodei os experimentos passando o codigo pela entrada padrao de `docker run ... python -`, sem gravar arquivo. Funciona, mas scripts de prova de conceito (SEC com reproducao) ficariam mais claros se pudessem ser gravados e reaproveitados. Decisao de ambiente (perfil em `agentes/`, area N4): se fizer sentido, escalar como `ADM-####`.

---

## Atendimento

Coordenador, 2026-10-01 (com o "sim" do humano): causa encontrada em `ferramentas/hooks/restringir_escrita.py`. O hook e lista de permissoes e o scratchpad da sessao nao esta em nenhuma lista, embora as instrucoes de sistema do Claude Code mandem usa-lo. Melhoria proposta: token `@scratchpad` no hook, que libera so o scratchpad da sessao atual (pelo `session_id` do evento), ativado para Seguranca e Revisor. Tratado junto com o COORD-0012 (mesma causa, mais o prefixo relativo resolvido pela pasta atual). Area N4 -> escalado como **ADM-0015**. Contorno sem gravar arquivo (`docker run ... python -`) foi correto; continua valendo ate o ADM-0015 ser atendido.
