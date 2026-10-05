---
tipo: referencia
status: ativo
origem: SEARCH-0009 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0009
tarefa: ambiente
autor: Projeto tmux; Docker (documentacao oficial)
url: https://github.com/tmux/tmux/wiki/FAQ
acessado_em: 2026-10-05
confianca: media
fontes: ["https://github.com/tmux/tmux/wiki/FAQ", "https://docs.docker.com/reference/cli/docker/container/run/"]
verificado_em: 2026-10-05
valido_para: "tmux 3.x"
revisar_em: 2027-04-05
criado: 2026-10-05
decisao: promovido
tags: [ambiente, tmux, container, terminal, adm-0009]
---
# tmux em container exige TERM tmux ou screen, locale UTF-8 e window-size para varios clientes

## Resumo

- **TERM:** dentro do tmux, `TERM` deve ser `screen`, `tmux` ou similar (`tmux-256color`). Fora do tmux, deve casar com o terminal real. Com `docker exec -it`, o Docker repassa o `TERM` do terminal do host; a imagem precisa ter o terminfo correspondente (pacote `ncurses-term` em Debian/Ubuntu, se faltar). Para cor, `set -g default-terminal "tmux-256color"` no `.tmux.conf`; para 24 bits, tmux 3.2+ usa `terminal-features` com `RGB`.
- **UTF-8:** o tmux decide pelo locale (`LC_ALL`, `LC_CTYPE`, `LANG`). Imagens minimas costumam nao definir locale: definir `LANG=C.UTF-8` (ou gerar um locale) na imagem, ou iniciar com `tmux -u`.
- **Tamanho da janela:** com `-t`, o Docker aloca um pseudo-TTY e o tamanho segue o terminal do cliente. Com mais de um cliente anexado, a janela usa por padrao o menor; configurar `window-size largest` (tmux >= 2.9) ou anexar com `tmux attach -d`.
- Fluxo tipico: `docker exec -it <container> tmux attach -t <sessao>` (com `-u`/`LANG` se os acentos quebrarem).

## O que aproveitar

Checklist para a imagem do ambiente: terminfo (`ncurses-term`), `LANG=C.UTF-8`, `default-terminal` e `window-size largest` no `.tmux.conf`.

## Ressalvas

FAQ do tmux e documentacao de `docker run` lidas em 2026-10-05. O comportamento de redimensionamento do `docker exec` nao esta descrito na documentacao e nao foi testado: teste antes de depender dele.

## Links confiaveis

- [tmux wiki: FAQ](https://github.com/tmux/tmux/wiki/FAQ): `TERM`, UTF-8, 256 cores/RGB e `window-size`.
- [docker container run](https://docs.docker.com/reference/cli/docker/container/run/): `-i`, `-t` e `-e TERM`.

## Notas derivadas

- [[Orquestrar sessoes do Claude Code - -p com permission-prompts none, hooks Stop e SessionEnd, mensagem entre sessoes e agent teams experimental]]: as sessoes abertas nas janelas tmux do container.
- [[Arquivos do volume montado ficam com o dono certo rodando o container com o UID do usuario do host]]: o outro cuidado de imagem ao acessar o container do host.

## Decisao do Bibliotecario

Promovido a `30_Referencias` (2026-10-05): sem duplicata no Brain. Confianca media mantida. Nota original ligava ao volume com dono root so de forma tangencial; a ligacao foi trocada pela de UID do host.
