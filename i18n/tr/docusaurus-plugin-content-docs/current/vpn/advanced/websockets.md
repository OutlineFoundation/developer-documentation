---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Outline istemcisi (1.15.0+ sürümleri)*

Bu eğitimde, normal Shadowsocks bağlantılarının engellendiği ortamlarda sansürü aşmak için güçlü bir teknik olan Shadowsocks-over-WebSockets'i uygulamanıza yardımcı olacak ayrıntılı bilgiler paylaşılmıştır. Shadowsocks trafiğini WebSockets içinde kapsülleyerek standart web trafiği olarak gizleyebilir, esnekliği ve erişilebilirliği artırabilirsiniz.

## 1. adım: Outline sunucusu yapılandırın ve çalıştırın {#step_1_configure_and_run_an_outline_server}

Aşağıdaki yapılandırmayı kullanarak yeni bir `config.yaml` dosyası oluşturun:

```yaml
web:
  servers:
    - id: server1
        listen: 127.0.0.1:<WEB_SERVER_PORT>

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

En yeni [`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases)'ı indirin ve oluşturulan yapılandırmayı kullanarak çalıştırın.

```sh
outline-ss-server -config=config.yaml
```

## 2. adım: Web sunucusunu internete açın {#step_2_expose_the_web_server}

WebSocket web sunucunuza herkesin erişebilmesi için internete açmanız ve [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security)'yi yapılandırmanız gerekir.
Bu işlem için birkaç seçeneğiniz vardır. [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) veya [Apache](https://httpd.apache.org/) gibi yerel bir web sunucusu kullanabilir ve geçerli bir TLS sertifikasına sahip olduğundan emin olabilirsiniz. Dilerseniz [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) ya da [ngrok](https://ngrok.com/) gibi bir tünel oluşturma hizmeti kullanabilirsiniz.

### TryCloudflare kullanılan örnek {#example_using_trycloudflare}

Bu örnekte, hızlıca bir tünel oluşturmak için [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) kullanacağız. Bu sayede, gelen bağlantı noktalarını açmadan yerel web sunucunuzu internete açmak için uygun ve güvenli bir yöntemden yararlanabilirsiniz.

1. [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)'i indirip yükleyin.

2. Yerel web sunucusu bağlantı noktanıza yönlendiren bir tünel oluşturun:

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Cloudflare, WebSocket uç noktanıza erişmek ve TLS'yi otomatik olarak işlemek için bir alt alan adı
`acids-iceland-davidson-lb.trycloudflare.com`) sağlar. Daha sonra ihtiyaç duyacağınız için bu alt alan adını not edin.

## 3. adım: Dinamik erişim anahtarı oluşturun {#step_3_create_a_dynamic_access_key}

[Erişim anahtarı yapılandırması](../management/config) biçimini kullanarak kullanıcılarınız için istemci erişim anahtarını içeren bir YAML dosyası oluşturun ve sunucu tarafında önceden yapılandırılmış WebSocket uç noktalarını ekleyin:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Dinamik erişim anahtarlarını içeren YAML dosyasını oluşturduktan sonra bu dosyayı kullanıcılarınıza iletmeniz gerekir. Dosyayı statik bir web barındırma hizmetinde barındırabilir veya dinamik olarak oluşturabilirsiniz. [Dinamik erişim anahtarlarını](../management/dynamic-access-keys) kullanma hakkında daha fazla bilgi edinin.

## 4. adım: Outline istemcisine bağlanın {#step_4_connect_with_the_outline_client}

Resmi [Outline istemcisi](../../download-links) uygulamalarından birini kullanın (1.15.0+ sürümleri) ve yeni oluşturduğunuz dinamik erişim anahtarını sunucu girişi olarak ekleyin. Shadowsocks-over-Websocket yapılandırmasını kullanarak sunucunuza tünel oluşturmak için **Bağlan**'ı tıklayın.

Şu anda Outline sunucunuz üzerinden internette gezindiğinizi doğrulamak için [IPInfo](https://ipinfo.io) gibi bir araç kullanın.
