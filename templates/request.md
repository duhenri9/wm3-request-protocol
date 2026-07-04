# Requisição — [nome da mudança]

## 1. Contexto

Explique rapidamente o que está acontecendo.

- Qual projeto/página/fluxo está envolvido?
- O que levou a esta requisição?
- Qual é o estado atual?

## 2. Problema real

Descreva o problema antes de propor solução.

Evite começar por "faça X".
Comece por "o que está errado, confuso, quebrado ou desalinhado?".

## 3. Fonte de verdade

Liste o que deve ser considerado como referência.

Exemplos:

- URL atual;
- print aprovado;
- PR anterior;
- documento;
- copy aprovada;
- regra de negócio;
- commit/base SHA;
- decisão do founder;
- comportamento em produção.

## 4. O que deve mudar

Liste apenas o que está dentro do escopo.

- [ ] Mudança 1
- [ ] Mudança 2
- [ ] Mudança 3

## 5. O que não deve mudar

Liste explicitamente o que está fora do escopo.

- [ ] Não alterar copy aprovada
- [ ] Não alterar layout base
- [ ] Não alterar checkout
- [ ] Não alterar autenticação
- [ ] Não criar nova rota
- [ ] Não mudar preço
- [ ] Não tocar em banco de dados

## 6. Critério de pronto

Como saberemos que a mudança ficou pronta?

- [ ] Build passa
- [ ] Typecheck passa
- [ ] Fluxo principal funciona
- [ ] CTA aponta para o lugar certo
- [ ] Mobile e desktop revisados
- [ ] Nenhuma promessa pública foi alterada
- [ ] Nenhum gate foi pulado

## 7. Validações obrigatórias

Liste os testes, checks ou revisões necessárias.

- [ ] lint
- [ ] typecheck
- [ ] build
- [ ] smoke local
- [ ] smoke produção
- [ ] revisão visual
- [ ] revisão de copy
- [ ] revisão de segurança
- [ ] aprovação do responsável

## 8. Riscos

O que pode dar errado?

- Pode quebrar o fluxo atual?
- Pode criar promessa pública indevida?
- Pode afetar checkout, intake, e-mail ou dados?
- Pode introduzir falso positivo?

## 9. Decisão de merge/publicação

Quando pode ir para produção?

- [ ] Após aprovação técnica
- [ ] Após aprovação visual
- [ ] Após aprovação de negócio
- [ ] Após gate operacional
- [ ] Não pode ir ainda; precisa virar draft

## 10. Linha de controle

Resumo em uma frase:

> Esta requisição existe para [objetivo] sem alterar [limite importante].
