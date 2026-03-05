---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Client Outline 1.15.0 e versioni successive.*

Questo tutorial fornisce una procedura dettagliata per aiutarti a implementare Shadowsocks-over-WebSockets, una potente tecnica per bypassare la censura in ambienti in cui le normali connessioni Shadowsocks sono bloccate. Incapsulando il traffico Shadowsocks all'interno di WebSockets, puoi mascherarlo come traffico web standard, migliorando la resilienza e l'accessibilità.

## Passaggio 1: configura ed esegui un server Outline

Crea un nuovo file `config.yaml` con la seguente configurazione:

Scarica l'ultimo [`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases) ed eseguilo utilizzando la configurazione creata:

## Passaggio 2: esponi il server web

Per rendere il tuo server web WebSocket accessibile pubblicamente, dovrai esporlo a internet e configurare [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
Puoi farlo in vari modi. Puoi utilizzare un server web locale come [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) o [Apache](https://httpd.apache.org/), assicurandoti che abbia un certificato TLS valido, oppure utilizzare un servizio di tunneling come [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) o [ngrok](https://ngrok.com/).

### Esempio con TryCloudflare

Per questo esempio, mostreremo come utilizzare [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) per creare un tunnel rapido. Ciò fornisce un modo pratico e sicuro di esporre il tuo server web locale senza aprire porte in entrata.

1. Scarica e installa [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. Crea un tunnel che punti alla porta del tuo server web locale:

Cloudflare fornirà un sottodominio (ad es. `acids-iceland-davidson-lb.trycloudflare.com`) per accedere al tuo endpoint WebSocket e gestire automaticamente TLS. Prendi nota di questo sottodominio, perché ti servirà in seguito.

## Passaggio 3: crea una chiave di accesso dinamica

Genera un file YAML della chiave di accesso client per i tuoi utenti utilizzando il formato della [configurazione delle chiavi di accesso](../management/config) e includi gli endpoint WebSocket precedentemente configurati sul lato server:

Dopo aver generato il file YAML della chiave di accesso dinamica, devi inviarlo ai tuoi utenti. Puoi ospitare il file su un servizio di web hosting statico o generarlo dinamicamente. Scopri di più su come utilizzare le [chiavi di accesso dinamiche](../management/dynamic-access-keys).

## Passaggio 4: connettiti al client Outline

Utilizza una delle applicazioni [client Outline](../../download-links) ufficiali del client Outline (1.15.0 e versioni successive) e aggiungi la tua chiave di accesso dinamica appena creata come voce server. Fai clic su **Connetti** per avviare il tunneling al tuo server utilizzando la configurazione Shadowsocks-over-Websocket.

Utilizza uno strumento come [IPInfo](https://ipinfo.io) per verificare che ora stai navigando su internet tramite il tuo server Outline.
