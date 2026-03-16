---
title: "Outline SDK を Go コードに追加する"
sidebar_label: "Outline SDK を Go コードに追加する"
---

このガイドでは、Go 環境をセットアップして、Go コード内で Outline SDK を使用するプロセスについて説明します。

ここでは、`splitfetch` というサンプル アプリケーションを作成し、SDK の機能を紹介します。このアプリケーションはウェブページを取得しますが、リクエストを 1 つのネットワーク パケットで送信するのではなく、**Outline SDK を使用して最初の TCP ストリームを 2 つのパケットに分割**します。これは、一部のネットワーク介入を回避するのに役立つことがあります。

このアプリケーションは、**Linux、Mac、Windows** で実行できます。モバイルアプリに統合する方法については、[Outline SDK をモバイルアプリに追加する](mobile-app-integration)をご覧ください。

## ステップ 1: Go をセットアップする {#step_1_set_up_go}

最初に、[Go プログラミング言語](https://go.dev/)が必要です。すでに Go（バージョン 1.21 以降）をインストールしている場合は、次のステップに進んでください。

インストールする際は、[公式ガイド](https://go.dev/doc/install)に従ってください。または、パッケージ管理システムを使用する場合は、以下を参照してください。

### Linux {#linux}

[Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu) の手順に従います。

### Mac {#mac}

```sh
brew install go
```

### Windows {#windows}

```powershell
winget install --id=GoLang.Go  -e
```

Go をインストールした後は、ターミナルで以下のコマンドを実行し、正しくインストールされていることを確認します。

```sh
go version
```

## ステップ 2: `splitfetch` アプリケーションを作成する {#step_2_create_the_splitfetch_application}

`splitfetch` プロジェクトをセットアップしましょう。最初にプロジェクト ディレクトリを作成し、Go モジュールを初期化します。

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

次に Outline SDK を pull し、`main.go` ファイルを作成します。

```sh
go get github.com/OutlineFoundation/outline-sdk@latest
touch main.go
```

## ステップ 3: アプリケーション内で Outline SDK を使用する {#step_3_use_outline_sdk_in_the_application}

任意のコードエディタで `main.go` ファイルを開き、以下のコードを貼り付けます。このコードには `splitfetch` アプリケーションに必要なロジックがすべて含まれています。

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

コードを保存した後、ターミナルで以下のコマンドを実行し、`go.mod` ファイルが正しく更新されたことを確認します。

```sh
go mod tidy
```

## ステップ 4: アプリケーションを実行する {#step_4_run_the_application}

コードの貼り付けが完了したら、`splitfetch` アプリケーションを実行します。

ターミナルで `splitfetch` ディレクトリから以下のコマンドを実行します。URL を引数として渡します。

```sh
go run . https://getoutline.org
```

これにより、アプリケーションがコンパイルされ、実行されます。ウェブページの HTML コンテンツが表示されます。

`go` なしで実行可能なスタンドアロンのプログラムを作成して配布したい場合は、`go build` コマンドを使用します。

### Linux と Mac {#linux-mac}

```sh
go build -o splitfetch .
```

### Windows {#windows_1}

```sh
go build -o splitfetch.exe .
```

ビルドが完了したら、アプリケーションを配布して実行することができます。次に例を示します。

```sh
./splitfetch https://getoutline.org
```
