# WM3 Request Protocol

[English](README.md) · **Português (Brasil)**

Um contrato open source, versionado, para transformar pedidos vagos de produto/software em requisições com **fonte de verdade, escopo, critérios observáveis, evidência exigida e autoridade de publicação**.

> Um pedido claro ainda não é prova de que o trabalho foi entregue.

## Em 60 segundos

Pedido fraco:

> Corrige o bug do cadastro e garante que ficou bom.

Pedido V1:

- **Problema:** e-mail duplicado retorna HTTP 500.
- **Fonte de verdade:** contrato atual de `POST /signup` + SHA base.
- **Em escopo:** tratamento de e-mail duplicado.
- **Fora do escopo:** auth provider, preço, schema do banco.
- **AC-1:** com e-mail já existente, retornar HTTP 409 e não aumentar a contagem de usuários.
- **Verificação:** fixture de integração + build no head revisado.
- **Indeterminado quando:** a fixture não consegue provar a contagem anterior.
- **Gate:** `READY_WHEN` AC-1 e evidências obrigatórias estiverem verdes.

Isso é diferente de dizer apenas `bug corrigido` ou `build passou`.

## O que existe na V1

```text
problema
  ↓
fonte de verdade + identidade
  ↓
em escopo / fora do escopo
  ↓
critérios de aceite observáveis
  ↓
evidências de verificação exigidas
  ↓
riscos + desconhecidos + autoridade
  ↓
gate de publicação
```

A V1 inclui:

- [especificação normativa](spec/request-protocol-v1.md);
- [JSON Schema](schema/request.v1.schema.json);
- [template humano V1](templates/request.md);
- GitHub Issue Forms e PR template;
- validator/linter sem dependências externas;
- fixtures válidas e deliberadamente inválidas;
- CI com controles negativos;
- documentação específica para [critérios de aceite](docs/acceptance-criteria.md), [fonte de verdade](docs/source-of-truth.md) e [anti-padrões](docs/anti-patterns.md).

## Validator

```bash
python tools/validate_request.py examples/machine-readable/valid-request.json
```

O validator retorna `VALID` ou `INVALID` para o **contrato da requisição** e produz hashes determinísticos. Ele não executa o trabalho e não afirma que a implementação foi entregue.

O JSON Schema usa Draft 2020-12. O validator local é propositalmente um linter sem dependências e não se apresenta como implementação completa do padrão JSON Schema.

## Estados importantes

Para o contrato da requisição:

- `VALID` — passou as regras estruturais/semânticas implementadas;
- `INVALID` — faltam campos ou existe contradição material;
- `INDETERMINATE` — um consumidor não consegue estabelecer um fato obrigatório com segurança.

Para o gate de publicação:

- `DRAFT`;
- `BLOCKED`;
- `READY_WHEN`.

`READY_WHEN` não significa “pronto”. Significa que as condições de progressão estão declaradas.

## Request Protocol ≠ RepoOps

O WM3 Request Protocol **define o contrato** do trabalho.

O [RepoOps](https://github.com/duhenri9/RepoOps) é um projeto separado para execução/manutenção de repositório com autoridade e evidência delimitadas.

Veja [Protocol vs RepoOps](docs/protocol-vs-repoops.md).

## Perfis

- `compact` — mudanças pequenas/baixo risco, mantendo os campos essenciais;
- `standard` — mudanças materiais de produto/software.

O perfil compacto existe para evitar burocracia desnecessária; ele não remove fonte de verdade, escopo, aceite, evidência ou autoridade.

## Migração

O protocolo público original, de julho de 2026, já tinha contexto, fonte de verdade, escopo e validação. A V1 separa melhor **comportamento observável** de **checks de implementação**, adiciona identidade/freshness, incerteza explícita e representação machine-readable.

Veja [migração V0 → V1](docs/migration-v0-to-v1.md).

## Contribuição e licença

Veja [CONTRIBUTING.md](CONTRIBUTING.md). O conteúdo/código é MIT. A licença não concede direitos sobre marcas da WM3 Digital; veja [TRADEMARKS.md](TRADEMARKS.md).

## Trabalho relacionado da WM3 Digital

O protocolo é útil de forma independente e não exige nenhum produto comercial. Para quem quiser conhecer uma iniciativa relacionada da WM3, o Audit 360 trabalha com alinhamento entre promessa, fluxo, código e contexto do projeto.
