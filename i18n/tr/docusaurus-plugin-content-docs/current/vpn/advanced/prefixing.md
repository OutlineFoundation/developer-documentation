---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

Outline istemcisinin 1.9.0 sürümü itibarıyla erişim anahtarlarında "önek" seçeneği desteklenmektedir. "Önek", Shadowsocks TCP bağlantısındaki [takviye değerin](https://shadowsocks.org/guide/aead.html) ilk baytları olarak kullanılan baytların listesidir.
Bu seçenek, bağlantının ağda desteklenen bir protokol gibi görünmesini sağlayarak, tanımadığı protokolleri reddeden güvenlik duvarlarını atlatır.

## Bu seçeneği ne zaman denemeliyim?

Outline dağıtımınızdaki kullanıcıların hâlâ engellendiğinden şüpheleniyorsanız birkaç farklı öneki deneyebilirsiniz.

## Talimatlar

Önek 16 bayttan uzun olamaz. Daha uzun önekler, takviye değer çakışmasına neden olabilir. Bu durum, şifreleme güvenliğini tehlikeye atıp bağlantıların tespit edilmesine yol açabilir. Karşılaştığınız engelleri aşmak için olabilecek en kısa öneki kullanın.

Kullandığınız bağlantı noktası, önekinizin taklit ettiği protokolle eşleşmelidir.
IANA, protokollerle bağlantı noktası numaralarını eşleyen bir [taşıma protokolü-bağlantı noktası numarası listesi](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) sunar.

Bazı etkili önekler, sık kullanılan protokollere benzer:

Önerilen bağlantı noktası
JSON biçiminde kodlanmış
URL biçiminde kodlanmış

HTTP isteği
80 (http)
`"POST "`
`POST%20`

HTTP yanıtı
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

TCP üzerinden DNS isteği
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

TLS uygulama verileri
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

TLS ServerHello
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh), 830 (netconf-ssh), 4334 (netconf-ch-ssh), 5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### Dinamik erişim anahtarları

[Dinamik erişim anahtarları](../management/dynamic-access-keys) (`ssconf://`) ile önek özelliğini kullanmak için JSON nesnesine "önek" anahtarı ekleyin ve istediğiniz öneki temsil eden değeri **JSON biçiminde** belirtin (Örnekleri yukarıdaki tabloda bulabilirsiniz). `U+0` - `U+FF` aralığındaki yazdırılamayan Unicode karakterlerini temsil edecek çıkış kodları (ör. \u00FF) kullanabilirsiniz. Örneğin:

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### Statik erişim anahtarları

**Statik erişim anahtarları** (ss://) ile önekleri kullanmak için mevcut anahtarınızı dağıtmadan önce değiştirmeniz gerekir. Outline Manager'ın oluşturduğu bir statik erişim anahtarınız varsa önekinizin **URL biçiminde kodlanmış** sürümünü alın (Yukarıdaki tabloda örneklerini görebilirsiniz.) ve aşağıdaki şekilde erişim anahtarınızın sonuna ekleyin:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Kodlama bilginiz ileri seviyedeyse tarayıcınızın `encodeURIComponent()` fonksiyonunu kullanarak **JSON biçiminde kodlanmış** önekinizi **URL biçiminde kodlanmış** öneke dönüştürebilirsiniz. Bunu yapmak için web denetleme konsolunuzu açın (Chrome'da "Geliştirici > JavaScript Web Konsolu") ve aşağıdaki kodu yazın:

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Enter tuşuna basın. Üretilen değer, "URL biçiminde kodlanmış" sürümdür. Örneğin:

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
