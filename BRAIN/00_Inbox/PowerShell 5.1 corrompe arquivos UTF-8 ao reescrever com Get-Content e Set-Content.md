---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/claude-desktop
tarefa: T-0002
confianca: alta
fontes: ["operacao/tarefas/T-0002.md (sessao dev 958f8d5b, 2026-09-29 23:09)", "logs/sessoes/2026-09"]
verificado_em: 2026-09-29
valido_para: "Windows PowerShell 5.1 (powershell.exe)"
criado: 2026-09-29
decisao:
tags: [powershell, windows, codificacao, armadilha]
---
# PowerShell 5.1 corrompe arquivos UTF-8 ao reescrever com Get-Content e Set-Content

## Conteudo proposto

**Sintoma:** depois de um agente mudar uma linha de um arquivo .md pelo terminal, os acentos viram lixo: "é" vira "Ã©", "ç" vira "Ã§", travessao vira "â€”".

**Causa raiz:** no Windows PowerShell 5.1, `Get-Content` le arquivos UTF-8 sem BOM como se fossem Windows-1252. O texto ja chega corrompido na memoria; o `Set-Content -Encoding utf8` apenas grava a corrupcao. `Out-File` e o redirecionamento `>` ainda gravam em UTF-16 por padrao.

**Solucao:**
- Agentes editam arquivos so com as ferramentas de edicao (Edit/Write), nunca reescrevendo pelo terminal. `Set-Content`, `Out-File`, `Add-Content` e `WriteAll*` ficaram bloqueados por permissao.
- Texto novo em Markdown sem acentos nem cedilha (decisao do Igor), o que torna os arquivos imunes a qualquer ferramenta.
- Para consertar um arquivo ja corrompido: em cada linha, `linha.encode("cp1252").decode("utf-8")`; se der erro, a linha estava correta e fica como esta.

**O que nao funcionou:** passar `-Encoding utf8` so no `Set-Content` (a leitura ja estava errada).

## Evidencia

Cartao T-0002 com 107 ocorrencias corrompidas apos o comando `(Get-Content ...) -replace ... | Set-Content ... -Encoding utf8` do Dev; 35 linhas restauradas com a ida e volta cp1252 -> utf-8 (commit f1d481a).

## Por que e reaproveitavel

Qualquer agente no Windows que use PowerShell para "mudar so uma linha" cai nisso.

## Relacionadas no Brain

- [[Primeira tarefa com papeis mostrou que o repasse por arquivos funciona]]

## Decisao do Bibliotecario
