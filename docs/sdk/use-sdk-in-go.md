---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

# Add Outline SDK to your Go code

This guide walks you through the process of setting up your Go environment and
using the Outline SDK in your Go code.

We will build an example application called `splitfetch` that showcases a
feature of the SDK. This application fetches a web page, but instead of sending
the request in a single network packet, **it uses the Outline SDK to split the
initial TCP stream into two separate packets**. This may help bypass some forms
of network intervention.

You will be able to run the application on **Linux, Mac, and Windows**.
For integrating with mobile apps, check out [Add Outline SDK to your mobile app](mobile-app-integration.md).

## Step 1: Set up Go

First up, you'll need the [Go programming language](https://go.dev/).
If you've already got Go (version 1.21 or newer) installed, you can skip to the
next step.

For installation, you can follow the [official guide](https://go.dev/doc/install);
or, if you use a package manager:

### Linux

  Follow the steps in [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### Mac

  ```sh
  brew install go
  ```

### Windows

  ```powershell
  winget install --id=GoLang.Go  -e
  ```

After Go is installed, you can verify that it is installed correctly by running
the following command in a terminal:

```sh
go version
```

## Step 2: Create the `splitfetch` Application

Let get the `splitfetch` project set up. First, create the project directory and
initialize a Go module:

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

Tip: For public projects, use your repository path like
`github.com/your-name/your-repo` instead of `example/splitfetch`.

Next, pull in the Outline SDK and create your `main.go` file:

```sh
go get github.com/Jigsaw-Code/outline-sdk@latest
touch main.go
```

## Step 3: Use Outline SDK in the Application

Open the `main.go` file in your favorite code editor and paste the following
code into it. This code contains all the logic for our `splitfetch` application.

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

After saving the code, run the following command in your terminal to make sure
the `go.mod` file is updated correctly.

```sh
go mod tidy
```

## Step 4: Run the Application

With the code in place, you can now run the `splitfetch` application.

From within the `splitfetch` directory, run the following command in your
terminal, passing a URL as an argument:

```sh
go run . https://getoutline.org
```

This compiles and runs the application, displaying the webpage's HTML content.

If you want to create and distribute a standalone program that you can run
without `go`, use the `go build` command:

### Linux & Mac

  ```sh
  go build -o splitfetch .
  ```

### Windows

  ```sh
  go build -o splitfetch.exe .
  ```

Once the build is finished, you can distribute and run your application.
For example:

```sh
./splitfetch https://getoutline.org
```
