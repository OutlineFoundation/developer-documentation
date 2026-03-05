---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

Questa guida spiega come utilizzare [Caddy](https://caddyserver.com/), un server web potente e facile da usare, per migliorare la configurazione del tuo server Outline. Le funzionalità di [HTTPS automatico](https://caddyserver.com/docs/automatic-https) e la configurazione flessibile di Caddy lo rendono una scelta eccellente per gestire il tuo server Outline, specialmente quando utilizzi un trasporto WebSocket.

## Cos'è Caddy?

Caddy è un server web open source noto per la sua facilità d'uso, l'HTTPS automatico e il supporto di vari protocolli. Semplifica la configurazione del server web e offre funzionalità come:

- **HTTPS automatico:** Caddy ottiene e rinnova automaticamente i certificati TLS, garantendo connessioni sicure.

- **Supporto di HTTP/3:** Caddy supporta l'ultimo protocollo HTTP/3 per un traffico web più veloce ed efficiente.

- **Estensibile con plug-in:** Caddy può essere esteso con plug-in per supportare varie funzionalità, tra cui reverse proxy e bilanciamento del carico.

## Passaggio 1: prerequisiti

- Scarica e installa [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Passaggio 2: configura il tuo dominio

Prima di avviare Caddy, assicurati che il tuo nome di dominio sia configurato correttamente per puntare all'indirizzo IP del tuo server.

- **Imposta i record A/AAAA:** accedi al tuo provider DNS e imposta i record A e AAAA per il tuo dominio in modo che puntino rispettivamente agli indirizzi IPv4 e IPv6 del tuo server.

- 

**Verifica i record DNS:** verifica che i tuoi record DNS siano impostati correttamente con una ricerca autorevole:

## Passaggio 3: crea ed esegui una build Caddy personalizzata

Utilizzando `xcaddy`, puoi creare un file binario `caddy` personalizzato che include il modulo server core Outline e altri moduli di estensione server di cui avrai bisogno.

## Passaggio 4: configura ed esegui il server Caddy con Outline

Crea un nuovo file `config.yaml` con la seguente configurazione:

Questa configurazione rappresenta una strategia Shadowsocks-over-WebSockets con un server web in ascolto sulla porta `443`, che accetta traffico aggregato Shadowsocks TCP e UDP rispettivamente nei percorsi `TCP_PATH` e `UDP_PATH`.

Esegui il server Caddy esteso con Outline utilizzando la configurazione creata:

Puoi trovare altre configurazioni di esempio nel nostro [repository GitHub outline-ss-server/outlinecaddy](https://github.com/Jigsaw-Code/outline-ss-server/tree/master/outlinecaddy/examples).

## Passaggio 5: crea una chiave di accesso dinamica

Genera un file YAML della chiave di accesso client per i tuoi utenti utilizzando il formato della [configurazione avanzata](../management/config) e includi gli endpoint WebSocket precedentemente configurati sul lato server:

Dopo aver generato il file YAML della chiave di accesso dinamica, devi inviarlo ai tuoi utenti. Puoi ospitare il file su un servizio di web hosting statico o generarlo dinamicamente. Scopri di più su come utilizzare le [chiavi di accesso dinamiche](../management/dynamic-access-keys).

## Passaggio 6: connettiti al client Outline

Utilizza una delle applicazioni [client Outline](../../download-links) ufficiali del client Outline (1.15.0 e versioni successive) e aggiungi la tua chiave di accesso dinamica appena creata come voce server. Fai clic su **Connetti** per avviare il tunneling al tuo server utilizzando la configurazione Shadowsocks-over-Websocket.

Utilizza uno strumento come [IPInfo](https://ipinfo.io) per verificare che ora stai navigando su internet tramite il tuo server Outline.
