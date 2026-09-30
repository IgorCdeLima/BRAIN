# Como configurar outro computador

Roteiro para trabalhar no ambiente 01_IA em outra maquina. Repositorios:

- Ambiente e Brain: https://github.com/IgorCdeLima/BRAIN
- Projeto lab: https://github.com/IgorCdeLima/lab

## 1. Programas

| Programa | Observacao |
|---|---|
| Git for Windows | Traz o Git Bash, usado pelos hooks |
| Python 3 | Com o lancador `py` (instalador oficial do python.org) |
| Claude Code (terminal) | PowerShell: `irm https://claude.ai/install.ps1 \| iex`; depois `claude` para fazer login |
| Docker Desktop | Precisa estar aberto para rodar o lab |
| Obsidian | Versao 1.12.7 ou maior |
| Orca | https://www.onorca.dev |

## 2. Clonar no mesmo caminho: D:\01_IA

Hooks, lancador e permissoes usam o caminho `D:\01_IA`. Clone exatamente assim:

```powershell
git clone https://github.com/IgorCdeLima/BRAIN.git D:\01_IA
git clone https://github.com/IgorCdeLima/lab.git D:\01_IA\projetos\lab
```

Se a maquina nao tiver disco `D:`, pare aqui: os caminhos precisam virar configuracao antes.

## 3. Ativar os hooks do Git (uma vez por repositorio)

```powershell
git -C D:\01_IA config core.hooksPath .githooks
git -C D:\01_IA\projetos\lab config core.hooksPath .githooks
```

## 4. Travar o modo bypass do Claude Code

Crie `C:\Users\<usuario>\.claude\settings.json` com:

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  }
}
```

## 5. Obsidian

- Abrir a pasta `D:\01_IA\BRAIN` como Vault.
- Configuracoes -> Sobre -> **Interface de linha de comando**: ativar e clicar em **Registrar**. Abrir um terminal novo e conferir com `obsidian version`.
- O Git e a fonte de verdade: nao use o Obsidian Sync para editar o mesmo conteudo nas duas maquinas.

## 6. Orca

- Adicionar os repositorios `D:\01_IA` e `D:\01_IA\projetos\lab`.
- Settings -> Agents: modo **Manual** (remover `--dangerously-skip-permissions` do Claude).
- Worktrees sempre com **terminal em branco**; o papel e iniciado pelo lancador.

## 7. Conferir

Num terminal em `D:\01_IA`, com o Obsidian aberto:

```powershell
D:\01_IA\ferramentas\papel bibliotecario --verificar
```

Esperado: `Tudo certo`.

## Rotina entre os dois computadores

1. **Ao comecar:** `git pull` nos dois repositorios (`D:\01_IA` e `D:\01_IA\projetos\lab`).
2. **Ao terminar:** commit e `git push` nos dois.
3. Nao deixe trabalho sem commit numa maquina e comece o mesmo arquivo na outra.
4. Ficam so na maquina (nao sincronizam): `logs/`, volumes do Docker, worktrees do Orca e configuracoes pessoais.
