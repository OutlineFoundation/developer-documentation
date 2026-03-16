---
title: "Configurer la clé d&apos;accès"
sidebar_label: "Configurer la clé d&apos;accès"
---

Outline utilise une configuration YAML pour définir les paramètres VPN et gérer le trafic TCP/UDP. Cette configuration permet une composabilité multiniveau, pour des configurations flexibles et extensibles.

L'élément [TunnelConfig](../reference/access-key-config#tunnelconfig) est indiqué dans la configuration de premier niveau.

## Exemples {#examples}

Voici à quoi ressemble généralement une configuration Shadowsocks :

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

Les protocoles TCP et UDP peuvent désormais être exécutés sur différents ports ou points de terminaison, et avec différents préfixes.

Vous pouvez utiliser des ancres YAML et la clé de fusion `<<` pour éviter la duplication :

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

Il est maintenant possible de composer des stratégies et de faire des multisauts.

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

En cas de protocoles bloquants ou difficiles à identifier comme Shadowsocks, vous pouvez utiliser Shadowsocks-over-Websockets. Découvrez un [exemple de configuration de serveur](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)
et comment le déployer. Voici à quoi ressemble une configuration client :

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

Le point de terminaison Websocket peut à son tour prendre un point de terminaison, lequel peut être utilisé pour contourner un blocage DNS :

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

Pour permettre une compatibilité avec différentes versions de client Outline, utilisez l'option `first-supported` dans votre configuration. C'est particulièrement important lorsque de nouvelles stratégies et fonctionnalités sont ajoutées à Outline, car tous les utilisateurs n'ont peut-être pas la dernière version du logiciel client. En utilisant `first-supported`, vous pouvez fournir une configuration unique qui fonctionne sur différentes plates-formes et versions de client, afin d'assurer une bonne rétrocompatibilité et une expérience utilisateur cohérente.

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
