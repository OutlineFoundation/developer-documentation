---
title: "Конфигурация ключей доступа"
sidebar_label: "Конфигурация ключей доступа"
---

Для определения параметров VPN и обработки TCP- и UDP-трафика Outline использует конфигурацию в формате YAML. Конфигурация поддерживает многоуровневую структуру, обеспечивая гибкость и возможность расширения настроек.

Объект верхнего уровня конфигурации – [TunnelConfig](../reference/access-key-config#tunnelconfig).

## Примеры {#examples}

Типичная конфигурация Shadowsocks выглядит следующим образом:

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

Обратите внимание, что теперь протоколы TCP и UDP могут работать на разных портах или конечных точках с разными префиксами.

Вы можете использовать анкеры YAML и ключ `<<`, чтобы избежать создания копий.

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

Теперь можно комбинировать стратегии и настраивать многоэтапные соединения:

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

В случае блокировки "маскирующихся" протоколов (например, Shadowsocks), вы можете использовать Shadowsocks-over-Websockets. Ознакомьтесь с [примером конфигурации сервера](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml), чтобы развернуть этот вариант. Конфигурация клиента выглядит следующим образом:

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

Обратите внимание, что конечная точка WebSocket также может принимать другую конечную точку, что позволяет обходить блокировку на основе DNS.

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

Чтобы обеспечить совместимость с различными версиями клиента Outline, используйте в конфигурации параметр `first-supported`. Это важно, поскольку в Outline постоянно добавляются новые стратегии и функции, но не у всех пользователей клиент может быть обновлен до последней версии. Применяя `first-supported`, вы можете создать универсальную конфигурацию, которая будет работать на разных платформах и в разных версиях клиента, обеспечивая обратную совместимость и удобство использования.

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
