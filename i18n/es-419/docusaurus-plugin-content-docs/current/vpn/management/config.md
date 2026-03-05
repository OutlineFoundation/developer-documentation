---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline utiliza una configuración basada en YAML para definir los parámetros VPN y gestionar
el tráfico TCP/UDP. La configuración admite la componibilidad en múltiples niveles,
lo que permite establecer parámetros de configuración flexibles y extensibles.

La configuración de nivel superior especifica una
[TunnelConfig](../reference/access-key-config#tunnelconfig).

## Ejemplos

Una configuración habitual de Shadowsocks se vería de la siguiente manera:

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

Observa cómo ahora podemos tener los protocolos TCP y UDP ejecutándose en diferentes puertos o extremos
con prefijos diferentes.

Puedes usar anclas YAML y la clave de combinación `<<` para evitar la duplicación:

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

Ahora puedes crear estrategias y saltos múltiples:

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

En caso de bloqueo de protocolos "look-like-nothing" como Shadowsocks, puedes
usar Shadowsocks sobre WebSockets. Consulta la [configuración de ejemplo del
servidor](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)
para saber cómo implementarla. Una configuración del cliente se vería de la siguiente manera:

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

Ten en cuenta que el extremo de WebSocket puede, a su vez, tomar un extremo, que se puede
aprovechar para evitar el bloqueo basado en DNS:

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

Para garantizar la compatibilidad entre las distintas versiones del cliente de Outline, usa la opción
`first-supported` en la configuración. Esto es muy importante
a medida que se agregan nuevas estrategias y funciones a Outline, ya que es posible que no todos los usuarios
actualicen a la versión más reciente del software del cliente. Con `first-supported`, puedes
proporcionar una única configuración que funcione sin problemas en diversas plataformas
y versiones de clientes, lo que garantiza la retrocompatibilidad y una experiencia del usuario
coherente.

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
