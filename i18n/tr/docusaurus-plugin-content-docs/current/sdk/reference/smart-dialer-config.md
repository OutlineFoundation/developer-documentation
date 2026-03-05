---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

**Smart Dialer** belirli bir test alan adı listesi için DNS ve TLS engellemesini kaldıran bir strateji arar. Aralarından seçim yapılacak birden fazla stratejiyi tanımlayan bir yapılandırma seçer.

## Smart Dialer için YAML yapılandırması

Smart Dialer'ın aldığı yapılandırma YAML biçimindedir. Örnek:

### DNS Yapılandırması

- `dns` alanı, test edilecek DNS çözümleyicilerin listesini belirtir.

- Her bir DNS çözümleyicinin türü şunlardan biri olabilir:

    - `system`: Sistemdeki çözümleyiciyi kullanın. Boş bir nesne ile belirtin.

    - `https`: Şifrelenmiş bir DNS over HTTPS (DoH) çözümleyici kullanın.

    - `tls`: Şifrelenmiş bir DNS over TLS (DoT) çözümleyici kullanın.

    - `udp`: UDP çözümleyici kullanın.

    - `tcp`: TCP çözümleyici kullanın.

#### DNS-over-HTTPS (DoH) Çözümleyici

- `name`: DoH sunucusunun alan adı.

- `address`: DoH sunucusunun ana makine:bağlantı noktası bilgisi. Varsayılan değer `name`:443'tür.

#### DNS-over-TLS (DoT) Çözümleyici

- `name`: DoT sunucusunun alan adı.

- `address`: DoT sunucusunun ana makine:bağlantı noktası bilgisi. Varsayılan değer `name`:853'tür.

#### UDP Çözümleyici

- `address`: UDP çözümleyicinin ana makine:bağlantı noktası bilgisi.

#### TCP Çözümleyici

- `address`: TCP çözümleyicinin ana makine:bağlantı noktası bilgisi.

### TLS Yapılandırması

- `tls` alanı, test edilecek TLS araçlarının listesini belirtir.

- Her bir TLS aracı, kullanılacak aracı belirten bir dizedir.

- Örneğin `override:host=cloudflare.net|tlsfrag:1`, Cloudflare ve TLS parçasıyla alan adı ön yüzünü değiştirme işlemini kullanan bir araç belirtir. Ayrıntılar için [yapılandırma belgelerine](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format) bakın.

### Yedek Yapılandırma

Yedek yapılandırma, proxy'siz stratejilerin hiçbiri bağlantı kuramadığında kullanılır. Örneğin, kullanıcının bağlantısını denemek için bir yedek proxy sunucusu belirtebilir. Önce diğer DNS/TLS stratejilerinin başarısız olması/zaman aşımına uğraması gerektiğinden, yedek yapılandırma kullanımının başlatılması yavaş olur.

Yedek dizeler şu özellikleri taşımalıdır:

- [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols) içinde tanımlandığı gibi geçerli bir `StreamDialer` yapılandırması

- `psiphon` alanının bir alt öğesi olarak geçerli bir Psiphon yapılandırması

#### Shadowsocks sunucusu ile ilgili örnek

#### SOCKS5 sunucusu ile ilgili örnek

#### Psiphon yapılandırması ile ilgili örnek

[Psiphon](https://psiphon.ca/) ağını kullanmak için:

1. Psiphon ekibi ile iletişime geçerek ağlarına erişim sağlayan bir yapılandırma alın. Bunun için bir sözleşmenizin olması gerekebilir.

2. Aldığınız Psiphon yapılandırmasını, Smart Dialer yapılandırmanızın `fallback` bölümüne ekleyin. JSON YAML ile uyumlu olduğundan, Psiphon yapılandırmanızı `fallback` bölümüne şu şekilde doğrudan yapıştırabilirsiniz:

### Smart Dialer'ı Kullanma

Smart Dialer'ı kullanmak için bir `StrategyFinder` nesnesi oluşturun ve `NewDialer` yöntemini çağırın. Bunun için test alan adları listesini ve YAML yapılandırmasını sağlamanız gerekir.
`NewDialer` yöntemi bir `transport.StreamDialer` değeri döndürür. Bu değer, bulunan stratejiyle bağlantı oluşturmak için kullanılabilir. Örneğin:

Bu basit bir örnek olup kendi kullanım alanınıza göre uyarlanması gerekebilir.
