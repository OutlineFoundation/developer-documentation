---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

本指南將引導您逐步設定 Go 開發環境，並示範如何在 Go 程式碼中使用 Outline SDK。

我們會建構名為 `splitfetch` 的範例應用程式來展示 SDK 的一項功能。這個應用程式會擷取網頁，但不是透過單一網路封包送出要求，而是**利用 Outline SDK，將初始的 TCP 串流拆成兩個封包傳送**。這有助於避開某些形式的網路干預。

這個應用程式可以在 **Linux、Mac 和 Windows** 作業系統上執行。如需整合至行動應用程式，請參閱「[在行動應用程式中加入 Outline SDK](mobile-app-integration)」。

## 步驟 1：設定 Go {#step_1_set_up_go}

首先需要安裝 [Go 程式設計語言](https://go.dev/)。如果已安裝 Go 1.21 以上版本，請直接跳到下一步。

安裝方式可參考[官方指南](https://go.dev/doc/install)，如果使用套件管理工具，也可依下列說明操作：

### Linux {#linux}

執行「[Go Wiki：Ubuntu](https://go.dev/wiki/Ubuntu)」所列步驟。

### Mac {#mac}

```sh
brew install go
```

### Windows {#windows}

```powershell
winget install --id=GoLang.Go  -e
```

Go 安裝完成後，在終端機上執行下列指令，就能檢查是否安裝成功：

```sh
go version
```

## 步驟 2：建立 `splitfetch` 應用程式 {#step_2_create_the_splitfetch_application}

接著要設定 `splitfetch` 專案。請先建立專案目錄，並初始化 Go 模組：

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

接著在專案中加入 Outline SDK，並建立 `main.go` 檔案：

```sh
go get github.com/OutlineFoundation/outline-sdk@latest
touch main.go
```

## 步驟 3：在應用程式中使用 Outline SDK {#step_3_use_outline_sdk_in_the_application}

在慣用的程式碼編輯器中開啟 `main.go` 檔案，並將以下程式碼貼入其中。這段程式碼包含 `splitfetch` 應用程式的所有邏輯。

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

	"github.com/OutlineFoundation/outline-sdk/transport"
	"github.com/OutlineFoundation/outline-sdk/transport/split"
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

儲存後，請在終端機上執行以下指令，確保 `go.mod` 檔案正確更新。

```sh
go mod tidy
```

## 步驟 4：執行應用程式 {#step_4_run_the_application}

程式碼準備就緒後，即可執行 `splitfetch` 應用程式。

在終端機中切換至 `splitfetch` 目錄，輸入以下指令，後面加上一個網址做為引數：

```sh
go run . https://getoutline.org
```

這個指令會編譯並執行應用程式，顯示網頁的 HTML 內容。

如果想建立並發布無需安裝 `go` 就能執行的獨立程式，請使用 `go build` 指令：

### Linux 和 Mac {#linux-mac}

```sh
go build -o splitfetch .
```

### Windows {#windows_1}

```sh
go build -o splitfetch.exe .
```

建構完成後，即可發布並執行應用程式。
例如：

```sh
./splitfetch https://getoutline.org
```
