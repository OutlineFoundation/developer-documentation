---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

Bu kılavuzda, Go ortamınızı ayarlama ve Go kodunuzda Outline SDK'yı kullanma süreçleri adım adım açıklanmaktadır.

SDK'nın bir özelliğini gösteren `splitfetch` adında bir örnek uygulama oluşturacağız. Bu uygulama bir web sayfasını getirir ancak talebi tek bir ağ paketinde göndermek yerine **Outline SDK'yı kullanarak ilk TCP akışını iki ayrı pakete böler**. Bu özellik, bazı ağ müdahalesi türlerinin atlatılmasını sağlayabilir.

Uygulamayı **Linux, Mac ve Windows** üzerinde çalıştırabilirsiniz.
Mobil uygulamalarla entegrasyon için [Outline SDK'yı mobil uygulamanıza ekleme](mobile-app-integration) başlıklı bölüme bakın.

## 1. adım: Go'yu ayarlayın

Öncelikle [Go programlama dili](https://go.dev/) gerekir.
Go (sürüm 1.21 veya sonraki bir sürümü) zaten yüklüyse sonraki adıma geçebilirsiniz.

Yükleme için [resmi kılavuzdaki](https://go.dev/doc/install) yönergeleri izleyebilirsiniz. Paket yöneticisi kullanıyorsanız:

### Linux

[Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu) sayfasındaki adımları izleyin.

### Mac

### Windows

Go yüklendikten sonra, aşağıdaki komutu terminalde çalıştırarak yüklemenin doğru bir şekilde yapılıp yapılmadığını doğrulayabilirsiniz:

## 2. adım: `splitfetch` uygulamasını oluşturun

Şimdi `splitfetch` projesini ayarlayalım. Öncelikle proje dizinini oluşturun ve bir Go modülü başlatın:

Ardından, Outline SDK'yı ekleyin ve `main.go` dosyanızı oluşturun:

## 3. adım: Uygulamada Outline SDK'yı kullanın

`main.go` dosyasını en sevdiğiniz kod düzenleyicide açın ve aşağıdaki kodu dosyaya yapıştırın. Bu kodda, `splitfetch` uygulamanıza dair mantık yer alır.

Kodu kaydettikten sonra, aşağıdaki komutu terminalde çalıştırarak `go.mod` dosyasının doğru şekilde güncellendiğinden emin olun.

## 4. adım: Uygulamayı çalıştırın

Kod hazırlandığına göre artık `splitfetch` uygulamasını çalıştırabilirsiniz.

`splitfetch` dizini içinden, aşağıdaki komutu terminalde çalıştırın. Bu işlemde bağımsız değişken olarak bir URL kullanın:

Böylece uygulama derlenip çalıştırılır ve web sayfasının HTML içeriği görüntülenir.

`go` olmadan çalıştırabileceğiniz bağımsız bir program oluşturup dağıtmak istiyorsanız `go build` komutunu kullanın:

### Linux ve Mac

### Windows

Derleme işlemi tamamlandıktan sonra, uygulamanızı dağıtıp çalıştırabilirsiniz.
Örneğin:
