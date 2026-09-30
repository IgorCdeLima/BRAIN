---
tipo: aprendizado
status: ativo
origem: T-0002 (curado pelo Bibliotecario a partir do candidato do claude-desktop)
confianca: alta
fontes: ["operacao/tarefas/T-0002.md", "projetos/lab: VER-0003, VER-0004, VER-0005, BUG-0003, BUG-0004, BUG-0005", "merge 26a0a6a"]
verificado_em: 2026-09-29
valido_para: "fluxo de tarefa v2 (Dev, Revisor, Bibliotecario)"
revisar_em: 2027-03-29
criado: 2026-09-29
tags: [retrospectiva, fluxo, revisao, requisitos]
decisao: promovido
---
# T-0002 mostrou que regra de entrada ambigua vira bug e que o Revisor precisa testar extremos

## O que aconteceu

A T-0002 (cadastro e listagem) precisou de 3 rodadas Dev -> Revisor (VER-0003 e VER-0004 reprovados, VER-0005 aprovado), com 3 bugs: valor "1.234" gravado como R$ 1,23 (BUG-0003), caractere NUL gerando erro 500 (BUG-0004) e valor com 27+ digitos gerando erro 500 (BUG-0005).

Funcionou: os ajustes da retrospectiva da T-0001 (Dev cita nota do Brain, propoe candidatos tambem nas correcoes, usa a porta da tarefa, lista passos do humano no cartao); testes isolados com banco proprio e rollback por teste; repasse por arquivos segurou 3 rodadas sem copiar conversa.

## O que aprendemos

1. **Regra de entrada ambigua vira bug.** O requisito dizia "duas casas decimais" sem definir "1.234" (milhar ou decimal?). Dev e Revisor escolheram interpretacoes diferentes.
2. **O Revisor precisa testar extremos de forma sistematica.** O BUG-0005 existia no primeiro commit e o VER-0003 nao o pegou.
3. **Ferramentas do ambiente falham em silencio:** o PowerShell corrompeu o cartao (ver [[PowerShell 5.1 corrompe arquivos UTF-8 ao reescrever com Get-Content e Set-Content]]) e o Obsidian fechado travou o Bibliotecario. Ambas ja bloqueadas/verificadas no lancador.

## O que muda a partir de agora

Itens 1 e 2 mexem em workflow e matriz (area N4) e **ficam como proposta ao humano**, sem edicao pelo Bibliotecario:

- Funcionalidade com entrada de usuario passa antes pelo Engenheiro, com a regra de formato escrita e exemplos validos e invalidos.
- Matriz de verificacao: para toda entrada de usuario, testar vazio, so espacos, muito longo, caracteres de controle, numeros gigantes, formatos ambiguos (e, em upload, arquivo tipico grande demais e chunked; ver [[Recusa previa por Content-Length esconde a validacao do upload]]).

Notas geradas pelos bugs: [[Valor em reais com ponto de milhar sem virgula e ambiguo - nao converta direto para Decimal]] e [[Texto com caractere NUL derruba insert no PostgreSQL com erro 500]].

## Origem

Cartao T-0002 (Entrega e 3 rodadas de Revisao), VER-0003 a VER-0005 e BUG-0003 a BUG-0005 no lab, merge 26a0a6a. Relacionada: [[Primeira tarefa com papeis mostrou que o repasse por arquivos funciona]].

## Decisao do Bibliotecario

Promovido a `10_Conhecimento`: retrospectiva com evidencia rastreavel e confianca alta. Propostas de mudanca de workflow encaminhadas ao humano (N4).
