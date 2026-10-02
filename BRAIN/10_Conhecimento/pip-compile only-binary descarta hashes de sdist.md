---
tipo: problema-solucao
status: ativo
origem: T-0014 (Dev), curado pelo Bibliotecario
tarefa: T-0014
confianca: media
fontes: ["experimento do Dev na T-0014 (lab)"]
verificado_em: 2026-10-02
valido_para: "pip-tools 7.6.1"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [pip-tools, supply-chain, docker, resultado-negativo]
---
# pip-compile com only-binary descarta hashes de sdist

## Sintoma

Resultado negativo. Ao endurecer o servico de lock com `--pip-args "--only-binary=:all:"` ou com `PIP_ONLY_BINARY=:all:`, o `pip-compile` (1) grava a linha `--only-binary :all:` no topo do travado e (2) remove os hashes dos sdist, deixando so os das wheels. O travado deixa de ser identico ao anterior.

## Ambiente

pip-tools 7.6.1 (T-0014, lab).

## Causa raiz

A opcao nao afeta so a resolucao: muda a saida, porque o pip-compile so lista hashes de artefatos que a politica permite. A premissa errada do Dev foi supor o contrario. Atencao: se o `.txt` antigo estiver ao lado do `.in`, o `--reuse-hashes` (padrao) pode **mascarar** esse efeito, mantendo os hashes antigos: [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]].

## Solucao

Nao usar `--only-binary` para endurecer o lock. Alternativa adotada: container sem root, com so os `.in` (somente leitura) e os `.txt` montados, e sistema de arquivos read-only.

Cuidados do mesmo servico:

- Montar a raiz do projeto no servico de lock expoe `.githooks/` (execucao no host); monte so os arquivos de dependencia ([[Servico de lock no Compose montando o repositorio inteiro alcanca os hooks do Git e executa no host]]).
- Arquivo montado individualmente deve ser regravado no lugar (`cat > arq`), nao trocado por `mv`.

## Como verificar que foi resolvido

Rodar o servico de lock duas vezes sobre os mesmos `.in` e `.txt` e conferir que o travado sai identico (`git diff` vazio).

## O que nao funcionou

`--pip-args "--only-binary=:all:"` e `PIP_ONLY_BINARY=:all:`: ambos geram o mesmo efeito (linha extra no topo e hashes de sdist removidos).

## Relacionadas

- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]
- [[pip-compile so preserva as versoes travadas se o arquivo de saida existir ao lado do in]]
- [[USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid]]: `no-new-privileges` e `cap_drop: [ALL]` no servico de lock funcionam sem quebrar o pip-compile (medido na T-0014).

## Decisao do Bibliotecario

Promovido (2026-10-02) como resultado negativo validado. O candidato original estava como `status: candidato` fora do formato do Inbox; reescrito no template.
