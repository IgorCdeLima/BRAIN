---
tipo: candidato
status: inbox
tipo_proposto: proposta-de-regra
origem: agente/revisor
tarefa: T-0011
pesquisa:
confianca: media
fontes: ["ferramentas/papel.py", "BRAIN/60_Agentes/Revisor.md", "BRAIN/70_Workflows/Matriz de verificacao.md", "operacao/tarefas/T-0011.md"]
verificado_em: 2026-10-01
valido_para: "fluxo de tarefa com interface: sim"
criado: 2026-09-30
decisao:
tags: [regra, revisor, designer, interface, lacuna-de-processo]
---
# Revisao visual em tarefa de criacao do proprio Designer

## Conteudo proposto

**Lacuna de regra** (para o humano decidir; regras sao N4):

- O Revisor so fecha tarefa com `interface: sim` se a secao "Revisao visual" estiver preenchida; vazia, ele avisa o humano que falta o Designer.
- Na T-0011 o executor e o proprio Designer (tarefa de criacao: brief, conceitos, prototipo). Ele nao pode revisar o proprio trabalho, entao a secao fica vazia por construcao e a tarefa trava em `revisao`.

Opcoes:

1. Tarefa de criacao com `papel: designer` usa `interface: nao` (a revisao visual vale para a implementacao do Dev), e a coluna "Documentacao de projeto" da matriz cobre o prototipo.
2. Manter `interface: sim` e a regra do Revisor dizer: "se o executor for o Designer, a revisao visual e dispensada; anotar a dispensa na secao".
3. Exigir uma segunda sessao de Designer como revisor visual.

**Fato novo (2026-10-01):** a opcao 3 nao funciona hoje. O lancador `ferramentas/papel.py` (linhas 256-264) so abre o Designer em modo revisao quando o cartao e de **outro** papel (`dono != papel` e `status: revisao` com `interface: sim`). Cartao com `papel: designer` em `revisao` da "NAO INICIADO". O humano tentou na T-0011 e ficou bloqueado; escolheu a opcao 2 (dispensa anotada no cartao). Para a opcao 3 valer, o Administrador teria de mudar o lancador.

Recomendacao do Revisor: opcao 1 ou 2, ja que a trava do lancador confirma que o desenho atual nao preve Designer revisando Designer.

## Decisao do Bibliotecario

**Mantido no Inbox, aguardando o humano** (2026-10-01): e proposta de mudanca de regra (Revisor, Matriz de verificacao, lancador), area N4; o Bibliotecario nao pode promover nem editar. O humano ja adotou na T-0011 a opcao 2 (dispensa anotada no cartao); falta decidir se vira regra. Nao e conhecimento a catalogar ate la.

## Por que vale guardar

Toda nova tarefa de design vai bater na mesma trava.
