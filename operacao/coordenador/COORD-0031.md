---
tipo: pedido-coordenador
id: COORD-0031
status: aberto
urgencia: nao-bloqueante
pedido_por: bibliotecario
tarefa: ambiente
criado: 2026-10-04
atendido_em:
adm:
tags: [regra, revisor, designer, interface, lacuna-de-processo]
---
# COORD-0031 - Formalizar como regra a dispensa de revisao visual quando o executor e o Designer

## Pedido

Mudanca de regra em area N4 (so via `ADM-####`, com aprovacao do humano). Formalizar a **opcao 2** do candidato `BRAIN/00_Inbox/Revisao visual em tarefa de criacao do proprio Designer.md`:

- [ ] Em `BRAIN/60_Agentes/Revisor.md`: acrescentar que, se o executor do cartao com `interface: sim` for o proprio Designer (tarefa de criacao: brief, conceitos, prototipo), a revisao visual e dispensada; o Designer anota a dispensa na secao "Revisao visual" do cartao e o Revisor nao trava o fechamento por essa secao.
- [ ] Em `BRAIN/70_Workflows/Matriz de verificacao.md` (e, se couber, `BRAIN/70_Workflows/Fluxo de design.md` e o template `Tarefa`): registrar a mesma excecao, deixando claro que a revisao visual continua obrigatoria para a implementacao feita pelo Dev.
- [ ] Nenhuma mudanca em `ferramentas/papel.py`: a opcao 3 (Designer revisando Designer) fica descartada, pois o lancador so abre o Designer em modo revisao para cartao de outro papel.

Pasta: raiz do ambiente (copia principal).

## Motivo

Na T-0011 o executor foi o Designer; a secao "Revisao visual" ficaria vazia por construcao e a tarefa travaria em `revisao`. O humano adotou a opcao 2 (dispensa anotada no cartao), mas ela so vale como excecao daquela tarefa. Toda nova tarefa de criacao do Designer bate na mesma trava. Regras e workflows sao N4, e o Bibliotecario nao pode edita-los.

Apos a decisao, o Bibliotecario promove o candidato (ou o arquiva, ligado a regra), conforme o resultado.

---

## Atendimento

<!-- Preenchido pelo Coordenador. -->
