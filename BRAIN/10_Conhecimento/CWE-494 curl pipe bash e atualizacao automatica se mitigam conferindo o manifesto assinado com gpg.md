---
tipo: padrao
status: ativo
origem: SEARCH-0011 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0018
pesquisa: SEARCH-0011
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/494.html", "https://code.claude.com/docs/en/setup"]
verificado_em: 2026-10-05
valido_para: "Claude Code 2.1.89 em diante (manifesto assinado); CWE 4.20"
criado: 2026-10-05
decisao: promovido
revisar_em: 2027-01-05
tags: [seguranca, cwe, cwe-494, cadeia-de-suprimento, claude-code]
---
# CWE-494 curl pipe bash e atualizacao automatica se mitigam conferindo o manifesto assinado com gpg

## Contexto

**O que e (MITRE):** CWE-494 e baixar e executar codigo remoto sem verificar origem e integridade; a consequencia e execucao de codigo nao autorizado com os privilegios da aplicacao. Mitigacao: assinatura criptografica validada antes de executar, privilegio minimo e sandbox.

**Como aparece:** `curl -fsSL https://claude.ai/install.sh | bash` executa o que vier, sem conferencia; e a atualizacao automatica em segundo plano baixa binarios novos sem passo humano.

## Problema

Uma imagem ou maquina que instala o Claude Code por script remoto, ou o deixa se atualizar sozinho, passa a executar binarios que ninguem conferiu.

## Solucao

**Verificacao oficial do Claude Code (manifesto assinado, versoes 2.1.89+):**

1. Importar a chave: `curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import` e conferir o fingerprint `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`.
2. Baixar `manifest.json` e `manifest.json.sig` de `https://downloads.claude.ai/claude-code-releases/<VERSAO>/`.
3. `gpg --verify manifest.json.sig manifest.json` deve dar `Good signature` (o aviso de chave nao certificada e esperado).
4. Comparar o `sha256sum` do binario com `platforms.<plataforma>.checksum` do manifesto (o binario instalado fica em `~/.local/share/claude/versions/<VERSAO>`).

No Linux o binario nao tem assinatura propria; a garantia vem do manifesto. Alternativa: repositorio apt/dnf/apk assinado, em que o gerenciador verifica sozinho (fingerprint do apt: `31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`).

**Controle para imagem de container:** instalar versao exata (`install.sh | bash -s <versao>`) ou por pacote assinado, verificar o manifesto no build e travar a atualizacao com `DISABLE_UPDATES=1` (bloqueia tambem `claude update`; `DISABLE_AUTOUPDATER` so para o segundo plano). Atualizar so reconstruindo a imagem.

## Trade-offs

- **Ganha:** instalacao reproduzivel e conferida; nenhuma atualizacao sem decisao humana.
- **Perde:** correcoes de seguranca do Claude Code so entram quando alguem reconstroi a imagem.

## Quando NAO usar

Maquina descartavel sem credencial e sem acesso a nada sensivel, onde o custo da conferencia supera o risco.

## Evidencia

Pagina oficial "Advanced setup" do Claude Code (lida em 2026-10-05, exemplos com 2.1.89 e 2.1.211) e pagina oficial da CWE-494 (4.20). Nada executado.

## Links confiaveis

- [CWE-494](https://cwe.mitre.org/data/definitions/494.html): definicao e mitigacoes.
- [Claude Code - Advanced setup, Binary integrity](https://code.claude.com/docs/en/setup): passos de verificacao do manifesto, pacotes assinados, versao fixa e DISABLE_UPDATES.

## Relacionadas

- [[Claude Code numa imagem - instalador nativo aceita versao exata e DISABLE_UPDATES trava toda atualizacao]]: como fixar a versao na imagem.
- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]: mesma ideia (origem conferida) para dependencias Python.
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento` como padrao, no formato das demais notas CWE; incluido no Mapa das CWE. Sem duplicata. Base para SEC-T0018-04.
