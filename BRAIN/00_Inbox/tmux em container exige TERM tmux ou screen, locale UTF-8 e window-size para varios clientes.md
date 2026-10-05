---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: ambiente
pesquisa: SEARCH-0009
confianca: media
fontes: [https://github.com/tmux/tmux/wiki/FAQ, https://docs.docker.com/reference/cli/docker/container/run/]
verificado_em: 2026-10-05
valido_para: tmux 3.x
criado: 2026-10-05
decisao:
tags: [ambiente, tmux, container, terminal, adm-0009]
---
# tmux em container exige TERM tmux ou screen, locale UTF-8 e window-size para varios clientes

## Conteudo proposto

- **TERM:** dentro do tmux, `TERM` deve ser `screen`, `tmux` ou similar (`tmux-256color`). Fora do tmux, deve casar com o terminal real. Com `docker exec -it`, o Docker repassa o `TERM` do terminal do host; a imagem precisa ter o terminfo correspondente (pacote `ncurses-term` em Debian/Ubuntu, se faltar). Para cor, `set -g default-terminal "tmux-256color"` no `.tmux.conf`; para 24 bits, tmux 3.2+ usa `terminal-features` com `RGB`.
- **UTF-8:** o tmux decide pelo locale (`LC_ALL`, `LC_CTYPE`, `LANG`). Imagens minimas costumam nao definir locale: definir `LANG=C.UTF-8` (ou gerar um locale) na imagem, ou iniciar com `tmux -u`.
- **Tamanho da janela:** com `-t`, o Docker aloca um pseudo-TTY e o tamanho segue o terminal do cliente; a documentacao de `docker run` nao detalha o redimensionamento, entao teste. Com mais de um cliente anexado, a janela usa por padrao o menor; configurar `window-size largest` (tmux >= 2.9) ou anexar com `tmux attach -d`.
- Fluxo tipico: `docker exec -it <container> tmux attach -t <sessao>` (com `-u`/`LANG` se os acentos quebrarem).

## Evidencia

FAQ oficial do tmux e documentacao de `docker run`, lidas em 2026-10-05. O comportamento de redimensionamento do `docker exec` nao esta descrito na documentacao e nao foi testado aqui.

## Links confiaveis

- [tmux wiki: FAQ](https://github.com/tmux/tmux/wiki/FAQ): `TERM`, UTF-8, 256 cores/RGB e `window-size`.
- [docker container run](https://docs.docker.com/reference/cli/docker/container/run/): `-i`, `-t` e `-e TERM`.

## Por que e reaproveitavel

Qualquer ambiente que rode sessoes tmux dentro de um container acessado do host.

## Relacionadas no Brain

- [[Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio]]

## Decisao do Bibliotecario
