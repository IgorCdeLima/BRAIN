---
tipo: decisao
status: aceita
decidido_em: 2026-09-30
decidido_por: Igor
substituida_por:
criado: 2026-09-30
tags: [ambiente, agentes, administracao, permissoes]
---
# ADR-0018 Papel Administrador com senha e aprovacao a cada mudanca

## Contexto

- As mudancas de ambiente (papeis, permissoes, lancador, lista de fontes) e os merges eram feitos pelo humano ou por uma sessao do app desktop **sem papel**. O hook trata essa sessao como humana: os commits entravam sem os trailers `Agente/Tarefa/Modelo`.
- O humano quer um papel que faca o que ele faz, ou o oriente, acima do Coordenador, sempre apresentando cada mudanca e pedindo aprovacao, e protegido por senha.

## Decisao

1. **Papel `administrador`** (Opus, copia principal, branch `main` ou `admin/*`): acesso as areas N4 e merge para a `main`. Perfil em modo `default`: toda edicao e todo comando que altera algo perguntam; leitura e livre. Sem busca aberta na web.
2. **Senha no lancador, nao no Claude:** `papel administrador` pede a senha no terminal (`getpass`, oculta) antes de abrir a sessao. Hash PBKDF2-SHA256 (600 mil iteracoes, sal aleatorio) em `~/.config/01_ia/admin.senha`, fora do repositorio; leitura negada a todos os papeis nas configuracoes dos projetos e no perfil. Criada no primeiro uso.
3. **Hook do Git:** o administrador passa pelas areas protegidas e restritas; so as areas fechadas a todos os papeis (`logs/`) continuam negadas. Trailers obrigatorios (`Agente: administrador`, `Tarefa: admin-AAAA-MM-DD`).
4. **Hierarquia:** humano > administrador > coordenador > demais papeis. O Coordenador escala ao administrador o que exige area N4 ou decisao de ambiente.
5. A regra 1 do `CLAUDE.md` ("nunca edite as proprias regras") passa a ter uma unica excecao: o administrador, com aprovacao a cada mudanca.

## Alternativas consideradas

| Alternativa | Por que nao |
|---|---|
| Senha digitada no chat do Claude | O modelo veria a senha; nao protege nada |
| Senha em arquivo do repositorio | Todos os papeis leem a raiz |
| Continuar com sessao sem papel | Commits sem rastreio; nenhuma restricao de escopo |
| Administrador em `acceptEdits` | O humano quer ver e aprovar cada mudanca |

## Consequencias

- A senha protege contra abrir o administrador por engano ou por outra pessoa no computador. A protecao contra os agentes continua sendo o lancador (recusa dentro do Claude) e a aprovacao a cada mudanca.
- O modo `default` torna as sessoes mais lentas (muitas perguntas): e o custo aceito pelo nivel de acesso.
- Sessoes sem papel ficam so para emergencia (ex.: o lancador quebrado).
