# Piloto 1 — T-0001 (2026-09-28)

Primeira execução da T-0001, preservada como referência. **Não foi mergeada.**

- Código: tag `piloto-1/T-0001` no repositório `projetos/lab` (commit `bcd65e8`).
- Todas as sessões rodaram **sem papel** (o Claude padrão do Orca foi usado no lugar do comando do papel): sem perfil de permissões, modelo Opus, trailers definidos à mão.
- A verificação independente achou um defeito real (A1: `/health` 500 → 503), corrigido em `bcd65e8`.
- Lições que viraram mudanças: lançador `papel` com validações, recusa de commit de agente sem papel, papel Revisor, repasse por arquivos. Ver ADR-0013.

Arquivos: cartão como ficou, rascunho do VER-0001 e registros das duas conversas.
