---
title: "Configurazione delle chiavi di accesso"
sidebar_label: "Configurazione delle chiavi di accesso"
---

Outline utilizza una configurazione basata su YAML per definire i parametri VPN e gestire il traffico TCP/UDP. La configurazione supporta la componibilità a più livelli, consentendo configurazioni flessibili ed estensibili.

La configurazione di livello superiore specifica un [TunnelConfig](../reference/access-key-config#tunnelconfig).

## Esempi {#examples}

Una tipica configurazione Shadowsocks sarà simile a questa:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks
    endpoint: ss.example.com:80
    cipher: chacha20-ietf-poly1305
    secret: SECRET
    prefix: "POST "  # HTTP request

  udp:
    $type: shadowsocks
    endpoint: ss.example.com:53
    cipher: chacha20-ietf-poly1305
    secret: SECRET
    prefix: "\u0097\u00a7\u0001\u0000\u0000\u0001\u0000\u0000\u0000\u0000\u0000\u0000"  # DNS query
```

Tieni presente che ora possiamo avere TCP e UDP in esecuzione su porte o endpoint diversi e con prefissi diversi.

Puoi utilizzare anchor YAML e la chiave di unione `<<` per evitare duplicati:

```yaml
transport:
  $type: tcpudp

  tcp:
    <<: &shared
      $type: shadowsocks
      endpoint: ss.example.com:4321
      cipher: chacha20-ietf-poly1305
      secret: SECRET
    prefix: "POST "

  udp: *shared
```

Ora è possibile comporre strategie ed eseguire hop multipli:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: dial
      address: exit.example.com:4321
      dialer:
        $type: shadowsocks
        address: entry.example.com:4321
        cipher: chacha20-ietf-poly1305
        secret: ENTRY_SECRET

    cipher: chacha20-ietf-poly1305
    secret: EXIT_SECRET

  udp: *shared
```

In caso di blocco dei protocolli "look-like-nothing" come Shadowsocks, puoi utilizzare Shadowsocks-over-Websockets. Fai riferimento alla [configurazione di esempio del server](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) per sapere come eseguirne il deployment. Una configurazione client apparirà così:

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```

Nota che l'endpoint Websocket può, a sua volta, prendere un endpoint, che può essere sfruttato per bypassare il blocco basato su DNS:

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
        endpoint: cloudflare.net:443
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
        endpoint: cloudflare.net:443
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```

Per garantire la compatibilità tra diverse versioni del client Outline, utilizza l'opzione `first-supported` nella tua configurazione. Ciò è particolarmente importante perché vengono aggiunte nuove strategie e funzionalità a Outline, poiché non tutti gli utenti potrebbero aver aggiornato il software client più recente. Utilizzando `first-supported`, puoi fornire una singola configurazione che funziona senza problemi su diverse piattaforme e versioni client, garantendo la compatibilità con le versioni precedenti e un'esperienza utente coerente.

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
      $type: first-supported
      options:
        - $type: websocket
          url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
        - ss.example.com:4321
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
      $type: first-supported
      options:
        - $type: websocket
          url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
        - ss.example.com:4321
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```
