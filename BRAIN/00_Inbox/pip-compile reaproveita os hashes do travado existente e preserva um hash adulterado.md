---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/seguranca
tarefa: T-0014
pesquisa: SEARCH-0006
confianca: media
fontes: []
verificado_em: 2026-10-02
valido_para: pip-tools 7.6.1, pip 26.2.1
criado: 2026-10-02
decisao:
tags: [seguranca, pip-tools, hashes, supply-chain, armadilha]
---
# pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado

## Conteudo proposto

Com o arquivo de saida (`requirements.txt`) presente, o `pip-compile --generate-hashes` reaproveita nao so os pinos, mas tambem os **hashes**: `--reuse-hashes` e o padrao. Para pacote cujo pino nao muda, o hash vem do arquivo antigo, nao do indice.

Consequencias:

- um hash trocado ou acrescentado no travado sobrevive a toda regeneracao; "regenerar e comparar" nao confere nada;
- adotar uma opcao que mudaria os hashes (ex.: `--only-binary=:all:`, que deixa so os hashes de wheel) parece nao ter efeito, porque os hashes antigos (de sdist) continuam.

Solucao: `--no-reuse-hashes` no servico/CI de lock. Os pinos continuam preservados (vem do `.txt`); os hashes passam a ser recalculados. Custo: mais lento.

## Evidencia

Experimento da Seguranca (T-0014, lab, SEC-T0014-05), copia descartavel: hash de um pacote trocado por zeros -> `pip-compile` com reaproveitamento manteve o hash falso; com `--no-reuse-hashes` voltou o verdadeiro, versoes iguais, e 24 hashes de sdist sairam (arquivo com `--only-binary :all:`). `pip-compile --help` (7.6.1) lista `--reuse-hashes / --no-reuse-hashes`.

## Links confiaveis

- [pip-tools, options.py (codigo-fonte)](https://github.com/jazzband/pip-tools/blob/main/piptools/scripts/options.py): `--reuse-hashes/--no-reuse-hashes`, padrao `True`; ajuda oficial: "Improve the speed of --generate-hashes by reusing the hashes from an existing output file." (a pagina de docs do pip-tools nao descreve o flag nem recomenda `--no-reuse-hashes`; a recomendacao para CI/auditoria e deducao nossa, verificada no experimento).
- [CWE-345](https://cwe.mitre.org/data/definitions/345.html): classe da falha (verificacao insuficiente da autenticidade dos dados); ver [[CWE-345 e a classe de hash copiado sem reconferir no indice - filha mais proxima e CWE-354]].

## Por que e reaproveitavel

Qualquer projeto que gere travados com `pip-compile --generate-hashes` reaproveitando o `.txt` anterior (o que e preciso para nao subir as indiretas).

## Relacionadas no Brain

- [[pip-compile so preserva as versoes travadas se o arquivo de saida existir ao lado do in]]
- [[pip-compile only-binary descarta hashes de sdist]]
- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]

## Decisao do Bibliotecario
