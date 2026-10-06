---
tipo: padrao
status: ativo
origem: SEARCH-0011 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0018
pesquisa: SEARCH-0011
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/522.html", "https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html"]
verificado_em: 2026-10-05
valido_para: "CWE 4.20"
criado: 2026-10-05
decisao: promovido
revisar_em: 2027-01-05
tags: [seguranca, cwe, cwe-522, credencial, container]
---
# CWE-522 token de ferramenta legivel pelo mesmo usuario se trata com permissao 0600 e escopo minimo

## Contexto

**O que e (MITRE):** CWE-522 e guardar ou transmitir credenciais por metodo inseguro, sujeito a interceptacao ou leitura nao autorizada. Consequencia: assumir a identidade do dono da credencial.

**No ambiente 01_IA:** o token OAuth do Claude Code fica em arquivo no home do usuario. Todo processo do mesmo UID no container (outra sessao, comando do agente) consegue le-lo. O sandbox de processo reduz esse caminho, mas nao o elimina.

## Problema

Credencial de ferramenta legivel por qualquer processo do mesmo usuario, ou gravada na imagem, permite que uma sessao comprometida assuma a identidade do dono.

## Solucao

Mitigacoes das fontes (MITRE + OWASP): proteger a credencial com mecanismo adequado (cofre, keystore, segredo injetado em tempo de execucao em vez de gravado na imagem) e dar a ela o menor privilegio possivel.

**Controles verificaveis (proposta do Pesquisador, inferida das mitigacoes; nao e texto da fonte e ainda nao foi validada):**

1. `stat -c '%a %U' <arquivo de credencial>` retorna `600` e o usuario esperado.
2. `docker history` e as camadas da imagem nao contem o arquivo (a credencial entra por volume ou segredo em tempo de execucao).
3. O sandbox de comandos nega a leitura do caminho da credencial: `cat` dentro de uma sessao de agente deve falhar.
4. Token revogavel, com escopo minimo e rotacao documentada.

## Trade-offs

- **Ganha:** uma sessao comprometida nao leva a credencial junto.
- **Perde:** negar a leitura quebra ferramentas do agente que dependem do arquivo (ver a nota do sandbox).

## Quando NAO usar

Credencial descartavel de teste, sem acesso a nada real.

## Evidencia

Definicao e mitigacoes lidas na pagina oficial da CWE-522 (4.20) e regra de segredos do OWASP Docker Security Cheat Sheet (RULE #12). Os controles 1 a 4 sao inferencia. Nao li a documentacao de armazenamento de credenciais do Claude Code; local e permissoes reais do arquivo do token estao **nao confirmados**.

## Links confiaveis

- [CWE-522](https://cwe.mitre.org/data/definitions/522.html): definicao, consequencias e mitigacoes.
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): segredos em containers (RULE #12) e usuario sem privilegio (RULE #2).

## Relacionadas

- [[Sandbox do Claude Code so protege a pasta de configuracao contra escrita - negue a leitura da credencial em managed settings]]: como negar a leitura da credencial no Claude Code.
- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]: usuario sem privilegio no container.
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento` como padrao. Sem duplicata. Os controles inferidos ficaram rotulados como proposta. Base para SEC-T0018-01 e a analise da T-0019.
