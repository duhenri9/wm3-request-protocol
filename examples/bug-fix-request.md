# Exemplo — Correção de bug sem mudar produto

## Contexto

Um botão aprovado visualmente perde contraste quando o usuário passa o cursor.

## Problema real

O texto do botão fica difícil de ler no estado hover. Isso é um bug visual e de acessibilidade, não uma oportunidade para redesenhar a seção.

## Fonte de verdade

- componente atual aprovado;
- paleta atual;
- texto do botão atual;
- rota onde o botão aparece.

## O que deve mudar

- corrigir o estado hover para manter contraste suficiente;
- preservar o texto do botão;
- preservar tamanho, posição e destino do link.

## O que não deve mudar

- não alterar CTA;
- não alterar copy da seção;
- não alterar layout;
- não mudar oferta;
- não criar novo componente.

## Critério de pronto

- texto continua legível em default e hover;
- foco por teclado continua visível;
- desktop e mobile revisados;
- alteração limitada ao estilo do botão.
