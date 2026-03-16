---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

Bu kılavuzda, Go ortamınızı ayarlama ve Go kodunuzda Outline SDK'yı kullanma süreçleri adım adım açıklanmaktadır.

SDK'nın bir özelliğini gösteren `splitfetch` adında bir örnek uygulama oluşturacağız. Bu uygulama bir web sayfasını getirir ancak talebi tek bir ağ paketinde göndermek yerine **Outline SDK'yı kullanarak ilk TCP akışını iki ayrı pakete böler**. Bu özellik, bazı ağ müdahalesi türlerinin atlatılmasını sağlayabilir.

Uygulamayı **Linux, Mac ve Windows** üzerinde çalıştırabilirsiniz.
Mobil uygulamalarla entegrasyon için [Outline SDK'yı mobil uygulamanıza ekleme](mobile-app-integration) başlıklı bölüme bakın.

## 1. adım: Go'yu ayarlayın {#step_1_set_up_go}

Öncelikle [Go programlama dili](https://go.dev/) gerekir.
Go (sürüm 1.21 veya sonraki bir sürümü) zaten yüklüyse sonraki adıma geçebilirsiniz.

Yükleme için [resmi kılavuzdaki](https://go.dev/doc/install) yönergeleri izleyebilirsiniz. Paket yöneticisi kullanıyorsanız:

### Linux {#linux}

[Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu) sayfasındaki adımları izleyin.

### Mac {#mac}

```sh
brew install go
```

### Windows {#windows}

```powershell
winget install --id=GoLang.Go  -e
```

Go yüklendikten sonra, aşağıdaki komutu terminalde çalıştırarak yüklemenin doğru bir şekilde yapılıp yapılmadığını doğrulayabilirsiniz:

```sh
go version
```

## 2. adım: `splitfetch` uygulamasını oluşturun {#step_2_create_the_splitfetch_application}

Şimdi `splitfetch` projesini ayarlayalım. Öncelikle proje dizinini oluşturun ve bir Go modülü başlatın:

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

Ardından, Outline SDK'yı ekleyin ve `main.go` dosyanızı oluşturun:

```sh
go get github.com/Jigsaw-Code/outline-sdk@latest
touch main.go
```

## 3. adım: Uygulamada Outline SDK'yı kullanın {#step_3_use_outline_sdk_in_the_application}

`main.go` dosyasını en sevdiğiniz kod düzenleyicide açın ve aşağıdaki kodu dosyaya yapıştırın. Bu kodda, `splitfetch` uygulamanıza dair mantık yer alır.

```go
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"os"

	"github.com/Jigsaw-Code/outline-sdk/transport"
	"github.com/Jigsaw-Code/outline-sdk/transport/split"
)

// The number of bytes to send in the first packet.
const splitPacketSize = 3

func main() {
	// 1. Get the URL from the command-line arguments.
	if len(os.Args) < 2 {
		log.Fatalf("Usage: %s <URL>", os.Args[0])
	}
	url := os.Args[1]

	// 2. Create a split dialer from the Outline SDK.
	// This dialer wraps a standard TCP dialer to add the splitting behavior.
	dialer, err := split.NewStreamDialer(&transport.TCPDialer{}, split.NewFixedSplitIterator(splitPacketSize))
	if err != nil {
		log.Fatalf("Failed to create split dialer: %v", err)
	}

	// 3. Configure an HTTP client to use our custom split dialer for TCP connections.
	httpClient := &http.Client{
		Transport: &http.Transport{
			DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
				return dialer.DialStream(ctx, addr)
			},
		},
	}

	// 4. Use the custom client to make the HTTP GET request.
	resp, err := httpClient.Get(url)
	if err != nil {
		log.Fatalf("HTTP request failed: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Failed to read response body: %v", err)
	}
	fmt.Println(string(body))
}
```

Kodu kaydettikten sonra, aşağıdaki komutu terminalde çalıştırarak `go.mod` dosyasının doğru şekilde güncellendiğinden emin olun.

```sh
go mod tidy
```

## 4. adım: Uygulamayı çalıştırın {#step_4_run_the_application}

Kod hazırlandığına göre artık `splitfetch` uygulamasını çalıştırabilirsiniz.

`splitfetch` dizini içinden, aşağıdaki komutu terminalde çalıştırın. Bu işlemde bağımsız değişken olarak bir URL kullanın:

```sh
go run . https://getoutline.org
```

Böylece uygulama derlenip çalıştırılır ve web sayfasının HTML içeriği görüntülenir.

`go` olmadan çalıştırabileceğiniz bağımsız bir program oluşturup dağıtmak istiyorsanız `go build` komutunu kullanın:

### Linux ve Mac {#linux-mac}

```sh
go build -o splitfetch .
```

### Windows {#windows_1}

```sh
go build -o splitfetch.exe .
```

Derleme işlemi tamamlandıktan sonra, uygulamanızı dağıtıp çalıştırabilirsiniz.
Örneğin:

```sh
./splitfetch https://getoutline.org
```
