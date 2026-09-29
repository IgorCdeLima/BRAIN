---
tipo: workflow
status: ativo
versao: 1
criado: 2026-09-28
tags: [qualidade, verificacao]
---
# Matriz de verificação

Verificações obrigatórias por tipo de mudança. Uma tarefa só é concluída quando **cada verificação obrigatória tem um registro `VER-####`** — com resultado, ou justificativa explícita de por que não se aplica.

| Verificação | Código | Documentação de projeto | Conhecimento (Brain) | Regras / config de agentes |
|---|---|---|---|---|
| Testes automáticos passam | ✅ | — | — | — |
| Lint / formatação | ✅ | ✅ (Markdown) | — | ✅ (JSON válido) |
| Revisão de código (outro agente) | ✅ | — | — | — |
| Revisão de segurança | se tocar auth, dados, segredos, rede ou dependências | — | — | ✅ |
| Critérios de aceite atendidos | ✅ | ✅ | — | — |
| Diagramas coerentes com o código | se mudou modelo | ✅ | — | — |
| Duplicata no Brain verificada | — | — | ✅ | — |
| Fontes e `verificado_em` preenchidos | — | — | ✅ | — |
| Aprovação humana | merge na `main` | se mudar requisitos | — | ✅ **sempre** |

## Tamanho da tarefa

- **Trivial** (texto, ajuste pequeno sem lógica): lint + revisão rápida.
- **Normal**: matriz completa.
- **Grande**: matriz completa + spec aprovada + ADR se houver decisão de arquitetura.

## Regras

- Verificação **não feita** é registrada como lacuna no `VER-####`, com o motivo. Omitir é falha.
- Quem executou a tarefa não registra a própria revisão de código.
- **Um VER vale para um commit.** Se o branch receber um novo commit depois da verificação, é preciso um novo VER sobre o novo commit. O VER anterior permanece como histórico.
- O Revisor confere a matriz antes de aprovar; o humano confere de novo antes do merge (e, na fase 3, o Coordenador).
