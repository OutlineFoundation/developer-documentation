---
title: "Concepts"
sidebar_label: "Concepts"
---

O Outline ajuda os usuários a ignorar restrições para acessar a Internet aberta. Aqui estão
alguns conceitos-chave para entender como isso funciona:

## Provedores de serviços e usuários finais

O sistema Outline envolve duas funções principais: **provedores de serviços**, que gerenciam os servidores, e **usuários finais**, que acessam a Internet por esses servidores.

- Os **provedores de serviços** criam servidores do Outline, geram **chaves de acesso**
e **as distribuem** para os usuários finais. Uma maneira de fazer isso é usando o
aplicativo **Outline Manager**.

- Os **usuários finais** instalam o **app cliente do Outline**, colam a
**chave de acesso** recebida e se **conectam** a um túnel seguro.

## Chaves de acesso

Chaves de acesso são credenciais que permitem aos usuários se conectar a um servidor
do Outline. Elas têm as informações necessárias para que o app cliente do Outline
estabeleça uma conexão segura. Existem dois tipos de chaves de acesso:

- As **chaves de acesso estáticas** codificam todas as informações do servidor necessárias para conexão
(endereço, porta, senha e método de criptografia do servidor), impedindo que as informações
de acesso sejam modificadas. Os usuários colam a chave no
app cliente do Outline.

Exemplo:

- As **chaves de acesso dinâmicas** permitem que um provedor de serviços hospede remotamente as informações
de acesso ao servidor. Isso permite aos provedores atualizar a configuração do servidor
(endereço, porta, senhas e método de criptografia do servidor) sem precisar
emitir novas chaves de acesso para os usuários finais. Para uma documentação mais detalhada, consulte
[Chaves de acesso dinâmicas](vpn/management/dynamic-access-keys).
