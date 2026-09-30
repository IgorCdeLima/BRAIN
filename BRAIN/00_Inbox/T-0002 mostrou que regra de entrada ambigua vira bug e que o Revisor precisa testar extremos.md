---
tipo: candidato
status: inbox
tipo_proposto: aprendizado
origem: agente/claude-desktop
tarefa: T-0002
confianca: alta
fontes: ["operacao/tarefas/T-0002.md", "projetos/lab: VER-0003, VER-0004, VER-0005, BUG-0003, BUG-0004, BUG-0005", "merge 26a0a6a"]
verificado_em: 2026-09-29
valido_para: "fluxo de tarefa v2 (Dev, Revisor, Bibliotecario)"
criado: 2026-09-29
decisao:
tags: [retrospectiva, fluxo, revisao, requisitos]
---
# T-0002 mostrou que regra de entrada ambigua vira bug e que o Revisor precisa testar extremos

## Conteudo proposto

**O que aconteceu.** A T-0002 (cadastro e listagem) precisou de 3 rodadas Dev -> Revisor ate a aprovacao (VER-0003 e VER-0004 reprovados, VER-0005 aprovado), com 3 bugs: valor "1.234" gravado como R$ 1,23 (BUG-0003), caractere NUL gerando erro 500 (BUG-0004) e valor com 27+ digitos gerando erro 500 (BUG-0005).

**O que funcionou.**
- Os ajustes da retrospectiva da T-0001 pegaram: o Dev citou nota do Brain (httpx2), propos candidatos tambem nas correcoes, usou a porta da tarefa (8002) e listou os passos do humano no cartao.
- Testes isolados do banco da aplicacao (banco lab_test + rollback por teste) funcionaram.
- O repasse por arquivos segurou 3 rodadas sem copiar conversa.

**O que mudar.**
1. **Regra de entrada ambigua vira bug.** O requisito dizia "duas casas decimais" mas nao definia como tratar "1.234" (milhar ou decimal?). O Dev escolheu uma interpretacao, o Revisor outra. Funcionalidade com entrada de usuario deveria passar pelo Engenheiro de Software antes, com a regra de formato escrita e exemplos (validos e invalidos).
2. **O Revisor precisa testar extremos de forma sistematica.** O BUG-0005 ja existia no primeiro commit e o VER-0003 nao o pegou. Sugestao para a matriz de verificacao: para toda entrada de usuario, testar vazio, so espacos, muito longo, caracteres de controle, numeros gigantes e formatos ambiguos.
3. **Ferramentas do ambiente falharam em silencio:** reescrita pelo PowerShell corrompeu o cartao (ver [[PowerShell 5.1 corrompe arquivos UTF-8 ao reescrever com Get-Content e Set-Content]]) e o Obsidian fechado travou o Bibliotecario. As duas ja foram bloqueadas/verificadas no lancador.

Os itens 1 e 2 mexem em workflow e matriz (area N4): ficam como proposta ao humano.

## Evidencia

Cartao T-0002 (Entrega e 3 rodadas de Revisao), VER-0003 a VER-0005 e BUG-0003 a BUG-0005 no repositorio lab, merge 26a0a6a.

## Por que e reaproveitavel

Toda funcionalidade com formulario (T-0003 upload, projetos futuros) tem entradas de usuario com as mesmas armadilhas.

## Relacionadas no Brain

- [[Primeira tarefa com papeis mostrou que o repasse por arquivos funciona]]

## Decisao do Bibliotecario
