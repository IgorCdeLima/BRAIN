---
tipo: pedido-coordenador
id: COORD-0012
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0012
criado: 2026-10-01
atendido_em: 2026-10-01
adm: ADM-0015
tags: [ambiente, permissoes, revisor, scratchpad]
---
# COORD-0012 - Perfil do Revisor bloqueia escrita no scratchpad da sessao

## Pedido

- [x] -> ADM-0015. Erro inesperado (mesma causa do COORD-0010, agora no papel Revisor): avaliar se o perfil do Revisor deve liberar escrita no scratchpad da sessao do Claude Code. Tratar junto com o COORD-0010.
  - O que tentava: gravar `exp.py` e `e4.py` no scratchpad indicado pelo sistema (`/tmp/claude-1000/<sessao>/scratchpad`) para reexecutar os experimentos E1 a E11 da analise da T-0012.
  - Pasta: worktree `T-0012-ameacas-pillow` do lab.
  - Erro exato do hook PreToolUse:Write: "Este papel so pode escrever em: qualidade, .../operacao/tarefas, .../operacao/pesquisas, .../operacao/coordenador, .../BRAIN/00_Inbox. Escrita em '/tmp/claude-1000/.../scratchpad/exp.py' negada."
- [x] -> ADM-0015. Observacao para o mesmo ajuste: o item `qualidade` do hook e relativo ao diretorio atual. Depois de um `cd` para outra pasta (ex.: `operacao/coordenador`), a escrita em `<worktree>/qualidade/...` tambem foi negada; voltando ao worktree, funcionou. Avaliar usar o caminho absoluto do worktree na regra.

## Motivo

Nao contornei: os experimentos rodaram passando o codigo pela entrada padrao de `docker run ... python -`, sem gravar arquivo. O Revisor reexecuta experimentos em quase toda tarefa de seguranca; scripts gravados seriam mais claros e reaproveitaveis. Perfil e area N4: se fizer sentido, escalar como `ADM-####`.

---

## Atendimento

Coordenador, 2026-10-01 (com o "sim" do humano): causa do scratchpad igual a do COORD-0010. Causa da observacao confirmada no hook: `cwd = Path(evento.get("cwd"))` (linha 26) usa a pasta **atual** da sessao, que muda com `cd`, e o prefixo `qualidade` vira `<pasta atual>/qualidade`. Melhoria proposta: ancorar prefixos relativos em `CLAUDE_PROJECT_DIR` (pasta em que a sessao comecou), com teste de que a variavel chega ao hook. Area N4 -> escalado como **ADM-0015** (junto com o COORD-0010). Aviso aos papeis ate la: nao fazer `cd` antes de gravar em caminho relativo do worktree; usar caminho absoluto.

Administrador, 2026-10-02 (com o "sim" do humano): atendido pelo ADM-0015, commit `d1f6de2`, merge na `main`. O Revisor agora grava no scratchpad da propria sessao (`@scratchpad`), e os prefixos relativos (`qualidade`) valem a partir da pasta em que a sessao comecou (`CLAUDE_PROJECT_DIR`; sem a variavel, comportamento antigo). Verificacao em sessao real: [[COORD-0020]] (T-0015). Ate la, o aviso acima (caminho absoluto depois de `cd`) continua prudente.
