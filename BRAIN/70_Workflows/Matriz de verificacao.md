---
tipo: workflow
status: ativo
versao: 1
criado: 2026-09-28
tags: [qualidade, verificacao]
---
# Matriz de verificação

Verificações obrigatórias por tipo de mudança. Uma tarefa só é concluída quando **cada verificação obrigatória tem um registro `VER-####`** — com resultado, ou justificativa explícita de por que não se aplica.

| Verificação | Código | Documentação de projeto | Conhecimento (Brain) | Regras / config de agentes |
|---|---|---|---|---|
| Testes automáticos passam | ✅ | — | — | — |
| Lint / formatação | ✅ | ✅ (Markdown) | — | ✅ (JSON válido) |
| Revisão de código (outro agente) | ✅ | — | — | — |
| Revisão de segurança | se tocar auth, dados, segredos, rede ou dependências | — | — | ✅ |
| Revisao do papel Seguranca (`SEC-####`), sem bloqueante aberto | se `seguranca: sim` | — | — | — |
| Entradas extremas (ver lista abaixo) testadas em cada campo de entrada do usuario | se houver entrada de usuario | — | — | — |
| Revisao visual do Designer (`UX-####`), sem bloqueante aberto | se `interface: sim` e o executor nao for o Designer (tarefa de criacao: dispensada, anotada no cartao) | — | — | — |
| Regras de formato da entrada definidas pelo Engenheiro, com exemplos validos e invalidos | se houver entrada de usuario (conferir que a regra existe e foi seguida) | ✅ se definir entrada | — | — |
| Critérios de aceite atendidos | ✅ | ✅ | — | — |
| Diagramas coerentes com o código | se mudou modelo | ✅ | — | — |
| Duplicata no Brain verificada | — | — | ✅ | — |
| Fontes e `verificado_em` preenchidos | — | — | ✅ | — |
| Requisitos verificáveis, com premissas e questões em aberto separadas | — | ✅ | — | — |
| Diagramas respondem uma pergunta real e seguem os [[Padroes de modelagem]] | — | ✅ | — | — |
| Avaliação de tecnologia com ≥ 2 alternativas, pesos prévios e fontes oficiais | — | se houver | — | — |
| ADR com alternativas e consequências, `status: proposta` | — | se houver decisão | — | — |
| Cartões de implementação com critérios derivados dos requisitos | — | se houver | — | — |
| Aprovação humana | merge na `main` | se mudar requisitos; ADRs sempre | — | ✅ **sempre** |

## Entradas extremas (checklist do Revisor)

Para cada campo que recebe dado do usuario (formulario, parametro, upload), testar na aplicacao rodando e registrar o resultado no VER:

- vazio e so espacos;
- muito longo (limite + 1 e algo absurdo, ex.: 1 MB);
- caracteres de controle (NUL `\x00`, quebras de linha, tabulacao) e emoji;
- HTML e script (`<b>`, `<script>`) -> deve aparecer escapado;
- numeros: zero, negativo, gigante (30+ digitos), muitas casas decimais, formatos ambiguos (`1.234`, `1,234`);
- tipo errado (texto onde se espera numero, arquivo com extensao trocada).

Nenhuma entrada pode gerar erro 500: entrada invalida vira resposta de validacao (ex.: 422). Origem: retrospectiva da T-0002 (o BUG-0005 existia desde o primeiro commit e passou pela primeira revisao).

## Tamanho da tarefa

- **Trivial** (texto, ajuste pequeno sem lógica): lint + revisão rápida.
- **Normal**: matriz completa.
- **Grande**: matriz completa + spec aprovada + ADR se houver decisão de arquitetura.

## Regras

- Verificação **não feita** é registrada como lacuna no `VER-####`, com o motivo. Omitir é falha.
- Quem executou a tarefa não registra a própria revisão de código.
- **Um VER vale para um commit.** Se o branch receber um novo commit depois da verificação, é preciso um novo VER sobre o novo commit. O VER anterior permanece como histórico.
- O Revisor confere a matriz antes de aprovar; o humano confere de novo antes do merge (e, na fase 3, o Coordenador).
