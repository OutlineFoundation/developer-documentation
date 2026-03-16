---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

O Outline usa uma configuração baseada em YAML para definir parâmetros de VPN e gerenciar
o tráfego TCP/UDP. A configuração oferece suporte à composição em vários níveis,
permitindo configurações flexíveis e extensíveis.

A configuração de nível superior especifica uma
[TunnelConfig](../reference/access-key-config#tunnelconfig).

## Exemplos {#examples}

Uma configuração típica do Shadowsocks será semelhante a esta:

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

Observe como agora podemos ter TCP e UDP em execução em diferentes portas ou endpoints e
com diferentes prefixos.

Você pode usar âncoras YAML e a chave de mesclagem `<<` para evitar duplicação:

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

Agora é possível compor estratégias e fazer vários saltos:

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

Em caso de bloqueio de protocolos look-like-nothing como o Shadowsocks, você pode
usar o Shadowsocks sobre Websockets. Confira o [exemplo de
configuração do servidor](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) (em inglês)
para saber como implantá-lo. Uma configuração de cliente será semelhante a:

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

Observe que o endpoint do Websocket pode, por sua vez, tomar um endpoint, que pode ser
aproveitado para ignorar o bloqueio baseado em DNS:

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

Para garantir a compatibilidade entre diferentes versões do app cliente do Outline, use a
opção `first-supported` na sua configuração. Isso é particularmente importante
à medida que novas estratégias e recursos são adicionados ao Outline, porque nem todos os usuários podem ter
atualizado para o software cliente mais recente. Ao usar o `first-supported`, você pode
fornecer uma configuração única que funciona em várias plataformas
e versões de cliente, garantindo compatibilidade com versões anteriores e uma experiência
de usuário consistente.

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
