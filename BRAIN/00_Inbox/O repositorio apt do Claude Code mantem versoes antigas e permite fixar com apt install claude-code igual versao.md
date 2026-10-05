---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0010
confianca: alta
fontes: [https://code.claude.com/docs/en/setup, https://downloads.claude.ai/claude-code/apt/stable/dists/stable/main/binary-amd64/Packages]
verificado_em: 2026-10-05
valido_para: repositorio apt stable em 2026-10-05 (60 versoes, 2.1.108-1 a 2.1.285-1)
criado: 2026-10-05
decisao:
tags: [claude-code, apt, versao, container, instalacao]
---
# O repositorio apt do Claude Code mantem versoes antigas e permite fixar com apt install claude-code=versao

## Conteudo proposto

- O indice `Packages` do canal `stable` (amd64) listava em 2026-10-05 **60 versoes** (de `2.1.108-1` a `2.1.285-1`), com sufixo `-1`. Logo `apt install claude-code=2.1.285-1` e viavel (confirme com `apt-cache madison claude-code`). Os canais sao dois repositorios: `.../apt/stable` (suite `stable`, ~1 semana de atraso) e `.../apt/latest` (suite `latest`).
- Instalacao por apt nao se atualiza sozinha (so por `apt upgrade`), entao nao precisa de `DISABLE_UPDATES` para congelar; para evitar upgrade acidental use `apt-mark hold claude-code`.
- Chave de assinatura: `https://downloads.claude.ai/keys/claude-code.asc`, fingerprint `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`; conferir com `gpg --show-keys`.
- Limite: a doc nao promete retencao; a lista e observacao do dia. Alternativa documentada para versao exata: `curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89`.

## Evidencia

Indice `Packages` lido em 2026-10-05; pagina `setup` descreve canais e comandos.

## Links confiaveis

- [Advanced setup - Linux package managers](https://code.claude.com/docs/en/setup#install-with-linux-package-managers): repositorios, chave, canais.
- [Indice Packages do canal stable](https://downloads.claude.ai/claude-code/apt/stable/dists/stable/main/binary-amd64/Packages): versoes disponiveis.

## Por que e reaproveitavel

Imagens reprodutiveis (Dockerfile) com versao fixa e atualizacao deliberada.

## Relacionadas no Brain

- [[Claude Code numa imagem - instalador nativo aceita versao exata e DISABLE_UPDATES trava toda atualizacao]]

## Decisao do Bibliotecario
