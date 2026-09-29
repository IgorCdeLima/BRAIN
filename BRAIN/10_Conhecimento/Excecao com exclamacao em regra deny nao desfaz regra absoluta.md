---
tipo: problema-solucao
status: ativo
origem: agente/claude-desktop (candidato da tarefa F2-2.1, curado pelo Bibliotecário)
confianca: alta
fontes: ["https://code.claude.com/docs/en/permissions", "teste no ambiente 01_IA em 2026-09-28"]
verificado_em: 2026-09-28
valido_para: Claude Code 2.1.28x
revisar_em: 2026-12-28
criado: 2026-09-28
tags: [claude-code, permissoes]
decisao: promovido
---
# Exceção com ! em regra deny não desfaz regra absoluta

## Sintoma

Uma regra `deny` de exceção com `!` (negação estilo gitignore) não libera o arquivo esperado. Exemplo: com `Read(//**/.env.*)` e `Read(!**/.env.example)`, o `.env.example` continua bloqueado. Do mesmo modo, "negar tudo exceto X" para escrita (`Edit(**)` + `Edit(!X/**)`) não abre a pasta X.

## Ambiente

Claude Code 2.1.28x, perfis de papel passados por `--settings` (ver [[ADR-0011 Perfis por papel via settings]]).

## Causa raiz

A regra `!` só abre exceção em regras **relativas** à pasta da sessão (`path` ou `./path`) listadas antes dela no mesmo arquivo. Ela não desfaz regras ancoradas com `//` (absoluta), `~/` ou `/`. Para o caso de `Edit(**)` + `Edit(!X/**)`, a documentação não garante o efeito e o teste também falhou.

## Solução

- Leitura: usar a regra relativa. `Read(**/.env.*)` + `Read(!**/.env.example)` libera `.env.example` e mantém `.env.local` bloqueado.
- "Bloquear tudo exceto X" em escrita: usar um hook `PreToolUse` com lista de permissões (foi a solução adotada no perfil do Revisor, que escreve só em `qualidade/`).

## Como verificar que foi resolvido

Rodar `claude -p` com o perfil em `--settings`, em worktree temporário, e tentar ler `.env.example` e `.env.local` (só o primeiro deve ser liberado) e escrever dentro e fora da pasta permitida.

## O que não funcionou

- `Read(//**/.env.*)` + `Read(!**/.env.example)`: exceção ignorada por causa da âncora `//`.
- `Edit(**)` + `Edit(!qualidade/**)`: escrita em `qualidade/` continuou negada.

## Origem

Tarefa F2-2.1 (perfil do Revisor). Relacionadas: [[ADR-0006 Modelo de permissoes]] (modelo de permissões que este perfil implementa) e [[ADR-0013 Lancador de papeis e identidade dos agentes]] (lançador que aplica os perfis por papel).

## Decisão do Bibliotecário

**Promovido** em 2026-09-28. Sem duplicata no Brain (busca por deny, `.env.example` e permissões só achou ADRs). Reescrito no template `Problema-Solucao`; confiança alta mantida (teste reproduzido + documentação oficial); `revisar_em` em 3 meses por depender da versão do Claude Code.
