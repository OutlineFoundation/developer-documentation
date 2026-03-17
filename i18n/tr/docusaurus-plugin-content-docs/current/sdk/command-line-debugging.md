---
title: "Outline SDK ile Ağ Müdahalelerini Uzaktan Karakterize Etme ve Atlatma"
sidebar_label: "Outline SDK ile Ağ Müdahalelerini Uzaktan Karakterize Etme ve Atlatma"
---

Bu kılavuzda, Outline SDK'nın komut satırı araçlarını kullanarak ağdaki uzaktan müdahaleleri nasıl anlayıp engelleyeceğiniz gösterilmektedir. Ağ müdahalesini ölçmek, atlatma stratejilerini test etmek ve sonuçları analiz etmek için SDK'nın araçlarını nasıl kullanacağınızı öğreneceksiniz. Bu rehberde `resolve`, `fetch` ve `http2transport` araçlarına odaklanılacaktır.

## Outline SDK Araçlarını Kullanmaya Başlama

Outline SDK araçlarını doğrudan komut satırından kullanmaya başlayabilirsiniz.

### DNS'yi çözme

`resolve` aracı, belirtilen bir çözümleyiciyle DNS aramaları yapmanıza olanak tanır.

Bir alanın A kaydını çözmek için:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

CNAME kaydını çözmek için:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### Web sayfası getirme

`fetch` aracı, bir web sayfasının içeriğini almak için kullanılabilir.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

Ayrıca bağlantının QUIC kullanmasını da zorlayabilir.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### Yerel proxy kullanma

`http2transport` aracı, trafiğinizi yönlendirmek için yerel bir proxy oluşturur.
Shadowsocks aktarımıyla yerel proxy başlatmak için:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

Ardından, bu proxy'yi curl gibi diğer araçlarla kullanabilirsiniz:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## Hileli Atlatma Stratejilerini Belirtme

Outline SDK, farklı ağ müdahale biçimlerini atlamak için birleştirilebilen çeşitli atlatma stratejilerinin belirtilmesine olanak tanır. Bu stratejilerin
özellikleri [Go dokümanlarında](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl) yer alır.

### Bileşenlere Ayrılabilir Stratejiler

Bu stratejiler, daha güçlü atlatma teknikleri oluşturmak için birleştirilebilir.

* **TLS parçalama ile DNS-over-HTTPS**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5-over-TLS with Domain Fronting**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Shadowsocks ile Çoklu Atlama Yönlendirme**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## Uzaktan erişim ve ölçüm

Farklı bölgelerde yaşanan ağ parazitini ölçmek için uzak proxy'leri kullanabilirsiniz. Bağlanmak için uzaktan proxy'ler bulabilir veya oluşturabilirsiniz.

### Uzaktan Erişim Seçenekleri

`fetch` aracını kullanarak bağlantıları uzaktan çeşitli şekillerde test edebilirsiniz.

#### Outline Sunucusu

Shadowsocks aktarımıyla standart bir Outline sunucusuna uzaktan bağlanın.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SSH üzerinden SOCKS5

SSH tüneli kullanarak SOCKS5 proxy'si oluşturun.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

Fetch kullanarak bu tünele bağlanma

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## Örnek olay: İran'da YouTube engellemesini atlama

Ağ parazitini tespit etme ve atlama ile ilgili pratik bir örneği aşağıda bulabilirsiniz.

### Bloğu Algılama

YouTube ana sayfası İranlı bir proxy üzerinden getirilmeye çalışıldığında istek zaman aşımına uğruyor. Bu durum, engelleme olduğunu gösteriyor.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

Bu komut, zaman aşımı nedeniyle başarısız olur.

### TLS parçalama ile atlama

Taşımaya TLS parçalama ekleyerek bu engeli atlayabiliriz.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Bu komut, YouTube ana sayfasının başlığını başarıyla alır. Başlık, `<title>YouTube</title>` şeklindedir.

### TLS parçalama ve DNS-over-HTTPS ile atlama

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Bu işlem de `<title>YouTube</title>` değerini başarıyla döndürür.

### Outline sunucusuyla atlama

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Bu da `<title>YouTube</title>` değerini döndürür.

## Daha Fazla Analiz ve Kaynak

Tartışmalar ve sorular için [Outline SDK Tartışma Grubu](https://github.com/OutlineFoundation/outline-sdk/discussions)'nu ziyaret edin.
