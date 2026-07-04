# Exemplo — Ajuste de intake sem falso positivo

## Contexto

O formulário envia pedidos de auditoria para o e-mail administrativo.

## Problema real

Se o provedor de e-mail rejeitar o envio, o sistema não pode fingir que o pedido foi recebido.

## Fonte de verdade

- payload esperado do formulário;
- regra de negócio: pedido só é aceito se ao menos um canal de entrega funcionar;
- e-mail administrativo configurado;
- comportamento esperado de sucesso/falha.

## O que deve mudar

- checar explicitamente o retorno do provedor de e-mail;
- registrar erro sanitizado;
- retornar falha honesta quando nenhum canal funcionar.

## O que não deve mudar

- não alterar preço;
- não ativar checkout;
- não criar banco de dados;
- não mudar copy pública;
- não expor segredo em log.

## Critério de pronto

- sucesso retorna apenas quando entrega funciona;
- falha retorna mensagem clara;
- logs não expõem segredo;
- smoke confirma envio real.
