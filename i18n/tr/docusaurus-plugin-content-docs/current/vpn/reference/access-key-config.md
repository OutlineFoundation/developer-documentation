---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## Tüneller (Tunnel)

### TunnelConfig

Tünel, bir Outline yapılandırmasındaki en üst düzey nesnedir. VPN'in nasıl yapılandırılması gerektiğini belirtir.

**Biçim:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**Biçim:** *struct*

**Alanlar:**

- `transport` ([TransportConfig](#transportconfig)): hedef varış noktasıyla paket alışverişi yapmak için kullanılacak araç

- `error` (*struct*): hizmet hatası durumunda kullanıcıya iletilecek bilgiler (ör. anahtarın süresi doldu, kota tükendi)

    - `message` (*string*): kullanıcıya gösterilecek açıklayıcı mesaj

    - `details` (*string*): hata ayrıntılarını açtığında kullanıcıya gösterilecek mesaj (Sorun giderme açısından yararlıdır.)

`error` ve `transport` alanları aynı anda olamaz.

Başarılı örnek:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Hatalı örnek:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Araçlar (Transport)

### TransportConfig

Paketlerin hedef varış noktasıyla nasıl değiştirilmesi gerektiğini belirtir.

**Biçim:** [Interface](#interface)

Desteklenen Interface türleri:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

TCPUDPConfig, ayrı TCP ve UDP stratejilerinin ayarlanmasına izin verir.

**Biçim:** *struct*

**Alanlar:**

- `tcp` ([DialerConfig](#dialerconfig)): TCP bağlantıları için kullanılacak akış çevirici

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): UDP paketleri için kullanılacak paket işleyici

Farklı uç noktalara TCP ve UDP gönderme örneği:

```yaml
tcp:
  $type: shadowsocks
  endpoint: ss.example.com:80
  <<: &cipher
    cipher: chacha20-ietf-poly1305
    secret: SECRET
  prefix: "POST "

udp:
  $type: shadowsocks
  endpoint: ss.example.com:53
  <<: *cipher
```

## Uç noktalar (Endpoint)

Uç noktalar, sabit bir uç nokta ile bağlantı kurar. Uç noktaya özgü optimizasyonlara izin verdiği için çeviricilerden daha çok tercih edilir. Akış ve paket uç noktaları vardır.

### EndpointConfig

**Biçim:** *string* | [Interface](#interface)

*string* uç noktası, seçilen uç noktanın ana makine:bağlantı noktası adresidir. Bağlantı, varsayılan çevirici kullanılarak kurulur.

Akış ve paket uç noktaları için desteklenen Interface türleri:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

Sabit bir adresi çevirerek bağlantı kurar. Çevirici kullanarak stratejilerin birleştirilmesine imkan tanıyabilir.

**Biçim:** *struct*

**Alanlar:**

- `address` (*string*): çevrilecek uç nokta adresi

- `dialer` ([DialerConfig](#dialerconfig)): adresi çevirmek için kullanılacak çevirici

### WebsocketEndpointConfig

Akış ve paket bağlantıları ile bir uç nokta arasında Websockets üzerinden tünel açar.

Akış bağlantıları için her yazma işlemi bir Websocket mesajına dönüştürülür. Paket bağlantıları için her paket bir Websocket mesajına dönüştürülür.

**Biçim:** *struct*

**Alanlar:**

- `url` (*string*): Websocket uç noktasının URL'si. Şema, TLS kullanılan Websocket bağlantıları için `https` veya `wss`, şifrelenmemiş Websocket bağlantıları için `http` ya da `ws` şeklinde olmalıdır. 

- `endpoint` ([EndpointConfig](#endpointconfig)): Bağlanılacak web sunucusu uç noktası. Bu alan yoksa URL'de belirtilen adrese bağlanır.

## Çeviriciler

Çeviriciler, belirli bir uç nokta adresiyle bağlantı kurar. Akış ve paket çeviricileri kullanılır.

### DialerConfig

**Biçim:** *null* | [Interface](#interface)

*null* (boş) çeviricisi, akış için doğrudan TCP bağlantılarını ve paketler için doğrudan UDP bağlantılarını kullanan varsayılan çevirici anlamına gelir.

Akış ve paket çeviricileri için desteklenen Interface türleri:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Paket işleyiciler (PacketListener)

Paket işleyiciler, birden fazla hedefe paket göndermek için kullanılabilecek sınırsız bir paket bağlantısı kurar.

### PacketListenerConfig

**Biçim:** *null* | [Interface](#interface)

*null* (boş) paket işleyicisi, bir UDP paket işleyici olan varsayılan paket işleyici anlamına gelir.

Desteklenen Interface türleri:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Stratejiler

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig, araç olarak Shadowsocks kullanan bir tüneli temsil eder. Geriye dönük uyumluluk için eski biçimi uygular.

**Biçim:** *struct*

**Alanlar:**

- `server` (*string*): bağlanılacak ana makine

- `server_port` (*number*): bağlanılacak bağlantı noktası numarası

- `method` (*string*): kullanılacak [AEAD şifresi](https://shadowsocks.org/doc/aead.html#aead-ciphers)

- `password` (*string*): Şifreleme anahtarı oluşturmak için kullanılır.

- `prefix` (*string*): kullanılacak [önek gizleme yöntemi](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/).
Akış ve paket bağlantılarında desteklenir.

Örnek:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

LegacyShadowsocksURI, araç olarak Shadowsocks kullanan bir tüneli temsil eder.
Geriye dönük uyumluluk için eski URL biçimini uygular.

**Biçim:** *string*

[LegacyShadowsocksURI biçimini](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) ve [SIP002 URI şemasını](https://shadowsocks.org/doc/sip002.html) inceleyin. Eklentiler desteklenmez.

Örnek:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

ShadowsocksConfig, akış veya paket çeviricilerinin yanı sıra Shadowsocks kullanan bir paket işleyici de temsil edebilir.

**Biçim:** *struct*

**Alanlar:**

- `endpoint` ([EndpointConfig](#endpointconfig)): bağlanılacak Shadowsocks uç noktası

- `cipher` (*string*): kullanılacak [AEAD şifresi](https://shadowsocks.org/doc/aead.html#aead-ciphers)

- `secret` (*string*): Şifreleme anahtarı oluşturmak için kullanılır.

- `prefix` (*string*, isteğe bağlı): kullanılacak [önek gizleme yöntemi](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/).
Akış ve paket bağlantılarında desteklenir.

Örnek:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Meta tanımlar

### FirstSupportedConfig

Uygulama tarafından desteklenen ilk yapılandırmayı kullanır. Bu yöntem, eski yapılandırmalarla geriye dönük uyumludur ve yeni yapılandırmaları dahil eder.

**Biçim:** *struct*

**Alanlar:**

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)): dikkate alınacak seçenekler listesi

Örnek:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface

Arayüzler birden fazla uygulamadan birinin seçilmesine izin verir. Yapılandırmanın temsil ettiği türü belirtmek için `$type` alanını kullanır.

Örnek:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
