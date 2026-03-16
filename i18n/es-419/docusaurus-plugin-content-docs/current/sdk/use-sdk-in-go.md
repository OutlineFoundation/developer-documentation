---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

En esta guía, se explica el proceso de configuración de tu entorno de Go y
cómo usar el SDK de Outline en ese lenguaje de programación.

Para demostrar una función del SDK,
crearemos una aplicación de ejemplo llamada `splitfetch`. Esta recupera una página web, pero, en vez de enviar
la solicitud en un solo paquete de red, **usa el SDK de Outline para dividir la
transmisión de TCP inicial en dos paquetes separados**, lo que puede ayudar a evitar algunas formas
de intervención de la red.

Podrás ejecutar la aplicación en **Linux, macOS y Windows**.
Para realizar integraciones con apps para dispositivos móviles, consulta [Agrega el SDK de Outline a tu app para dispositivos móviles](mobile-app-integration).

## Paso 1: Configura Go {#step_1_set_up_go}

Primero, necesitarás el [lenguaje de programación Go](https://go.dev/).
Si ya tienes instalada la versión 1.21 (o una posterior), puedes avanzar al
siguiente paso.

Para instalarlo, puedes seguir la [guía oficial](https://go.dev/doc/install)
o seguir estos pasos si usas un administrador de paquetes:

### Linux {#linux}

Sigue los pasos que se indican en [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### macOS {#mac}

```sh
brew install go
```

### Windows {#windows}

```powershell
winget install --id=GoLang.Go  -e
```

Luego, para verificar que Go se haya instalado correctamente,
ejecuta este comando en la terminal:

```sh
go version
```

## Paso 2: Crea la aplicación `splitfetch` {#step_2_create_the_splitfetch_application}

Configuremos el proyecto `splitfetch`. Primero, crea el directorio del proyecto y, luego,
inicializa un módulo de Go:

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

Luego, agrega el SDK de Outline y crea el archivo `main.go`.

```sh
go get github.com/Jigsaw-Code/outline-sdk@latest
touch main.go
```

## Paso 3: Usa el SDK de Outline en la aplicación {#step_3_use_outline_sdk_in_the_application}

Abre el archivo `main.go` en el editor de código que prefieras y pega el siguiente
código en él, que contiene toda la lógica de la aplicación `splitfetch`.

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

Después de guardar el código, ejecuta el siguiente comando en la terminal para asegurarte
de que el archivo `go.mod` se haya actualizado correctamente.

```sh
go mod tidy
```

## Paso 4: Ejecuta la aplicación {#step_4_run_the_application}

Ahora que implementaste el código, puedes ejecutar la aplicación `splitfetch`.

En el directorio `splitfetch`, ejecuta el siguiente comando en la
terminal, pasando una URL como argumento:

```sh
go run . https://getoutline.org
```

Con esta acción, se compila y ejecuta la aplicación, que muestra el contenido HTML de la página web.

Si quieres crear y distribuir un programa independiente que puedas ejecutar
sin `go`, usa el comando `go build`:

### Linux y macOS {#linux-mac}

```sh
go build -o splitfetch .
```

### Windows {#windows_1}

```sh
go build -o splitfetch.exe .
```

Cuando se termine de compilar la aplicación, podrás distribuirla y ejecutarla.
Por ejemplo:

```sh
./splitfetch https://getoutline.org
```
