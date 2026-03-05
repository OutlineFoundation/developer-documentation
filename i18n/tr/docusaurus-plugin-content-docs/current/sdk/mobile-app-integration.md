---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

Bu belgede, Outline SDK'yı mobil uygulamalarınıza nasıl entegre edeceğiniz açıklanmaktadır. Basitleştirilmiş yerel proxy yönetimi için `MobileProxy` kitaplığına odaklanılmıştır.

Go temelli bir kitaplık olan `MobileProxy`, proxy işlevlerini mobil uygulamalara entegrasyonunu iyileştirmek için tasarlanmıştır. Mobil uygulama kitaplıklarını oluşturmak için [Go Mobile](https://go.dev/wiki/Mobile)'dan yararlanır. Böylece, uygulamanızın ağ kitaplıklarını trafiği yerel bir proxy üzerinden yönlendirecek şekilde yapılandırabilirsiniz.

**MobileProxy kullanılmayan uygulama**

![MobileProxy kullanılmayan içerik uygulaması](/images/mobileproxy-before.png)

**MobileProxy kullanılan uygulama**

![MobileProxy kullanılan içerik uygulaması](/images/mobileproxy-after.png)

## 1. adım: MobileProxy mobil uygulama kitaplıklarını oluşturun

Go kodunu Android ve iOS'e yönelik kitaplıklar hâlinde derlemek için [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile)'ı kullanın.

1. Outline SDK deposunu klonlayın:

2. [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) ile Go Mobile ikili programlarını derleyin:

#### Psiphon desteği ekleme

Şu ek adımları izleyerek [Psiphon](https://psiphon.ca/) ağını kullanma desteği ekleyebilirsiniz:

    - Psiphon ekibine ulaşarak ağlarına erişim sağlayan bir yapılandırma alın. Bunun için bir sözleşmenizin olması gerekebilir.

    - Aldığınız Psiphon yapılandırmasını, `SmartDialer` yapılandırmanızın `fallback` bölümüne ekleyin.

    - `-tags psiphon` işaretini kullanarak MobileProxy'yi derleyin:

Psiphon kod tabanı GPL kapsamında lisanslandığından kodunuza lisans kısıtlamaları uygulanabilir. Bu nedenle `-tags psiphon` işareti zorunludur. Psiphon ekibinden özel bir lisans almanız önerilir.

3. Mobil uygulama kitaplıklarını oluşturun ve projenize ekleyin:

### Android

Oluşturulan `out/mobileproxy.aar` paketini içe aktarmak için Android Studio'da **Dosya > Projeyi İçe Aktar…** seçeneğini belirleyin. Daha fazla yardım için Go Mobile'ın [Building and deploying to Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) (Uygulama derleme ve Android'e dağıtma) başlıklı bölümünü inceleyin.

### iOS

`out/mobileproxy.xcframework` paketini Xcode projesine sürükleyin. Daha fazla yardım için Go Mobile'ın [Building and deploying to Android](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) (Uygulama derleme ve iOS'e dağıtma) başlıklı bölümünü inceleyin.

## 2. adım: MobileProxy'yi çalıştırın

`MobileProxy` yerel proxy'sini uygulamanızın çalışma zamanında başlatın.
Dinamik strateji seçimi için statik bir araç yapısı ya da akıllı proxy kullanabilirsiniz.

- **Statik araç yapılandırması**: Yerel bir adres ve araç yapılandırmasıyla `RunProxy` işlevini kullanın.

### Android

### iOS

- **Akıllı proxy**: Akıllı proxy, DNS ve TLS stratejilerini belirtilen test alan adlarına göre dinamik olarak seçer. Yapılandırma stratejisini YAML biçiminde ([örnek](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)) belirtmeniz gerekir.

### Android

### iOS

## 3. adım: HTTP istemcilerini ve ağ kitaplıklarını yapılandırın

Ağ kitaplıklarınızı yerel proxy adresini ve bağlantı noktasını kullanacak şekilde yapılandırın.

### Dart/Flutter HttpClient

Proxy'yi [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html) ile ayarlayın.

### OkHttp (Android)

Proxy'yi [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/) ile ayarlayın.

### JVM (Java, Kotlin)

Proxy'yi [sistem özellikleriyle](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html) kullanılacak şekilde yapılandırın:

### Android Web Görünümü

[`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController) kitaplığını kullanarak uygulamanızdaki tüm web görünümlerine bir proxy yapılandırması uygulayın:

### iOS Web Görünümü

iOS 17 sürümünden itibaren, [`WKWebsiteDataStore` özelliğini](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) kullanarak `WKWebView` görünümüne proxy yapılandırması uygulayabilirsiniz:

## İleri düzey: Özel mobil uygulama kitaplığı oluşturma

İleri düzey kullanım alanları için kendi mobil uygulama kitaplıklarınızı oluşturabilirsiniz:

1. **Go kitaplığı oluşturma**: Zorunlu SDK işlevlerini sarmalayan bir Go paketi oluşturun.

2. **Mobil uygulama kitaplıkları oluşturma**: Android Archive (AAR) ve Apple çerçeveleri oluşturmak için `gomobile bind` komutunu kullanın. Örnekler:

    - [Outline Android Archive](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple Çerçevesi](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Uygulamanıza entegre etme**: Oluşturulan kitaplığı mobil uygulamanıza ekleyin.
