---
tipo: aprendizado
status: ativo
origem: T-0011 (Revisor), curado pelo Bibliotecario
tarefa: T-0011
confianca: media
fontes: ["ferramentas/papel.py (linhas 256-264)", "BRAIN/60_Agentes/Revisor.md", "BRAIN/70_Workflows/Matriz de verificacao.md", "operacao/tarefas/T-0011.md"]
verificado_em: 2026-10-04
valido_para: "fluxo de tarefa com interface: sim, lancador papel atual"
revisar_em: 2027-01-04
criado: 2026-09-30
decisao: promovido
tags: [regra, revisor, designer, interface, lacuna-de-processo]
---
# Tarefa de criacao do Designer trava na revisao visual porque ele nao revisa o proprio trabalho

## O que aconteceu

O Revisor so fecha tarefa com `interface: sim` se a secao "Revisao visual" estiver preenchida. Na T-0011 o executor foi o proprio Designer (brief, conceitos, prototipo), que nao pode revisar o proprio trabalho: a secao ficou vazia por construcao e a tarefa travou em `revisao`.

Revisao por uma segunda sessao de Designer tambem nao funciona: o lancador `ferramentas/papel.py` so abre o Designer em modo revisao quando o cartao e de **outro** papel (`dono != papel`, `status: revisao`, `interface: sim`). Cartao com `papel: designer` em `revisao` da "NAO INICIADO".

## O que aprendemos

O desenho atual nao preve Designer revisando Designer. Para tarefa de criacao do Designer, a revisao visual so faz sentido sobre a implementacao do Dev.

## O que muda a partir de agora

- **Na pratica (T-0011):** o humano adotou a dispensa da revisao visual, anotada na secao do cartao. Ao cair em caso igual, anote a dispensa e avise o humano.
- **Proposta de regra (N4, pendente):** formalizar essa dispensa no Revisor e na Matriz de verificacao, mantendo a revisao visual obrigatoria na implementacao do Dev. Pedido: `COORD-0031`. Alternativa registrada: tarefa de criacao com `interface: nao`. Opcao descartada: segunda sessao de Designer (exigiria mudar o lancador).

## Origem

[[T-0011]] (Revisor, 2026-09-30; fato do lancador reconferido em 2026-10-01). Papeis: [[ADR-0015 Papel Designer]].

## Decisao do Bibliotecario

**Promovido em 2026-10-04**, a pedido do humano. Registra o aprendizado e a pratica adotada; a regra em si segue como proposta N4 em `COORD-0031`. Quando a regra for aprovada, atualizar a secao "O que muda" para apontar para ela.
