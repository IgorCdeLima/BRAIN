---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0023
pesquisa: SEARCH-0010
confianca: media
fontes: [https://learn.chatgpt.com/docs/codex/cli, https://learn.chatgpt.com/docs/agent-approvals-security]
verificado_em: 2026-10-05
valido_para: documentacao do Codex em 2026-10-05
criado: 2026-10-05
decisao:
tags: [codex, openai, container, sandbox, credencial]
---
# Codex CLI instala por script, guarda credencial em CODEX_HOME/auth.json e limita comandos com sandbox bwrap e seccomp

## Conteudo proposto

- **Instalar (Linux):** `curl -fsSL https://chatgpt.com/codex/install.sh | sh`; tambem npm, Homebrew ou binario. **Atualizar:** rodar o mesmo instalador de novo.
- **Credencial:** login padrao "Sign in with ChatGPT"; fica em `auth.json` na pasta de config do Codex, cujo local muda com a variavel `CODEX_HOME` (padrao `~/.codex`, confirmar). Sem navegador (container): login por **device auth**.
- **Limites:** modos de sandbox `read-only`, `workspace-write` (padrao) e `danger-full-access`; politicas de aprovacao `on-request`, `never`, `granular`. **Rede desligada por padrao**; quando ligada, regras de dominio allowlist-first.
- **Linux:** implementa com `bwrap` + `seccomp`; a doc avisa que em Docker o sandbox pode precisar de reconfiguracao porque operacoes de namespace podem ser restritas (mesmo problema do bubblewrap do Claude Code). A doc consultada nao detalha a configuracao. Sem sandbox funcional, o isolamento fica com o container.
- Pendente: chaves exatas do `config.toml` e o comportamento em container sem privilegio (testar).

## Evidencia

Duas paginas oficiais lidas; a pagina de sandboxing dedicada devolveu 404 nas URLs tentadas.

## Links confiaveis

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli): instalacao, atualizacao, login, `CODEX_HOME`.
- [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security): sandbox, aprovacoes, rede, implementacao Linux.

## Por que e reaproveitavel

T-0023: rodar o Codex no container do ambiente com credencial em volume e limites explicitos.

## Relacionadas no Brain

- [[Bubblewrap do Claude Code em container sem privilegio falha no proc e enableWeakerNestedSandbox resolve ao custo de isolamento]]

## Decisao do Bibliotecario
