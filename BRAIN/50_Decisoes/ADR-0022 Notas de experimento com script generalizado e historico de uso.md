---
tipo: decisao
status: aceita
decidido_em: 2026-10-02
decidido_por: humano
substituida_por:
criado: 2026-10-02
tags: [brain, experimento, scripts, seguranca, revisor, bibliotecario, ambiente]
---
# ADR-0022 Notas de experimento com script generalizado e historico de uso

## Contexto

- Seguranca e Revisor escrevem scripts para provar abusos, reproduzir defeitos e medir recursos (ex.: T-0010 e T-0012: pico de memoria do Pillow, PNG de 16 bits saturado). Com o `@scratchpad` (`ADM-0015`) os scripts podem ser gravados, mas ficam fora do Git e somem no fim da sessao.
- Os candidatos atuais descrevem o metodo e nao trazem o script. Quem repete o experimento reescreve do zero e pode errar num detalhe que o codigo deixaria evidente (ex.: gerar a entrada num subprocesso para nao contaminar o pico de memoria).
- O humano quer notas que digam por que o script e usado, como, quando e por que ele e nao outro; que acompanhem onde foi reutilizado, em que contexto e se precisou mudar; e que ele mesmo possa ler. Pedido em `ADM-0016`.

## Decisao

1. Novo tipo de nota `experimento` (template `BRAIN/99_Sistema/Templates/Experimento.md`), uma pergunta por nota, com `categoria`: `seguranca` (abuso, prova de conceito), `teste` (reproduzir defeito ou comportamento) ou `medicao` (memoria, tempo, tamanho).
2. **Script sempre generalizado:** sem nomes, caminhos, dados ou URLs do projeto e sem segredos; do projeto de origem fica so o link para o VER/SEC. Script de seguranca roda sempre contra alvo isolado (localhost, container proprio, `--network none`).
3. A nota traz: objetivo, quando usar, por que este metodo e nao outro, ambiente, como rodar, script, como interpretar, limites, **Historico de uso** (data, tarefa e registro, contexto e motivo, resultado, se o script mudou) e **Versoes anteriores** (nada e apagado).
4. Fluxo: Seguranca e Revisor buscam uma nota de experimento antes de escrever um script. Script novo e reaproveitavel vira nota propria no Inbox. O reuso fica registrado no VER/SEC ("Experimentos reutilizados"), e o script alterado vira proposta de versao nova no Inbox. O Bibliotecario promove para `10_Conhecimento`, copia os reusos para o Historico de uso e atualiza `ultimo_uso`.
5. Script que protege contra um defeito de um projeto especifico vira tambem teste automatico **no projeto** (trabalho do Dev, regra 3 do `CLAUDE.md`). O Brain guarda a versao geral.

## Alternativas consideradas

| Alternativa | Pros | Contras |
|---|---|---|
| Arquivos `.py` soltos numa pasta do Brain | Executavel direto | Sem contexto, sem busca por titulo/tags, sem historico; vira lixo sem curadoria |
| Script so dentro do VER/SEC do projeto | Ja e a regra do ADM-0015; rastreavel | Preso a um projeto; nao e achado por outra tarefa |
| Candidato comum com um bloco de codigo | Nenhum template novo | Mistura conhecimento e procedimento; nao tem lugar para historico e versoes |
| **Nota propria de experimento (escolhida)** | Contexto + script + historico; busca por `tipo` e `categoria`; curadoria normal | Mais um template; o Bibliotecario precisa manter o historico |
| Quem reutiliza edita o historico direto | Historico sempre em dia | Quebra a regra de que so o Bibliotecario escreve em `10_Conhecimento` |

## Consequencias

- **Positivas:** experimentos reproduziveis entre tarefas e projetos; `ultimo_uso` e o historico mostram se o script ainda vale e se compensa mante-lo; o humano le o porque e o como num so lugar.
- **Negativas / riscos:** script envelhece com versoes de bibliotecas (mitigado por `valido_para`, `verificado_em` e o historico); generalizar pode tirar o detalhe que fazia o script funcionar (mitigado pelo link ao VER/SEC de origem); script de abuso no Brain (mitigado por alvo isolado e curadoria); o historico depende de quem reutiliza registrar o uso no VER/SEC.

## Relacionadas

- `ADM-0015` - scratchpad da sessao para Seguranca e Revisor.
- `ADM-0016` - pedido do humano que originou esta decisao.
- [[Seguranca]], [[Revisor]], [[Bibliotecario]] - quem propoe, registra o reuso e cura.
