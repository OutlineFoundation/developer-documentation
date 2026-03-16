---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

In deze handleiding wordt uitgelegd hoe je [Caddy](https://caddyserver.com/), een krachtige en gebruiksvriendelijke webserver, kunt gebruiken als aanvulling op je Outline-serverinstallatie. De functies voor [automatische HTTPS](https://caddyserver.com/docs/automatic-https) en flexibele configuratie van Caddy maken van Caddy een uitstekende keuze om je Outline-server op te serven, vooral als je WebSocket-transport gebruikt.

## Wat is Caddy? {#what_is_caddy}

Caddy is een open source webserver die bekendstaat vanwege de gebruiksvriendelijkheid, automatische HTTPS en ondersteuning voor verschillende protocollen. Caddy maakt de configuratie van webservers makkelijker en biedt functies als:

- **Automatische HTTPS:** Caddy verkrijgt en vernieuwt automatisch TLS-certificaten en zorgt zo voor een beveiligde verbinding.

- **Ondersteuning voor HTTP/3:** Caddy ondersteunt het nieuwste HTTP/3-protocol voor sneller en efficiënter webverkeer.

- **Uitbreidbaar met plug-ins:** Je kunt Caddy uitbreiden met plug-ins om verschillende functies toe te voegen, zoals omgekeerde proxy's en load balancing.

## Stap 1: Vereisten {#step_1_prerequisites}

- Download en installeer [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Stap 2: Stel je domein in {#step_2_configure_your_domain}

Zorg voordat je aan de slag gaat met Caddy dat je domeinnaam zo is ingesteld dat deze wijst naar het IP-adres van je server.

- **Stel A/AAAA-records in:** Log in bij je DNS-provider en stel de A- en AAAA-records van je domein zo in dat ze wijzen naar respectievelijk het IPv4- en IPv6-adres van je server.

- **Controleer DNS-records:** Controleer of je DNS-records juist zijn ingesteld met een autoritatieve lookup:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## Stap 3: Maak een aangepaste Caddy-build en voer deze uit {#build-and-run}

Met `xcaddy` kun je een aangepast binair bestand voor `caddy` maken die de kernmodule van de Outline-server en andere nodige extensiemodules van de server bevat.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## Stap 4: Stel de Caddy-server in en voer deze uit met Outline {#step_4_configure_and_run_the_caddy_server_with_outline}

Maak een nieuw `config.yaml`-bestand met de volgende configuratie:

```yaml
apps:
  http:
    servers:
      server1:
        listen:
          - ":443"
        routes:
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<TCP_PATH>
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<UDP_PATH>
            handle:
              - handler: websocket2layer4
                type: packet
                connection_handler: ss1
  outline:
    shadowsocks:
      replay_history: 10000
    connection_handlers:
      - name: ss1
        handle:
          handler: shadowsocks
          keys:
            - id: user-1
              cipher: chacha20-ietf-poly1305
              secret: <SHADOWSOCKS_SECRET>
```

Deze configuratie vertegenwoordigt een Shadowsocks-over-WebSockets-strategie met een webserver die luistert op poort `443` en TCP-en UDP-verkeer verpakt door Shadowsocks accepteert via respectievelijk pad `TCP_PATH` en `UDP_PATH`.

Voer de Caddy-server uitgebreid met Outline uit door middel van de gemaakte configuratie:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

Je vindt meer voorbeeldconfiguraties in onze [GitHub-repository outline-ss-server/outlinecaddy](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples).

## Stap 5: Maak een dynamische toegangssleutel {#step_5_create_a_dynamic_access_key}

Maak een YAML-bestand met de clienttoegangssleutel voor je gebruikers met de indeling voor de [geavanceerde configuratie](../management/config). Voeg het WebSockets-eindpunt toe dat je eerder hebt ingesteld aan de serverzijde:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Nadat je het YAML-bestand met de dynamische toegangssleutel hebt gemaakt, moet je zorgen dat je gebruikers er toegang toe hebben. Je kunt het bestand hosten op een statische webhostingservice of het dynamisch genereren. Meer informatie over hoe je [dynamische toegangssleutels](../management/dynamic-access-keys) gebruikt.

## Stap 6: Maak verbinding met de Outline-client {#step_6_connect_with_the_outline_client}

Gebruik een van de officiële apps voor de [Outline-client](../../download-links) (versie 1.15.0+) en voeg de dynamische toegangssleutel die je net hebt gemaakt toe als serverinvoer. Klik op **Verbinden** om het tunnelen naar je server te starten met de Shadowsocks-over-WebSocket-configuratie.

Gebruik een tool als [IPInfo](https://ipinfo.io) om te controleren of je nu browst op internet via je Outline-server.
