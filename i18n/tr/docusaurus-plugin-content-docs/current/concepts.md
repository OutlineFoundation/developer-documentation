---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline, kullanıcıların açık internete erişmelerinin önündeki kısıtlamaları aşmalarına yardımcı olur. Outline'ın işleyiş şeklini gösteren bazı temel konseptleri aşağıda bulabilirsiniz:

## Servis sağlayıcılar ve son kullanıcılar {#service_providers_and_end_users}

Outline sisteminde iki ana rol vardır: sunucuları yöneten **servis sağlayıcılar** ve bu sunucular üzerinden internete erişen **son kullanıcılar**.

- **Servis sağlayıcılar**; Outline sunucularını oluşturur, **erişim anahtarlarını** üretir ve son kullanıcılara **anahtarları dağıtır**. Bunu yapmak için **Outline Manager** uygulamasını kullanabilirler.

- **Son kullanıcılar**; **Outline istemcisi** uygulamasını yükler, aldıkları **erişim anahtarını** yapıştırır ve güvenli bir tünele **bağlanır**.

## Erişim anahtarları {#access-keys}

Erişim anahtarları, kullanıcıların Outline sunucusuna bağlanmasına olanak tanıyan kimlik bilgileridir. Outline istemcisinin güvenli bağlantı kurması için gerekli bilgileri içerir. İki tür erişim anahtarı vardır:

- **Statik erişim anahtarları**, bağlanmak için gereken tüm sunucu bilgilerini (sunucu adresi, bağlantı noktası, şifre, şifreleme yöntemi) şifreleyerek erişim bilgilerinin değiştirilmesini önler. Kullanıcılar, bu anahtarı Outline istemcisine yapıştırır.

Örnek:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo1UkVmeFRqbHR6Mkw@outline-server.example.com:17178/?outline=1
```

- **Dinamik erişim anahtarları**, servis sağlayıcının sunucu erişim bilgilerini uzaktan barındırmasına izin verir. Bu sayede servis sağlayıcı, son kullanıcılara yeni erişim anahtarları tahsis etmeye gerek kalmadan sunucu yapılandırmalarını (sunucu adresi, bağlantı noktası, şifreler, şifreleme yöntemi) güncelleyebilir. Daha ayrıntılı dokümanlara göz atmak için [Dinamik erişim anahtarları](vpn/management/dynamic-access-keys)'na göz atın.
