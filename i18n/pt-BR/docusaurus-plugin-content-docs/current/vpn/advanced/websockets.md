---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*App cliente do Outline v1.15.0+.*

Este tutorial mostra em detalhes como implementar
o Shadowsocks sobre WebSockets, uma técnica potente para contornar a censura em
ambientes onde as conexões normais do Shadowsocks são bloqueadas. Ao encapsular
o tráfego do Shadowsocks dentro de WebSockets, você pode disfarçá-lo como tráfego padrão da Web,
aumentando a resiliência e a acessibilidade.

## Etapa 1: configure e execute um servidor do Outline

Crie um novo arquivo `config.yaml` com a seguinte configuração:

Baixe a versão mais recente do
[`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases) (em inlgês)
e execute-a usando a configuração criada:

## Etapa 2: exponha o servidor da Web

Para tornar seu servidor da Web WebSocket acessível publicamente, é necessário que ele seja exposto à Internet. Também é preciso
configurar o [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) (em inglês).
Há várias formas de fazer isso. Você pode usar um servidor da Web local, como
[Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) ou
[Apache](https://httpd.apache.org/), garantindo que ele tenha um certificado TLS válido, ou
empregar um serviço de encapsulamento como o [Cloudflare
Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
ou o [ngrok](https://ngrok.com/) (todos os links em inglês).

### Exemplo usando o TryCloudflare

Neste exemplo, vamos demonstrar o uso do
[TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) (em inglês)
para criar um túnel rápido. Essa é uma forma maneira conveniente e segura de expor
seu servidor da Web local sem abrir portas de entrada.

1. Faça o download do
[`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) (em inglês) e instale-o.

2. Crie um túnel apontando para a porta do seu servidor da Web local:

O Cloudflare vai fornecer um subdomínio (por exemplo,
`acids-iceland-davidson-lb.trycloudflare.com`) para acessar seu endpoint WebSocket
e gerenciar automaticamente o TLS. Anote esse subdomínio, porque ele será necessário
mais tarde.

## Etapa 3: crie uma chave de acesso dinâmica

Gere um arquivo YAML de chaves de acesso do cliente para seus usuários com o formato de [configuração de chave de acesso](../management/config)
e inclua os endpoints do WebSocket que foram configurados
no lado do servidor:

Depois de gerar o arquivo YAML de chaves de acesso dinâmicas, você terá que entregá-lo aos seus
usuários. É possível armazenar o arquivo em um serviço estático de hospedagem na Web ou gerá-lo dinamicamente. Saiba mais sobre como usar as [chaves de acesso
dinâmicas](../management/dynamic-access-keys).

## Etapa 4: conecte-se com o app cliente do Outline

Use um dos aplicativos oficiais do [app cliente do Outline](../../download-links)
(versões 1.15.0+) e adicione a chave de acesso dinâmica que você criou como
uma entrada de servidor. Clique em **Conectar** para iniciar o encapsulamento para seu servidor usando a
configuração Shadowsocks sobre Websocket.

Use uma ferramenta como o [IPInfo](https://ipinfo.io) (em inglês) para verificar se você está navegando na
Internet pelo seu servidor Outline.
