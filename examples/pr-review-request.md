# Exemplo — Pedido de revisão de PR

## Contexto

Um PR altera a página principal de uma oferta e precisa ser revisado antes de sair de draft.

## Objetivo declarado do PR

Alinhar a página com a oferta atual, sem mudar checkout, preço ou fluxo de captação.

## Delta real a revisar

- arquivos de página;
- componentes de CTA;
- copy pública;
- formulário/intake, se tocado;
- documentação operacional.

## Pontos de atenção

- a copy nova contradiz a oferta aprovada?
- algum CTA sugere compra automática?
- o PR ativa checkout sem aprovação?
- o formulário ainda aponta para o fluxo correto?
- mobile e desktop continuam legíveis?

## Validações necessárias

- diff revisado;
- lint/build/typecheck;
- screenshot desktop;
- screenshot mobile;
- smoke do fluxo principal;
- aprovação do responsável pela oferta.

## Decisão esperada

- approve, se o PR estiver dentro do escopo;
- request changes, se mudar promessa, preço, CTA ou fluxo sem autorização;
- manter draft, se faltar validação operacional.
