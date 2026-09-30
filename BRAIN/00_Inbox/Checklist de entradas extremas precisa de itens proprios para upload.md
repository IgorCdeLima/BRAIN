---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/engenheiro
tarefa: T-0006
pesquisa:
confianca: alta
fontes: ["projetos/lab: BUG-0006, SEC-0001, VER-0006, VER-0007", "BRAIN/70_Workflows/Matriz de verificacao.md"]
verificado_em: 2026-09-30
valido_para: "Matriz de verificacao v1, Padroes de modelagem v1"
criado: 2026-09-30
decisao:
tags: [upload, verificacao, requisitos, entradas-extremas, proposta-n4]
---
# Checklist de entradas extremas precisa de itens proprios para upload

## Conteudo proposto

O checklist de entradas extremas da Matriz de verificacao e o guia de requisitos ("muito longo: limite + 1 e algo absurdo") foram pensados para texto e numero. Para arquivo, "limite + 1" e "absurdo" nao pegam o caso que quebrou a T-0003: a foto **tipica** grande demais (3 a 5 MB), que caia num teto anti-DoS e virava 413 em JSON (BUG-0006). A retrospectiva da T-0002 ja propos esses itens, mas eles nao entraram na matriz.

**Proposta ao humano (M4, area N4)** - acrescentar a Matriz ("Entradas extremas") e aos Padroes de modelagem (exemplos de entrada), para campos de upload:

- limite + 1 byte;
- arquivo **tipico** grande demais (ex.: foto de celular de 3 a 5 MB) enviado como o navegador envia (`curl -H "Expect:"`);
- acima do teto anti-DoS (se houver): o que o usuario ve;
- envio sem `Content-Length` (chunked);
- cabecalho valido com corpo invalido; tipo disfarcado (extensao trocada, SVG, HTML);
- arquivo de 0 byte e campo vazio.

## Evidencia

BUG-0006 (teste de "tamanho excedido" usava 2 MB + 58 bytes, abaixo da faixa do teto), SEC-0001 (chunked), VER-0007 (os casos acima, testados pelo Revisor, fecharam a tarefa). A tabela "Exemplos de entrada - imagem" do `requisitos.md` do lab (T-0006) ja segue este formato.

## Links confiaveis

- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html): limites e validacao de arquivo (via [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]).

## Por que e reaproveitavel

Todo projeto com upload.

## Relacionadas no Brain

- [[Recusa previa por Content-Length esconde a validacao do upload]]
- [[T-0002 mostrou que regra de entrada ambigua vira bug e que o Revisor precisa testar extremos]]

## Decisao do Bibliotecario
