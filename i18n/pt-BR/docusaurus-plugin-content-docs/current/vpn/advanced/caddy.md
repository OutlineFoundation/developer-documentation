---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

Este guia explica como usar o [Caddy](https://caddyserver.com/), um servidor da Web
potente e fácil de usar, para aprimorar a configuração do seu servidor Outline (os links relacionados ao Caddy nesta página estão em inglês). Com
[HTTPS automático](https://caddyserver.com/docs/automatic-https) e
configuração flexível, o Caddy é uma excelente opção para atender ao seu servidor Outline,
especialmente ao usar um transporte WebSocket.

## O que é Caddy?

O Caddy é um servidor da Web de código aberto conhecido por sua facilidade de uso, HTTPS automático
e suporte a vários protocolos. Ele simplifica a configuração do servidor da Web e
oferece recursos como:

- **HTTPS automático**: o Caddy obtém e renova automaticamente os certificados TLS,
garantindo conexões seguras.

- **Suporte a HTTP/3**: o Caddy aceita o protocolo HTTP/3 mais recente, garantindo mais rapidez e eficácia no tráfego da Web.

- **Extensível com plug-ins**: o Caddy aceita plug-ins para permitir
várias funcionalidades, como proxy reverso e balanceamento de carga.

## Etapa 1: pré-requisitos

- Baixe e instale o [`xcaddy`](https://github.com/caddyserver/xcaddy)

## Etapa 2: configurar seu domínio

Antes de iniciar o Caddy, verifique se o nome de domínio está configurado para apontar
para o endereço IP do seu servidor.

- **Defina registros A/AAAA**: entre no seu provedor de DNS e defina os registros A e AAAA
do seu domínio para apontar para os endereços IPv4 e IPv6 do seu servidor, respectivamente.

- 

**Verifique os registros DNS**: verifique se os registros DNS estão definidos corretamente com uma
pesquisa autoritativa:

## Etapa 3: criar e executar um build personalizado do Caddy

Com o `xcaddy`, é possível criar um `caddy` binário personalizado que inclui o módulo de servidor principal do Outline
e outros módulos de extensão de servidor necessários.

## Etapa 4: configurar e executar o servidor do Caddy com o Outline

Crie um novo arquivo `config.yaml` com a seguinte configuração:

Essa configuração representa uma estratégia do Shadowsocks sobre WebSockets com um servidor da Web
que detecta na porta `443`, aceitando tráfego TCP e UDP encapsulado
do Shadowsocks nos caminhos `TCP_PATH` e `UDP_PATH`,
respectivamente.

Execute o servidor Caddy estendido com o Outline usando a configuração criada:

Você pode encontrar mais exemplos de configurações em nosso [repositório do GitHub
outline-ss-server/outlinecaddy](https://github.com/Jigsaw-Code/outline-ss-server/tree/master/outlinecaddy/examples) (em inglês).

## Etapa 5: criar uma chave de acesso dinâmica

Gere um arquivo YAML de chave de acesso do cliente para seus usuários usando
o formato de [configuração avançada](../management/config) e inclua os endpoints
do WebSocket configurados anteriormente no lado do servidor:

Depois de gerar o arquivo YAML de chaves de acesso dinâmicas, você terá que entregá-lo aos seus
usuários. É possível hospedar o arquivo em um serviço estático de hospedagem
na Web ou gerá-lo dinamicamente. Saiba mais sobre como usar as [chaves de acesso
dinâmicas](../management/dynamic-access-keys).

## Etapa 6: estabelecer conexão com o app cliente do Outline

Use um dos aplicativos oficiais do [app cliente do Outline](../../download-links)
(versões 1.15.0+) e adicione a chave de acesso dinâmica que você criou como
uma entrada de servidor. Clique em **Conectar** para iniciar o encapsulamento para seu servidor usando a
configuração Shadowsocks sobre WebSocket.

Use uma ferramenta como o [IPInfo](https://ipinfo.io) (em inglês) para verificar se você está navegando na
Internet pelo seu servidor Outline.
