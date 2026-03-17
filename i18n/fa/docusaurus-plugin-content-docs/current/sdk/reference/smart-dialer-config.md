---
title: "پیکربندی شماره‌گیر هوشمند"
sidebar_label: "پیکربندی شماره‌گیر هوشمند"
---

**شماره‌گیر هوشمند** راهبردی را جستجو می‌کند که ساناد و «امنیت لایه انتقال» را برای
فهرست آزمایش دامنه‌های ارائه‌شده رفع انسداد می‌کند. از پیکربندی‌ای استفاده می‌کند که چندین راهبرد را شرح می‌دهد
تا از میان آن‌ها انتخاب شود.

## پیکربندی YAML برای «شماره‌گیر هوشمند» {#yaml_config_for_the_smart_dialer}

پیکربندی‌ای که «شماره‌گیر هوشمند» استفاده می‌کند در قالب YAML است. برای مثال:

```yaml
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1

fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

### پیکربندی ساناد {#dns_configuration}

- فیلد `dns` فهرستی از رافع‌های ساناد را برای آزمایش معین می‌کند.

- هر رافع ساناد می‌تواند یکی‌از انواع زیر باشد:

    - ‫`system`: استفاده کردن از رافع سیستم. با شیء خالی معین می‌شود.

    - ‫`https`: استفاده کردن از ساناد رمزگذاری‌شده روی رافع (DoH) اچ‌تی‌تی‌پی‌اس.

    - ‫`tls`: استفاده کردن از ساناد رمزگذاری‌شده روی رافع (DoT) «امنیت لایه انتقال».

    - ‫`udp`: استفاده کردن از رافع UDP.

    - ‫`tcp`: استفاده کردن از رافع TCP.

#### رافع DNS-over-HTTP (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- ‫`name`:نام دامنه سرور DoH.

- ‫`address`: میزبان:درگاه سرور DoH. پیش‌فرض‌ها به `name`‏:۴۴۳.

#### رافع DNS-over-TLS (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- ‫`name`: نام دامنه سرور DoT

- ‫`address`: میزبان:درگاه سرور DoT. پیش‌فرض‌ها به `name`‏:۸۵۳.

#### رافع UDP {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- ‫`address`: میزبان:درگاه رافع UDP.

#### رافع TCP {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- ‫`address`: میزبان:درگاه رافع TCP.

### پیکربندی «امنیت لایه انتقال» {#tls_configuration}

- فیلد `tls` فهرستی از رافع‌های «امنیت لایه انتقال» را برای آزمایش معین می‌کند.

- هر حمل‌ونقل «امنیت لایه انتقال» رشته‌ای است که حمل‌ونقل برای استفاده را معین می‌کند.

- برای نمونه، `override:host=cloudflare.net|tlsfrag:1` حمل‌ونقلی را معین می‌کند که
از دامنه‌ای استفاده می‌کند که خط مقدم آن تکه‌تکه‌سازی «امنیت لایه انتقال» و Cloudflare است. برای جزئیات بیشتر،
[مستندسازی پیکربندی](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Config_Format)
را ببینید.

### پیکربندی جایگزین {#fallback_configuration}

پیکربندی جایگزین وقتی استفاده می‌شود که هیچ‌یک از راهبردهای بدون پراکسی نتوانند
ارتباط را برقرار کنند. برای نمونه، می‌توان پراکسی سرور پشتیبان را معین کرد تا برای
اتصال کاربر عمل کند. شروع بااستفاده از جایگزین کندتر خواهد بود زیرا پیش‌از آن ابتدا
باید راهبردهای دیگر ساناد/ «امنیت لایه انتقال» عمل نکنند/ مهلت آن‌ها تمام شود.

رشته‌های جایگزین باید:

- رشته پیکربندی `StreamDialer` همان‌گونه که در [`configurl`](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Proxy_Protocols) تعریف شده است معتبر باشد.

- شیء پیکربندی Psiphon معتبری به‌عنوان فرزند فیلد `psiphon` باشد.

#### نمونه سرور Shadowsocks {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### نمونه سرور SOCKS5 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### نمونه پیکربندی Psiphon {#psiphon_config_example}

برای استفاده کردن از شبکه [Psiphon](https://psiphon.ca/)، شما باید:

1. با تیم Psiphon تماس بگیرید تا پیکربندی‌ای را دریافت کنید که به شما اجازه دسترسی به
شبکه می‌دهد. برای دریافت کردن این اجازه، ممکن است به قرارداد نیاز داشته باشید.

2. پیکربندی Psiphon را که دریافت کرده‌اید به بخش `fallback` در
پیکربندی «شماره‌گیر هوشمند» خودتان اضافه کنید. چون JSON با YAML سازگار است، می‌توانید پیکربندی Psiphon خودتان را مستقیماً در
بخش `fallback` کپی و جای‌گذاری کنید، مثل این:

```yaml
fallback:
  - psiphon: {
      "PropagationChannelId": "FFFFFFFFFFFFFFFF",
      "SponsorId": "FFFFFFFFFFFFFFFF",
      "DisableLocalSocksProxy" : true,
      "DisableLocalHTTPProxy" : true,
      ...
    }
```


:::note
پایگاه کد Psiphon تحت پروانه GPL است که می‌تواند روی کدهای شما محدودیت‌های پروانه‌دار اعمال کند. می‌توانید دریافت پروانه ویژه آن را درنظر بگیرید.
:::

### چگونگی استفاده کردن از «شماره‌گیر هوشمند» {#how_to_use_the_smart_dialer}

برای استفاده کردن از «شماره‌گیر هوشمند»، شیء `StrategyFinder` را بسازید و با
گذر از فهرست دامنه‌های آزمایشی و پیکربندی YAML، به‌روش `NewDialer` تماس بگیرید.
روش `NewDialer`‏ `transport.StreamDialer` را برمی‌گرداند که می‌تواند برای
ساختن اتصال‌هایی به‌کار رود که از راهبرد یافت‌شده استفاده می‌کنند. برای مثال:

```go
finder := &smart.StrategyFinder{
    TestTimeout:  5 * time.Second,
    LogWriter:   os.Stdout,
    StreamDialer: &transport.TCPDialer{},
    PacketDialer: &transport.UDPDialer{},
}

configBytes := []byte(`
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
`)

dialer, err := finder.NewDialer(
  context.Background(),
  []string{"www.google.com"},
  configBytes
)
if err != nil {
    // Handle error.
}

// Use dialer to create connections.
```

این مثالی ساده است و ممکن است برای استفاده کردن برای مورد ویژه شما لازم باشد آن را سازگار کنید.
