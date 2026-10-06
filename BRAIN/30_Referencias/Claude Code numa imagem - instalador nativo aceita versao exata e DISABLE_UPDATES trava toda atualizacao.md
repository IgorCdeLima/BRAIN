---
tipo: referencia
status: ativo
origem: T-0018 (Engenheiro) e SEARCH-0010 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0010
tarefa: T-0018
autor: Anthropic (documentacao oficial do Claude Code)
url: https://code.claude.com/docs/en/setup
acessado_em: 2026-10-05
confianca: media
fontes: ["https://code.claude.com/docs/en/setup", "https://code.claude.com/docs/en/devcontainer", "https://downloads.claude.ai/claude-code/apt/stable/dists/stable/main/binary-amd64/Packages"]
verificado_em: 2026-10-05
valido_para: "Claude Code 2.1.x (docs de 2026-10); indice apt stable de 2026-10-05"
revisar_em: 2027-01-05
criado: 2026-10-05
decisao: promovido
tags: [claude-code, container, instalacao, versao, apt, adm-0009]
---
# Claude Code numa imagem - instalador nativo aceita versao exata e DISABLE_UPDATES trava toda atualizacao

## Resumo

Formas de instalar o Claude Code numa imagem com versao fixa e reproduzivel. Complementa [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]], que so cita o npm para fixar versao.

- **Instalador nativo com versao:** `curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89` (aceita versao exata ou canal `stable`/`latest`). Instala em `~/.local/bin/claude`, apontando para `~/.local/share/claude/versions/<versao>`; um lancador proprio nesse caminho e respeitado desde a 2.1.207.
- **Travar atualizacao:** `DISABLE_AUTOUPDATER=1` so desliga a verificacao em segundo plano (`claude update` ainda funciona); `DISABLE_UPDATES` bloqueia todos os caminhos. Conferir com `claude doctor`.
- **Repositorios apt/dnf/apk assinados** (`downloads.claude.ai/claude-code/...`, canais `stable` e `latest`): o gerenciador confere a assinatura, o binario fica em pasta do sistema e nao ha atualizacao automatica (so `apt upgrade`; para evitar upgrade acidental, `apt-mark hold claude-code`). Chave: `https://downloads.claude.ai/keys/claude-code.asc`, fingerprint `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE` (conferir com `gpg --show-keys`).
- **Versao exata pelo apt:** o indice `Packages` do canal `stable` (amd64) listava em 2026-10-05 **60 versoes** (de `2.1.108-1` a `2.1.285-1`, sufixo `-1`), entao `apt install claude-code=2.1.285-1` e viavel (confirme com `apt-cache madison claude-code`). Os canais sao dois repositorios: `.../apt/stable` (~1 semana de atraso) e `.../apt/latest`. A doc **nao promete retencao**: a lista e observacao do dia.
- **npm:** exige Node.js 22+; instala o mesmo binario nativo.
- **Integridade:** `manifest.json` e `manifest.json.sig` por versao (desde a 2.1.89); os binarios Linux nao tem assinatura individual. Passos de conferencia em [[CWE-494 curl pipe bash e atualizacao automatica se mitigam conferindo o manifesto assinado com gpg]].

## O que aproveitar

Para uma imagem do ambiente 01_IA ou de CI: fixar a versao exata (apt `=versao` ou `install.sh | bash -s <versao>`), conferir o manifesto no build e atualizar so reconstruindo a imagem.

## Ressalvas

- Nada foi executado numa imagem ainda (a T-0020 vai executar); so leitura das paginas oficiais e do indice apt em 2026-10-05.
- A retencao de versoes antigas no apt e observacao de um dia, nao compromisso da Anthropic.
- Links confiaveis: [Advanced setup](https://code.claude.com/docs/en/setup) (versao especifica, apt/dnf/apk, npm, `DISABLE_UPDATES`, manifesto assinado), [Development containers](https://code.claude.com/docs/en/devcontainer) (Feature, volume com `CLAUDE_CONFIG_DIR`, managed settings) e o [indice Packages do canal stable](https://downloads.claude.ai/claude-code/apt/stable/dists/stable/main/binary-amd64/Packages).

## Notas derivadas

- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]
- [[CWE-494 curl pipe bash e atualizacao automatica se mitigam conferindo o manifesto assinado com gpg]]

## Decisao do Bibliotecario

Promovido (2026-10-05) para `30_Referencias`. **Fundido** com o candidato "O repositorio apt do Claude Code mantem versoes antigas..." (SEARCH-0010, confianca alta so para a observacao do indice), cujo conteudo entrou aqui; o candidato foi para `90_Arquivo`. A frase antiga "fixar versao exata no apt nao esta documentado" foi substituida pelo achado do indice.
