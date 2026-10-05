---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: ambiente
pesquisa: SEARCH-0009
confianca: media
fontes: [https://code.claude.com/docs/en/devcontainer]
verificado_em: 2026-10-05
valido_para: Claude Code docs de 2026-10 (CLI 2.1.x)
criado: 2026-10-05
decisao:
tags: [ambiente, container, claude-code, devcontainer, adm-0009]
---
# Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root

## Conteudo proposto

- **Instalacao:** a Anthropic publica a Dev Container Feature `ghcr.io/anthropics/devcontainer-features/claude-code:1.0` (instala o CLI; instala Node se a imagem nao tiver). O tag `:1.0` fixa o script da feature, nao a versao do CLI. Para fixar o CLI: `npm install -g @anthropic-ai/claude-code@X.Y.Z` no Dockerfile e `DISABLE_AUTOUPDATER=1` no ambiente. Nao ha imagem base mantida: o repositorio `anthropics/claude-code` (`.devcontainer/`) e so um **exemplo** (Dockerfile + `init-firewall.sh` + volumes).
- **Login sem segredo na imagem:** rodar `claude` dentro do container e seguir o login (conta claude.ai ou Console). Se o callback do navegador nao chegar, colar o codigo no prompt `Paste code here if prompted`. Para execucao sem navegador: `CLAUDE_CODE_OAUTH_TOKEN` (gerado por `claude setup-token`) ou `ANTHROPIC_API_KEY`, passados como variavel de ambiente em runtime, nunca no Dockerfile nem no repositorio.
- **Onde ficam config e transcricoes:** em `~/.claude` (token, settings, historico de sessoes). A conta OAuth fica em `~/.claude.json`, **fora** da pasta; por isso, para persistir o login, montar um volume nomeado em `~/.claude` **e** definir `CLAUDE_CONFIG_DIR` com o mesmo caminho (assim o `.claude.json` vai para dentro do volume). Retencao das transcricoes: `cleanupPeriodDays`.
- **Politica fixa na imagem:** `/etc/claude-code/managed-settings.json` (Linux) tem a maior precedencia; quem edita o Dockerfile pode removê-lo, entao nao e barreira contra quem escreve no repositorio.
- **`--dangerously-skip-permissions`:** a documentacao so o recomenda com usuario **nao root** (o CLI recusa como root) e avisa que o container **nao impede** exfiltrar tudo que esta dentro dele, inclusive as credenciais em `~/.claude`, se o projeto for malicioso. Nao montar `~/.ssh` nem credenciais de nuvem; preferir tokens curtos ou restritos ao repositorio. Opcao menos drastica: modo `auto`; para proibir o flag: `permissions.disableBypassPermissionsMode: "disable"` nas managed settings.
- **Firewall:** o exemplo usa `init-firewall.sh` com as capabilities `NET_ADMIN` e `NET_RAW` para limitar a saida de rede aos dominios necessarios. Nao e requisito do Claude Code; e opcional.

## Evidencia

Pagina oficial "Development containers" da documentacao do Claude Code, lida em 2026-10-05.

## Links confiaveis

- [Claude Code: Development containers](https://code.claude.com/docs/en/devcontainer): instalacao, volume + `CLAUDE_CONFIG_DIR`, managed settings, firewall e avisos sobre `--dangerously-skip-permissions`.
- [Exemplo .devcontainer do repositorio claude-code](https://github.com/anthropics/claude-code/tree/main/.devcontainer): Dockerfile, `devcontainer.json` e `init-firewall.sh` de referencia.
- [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory): o que o volume guarda (credenciais, settings, sessoes).

## Por que e reaproveitavel

Qualquer papel ou projeto que rode agentes em container precisa destas tres decisoes: onde fica o login, o que montar como volume e quando o bypass de permissoes e aceitavel.

## Relacionadas no Brain

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]

## Decisao do Bibliotecario
