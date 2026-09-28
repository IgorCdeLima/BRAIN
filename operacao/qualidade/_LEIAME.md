# qualidade — catálogo de verificações, bugs e segurança

- `verificacoes/` — `VER-####`: o que foi checado, por quem, em qual commit, com qual resultado.
- `bugs/` — `BUG-####`: um arquivo por defeito, com reprodução e ciclo de vida.
- `seguranca/` — `SEC-####`: achados de segurança. **Nunca registrar segredos.**

## Permissões

- **Escrevem:** Revisor, Segurança e Coordenador (QA em fases futuras).
- **Todos os outros agentes: somente leitura.**
- Nada é apagado; registros só mudam de status.
- Quem corrige um bug não o verifica.

Ciclo de vida do bug: `novo → confirmado → em-correcao → corrigido → verificado → fechado`
(ou `duplicado` · `nao-reproduz` · `risco-aceito`).
