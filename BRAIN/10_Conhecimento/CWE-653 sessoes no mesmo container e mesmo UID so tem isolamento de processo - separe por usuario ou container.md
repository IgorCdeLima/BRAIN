---
tipo: padrao
status: ativo
origem: SEARCH-0011 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0018
pesquisa: SEARCH-0011
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/653.html", "https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html"]
verificado_em: 2026-10-05
valido_para: "CWE 4.20"
criado: 2026-10-05
decisao: promovido
revisar_em: 2027-01-05
tags: [seguranca, cwe, cwe-653, container, isolamento]
---
# CWE-653 sessoes no mesmo container e mesmo UID so tem isolamento de processo - separe por usuario ou container

## Contexto

**O que e (MITRE):** CWE-653 e nao separar adequadamente funcoes ou recursos que exigem niveis de privilegio diferentes; uma falha na parte de menor privilegio alcanca a de maior. Consequencias: ganho de privilegio e contorno de protecoes.

**No ambiente 01_IA:** varias tarefas e sessoes no mesmo container, com o mesmo UID, separadas so pelo sandbox de processo.

## Problema

Uma sessao comprometida (ex.: injecao por conteudo web) compartilha arquivos, home e credenciais com todas as outras sessoes do container.

## Solucao

Mitigacoes das fontes:

- **MITRE:** distribuir privilegios entre modulos ou entidades distintos, minimizar interfaces entre componentes e usar controle de acesso forte nas fronteiras.
- **OWASP Docker:** usuario sem privilegio (RULE #2), limitar capabilities (#3), `--security-opt=no-new-privileges` (#4), cuidado com a conectividade entre containers (#5), seccomp/AppArmor/SELinux (#6).

**Controles verificaveis (proposta do Pesquisador, inferida; nao e texto da fonte e ainda nao foi validada):**

1. `docker inspect` mostra `User` nao root, `CapDrop` com `ALL` e `no-new-privileges`.
2. Teste de fronteira: de uma sessao, tentar ler o worktree e o home de outra; deve ser negado. Se for permitido, o isolamento e so de convencao.
3. Se o teste 2 falhar e o risco nao for aceito: UID distinto por tarefa ou um container por tarefa.

## Trade-offs

- **Ganha:** uma sessao comprometida fica contida.
- **Perde:** UID por tarefa ou container por tarefa aumentam a complexidade (volumes, posse de arquivos, custo de recursos).

## Quando NAO usar

Quando todas as sessoes ja sao do mesmo nivel de confianca e o container inteiro e descartavel.

## Evidencia

Texto da pagina oficial CWE-653 (4.20) e das regras do OWASP Docker Security Cheat Sheet. Controles 1 a 3 sao inferencia; nada executado.

## Links confiaveis

- [CWE-653](https://cwe.mitre.org/data/definitions/653.html): definicao, consequencias, mitigacoes.
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): regras 2 a 6 de endurecimento e isolamento do container.

## Relacionadas

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]
- [[USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid]]: complementa as regras #3 e #4.
- [[CWE-522 token de ferramenta legivel pelo mesmo usuario se trata com permissao 0600 e escopo minimo]]: a credencial e o que as sessoes mais compartilham.
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento` como padrao. Sem duplicata. Base para a decisao de isolamento da T-0019 e para SEC-T0018-02.
