---
tipo: experimento
status: inbox
categoria: seguranca | teste | medicao
linguagem:
origem: agente/<papel>
tarefa:
confianca: media
fontes: []
verificado_em: {{date:YYYY-MM-DD}}
valido_para:
ultimo_uso: {{date:YYYY-MM-DD}}
criado: {{date:YYYY-MM-DD}}
decisao:
tags: [experimento]
---
# {{title}}

<!-- Titulo diz o que o experimento mede ou prova. Ex.: "Medir pico de memoria curto com ru_maxrss em container com teto rigido".
     Uma pergunta por nota. Script GENERALIZADO: sem nomes, caminhos, dados ou URLs do projeto, sem segredos.
     Do projeto de origem fica so o link para o VER/SEC no Historico de uso.
     status: inbox (proposta) -> ativo (curado) -> obsoleto (superado, com link para o substituto).
     categoria: seguranca (abuso/prova de conceito) | teste (reproduzir defeito ou comportamento) | medicao (memoria, tempo, tamanho).
     ultimo_uso: data da linha mais recente do Historico de uso.
     decisao (preenchida pelo Bibliotecario): promovido | fundido | devolvido | arquivado -->

## Objetivo

<!-- Que pergunta o experimento responde e por que ela importa. -->

## Quando usar

<!-- Situacoes em que vale rodar de novo: sintoma, tipo de tarefa, criterio de aceite. E quando NAO usar. -->

## Por que este metodo e nao outro

<!-- Alternativas consideradas e por que foram descartadas (ex.: "docker stats amostra a cada ~1 s e perde o pico"). -->

## Ambiente

<!-- Versoes e condicoes em que foi validado: linguagem, bibliotecas, sistema, imagem, limites do container. -->

## Como rodar

<!-- Comando exato. Seguranca: SEMPRE contra alvo isolado (localhost, container proprio, `--network none`), nunca contra sistema de terceiros. -->

```bash

```

## Script

<!-- Minimo e comentado. Parametros no topo, sem valores do projeto. -->

```python

```

## Como interpretar

<!-- Saida esperada, o que confirma e o que refuta. Exemplo de saida real, se ajudar. -->

## Limites e cuidados

<!-- O que o experimento nao mede, falsos positivos ou negativos, risco ao rodar (memoria, disco, rede). -->

## Historico de uso

<!-- Uma linha por uso, a mais nova embaixo. Quem reutiliza registra no VER/SEC ("Experimentos reutilizados");
     o Bibliotecario copia para ca na curadoria. Script alterado: a versao anterior vai para "Versoes anteriores" (nada e apagado). -->

| Data | Tarefa e registro | Contexto e motivo do uso | Resultado | Script mudou? |
|---|---|---|---|---|
|  |  |  |  | nao |

## Versoes anteriores

<!-- Script substituido, com a data e o motivo da mudanca (versao de biblioteca, defeito no script). -->

## Relacionadas no Brain

<!-- Nota de conhecimento que este experimento sustenta (ex.: CWE ou problema-solucao) e o motivo da ligacao. -->

- [[ ]]

## Decisao do Bibliotecario

<!-- Preenchido na curadoria: decisao, motivo e link para a nota final. -->
