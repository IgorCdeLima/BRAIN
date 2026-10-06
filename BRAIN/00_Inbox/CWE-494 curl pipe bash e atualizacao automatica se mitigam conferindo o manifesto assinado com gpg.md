---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0011
confianca: media
fontes: [https://cwe.mitre.org/data/definitions/494.html, https://code.claude.com/docs/en/setup]
verificado_em: 2026-10-05
valido_para: Claude Code 2.1.89 em diante (manifesto assinado); CWE 4.20
criado: 2026-10-05
decisao:
tags: [seguranca, cwe, cadeia-de-suprimento, claude-code]
---
# CWE-494 curl pipe bash e atualizacao automatica se mitigam conferindo o manifesto assinado com gpg

## Conteudo proposto

**O que e (MITRE):** baixar e executar codigo remoto sem verificar origem e integridade. Consequencia: execucao de codigo nao autorizado com os privilegios da aplicacao. Mitigacao: assinatura criptografica validada antes de executar; privilegio minimo; sandbox.

**Como aparece:** `curl -fsSL https://claude.ai/install.sh | bash` executa o que vier, sem conferencia; e a atualizacao automatica em segundo plano baixa binarios novos sem passo humano.

**Verificacao oficial do Claude Code (manifesto assinado, versoes 2.1.89+):**
1. Importar a chave: `curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import` e conferir o fingerprint `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`.
2. Baixar `manifest.json` e `manifest.json.sig` de `https://downloads.claude.ai/claude-code-releases/<VERSAO>/`.
3. `gpg --verify manifest.json.sig manifest.json` deve dar `Good signature` (o aviso de chave nao certificada e esperado).
4. Comparar `sha256sum` do binario com `platforms.<plataforma>.checksum` do manifesto (binario instalado fica em `~/.local/share/claude/versions/<VERSAO>`).
Linux: o binario nao tem assinatura propria; a garantia vem do manifesto. Alternativa: repositorio apt/dnf/apk assinado, em que o gerenciador de pacotes verifica sozinho (fingerprint do apt: `31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`).

**Controle para imagem de container:** instalar versao exata (`install.sh | bash -s <versao>`) ou via pacote assinado, verificar o manifesto no build, e travar atualizacao com `DISABLE_UPDATES=1` (bloqueia tambem `claude update`; `DISABLE_AUTOUPDATER` so para o segundo plano). Atualizar so reconstruindo a imagem.

## Evidencia

Pagina oficial "Advanced setup" do Claude Code (lida em 2026-10-05, exemplos com 2.1.89 e 2.1.211) e pagina oficial da CWE-494 (4.20).

## Links confiaveis

- [CWE-494](https://cwe.mitre.org/data/definitions/494.html): definicao e mitigacoes.
- [Claude Code - Advanced setup, Binary integrity](https://code.claude.com/docs/en/setup): passos de verificacao do manifesto, pacotes assinados, versao fixa e DISABLE_UPDATES.

## Por que e reaproveitavel

Qualquer imagem que instale ferramenta por script remoto; base para SEC-T0018-04.

## Relacionadas no Brain

- [[Claude Code numa imagem - instalador nativo aceita versao exata e DISABLE_UPDATES trava toda atualizacao]]
- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]
