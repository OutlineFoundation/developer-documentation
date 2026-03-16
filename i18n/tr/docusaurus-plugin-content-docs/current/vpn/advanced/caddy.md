---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

Bu rehberde, güçlü ve kullanıcı dostu [Caddy](https://caddyserver.com/) web sunucusunu kullanarak Outline sunucu kurulumunuzu nasıl optimize edeceğiniz gösterilmektedir. [Otomatik HTTPS](https://caddyserver.com/docs/automatic-https) özellikleri ve esnek yapılandırması sayesinde Caddy, özellikle WebSocket taşıyıcısı kullanılırken Outline sunucunuzu desteklemek için ideal bir seçenektir.

## Caddy nedir? {#what_is_caddy}

Caddy; kullanım kolaylığı, otomatik HTTPS ve çeşitli protokolleri desteklemesiyle bilinen açık kaynaklı bir web sunucusudur. Web sunucusu yapılandırmasını basitleştirir ve şu gibi özelliklere sahiptir:

- **Otomatik HTTPS:** Caddy, TLS sertifikalarını otomatik olarak alıp yenileyerek güvenli bağlantılar sağlar.

- **HTTP/3 desteği:** Caddy, daha hızlı ve daha verimli web trafiği için en yeni HTTP/3 protokolünü destekler.

- **Eklentilerle genişletilebilirlik:** Caddy, ters proxy ve yük dengeleme gibi çeşitli işlevleri desteklemek için eklentilerle genişletilebilir.

## 1. adım: Ön koşullar {#step_1_prerequisites}

- [`xcaddy`](https://github.com/caddyserver/xcaddy)'yi indirip yükleyin.

## 2. adım: Alan adınızı yapılandırın {#step_2_configure_your_domain}

Caddy'yi başlatmadan önce alan adınızın, sunucunuzun IP adresini gösterecek şekilde doğru yapılandırıldığından emin olun.

- **A/AAAA kayıtlarını ayarlayın:** DNS sağlayıcınızda oturum açın ve alan adınızın A ile AAAA kayıtlarını sırasıyla sunucunuzun IPv4 ve IPv6 adreslerini gösterecek şekilde ayarlayın.

- **DNS kayıtlarını doğrulayın:** Yetkili bir aramayla DNS kayıtlarınızın doğru ayarlandığını onaylayın:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## 3. adım: Özel Caddy derlemesi oluşturup çalıştırın {#build-and-run}

`xcaddy` kullanarak, Outline temel sunucu modülünü ve diğer gerekli sunucu uzantısı modüllerini içeren özel bir `caddy` ikili programı oluşturabilirsiniz.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## 4. adım: Outline ile Caddy sunucusunu yapılandırıp çalıştırın {#step_4_configure_and_run_the_caddy_server_with_outline}

Aşağıdaki yapılandırmayı kullanarak yeni bir `config.yaml` dosyası oluşturun:

```yaml
apps:
  http:
    servers:
      server1:
        listen:
          - ":443"
        routes:
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<TCP_PATH>
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<UDP_PATH>
            handle:
              - handler: websocket2layer4
                type: packet
                connection_handler: ss1
  outline:
    shadowsocks:
      replay_history: 10000
    connection_handlers:
      - name: ss1
        handle:
          handler: shadowsocks
          keys:
            - id: user-1
              cipher: chacha20-ietf-poly1305
              secret: <SHADOWSOCKS_SECRET>
```

Bu yapılandırma, bir web sunucusunun `443` bağlantı noktasını dinleyip sırasıyla `TCP_PATH` ve `UDP_PATH` yollarındaki TCP ve UDP ile sarmalanmış Shadowsocks trafiğini kabul ettiği bir "Shadowsocks-over-WebSockets" stratejisidir.

Oluşturulan yapılandırma kullanılarak Outline ile genişletilmiş Caddy sunucusunu çalıştırın:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

[outline-ss-server/outlinecaddy GitHub depomuzda](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples) daha fazla sayıda örnek yapılandırma bulabilirsiniz.

## 5. adım: Dinamik erişim anahtarı oluşturun {#step_5_create_a_dynamic_access_key}

[Gelişmiş yapılandırma](../management/config) biçimini kullanarak kullanıcılarınız için istemci erişim anahtarlarını içeren bir YAML dosyası oluşturun ve sunucu tarafında önceden yapılandırılmış WebSocket uç noktalarını ekleyin:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Dinamik erişim anahtarlarını içeren YAML dosyasını oluşturduktan sonra bu dosyayı kullanıcılarınıza iletmeniz gerekir. Dosyayı statik bir web barındırma hizmetinde barındırabilir veya dinamik olarak oluşturabilirsiniz. [Dinamik erişim anahtarlarını](../management/dynamic-access-keys) kullanma hakkında daha fazla bilgi edinin.

## 6. adım: Outline istemcisine bağlanın {#step_6_connect_with_the_outline_client}

Resmi [Outline istemcisi](../../download-links) uygulamalarından birini kullanın (1.15.0 ve sonraki sürümler) ve yeni oluşturduğunuz dinamik erişim anahtarını sunucu girişi olarak ekleyin. "Shadowsocks-over-Websocket" yapılandırmasını kullanarak sunucunuza tünel oluşturmak için **Bağlan**'ı tıklayın.

İnternette Outline sunucunuz üzerinden gezinmekte olduğunuzu doğrulamak için [IPInfo](https://ipinfo.io) gibi bir araç kullanın.
