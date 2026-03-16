---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

In diesem Leitfaden werden Sie Schritt für Schritt durch die Einrichtung Ihrer Go-Umgebung geführt und Sie erfahren, wie Sie das Outline SDK in Ihrem Go-Code verwenden.

Wir werden eine Beispiel-App mit der Bezeichnung `splitfetch` erstellen, die eine Funktion des SDK vorstellt. Diese Anwendung ruft eine Webseite ab, doch anstatt die Anfrage in einem einzigen Netzwerk-Paket zu senden, **verwendet sie das Outline SDK, um den initialen TCP-Stream in zwei separate Pakete aufzuteilen**. Dies kann dazu beitragen, einige Formen der Netzintervention zu umgehen.

Sie können die App unter **Linux, Mac und Windows** ausführen.
Informationen zur Einbindung in mobile Apps finden Sie hier: [Outline SDK zu Ihrer mobilen App hinzufügen](mobile-app-integration).

## Schritt 1: Go einrichten {#step_1_set_up_go}

Zuerst brauchen Sie [Go (Programmiersprache)](https://go.dev/).
Wenn Sie Go bereits installiert haben (Version 1.21 oder höher), können Sie direkt zum nächsten Schritt weitergehen.

Für die Installation können Sie den Schritten im [offiziellen Leitfaden](https://go.dev/doc/install) folgen oder, wenn Sie einen Paketmanager verwenden:

### Linux {#linux}

Folgen Sie den in [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu) beschriebenen Schritten.

### Mac {#mac}

```sh
brew install go
```

### Windows {#windows}

```powershell
winget install --id=GoLang.Go  -e
```

Nach der Installation von Go können Sie überprüfen, ob es korrekt installiert wurde, indem Sie den folgenden Befehl in einem Terminal ausführen:

```sh
go version
```

## Schritt 2: `splitfetch`-App erstellen {#step_2_create_the_splitfetch_application}

Richten Sie das `splitfetch`-Projekt ein. Dazu müssen Sie zuerst das Projektverzeichnis erstellen und ein Go-Modul initialisieren:

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

Ziehen Sie dann das Outline SDK hinzu und erstellen Sie Ihre `main.go`-Datei:

```sh
go get github.com/Jigsaw-Code/outline-sdk@latest
touch main.go
```

## Schritt 3: Outline SDK in der Anwendung verwenden {#step_3_use_outline_sdk_in_the_application}

Öffnen Sie die `main.go`-Datei in Ihrem bevorzugten Code-Editor und fügen Sie den folgenden Code ein. Dieser Code enthält sämtliche Logik für unsere `splitfetch`-App.

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

Nach dem Speichern des Codes führen Sie den folgenden Befehl in Ihrem Terminal aus, um zu prüfen, ob die `go.mod`-Datei ordnungsgemäß aktualisiert wurde.

```sh
go mod tidy
```

## Schritt 4: Anwendung ausführen {#step_4_run_the_application}

Mit dem erstellten Code können Sie die `splitfetch`-App nun ausführen.

Führen Sie im `splitfetch`-Verzeichnis den folgenden Befehl in Ihrem Terminal aus und geben Sie dabei eine URL als Argument an:

```sh
go run . https://getoutline.org
```

Damit wird die Anwendung kompiliert und ausgeführt und der HTML-Inhalt der Webseite angezeigt.

Wenn Sie ein eigenständiges Programm erstellen und verteilen möchten, das ohne `go` ausgeführt werden kann, verwenden Sie den Befehl `go build`:

### Linux und Mac {#linux-mac}

```sh
go build -o splitfetch .
```

### Windows {#windows_1}

```sh
go build -o splitfetch.exe .
```

Sobald der Build erstellt ist, können Sie Ihre App verteilen und ausführen.
Beispiel:

```sh
./splitfetch https://getoutline.org
```
