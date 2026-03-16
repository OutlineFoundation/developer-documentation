---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline SDK’nın temelinde, birleştirmeye ve kolay yeniden kullanıma olanak sağlayan, birlikte çalışabilir arayüzler şeklinde tanımlanan bazı temel kavramlar yer alır.

## Bağlantılar {#connections}

Bağlantılar, soyut bir araç üzerinden iki uç nokta arasında iletişimi sağlar. İki tür bağlantı bulunur:

- `transport.StreamConn`: TCP ve `SOCK_STREAM` Posix yuvası türü gibi akış temelli bağlantı.

- `transport.PacketConn`: UDP ve `SOCK_DGRAM` Posix yuvası türü gibi veri birimi temelli bağlantı.
Go'nun standart kitaplığında kural bu şekilde olduğundan, "veri birimi" yerine "paket" terimini kullanıyoruz.

Bağlantılar, yeni bir araç üzerinden iç içe bağlantılar oluşturmak için sarmalanabilir.
Örneğin `StreamConn` TCP, TCP üzerinden TLS, TCP üzerinden TLS üzerinden HTTP, QUIC vb. bağlantısını kullanabilir.

## Çeviriciler {#dialers}

Çeviriciler, temel aktarım veya proxy protokolünü kapsüllemeyi sağlarken, bir ana makine:bağlantı noktası adresi verilen bağlantıların oluşturulmasını sağlar.
`StreamDialer` ve `PacketDialer` türleri, belirli bir adreste sırasıyla `StreamConn` ve `PacketConn` bağlantıları oluşturur. Çeviriciler iç içe de yerleştirilebilir.
Örneğin bir TLS akış çevirici, TCP çevirici kullanarak TCP bağlantısıyla desteklenen bir `StreamConn` oluşturabilir. Daha sonra, TCP `StreamConn` ile desteklenen bir TLS `StreamConn` oluşturabilir. SOCKS5-over-TLS çevirici, TLS çevirici kullanarak proxy'ye TLS `StreamConn` oluşturabilir ve daha sonra hedef adrese SOCKS5 bağlantısını kurar.

## Çözümleyiciler {#resolvers}

Çözümleyiciler (`dns.Resolver`), temel algoritmayı veya protokolü kapsüllerken DNS sorularının yanıtlanmasını etkinleştirir.
Çözümleyiciler, çoğunlukla alan adlarının IP adresleriyle eşlenmesi için kullanılır.
