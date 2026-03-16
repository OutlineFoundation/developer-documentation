---
title: "Zugriffsschlüssel-Konfiguration"
sidebar_label: "Zugriffsschlüssel-Konfiguration"
---

Outline nutzt eine YAML-basierte Konfiguration, um VPN-Parameter zu definieren und TCP-/UDP-Traffic zu bewältigen. Die Konfiguration unterstützt Komponierbarkeit auf mehreren Ebenen und ermöglicht so flexible und erweiterbare Setups.

[TunnelConfig](../reference/access-key-config#tunnelconfig) ist das Element auf oberster Ebene der Konfiguration.

## Beispiele {#examples}

Eine typische Shadowsocks-Konfiguration sieht so aus:

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

Hinweis: TCP und UDP können über verschiedene Ports oder auf unterschiedlichen Endpunkten ausgeführt werden und sich in ihren Präfixen unterscheiden.

Sie können YAML-Anker und den Merge-Schlüssel `<<` verwenden, um Duplikate zu vermeiden:

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

Es ist jetzt möglich, Strategien zu komponieren und Multi-Hops auszuführen:

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

Statt „getarnte“ Protokolle wie Shadowsocks zu blockieren, können Sie Shadowsocks-over-WebSockets verwenden. In der [Server-Beispielkonfiguration](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) sehen Sie, wie dies bereitgestellt wird. Eine Client-Konfiguration sieht so aus:

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

Hinweis: Der WebSocket-Endpunkt kann wiederum einen Endpunkt haben, der genutzt werden kann, um die DNS-basierte Blockierung zu umgehen:

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

Um die Kompatibilität mit unterschiedlichen Outline-Client-Versionen sicherzustellen, verwenden Sie die Option `first-supported` in Ihrer Konfiguration. Das ist besonders wichtig, da Outline neue Strategien und Funktionen hinzugefügt werden und möglicherweise nicht alle Nutzer die neueste Clientsoftware haben. Mit `first-supported` können Sie eine Konfiguration bereitstellen, die auf verschiedenen Plattformen und Clientversionen nahtlos funktioniert. So sorgen Sie für Abwärtskompatibilität und eine einheitliche Nutzererfahrung.

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
