---
tipo: pesquisa
id: SEARCH-0005
status: catalogada
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0014
criado: 2026-10-02
pesquisado_por: pesquisador
pesquisado_em: 2026-10-02
catalogado_em: 2026-10-02
notas: ["[[pip require-hashes nao confere pacote ja instalado na imagem base]]"]
tags: [seguranca, pip, hashes, supply-chain, cwe-829]
---
# SEARCH-0005 - pip --require-hashes confere o hash de pacote ja instalado?

## Pergunta

No modo `--require-hashes`, o pip (26.x) confere o hash de um requisito que ja esta instalado na mesma versao ("Requirement already satisfied")? A documentacao oficial ou o rastreador do pip recomenda `--force-reinstall` (ou ambiente limpo) para garantir a conferencia?

## Contexto

Revisao de seguranca da T-0014 (lab, SEC-T0014-01). Experimento: com os hashes do `pip==26.2.1` adulterados no travado, `pip install --require-hashes -r requirements-lock.txt` passa na imagem `python:3.13.15-slim` (que ja traz pip 26.2.1); com `--force-reinstall`, falha com "THESE PACKAGES DO NOT MATCH THE HASHES". Premissa usada: o pip pula a conferencia de pacote ja satisfeito. Falta fonte oficial que confirme e diga se e comportamento documentado.

## Ja buscado no Brain

- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]: nao cobre pacote ja instalado.
- pip Secure installs (https://pip.pypa.io/en/stable/topics/secure-installs/) e `pip install` (https://pip.pypa.io/en/stable/cli/pip_install/), abertas em 2026-10-02: nao mencionam o caso.

---

## Resposta

- **Resumo:** Sim, confirmado: com `--require-hashes` o pip nao confere hash de pacote ja instalado na versao pedida. No codigo do pip, `_get_installed_candidate()` (resolvelib/factory.py) aceita o instalado so pela versao; hashes so entram na busca no indice. `--force-reinstall` faz o pip ignorar o instalado, baixar e conferir. Nao e comportamento documentado nas paginas oficiais (Secure installs, pip install): a fonte e o codigo, entao pode mudar. Premissa da SEC-T0014-01 confirmada.
- **Notas geradas no Inbox:** [[pip require-hashes nao confere pacote ja instalado na imagem base]] (ja existia como pista; atualizada com a fonte)
- **Links confiaveis:** https://github.com/pypa/pip/blob/main/src/pip/_internal/resolution/resolvelib/factory.py ; https://pip.pypa.io/en/stable/topics/secure-installs/ ; https://pip.pypa.io/en/stable/cli/pip_install/
- **Sem resposta / limites:** nenhum issue/doc oficial do pip trata o caso; a issue uv #474 nao confirma o comportamento do pip (descartada como fonte). Leitura do codigo feita via resumo de pagina (WebFetch), recomendo o Revisor reconferir o trecho.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

- github.com/pypa/pip (codigo do pip, fonte primaria para comportamento nao documentado)

## Catalogacao

Decisao (Bibliotecario, 2026-10-02): promovida. Links confiaveis preservados. Ressalva: a fonte e o codigo do pip, nao a documentacao; o Revisor deve reconferir o trecho.

- [[pip require-hashes nao confere pacote ja instalado na imagem base]] (10_Conhecimento)
