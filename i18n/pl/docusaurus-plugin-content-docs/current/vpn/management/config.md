---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline korzysta z konfiguracji w formacie YAML do definiowania parametrów VPN i obsługi ruchu TCP/UDP. Konfiguracja obsługuje kompozycyjność na wielu poziomach, umożliwiając elastyczne i rozszerzalne konfiguracje.

Konfiguracja najwyższego poziomu określa [TunnelConfig](../reference/access-key-config#tunnelconfig).

## Przykłady {#examples}

Standardowa konfiguracja Shadowsocks będzie wyglądała w następujący sposób:

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

Zwróć uwagę, że TCP i UDP mogą być uruchamiane na różnych portach lub punktach końcowych oraz z różnymi zakresami.

Możesz korzystać z kotwic YAML oraz klucza scalającego `<<`, aby uniknąć duplikowania:

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

Można teraz tworzyć strategie i wykonywać liczne przeskoki:

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

W przypadku nietypowych protokołów, takich jak Shadowsocks, możesz skorzystać z Shadowsocks-over-Websockets. Zapoznaj się z [przykładową konfiguracją serwera](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml), aby dowiedzieć, się jak przeprowadzić wdrożenie. Konfiguracja klienta będzie wyglądała w następujący sposób:

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

Zwróć uwagę, że punkt końcowy Websocket może w konsekwencji wybrać punkt końcowy, który może zostać wykorzystany do ominięcia blokady systemu BNS.

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

Aby zadbać o zgodność między wieloma wersjami klienta Outline, skorzystaj z opcji `first-supported` w swojej konfiguracji. Jest to szczególnie istotne, jako że do Outline dodano nowe strategie i funkcje, a nie wszyscy użytkownicy zaktualizowali oprogramowanie klienta do najnowszej wersji. Korzystając z `first-supported`, możesz zapewnić pojedynczą konfigurację, która działa bezproblemowo na wielu różnych platformach i wersjach klienta, co przełoży się na zgodność wsteczną i spójne wrażenia użytkownika.

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
