---
title: "HTTPS automatico con Caddy"
sidebar_label: "HTTPS automatico con Caddy"
---

Questa guida spiega come utilizzare [Caddy](https://caddyserver.com/), un server web potente e facile da usare, per migliorare la configurazione del tuo server Outline. Le funzionalità di [HTTPS automatico](https://caddyserver.com/docs/automatic-https) e la configurazione flessibile di Caddy lo rendono una scelta eccellente per gestire il tuo server Outline, specialmente quando utilizzi un trasporto WebSocket.

## Cos'è Caddy? {#what_is_caddy}

Caddy è un server web open source noto per la sua facilità d'uso, l'HTTPS automatico e il supporto di vari protocolli. Semplifica la configurazione del server web e offre funzionalità come:

- **HTTPS automatico:** Caddy ottiene e rinnova automaticamente i certificati TLS, garantendo connessioni sicure.

- **Supporto di HTTP/3:** Caddy supporta l'ultimo protocollo HTTP/3 per un traffico web più veloce ed efficiente.

- **Estensibile con plug-in:** Caddy può essere esteso con plug-in per supportare varie funzionalità, tra cui reverse proxy e bilanciamento del carico.

## Passaggio 1: prerequisiti {#step_1_prerequisites}

- Scarica e installa [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Passaggio 2: configura il tuo dominio {#step_2_configure_your_domain}

Prima di avviare Caddy, assicurati che il tuo nome di dominio sia configurato correttamente per puntare all'indirizzo IP del tuo server.

- **Imposta i record A/AAAA:** accedi al tuo provider DNS e imposta i record A e AAAA per il tuo dominio in modo che puntino rispettivamente agli indirizzi IPv4 e IPv6 del tuo server.

- **Verifica i record DNS:** verifica che i tuoi record DNS siano impostati correttamente con una ricerca autorevole:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## Passaggio 3: crea ed esegui una build Caddy personalizzata {#build-and-run}

Utilizzando `xcaddy`, puoi creare un file binario `caddy` personalizzato che include il modulo server core Outline e altri moduli di estensione server di cui avrai bisogno.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## Passaggio 4: configura ed esegui il server Caddy con Outline {#step_4_configure_and_run_the_caddy_server_with_outline}

Crea un nuovo file `config.yaml` con la seguente configurazione:

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

Questa configurazione rappresenta una strategia Shadowsocks-over-WebSockets con un server web in ascolto sulla porta `443`, che accetta traffico aggregato Shadowsocks TCP e UDP rispettivamente nei percorsi `TCP_PATH` e `UDP_PATH`.

Esegui il server Caddy esteso con Outline utilizzando la configurazione creata:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

Puoi trovare altre configurazioni di esempio nel nostro [repository GitHub outline-ss-server/outlinecaddy](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples).

## Passaggio 5: crea una chiave di accesso dinamica {#step_5_create_a_dynamic_access_key}

Genera un file YAML della chiave di accesso client per i tuoi utenti utilizzando il formato della [configurazione avanzata](../management/config) e includi gli endpoint WebSocket precedentemente configurati sul lato server:

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

Dopo aver generato il file YAML della chiave di accesso dinamica, devi inviarlo ai tuoi utenti. Puoi ospitare il file su un servizio di web hosting statico o generarlo dinamicamente. Scopri di più su come utilizzare le [chiavi di accesso dinamiche](../management/dynamic-access-keys).

## Passaggio 6: connettiti al client Outline {#step_6_connect_with_the_outline_client}

Utilizza una delle applicazioni [client Outline](../../download-links) ufficiali del client Outline (1.15.0 e versioni successive) e aggiungi la tua chiave di accesso dinamica appena creata come voce server. Fai clic su **Connetti** per avviare il tunneling al tuo server utilizzando la configurazione Shadowsocks-over-Websocket.

Utilizza uno strumento come [IPInfo](https://ipinfo.io) per verificare che ora stai navigando su internet tramite il tuo server Outline.
