---
tipo: workflow
status: ativo
versao: 1
criado: 2026-09-29
tags: [modelagem, requisitos, diagramas, mermaid]
---
# Padrões de modelagem

Guia do Engenheiro de Software (e referência do Revisor). Base: [[ADR-0008 Mermaid como padrao de diagramas]].

## Onde fica cada artefato (no projeto)

| Artefato | Arquivo |
|---|---|
| Requisitos | `docs/requisitos/requisitos.md` (template `Requisitos`) |
| Modelos | `docs/modelos/<tema>.md` — um arquivo por tema (contexto, dados, fluxos…) |
| Decisões | `docs/adr/ADR-#### Titulo.md` (template `ADR`), nascem `proposta` |
| Avaliação de tecnologia | `docs/avaliacoes/<assunto>.md` (template `Avaliacao de tecnologia`) |

## Qual diagrama fazer

Só faça o diagrama que responde uma pergunta real. Proporcional ao tamanho:

| Diagrama (Mermaid) | Pergunta que responde | Trivial | Normal | Grande |
|---|---|---|---|---|
| Contexto — C4 nível 1 (`flowchart`) | Quem usa? Com que sistemas conversa? | — | se novo sistema | ✅ |
| Containers — C4 nível 2 (`flowchart` + `subgraph`) | Quais processos/serviços e como se ligam? | — | se mudar infra | ✅ |
| Casos de uso (`flowchart` ator → ação) | O que cada tipo de usuário precisa fazer? | — | ✅ | ✅ |
| Atividades (`flowchart`) | Como é o processo, com decisões? | — | se houver regras | ✅ |
| Domínio / classes (`classDiagram`) | Quais conceitos e como se relacionam? | — | se domínio não trivial | ✅ |
| ER (`erDiagram`) | Como os dados são guardados? Tipos e restrições? | — | se mudar o banco | ✅ |
| Sequência (`sequenceDiagram`) | Quem chama quem, em que ordem, e o que acontece no erro? | — | fluxos críticos | ✅ |
| Estados (`stateDiagram-v2`) | Por quais fases uma entidade passa? | — | se tiver ciclo de vida | se tiver |
| Implantação (`flowchart`) | Onde e como roda? | — | — | se houver infra |

## Convenções Mermaid

- Nomes em português, iguais aos do código quando existirem (`produto`, `valor`), para facilitar a conferência.
- ER com tipo **e** restrição no comentário (`numeric valor "NUMERIC(10,2) > 0"`).
- Sequência sempre com o caminho de erro (`alt ... else`), não só o feliz.
- Um diagrama por bloco, com um título `##` que diga a pergunta que ele responde.
- Imagem nunca é a fonte de verdade.

## Requisitos bem escritos

- Um requisito = uma capacidade ou restrição, com **ID estável** (`RF-03` nunca é renumerado; removido vira "(removido)").
- **Verificável:** dá para escrever um teste ou um passo de conferência ("valor maior que zero, duas casas" — não "valor válido").
- Separar **decisão do humano**, **premissa** (assumida, revisável) e **questão em aberto** (bloqueia ou não?).
- Requisito não funcional com número quando possível (tempo, tamanho, versão).
- **Todo campo de entrada do usuario tem regra de formato com exemplos**: pelo menos 3 validos e 3 invalidos, incluindo os casos ambiguos (ex.: `1.234` e milhar ou decimal?) e os extremos (vazio, muito longo, caracteres de controle). O Revisor testa exatamente esses exemplos.

## Avaliação de tecnologia

- Pelo menos **duas alternativas reais** além da escolhida.
- Critérios com **peso** definidos **antes** das notas; notas de 1 a 5 com justificativa curta.
- Versões e suporte (fatos voláteis) com fonte oficial e data de consulta.
- O resultado vira um ADR `proposta`; o humano aceita.
