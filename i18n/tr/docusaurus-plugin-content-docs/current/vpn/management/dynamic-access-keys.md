---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

Outline'da iki tür erişim anahtarı vardır: statik ve dinamik. Statik anahtarlar, tüm bağlantı bilgilerini anahtarın içinde kodlar. Dinamik anahtarlar ise bağlantı bilgilerinin konumunu kodlayarak bu bilgileri uzakta depolamanıza ve gerektiğinde değiştirmenize olanak tanır. Bu sayede, kullanıcılarınıza yeni anahtarlar oluşturmak ve dağıtmak zorunda kalmadan sunucu yapılandırmanızı güncelleyebilirsiniz. Bu belgede, Outline sunucunuzun daha esnek ve verimli yönetimi için dinamik erişim anahtarlarının nasıl kullanılacağı açıklanmaktadır.

Dinamik erişim anahtarlarınız tarafından kullanılacak erişim bilgilerini belirten üç biçim vardır:

### `ss://` bağlantısı kullanma

*Outline istemcisi (1.8.1 ve sonraki sürümler)*

Doğrudan mevcut `ss://` bağlantısını kullanabilirsiniz. Sunucuyu, bağlantı noktasını veya şifreleme yöntemini sık sık değiştirmeniz gerekmiyorsa ancak yine de sunucu adresini güncelleme esnekliğine sahip olmak istiyorsanız bu yöntem idealdir.

**Örnek:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### JSON nesnesi kullanma

*Outline istemcisi (1.8.0 ve sonraki sürümler)*

Bu yöntem, kullanıcılarınızın Outline bağlantısını tam olarak yönetmek için daha fazla esneklik sunar. Sunucu, bağlantı noktası, şifre ve şifreleme yöntemini bu şekilde güncelleyebilirsiniz.

**Örnek:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server:** VPN sunucunuzun alanı veya IP adresi.

- **server_port:** VPN sunucunuzun çalıştığı bağlantı noktası numarası.

- **password:** VPN'e bağlanmak için gereken şifre.

- **method:** VPN tarafından kullanılan şifreleme yöntemi. Desteklenen Shadowsocks [AEAD şifrelerine](https://shadowsocks.org/doc/aead.html) bakın.

### YAML nesnesi kullanma

*Outline istemcisi (1.15.0 ve sonraki sürümler)*

Bu yöntem, önceki JSON yöntemine benzer ancak Outline'ın gelişmiş yapılandırma biçiminden yararlanarak daha da fazla esneklik sağlar. Sunucu, bağlantı noktası, şifre, şifreleme yöntemi ve çok daha fazlasını güncelleyebilirsiniz.

**Örnek:**

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
  udp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
```

- **transport:** Kullanılacak araç protokollerini (bu durumda TCP ve UDP) tanımlar.

- **tcp/udp:** Her protokol için yapılandırmayı belirtir.

    - **$type:** Yapılandırma türünü belirtir. Burada Shadowsocks'tur.

    - **endpoint:** VPN sunucunuzun alan adı veya IP adresi ve bağlantı noktası.

    - **secret:** VPN'e bağlanmak için gereken şifre.

    - **cipher:** VPN tarafından kullanılan şifreleme yöntemi. Desteklenen Shadowsocks [AEAD şifrelerine](https://shadowsocks.org/doc/aead.html) bakın.

Araçlar, uç noktalar, çeviriciler ve paket işleyiciler de dahil olmak üzere Outline sunucunuza erişimi yapılandırabileceğiniz tüm yöntemler hakkında ayrıntılı bilgi için [Erişim Anahtarı Yapılandırması](config) bölümüne göz atın.

## Statik anahtardan erişim bilgilerini ayıklama

Mevcut bir statik erişim anahtarınız varsa JSON veya YAML tabanlı bir dinamik erişim anahtarı oluşturmak için bilgileri ayıklayabilirsiniz. Aşağıda statik erişim anahtarına bir örnek verilmiştir.

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Örnek:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Sunucu:** `outline-server.example.com`

- **Sunucu bağlantı noktası:** `8388`

- **Kullanıcı bilgisi:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` [Google Yönetici Araç Kutusu Kodlama/Kod Çözme](https://toolbox.googleapps.com/apps/encode_decode/) gibi bir araç kullanılarak [base64](https://en.wikipedia.org/wiki/Base64) şeklinde kodu çözülür.

    - **Yöntem**: `chacha20-ietf-poly1305`

    - **Şifre**: `example`

## Barındırma platformu seçme

Dinamik erişim anahtarı oluşturmayı öğrendiğinize göre erişim anahtarı yapılandırmanız için uygun bir barındırma platformu seçmelisiniz. Bu kararı verirken platformun güvenilirliği, güvenliği, kullanım kolaylığı ve sansüre dayanıklılığı gibi etmenleri göz önünde bulundurun. Platform, erişim anahtarı bilgilerinizi kesinti olmadan sürekli olarak yayınlayacak mı? Yapılandırmanızı koruyacak uygun güvenlik önlemlerine sahip mi? Platformda erişim anahtarı bilgilerinizi yönetmek ne kadar kolay? İnternet sansürü olan bölgelerden platforma erişilebilir mi?

Bilgiye erişimin kısıtlanabileceği durumlar için [Google Drive](https://drive.google.com), [pad.riseup.net](https://pad.riseup.net/), [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) (path-style erişimi olan), [Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) veya [GitHub gizli gist'leri](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists) gibi sansüre dayanıklı platformlarda barındırma yapabilirsiniz.
Dağıtımınıza özel ihtiyaçları değerlendirin ve erişilebilirlik ile güvenlik gerekliliklerinize uygun bir platform seçin.
