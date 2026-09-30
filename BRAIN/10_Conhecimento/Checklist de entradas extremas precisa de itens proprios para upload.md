---
tipo: padrao
status: ativo
origem: T-0006 (Engenheiro), curado pelo Bibliotecario
tarefa: T-0006
confianca: alta
fontes: ["projetos/lab: BUG-0006, SEC-0001, VER-0006, VER-0007", "BRAIN/70_Workflows/Matriz de verificacao.md", "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html"]
verificado_em: 2026-09-30
valido_para: "Matriz de verificacao v1, Padroes de modelagem v1"
revisar_em: 2027-03-30
criado: 2026-09-30
decisao: promovido
tags: [upload, verificacao, requisitos, entradas-extremas, proposta-n4]
---
# Checklist de entradas extremas precisa de itens proprios para upload

## Contexto

Campos de upload de arquivo em qualquer projeto. O checklist de entradas extremas da Matriz de verificacao e o guia de requisitos ("muito longo: limite + 1 e algo absurdo") foram pensados para texto e numero.

## Problema

Para arquivo, "limite + 1" e "absurdo" nao pegam o caso que quebrou a T-0003: a foto **tipica** grande demais (3 a 5 MB), que caia num teto anti-DoS e virava 413 em JSON (BUG-0006). O teste de "tamanho excedido" usava 2 MB + 58 bytes, abaixo da faixa do teto. A chunked sem `Content-Length` so apareceu na revisao (SEC-0001).

## Solucao

Para todo campo de upload, o checklist de entradas extremas inclui:

- limite + 1 byte;
- arquivo **tipico** grande demais (ex.: foto de celular de 3 a 5 MB) enviado como o navegador envia (`curl -H "Expect:"`);
- acima do teto anti-DoS (se houver): o que o usuario ve;
- envio sem `Content-Length` (chunked);
- cabecalho valido com corpo invalido; tipo disfarcado (extensao trocada, SVG, HTML);
- arquivo de 0 byte e campo vazio.

A tabela "Exemplos de entrada - imagem" do `requisitos.md` do lab (T-0006) ja segue este formato; VER-0007 testou esses casos e fechou a tarefa.

**Pendente (N4):** acrescentar esses itens a Matriz de verificacao ("Entradas extremas") e aos Padroes de modelagem e uma decisao do humano; o Bibliotecario nao edita 70_Workflows. A retrospectiva da T-0002 ja havia proposto algo parecido sem que entrasse na matriz.

## Trade-offs

- **Ganha:** pega o caso tipico que o limite + 1 nao pega; o usuario ve mensagem coerente em cada faixa.
- **Perde:** mais casos de teste por campo de upload.

## Quando NAO usar

Campos que so recebem texto ou numero; para eles vale o checklist atual.

## Links confiaveis

- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html): limites e validacao de arquivo (via [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]).

## Relacionadas

- [[Recusa previa por Content-Length esconde a validacao do upload]]: a mesma familia de armadilhas de tamanho.
- [[T-0002 mostrou que regra de entrada ambigua vira bug e que o Revisor precisa testar extremos]]: origem da proposta de checklist.
- [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]]: caso extremo de dimensao, nao de bytes.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento` como padrao (2026-09-30): evidencia em BUG-0006, SEC-0001 e VER-0007, sem duplicata. A mudanca na Matriz segue como proposta ao humano (N4).
