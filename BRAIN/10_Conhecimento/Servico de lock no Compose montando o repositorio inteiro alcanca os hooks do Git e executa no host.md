---
tipo: problema-solucao
status: ativo
origem: agente/seguranca (T-0009), curado pelo Bibliotecario
tarefa: T-0009
pesquisa:
confianca: alta
fontes: ["projetos/lab: SEC-0007 e SEC-0008 (revisao da T-0009, commit 30504a2)", "https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html", "https://cwe.mitre.org/data/definitions/829.html"]
verificado_em: 2026-10-01
valido_para: Docker Compose; pip-tools 7.6.1; pip 26.2.1; repositorio com core.hooksPath versionado
revisar_em: 2027-04-01
criado: 2026-10-01
decisao: promovido
tags: [seguranca, cwe-829, cwe-250, docker, compose, pip-tools, githooks, armadilha]
---
# Servico de lock no Compose montando o repositorio inteiro alcanca os hooks do Git e executa no host

## Sintoma

Um servico utilitario do Compose (ex.: `lock` com `pip-compile`) monta `.:/work` como root. Qualquer codigo que rode nesse container (sdist com `setup.py`, dependencia indireta adulterada da propria ferramenta) consegue gravar em `.githooks/`.

## Ambiente

Docker Compose; pip-tools 7.6.1; pip 26.2.1; repositorio com `core.hooksPath=.githooks` versionado.

## Causa raiz

Raiz do repositorio montada com escrita e usuario root. Se o repositorio usa `core.hooksPath=.githooks`, o hook gravado roda **no host** no proximo `git commit`: o codigo escapa do container sem nenhuma falha do Docker.

Prova (SEC-0008 do lab): `touch /work/.githooks/PROVA_ESCRITA` dentro do `lock` funcionou, uid 0, arquivo de dono root no host.

## Solucao

1. Montar so os arquivos de entrada (`:ro`) e uma pasta de saida; nunca a raiz.
2. `user: "${UID:-1000}:${GID:-1000}"` no servico (dispensa `chown`).
3. `pip-compile --pip-args "--only-binary=:all:"` para nao executar build de sdist ao resolver.
4. Travar com hash tambem a ferramenta que gera os hashes (estagio `lock`); senao ela e o elo sem controle.

## Como verificar que foi resolvido

`docker compose run --rm lock sh -c 'id -u; touch /work/.githooks/x'` deve mostrar uid diferente de 0 e falhar a escrita.

Resultados do lab (T-0009) que confirmam o `--require-hashes`: hash adulterado, pacote sem hash, indireta removida e versao trocada mantendo o hash antigo fazem o build falhar. Regenerar o travado numa copia e comparar com o commitado (`diff`) confere a integridade dos hashes.

## O que nao funcionou

Montar `.:/work` e rodar como root "porque e so um servico de apoio": foi exatamente a falha SEC-0008.

## Links confiaveis

- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): regras 2 (usuario) e 8 (somente leitura).
- [CWE-829 (MITRE)](https://cwe.mitre.org/data/definitions/829.html)

## Origem

SEC-0007 e SEC-0008 do `lab`, revisao de seguranca da T-0009.

## Relacionadas no Brain

- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]: o travamento que este servico gera; a ferramenta que o gera tambem precisa de controle.
- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]: mesma causa (root no container), aqui com alcance ao host via hooks.
- [[Imagem Docker que embute o codigo exige build antes de rodar pytest]]: servicos de verificacao do Compose.

## Decisao do Bibliotecario

Promovido (2026-10-01): confianca alta (prova reproduzida no SEC-0008), fontes OWASP e MITRE listadas pelo Seguranca. Sem duplicata: a nota CWE-250 trata USER no Dockerfile, nao o alcance aos hooks.
