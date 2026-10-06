---
tipo: referencia
status: ativo
origem: SEARCH-0010 (Pesquisador, item 7), curado pelo Bibliotecario
pesquisa: SEARCH-0010
tarefa: T-0023
autor: OpenAI (documentacao oficial do Codex)
url: https://learn.chatgpt.com/docs/codex/cli
acessado_em: 2026-10-05
confianca: media
fontes: ["https://learn.chatgpt.com/docs/codex/cli", "https://learn.chatgpt.com/docs/agent-approvals-security"]
verificado_em: 2026-10-05
valido_para: "documentacao do Codex em 2026-10-05"
revisar_em: 2027-01-05
criado: 2026-10-05
decisao: promovido
tags: [codex, openai, container, sandbox, credencial]
---
# Codex CLI instala por script, guarda credencial em CODEX_HOME/auth.json e limita comandos com sandbox bwrap e seccomp

## Resumo

- **Instalar (Linux):** `curl -fsSL https://chatgpt.com/codex/install.sh | sh`; tambem npm, Homebrew ou binario. **Atualizar:** rodar o mesmo instalador de novo.
- **Credencial:** o login padrao e "Sign in with ChatGPT"; fica em `auth.json` na pasta de config do Codex, cujo local muda com a variavel `CODEX_HOME` (padrao `~/.codex`, a confirmar). Sem navegador (container): login por **device auth**.
- **Limites:** modos de sandbox `read-only`, `workspace-write` (padrao) e `danger-full-access`; politicas de aprovacao `on-request`, `never` e `granular`. **Rede desligada por padrao**; quando ligada, regras de dominio allowlist-first.
- **Linux:** o sandbox usa `bwrap` e `seccomp`. A doc avisa que em Docker ele pode precisar de reconfiguracao porque operacoes de namespace podem ser restritas (o mesmo problema de [[Bubblewrap do Claude Code em container sem privilegio falha no proc e enableWeakerNestedSandbox resolve ao custo de isolamento]]). A doc consultada nao detalha a configuracao. Sem sandbox funcional, o isolamento fica com o container.

## O que aproveitar

Para rodar o Codex no container do ambiente (T-0023): credencial em volume apontado por `CODEX_HOME`, device auth para o login, rede desligada por padrao e `workspace-write` como modo.

## Ressalvas

- Pendente: chaves exatas do `config.toml` e comportamento em container sem privilegio (testar).
- Duas paginas oficiais lidas; a pagina de sandboxing dedicada devolveu 404 nas URLs tentadas.
- O instalador e `curl | sh` sem conferencia de assinatura documentada: ver [[CWE-494 curl pipe bash e atualizacao automatica se mitigam conferindo o manifesto assinado com gpg]] para o risco, que aqui vale igual.
- Links confiaveis: [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) (instalacao, atualizacao, login, `CODEX_HOME`) e [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security) (sandbox, aprovacoes, rede, implementacao Linux).

## Notas derivadas

- [[Bubblewrap do Claude Code em container sem privilegio falha no proc e enableWeakerNestedSandbox resolve ao custo de isolamento]]
- [[CWE-522 token de ferramenta legivel pelo mesmo usuario se trata com permissao 0600 e escopo minimo]]: `auth.json` e uma credencial legivel pelo mesmo usuario.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `30_Referencias`. Sem duplicata (nenhuma nota sobre Codex). Confianca media: fonte oficial, nada testado. O dominio `learn.chatgpt.com` ainda depende de decisao do humano sobre fontes confiaveis.
