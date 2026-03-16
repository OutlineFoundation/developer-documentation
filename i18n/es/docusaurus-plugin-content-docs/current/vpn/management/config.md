---
title: "Configuración de claves de acceso"
sidebar_label: "Configuración de claves de acceso"
---

Outline usa una configuración basada en YAML para definir los parámetros de la VPN y gestionar el tráfico TCP/UDP. La configuración admite la componibilidad en varios niveles, por lo que es flexible y ampliable.

La configuración de nivel superior especifica [TunnelConfig](../reference/access-key-config#tunnelconfig).

## Ejemplos {#examples}

Este es el aspecto de una configuración típica de Shadowsocks:

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

Fíjate en que ahora TCP y UDP pueden ejecutarse en puertos o endpoints distintos y con prefijos diferentes.

Puedes usar los anclas YAML y la clave de fusión `<<` para evitar los duplicados:

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

Ahora puedes redactar estrategias y hacer varios saltos:

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

Si se bloquean los protocolos que no se parecen a nada en particular como Shadowsocks, puedes usar la técnica Shadowsocks a través de Websockets. Consulta el [ejemplo de configuración del servidor](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) para saber cómo implementarlo. Este es el aspecto de la configuración del cliente:

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

El endpoint de Websocket puede, a su vez, tomar un endpoint, que puede servir para sortear el bloqueo basado en DNS:

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

Para asegurar la compatibilidad entre las distintas versiones del cliente de Outline, usa la opción `first-supported` en tu configuración. Esto cobra especial importancia a medida que se añaden nuevas estrategias y funciones a Outline, ya que es posible que no todos los usuarios hayan actualizado a la versión más reciente del software cliente. Si usas `first-supported`, puedes ofrecer una configuración que funcione a la perfección en las distintas plataformas y versiones del cliente, lo que garantiza la retrocompatibilidad y una experiencia de usuario coherente.

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
