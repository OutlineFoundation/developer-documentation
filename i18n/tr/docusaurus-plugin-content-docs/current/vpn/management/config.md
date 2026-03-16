---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline, VPN parametrelerini tanımlamak ve TCP/UDP trafiğini işlemek için YAML tabanlı bir yapılandırma kullanır. Yapılandırma, birden fazla düzeyde birleştirilebilirliği destekler. Böylece esnek ve genişletilebilir kurumlara olanak tanır.

Üst düzey yapılandırmada [TunnelConfig](../reference/access-key-config#tunnelconfig) kullanılır.

## Örnekler {#examples}

Standart bir Shadowsocks yapılandırması şöyle olur:

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

TCP ve UDP'nin artık farklı bağlantı noktalarında veya uç noktalarda ve farklı öneklerle nasıl çalıştığına dikkat edin.

Yinelemeyi önlemek için YAML anchor'larını ve `<<` birleştirme anahtarını kullanabilirsiniz:

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

Artık strateji oluşturabilir ve birden çok aşamalı işlemler yapabilirsiniz:

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

Shadowsocks gibi trafiği değiştiren protokollerin engellenmesi durumunda, Shadowsocks-over-Websockets kullanabilirsiniz. Nasıl dağıtılacağına ilişkin [sunucu örneği](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) yapılandırmasına bakın. Bir istemci yapılandırması şöyle olur:

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

Websocket uç noktasının da bir uç noktaya bağlanabileceğini unutmayın. Bu yöntem, DNS tabanlı engellemeyi atlamak için kullanılabilir:

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

Farklı Outline istemci sürümleri arasında uyumluluğu sağlamak için yapılandırmanızda `first-supported` seçeneğini kullanın. Bu yöntem, kullanıcıların tamamı en yeni istemci yazılımına güncelleme yapmamış olabileceğinden, Outline'a yeni stratejiler ve özellikler eklendikçe özellikle önemlidir. `first-supported` kullanarak, çeşitli platformlarda ve istemci sürümlerinde sorunsuz bir şekilde çalışan tek bir yapılandırma sunabilirsiniz. Böylece geriye dönük uyumluluk ve tutarlı bir kullanıcı deneyimi sağlayabilirsiniz.

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
