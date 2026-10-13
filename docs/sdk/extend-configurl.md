---
title: "Extend configurl with a Custom Strategy"
sidebar_label: "Extend configurl"
---

# Extend configurl with a custom strategy

The Outline SDK's [`configurl` package](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl)
turns configuration strings into network objects. You can register your own
configuration types in your Go application without changing the SDK.

In this guide, you will add `timeout:2s`: a configuration that limits how long
opening a connection can take. You will then combine it with a built-in strategy
and make an HTTP request to a local server. You need basic Go knowledge and
[Go 1.24.1 or later](https://go.dev/doc/install); no Outline server or access key
is required.

## How registration works

A **stream dialer** is an object with a `DialStream(ctx, "host:port")` method
that opens a connection, such as TCP. A **provider** builds dialers from
configuration. `configurl.NewDefaultProviders()` creates a container with the
built-in configuration types already registered.

To add a type, call `providers.StreamDialers.RegisterType` with a name and a
builder function. For `timeout:2s`, the name is `timeout`, and the builder reads
the duration, builds the underlying dialer, and returns a wrapper around it.
Registering a builder does not open a connection; calling the resulting dialer's
`DialStream` method does.

Configurations can be joined with `|`. Each part wraps the dialer built from
the parts to its left. For example:

```text
split:2|timeout:2s
```

This builds a timeout wrapper around the built-in `split:2` dialer, which splits
the initial outgoing stream after two bytes. Underneath both is the default TCP
dialer. The `|` character describes composition, not a choice between strategies.
We use `split` here to demonstrate combining a custom type with an existing SDK
type.

## Step 1: Create a Go module

Run these commands in a terminal:

```sh
mkdir configurl-example
cd configurl-example
go mod init example.com/configurl-example
go get golang.getoutline.org/sdk/x/configurl@v0.2.2
```

This guide uses version `v0.2.2` of the SDK's `x` module. The `x` APIs are
experimental, so pin a version when using them. Use the `golang.getoutline.org`
import paths shown here, including for the core `transport` package; older
examples may use GitHub import paths.

## Step 2: Register and use the custom type

Create `main.go` in the `configurl-example` directory and paste this complete
program into it:

```go
package main

import (
	"context"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"net/http/httptest"
	"time"

	"golang.getoutline.org/sdk/transport"
	"golang.getoutline.org/sdk/x/configurl"
)

func registerTimeout(providers *configurl.ProviderContainer) {
	providers.StreamDialers.RegisterType("timeout", func(ctx context.Context, config *configurl.Config) (transport.StreamDialer, error) {
		// In "timeout:2s", URL.Opaque is "2s".
		duration, err := time.ParseDuration(config.URL.Opaque)
		if err != nil || duration <= 0 {
			return nil, fmt.Errorf("timeout: expected a positive duration, such as 2s or 500ms")
		}

		// Build the configuration to the left of this part.
		base, err := providers.StreamDialers.NewInstance(ctx, config.BaseConfig)
		if err != nil {
			return nil, err
		}

		return transport.FuncStreamDialer(func(ctx context.Context, address string) (transport.StreamConn, error) {
			// Apply a fresh timeout each time a connection is opened.
			dialCtx, cancel := context.WithTimeout(ctx, duration)
			defer cancel()
			return base.DialStream(dialCtx, address)
		}), nil
	})
}

func main() {
	configText := flag.String("transport", "timeout:2s", "configurl configuration")
	flag.Parse()
	log.SetFlags(0)

	providers := configurl.NewDefaultProviders()
	registerTimeout(providers)
	dialer, err := providers.NewStreamDialer(context.Background(), *configText)
	if err != nil {
		log.Fatal(err)
	}

	// Start a local HTTP server so the example needs no external service.
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello through configurl!")
	}))
	defer server.Close()

	httpTransport := &http.Transport{
		DialContext: func(ctx context.Context, network, address string) (net.Conn, error) {
			return dialer.DialStream(ctx, address)
		},
	}
	defer httpTransport.CloseIdleConnections()
	client := &http.Client{Transport: httpTransport, Timeout: 5 * time.Second}
	response, err := client.Get(server.URL)
	if err != nil {
		log.Fatal(err)
	}
	defer response.Body.Close()
	if _, err := io.Copy(io.Discard, response.Body); err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Status)
}
```

The builder receives a parsed `configurl.Config`:

- `config.URL` describes the current part. For `timeout:2s`, its `Scheme` is
  `timeout` and its `Opaque` field is `2s`. This example uses `type:value`
  syntax, so read `Opaque`, not `URL.Query()`.
- `config.BaseConfig` describes the parts to the left. Passing it to
  `StreamDialers.NewInstance` preserves composition. When there are no parts to
  the left, it is `nil`, and the provider returns its default TCP dialer.

Use `NewStreamDialer` for a configuration **string** and `NewInstance` for an
already parsed `*configurl.Config`. Inside the builder, pass `config.BaseConfig`,
not `config` itself: passing the current config would call the same builder
again indefinitely.

`transport.FuncStreamDialer` turns a Go function into a stream dialer. Its
function runs on every dial and uses that call's context, so it respects caller
cancellation and earlier deadlines. The timeout applies to opening the
connection; it does not set read or write deadlines on the returned connection.
The underlying dialer must honor its context for the timeout to take effect.
The HTTP client's separate five-second timeout covers the whole HTTP request.

## Step 3: Run it and compose configurations

From the same directory, run:

```sh
go mod tidy
go run .
```

The program starts a temporary local server, connects through your custom
dialer, and prints:

```text
200 OK
```

Now combine the custom type with the built-in split strategy:

```sh
go run . -transport 'split:2|timeout:2s'
```

This also prints `200 OK`. Quote configurations containing `|` so your shell
passes the entire string to the program.
These successful requests demonstrate registration and composition; because the
local connection opens quickly, they do not demonstrate a timeout expiring.

Try an invalid duration:

```sh
go run . -transport 'timeout:invalid'
```

The builder rejects the configuration before any connection is opened:

```text
timeout: expected a positive duration, such as 2s or 500ms
exit status 1
```

## Use the pattern in your application

Keep the provider container you configured and use it to build your dialers.
Registration belongs to that container: a new `NewDefaultProviders()` call
does not inherit your custom types, and registering here does not add `timeout`
to other applications or prebuilt SDK tools. Register types during application
setup, before any goroutines use the providers. Use a distinct lowercase name;
registering an existing name replaces its builder.

This example registers a stream dialer only. For datagram connections, register
a builder returning `transport.PacketDialer` with `providers.PacketDialers`;
packet listeners have a separate `providers.PacketListeners` registry. A stream
registration does not automatically enable the same name in those registries.

To implement your own strategy, replace the duration parsing and wrapper with
your configuration format and dialer implementation. For wrappers, keep the
`BaseConfig` call so they compose with existing strategies. For the complete
API, see [Defining custom strategies](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Defining_custom_strategies)
and the [SDK's dialer concepts](/sdk/concepts#dialers).
