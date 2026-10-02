---
tipo: problema-solucao
status: ativo
origem: T-0014 (Revisor; Dev), curado pelo Bibliotecario
tarefa: T-0014
confianca: media
fontes: ["experimento do Revisor na T-0014 (lab, 2026-10-02)", "experimento do Dev na T-0014 (lab)"]
verificado_em: 2026-10-02
valido_para: "pip-tools 7.6.1, pip 26.2.1"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [pip-tools, dependencias, docker, armadilha]
---
# pip-compile so preserva as versoes travadas se o arquivo de saida existir ao lado do in

## Sintoma

Num servico de lock isolado, o `pip-compile` sobe **todas** as dependencias indiretas para a ultima versao do indice, sem nenhuma mudanca nos `.in`. Exemplo na T-0014: filelock 4.0.8 -> 4.0.9. A diferenca costuma ser atribuida por engano a "deriva do PyPI".

## Ambiente

pip-tools 7.6.1, pip 26.2.1; servico Docker Compose que copia os `.in` para uma pasta temporaria (`/tmp`).

## Causa raiz

O `pip-compile` reaproveita as versoes ja fixadas no arquivo de saida (`requirements.txt` gerado de `requirements.in`) e so muda o que a alteracao dos `.in` exige. Se o `.txt` existente nao estiver no caminho de saida (servico que copia **so** os `.in`), a resolucao comeca do zero. Isolar o servico de lock e boa pratica de seguranca, mas quebra a reprodutibilidade se os `.txt` atuais nao forem copiados junto.

## Solucao

Copiar tambem os travados atuais para a pasta de trabalho antes do `pip-compile`: `cp /in/*.in /out/*.txt /tmp/`. Com isso os 3 travados da T-0014 sairam identicos aos commitados.

Efeito colateral a conhecer: com o `.txt` ao lado, o `--reuse-hashes` tambem passa a valer ([[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]]).

## Como verificar que foi resolvido

Mesma imagem, mesmos `.in`: copiando so os `.in`, uma indireta muda de versao; copiando `.in` + `.txt`, o arquivo sai identico ao commitado (`git diff` vazio).

## O que nao funcionou

Tratar a diferenca como "deriva do PyPI" sem comparar o mecanismo (premissa errada da T-0014).

## Relacionadas

- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]
- [[Servico de lock no Compose montando o repositorio inteiro alcanca os hooks do Git e executa no host]]: o motivo de isolar o servico.
- [[pip-compile only-binary descarta hashes de sdist]]: outra armadilha do mesmo servico de lock, com o resultado de `no-new-privileges` e `cap_drop: [ALL]` (funcionam).

## Links confiaveis

- Pendente: o candidato pede ao Pesquisador a documentacao do pip-tools sobre "updating requirements" / reaproveitamento do output-file.

## Decisao do Bibliotecario

Promovido (2026-10-02). Funde o candidato do Dev "pip-compile em container com tmp precisa copiar tambem os txt existentes" (mesmo fato validado; arquivado).
