---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, qualidade]
---
# ADR-0009 Catálogo de qualidade

> **Atualização 2026-09-28:** a parte de logs (formato e local) foi substituída por [[ADR-0012 Logs em Markdown fora do Git]].

## Contexto

Com vários agentes, cada um verifica coisas diferentes e lacunas passam despercebidas. Bugs, erros e verificações precisam ser catalogados e consultáveis por todos.

## Decisão

- Registros: `VER-####` (verificação), `BUG-####` (defeito), `SEC-####` (segurança) em Markdown; logs de eventos e erros em JSONL, somente acréscimo.
- **Matriz de verificação**: cada tipo de tarefa tem verificações obrigatórias; tarefa só conclui quando todas têm registro. Verificação não feita é registrada como lacuna.
- **Escrevem**: Revisor, Segurança e Coordenador (QA no futuro). **Demais agentes: somente leitura.**
- Nada é apagado; quem corrige não verifica; segredos nunca são registrados.
- Local: `projetos/<nome>/qualidade` para projetos; `operacao/qualidade` para o ambiente.
- Todo agente consulta os bugs abertos dos arquivos que vai alterar antes de começar.

## Consequências

- **Positivas:** lacunas de verificação ficam visíveis; histórico de defeitos alimenta o Brain e o painel futuro.
- **Negativas / riscos:** a restrição de escrita depende dos perfis por papel e de hooks do Git (fases 0.12 e 1).
