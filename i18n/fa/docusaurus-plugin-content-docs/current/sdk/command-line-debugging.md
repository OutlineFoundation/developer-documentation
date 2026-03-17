---
title: "شناسایی از راه دور و دور زدن تداخل شبکه با Outline SDK"
sidebar_label: "شناسایی از راه دور و دور زدن تداخل شبکه با Outline SDK"
---

این راهنما نحوه استفاده از ابزارهای خط فرمان Outline SDK را برای درک و دور زدن تداخل شبکه از دیدگاه راه دور نشان می‌دهد. شما یاد خواهید گرفت که چگونه از ابزارهای SDK برای اندازه گیری تداخل شبکه، تست استراتژی های دور زدن و تجزیه و تحلیل نتایج استفاده کنید. این راهنما بر روی ابزارهای `resolve` ، `fetch` و `http2transport` تمرکز خواهد کرد.

##  شروع به کار با ابزار Outline SDK

 می توانید مستقیماً از خط فرمان استفاده از ابزار Outline SDK را شروع کنید.

###  DNS را حل کنید

 ابزار `resolve` به شما امکان می دهد جستجوهای DNS را با یک حل کننده مشخص انجام دهید.

 برای حل کردن رکورد A دامنه:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

 برای حل یک رکورد CNAME:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

###  واکشی یک صفحه وب

 ابزار `fetch` می تواند برای بازیابی محتوای یک صفحه وب استفاده شود.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

 همچنین می تواند اتصال را مجبور به استفاده از QUIC کند.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

###  از یک پروکسی محلی استفاده کنید

 ابزار `http2transport` یک پروکسی محلی برای هدایت ترافیک شما ایجاد می کند. برای شروع یک پروکسی محلی با انتقال Shadowsocks:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

 سپس می توانید از این پروکسی با ابزارهای دیگری مانند curl استفاده کنید:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

##  استراتژی های دور زدن را مشخص کنید

 Outline SDK اجازه می دهد تا استراتژی های دور زدن مختلفی را مشخص کند که می توانند برای دور زدن اشکال مختلف تداخل شبکه با هم ترکیب شوند. مشخصات این استراتژی ها در [مستندات پیش رو](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl) آمده است.

###  استراتژی های قابل ترکیب

 این استراتژی ها را می توان برای ایجاد تکنیک های دور زدن قوی تر ترکیب کرد.
*  **DNS-over-HTTPS با TLS Fragmentation** : `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`
*  **SOCKS5-over-TLS با دامنه دامنه** : `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`
*  **مسیریابی چند هاپ با Shadowsocks** : `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

##  دسترسی از راه دور و اندازه گیری
 برای اندازه گیری تداخل شبکه همانطور که در مناطق مختلف تجربه می شود، می توانید از پراکسی های راه دور استفاده کنید. می توانید پراکسی های راه دور را برای اتصال پیدا کنید یا ایجاد کنید.

###  گزینه های دسترسی از راه دور

 با استفاده از ابزار `fetch` می توانید اتصالات را از راه دور به روش های مختلف آزمایش کنید.

####  سرور طرح کلی

 از راه دور به یک سرور Outline استاندارد با انتقال Shadowsocks متصل شوید.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

####  SOCKS5 بیش از SSH

 با استفاده از یک تونل SSH یک پروکسی SOCKS5 ایجاد کنید.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

 با استفاده از fetch به آن تونل وصل شوید

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

##  مطالعه موردی: دور زدن مسدودسازی یوتیوب در ایران

 در اینجا یک مثال عملی از شناسایی و دور زدن تداخل شبکه آورده شده است.

###  بلوک را شناسایی کنید

 هنگام تلاش برای واکشی صفحه اصلی YouTube از طریق یک پروکسی ایرانی، زمان درخواست به پایان می رسد و نشان دهنده یک بلوک است. 

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

این دستور با مهلت زمانی ناموفق است.

###  دور زدن با TLS Fragmentation

 با افزودن تکه تکه شدن TLS به انتقال، می توانیم این بلوک را دور بزنیم. 

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

این دستور با موفقیت عنوان صفحه اصلی YouTube را که `<title>YouTube</title>` است بازیابی می کند. 

###  دور زدن با TLS Fragmentation و DNS-over-HTTPS 

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

این نیز با موفقیت `<title>YouTube</title>` را برمی گرداند.

###  دور زدن با سرور Outline 

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

این نیز `<title>YouTube</title>` را برمی گرداند.

##  تجزیه و تحلیل بیشتر و منابع

 برای بحث و پرسش، از [گروه گفتگوی Outline SDK](https://github.com/OutlineFoundation/outline-sdk/discussions) بازدید کنید.
