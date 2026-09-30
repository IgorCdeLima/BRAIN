---
tipo: problema-solucao
status: ativo
origem: agente/claude-desktop (candidato da tarefa T-0002, curado pelo Bibliotecario)
confianca: alta
fontes: ["operacao/tarefas/T-0002.md (sessao dev 958f8d5b, 2026-09-29 23:09)", "commit f1d481a", "teste de leitura no PowerShell 5.1.19041 em 2026-09-29"]
verificado_em: 2026-09-29
valido_para: "Windows PowerShell 5.1 (powershell.exe); nao vale para PowerShell 7+"
revisar_em: 2027-03-29
criado: 2026-09-29
tags: [powershell, windows, codificacao, armadilha]
decisao: promovido
---
# PowerShell 5.1 corrompe arquivos UTF-8 ao reescrever com Get-Content e Set-Content

## Sintoma

Depois de um agente mudar uma linha de um arquivo .md pelo terminal, os acentos viram lixo: "e" com acento vira "Ã©", cedilha vira "Ã§", travessao vira "â€”".

## Ambiente

Windows PowerShell 5.1 (`powershell.exe`), arquivos Markdown em UTF-8 sem BOM (o padrao deste ambiente).

## Causa raiz

`Get-Content` sem `-Encoding` le arquivo UTF-8 sem BOM como Windows-1252. O texto ja chega corrompido na memoria; gravar depois so grava a corrupcao. Medido em 2026-09-29: um arquivo com "é ç" lido por `Get-Content` no 5.1.19041 devolveu os bytes 195,169 como dois caracteres ("Ã©"), em vez de um.

Nao medido aqui: o destino padrao de `Out-File` e `>` (a documentacao do 5.1 diz UTF-16; o ambiente pode diferir). Em todo caso nenhum deles preserva UTF-8 sem BOM.

## Solucao

- Agentes editam arquivos so com as ferramentas de edicao (Edit/Write), nunca reescrevendo pelo terminal. `Set-Content`, `Out-File`, `Add-Content` e `WriteAll*` ficaram bloqueados por permissao (ver CLAUDE.md, regras 7 e 8).
- Texto novo em Markdown sem acentos nem cedilha, o que torna os arquivos imunes a qualquer ferramenta.
- Para consertar arquivo ja corrompido: em cada linha, `linha.encode("cp1252").decode("utf-8")`; se der erro, a linha estava correta e fica como esta.

## Como verificar que foi resolvido

Buscar por `Ã` e `â€` no arquivo: nenhuma ocorrencia. No cartao T-0002, 35 linhas foram restauradas assim (commit f1d481a).

## O que nao funcionou

Passar `-Encoding utf8` so no `Set-Content`: a leitura ja estava errada, entao a gravacao so fixou o erro.

## Origem

Cartao T-0002 com 107 ocorrencias corrompidas apos `(Get-Content ...) -replace ... | Set-Content ... -Encoding utf8` executado pelo Dev. Relacionada: [[Primeira tarefa com papeis mostrou que o repasse por arquivos funciona]] (mesmo piloto de papeis).

## Decisao do Bibliotecario

**Promovido** em 2026-09-29. Sem duplicata no Brain (a busca por PowerShell/UTF-8 so achou o proprio candidato). Evidencia: commit f1d481a e leitura reproduzida por mim no 5.1.19041. `revisar_em` porque depende de versao de ferramenta. A regra ja esta em CLAUDE.md; a nota guarda o porque e o conserto.
