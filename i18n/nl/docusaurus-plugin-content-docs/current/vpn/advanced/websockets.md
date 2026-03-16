---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Outline-client v1.15.0+.*

In deze handleiding staat stapsgewijs uitgelegd hoe je Shadowsocks-over-WebSockets implementeert. Dit is een krachtige techniek om censuur te omzeilen in omgevingen waar reguliere Shadowsocks-verbindingen zijn geblokkeerd. Door Shadowsocks-verkeer in te kapselen in WebSockets kun je het vermommen als standaard webverkeer. Zo is het beter bestand tegen censuur en beter toegankelijk.

## Stap 1: Stel een Outline-server in en voer deze uit {#step_1_configure_and_run_an_outline_server}

Maak een nieuw `config.yaml`-bestand met de volgende configuratie:

```yaml
web:
  servers:
    - id: server1
        listen: 127.0.0.1:<WEB_SERVER_PORT>

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

Download de nieuwste [`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases) en voer deze uit met de gemaakte configuratie:

```sh
outline-ss-server -config=config.yaml
```

## Stap 2: Stel de webserver bloot {#step_2_expose_the_web_server}

Om je WebSocket-webserver openbaar toegankelijk te maken, moet je deze blootstellen aan internet en [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) instellen.
Je kunt dit op verschillende manieren doen. Je kunt een lokale webserver gebruiken, zoals [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) of [Apache](https://httpd.apache.org/) (zorg daarbij dat deze een geldig TLS-certificaat heeft). Je kunt ook een tunnelingservice inzetten, zoals [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) of [ngrok](https://ngrok.com/).

### Voorbeeld met TryCloudflare {#example_using_trycloudflare}

In dit voorbeeld gebruiken we [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) om te demonstreren hoe je snel een tunnel maakt. Dit is een handige, goed beveiligde manier om je lokale webserver bloot te stellen zonder inkomende poorten te openen.

1. Download en installeer [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. Maak een tunnel die wijst naar je lokale webserverpoort:

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Je krijgt van Cloudflare een subdomein (zoals
`acids-iceland-davidson-lb.trycloudflare.com`) om toegang te krijgen tot je WebSocket-eindpunt en TLS automatisch af te handelen. Noteer dit subdomein, je hebt het later weer nodig.

## Stap 3: Maak een dynamische toegangssleutel {#step_3_create_a_dynamic_access_key}

Maak een YAML-bestand met de clienttoegangssleutel voor je gebruikers met de indeling voor de [configuratie van de toegangssleutel](../management/config). Voeg het WebSockets-eindpunt toe dat je eerder hebt ingesteld aan de serverzijde:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Nadat je het YAML-bestand met de dynamische toegangssleutel hebt gemaakt, moet je zorgen dat je gebruikers er toegang toe hebben. Je kunt het bestand hosten op een statische webhostingservice of het dynamisch genereren. Meer informatie over hoe je [dynamische toegangssleutels](../management/dynamic-access-keys) gebruikt.

## Stap 4: Maak verbinding met de Outline-client {#step_4_connect_with_the_outline_client}

Gebruik een van de officiële apps voor de [Outline-client](../../download-links) (versie 1.15.0+) en voeg de dynamische toegangssleutel die je net hebt gemaakt toe als serverinvoer. Klik op **Verbinden** om het tunnelen naar je server te starten met de Shadowsocks-over-WebSocket-configuratie.

Gebruik een tool als [IPInfo](https://ipinfo.io) om te controleren of je nu browst op internet via je Outline-server.
