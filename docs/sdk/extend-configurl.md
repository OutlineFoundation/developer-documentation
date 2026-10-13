---
title: "Extend configurl with Custom Strategies"
sidebar_label: "Extend configurl"
---

# Extend configurl with custom strategies

The Outline SDK's [`configurl` package](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl)
turns configuration strings into network objects. You can register your own
configuration types in your Go application without changing the SDK.

In this guide, you will add two types and combine them to trigger a timeout:

| Configuration | Behavior |
|---|---|
| `delay:200ms` | Wait 200 milliseconds before opening a connection. |
| `timeout:t=1s&error=too+slow` | Allow up to one second to open a connection, returning `too slow` if the timeout expires. |

The delay takes a single duration; the timeout takes `key=value` options. You
need basic Go knowledge and [Go 1.24.1 or later](https://go.dev/doc/install).
The example connects to a local TCP listener, so no Outline server or access key
is required.

## How registration works

A **stream dialer** is an object with a `DialStream(ctx, "host:port")` method
that opens a connection, such as TCP. A **provider** builds dialers from
configuration. [`configurl.NewDefaultProviders()`][new-default-providers]
creates a [`ProviderContainer`][provider-container] with the built-in
configuration types already registered.

To add a type, call
[`providers.StreamDialers.RegisterType`][register-type] with a name and a
builder function, whose signature is [`configurl.BuildFunc`][build-func]. For
`delay:200ms`, the name is `delay`, and the builder reads the duration, builds
the underlying dialer, and returns a wrapper around it. Registering a builder
does not open a connection; calling the resulting dialer's `DialStream` method
does.

Configurations can be joined with `|`. Each part wraps the dialer built from
the parts to its left. For example:

```text
delay:2s|timeout:t=100ms&error=too+slow
```

The outer timeout wrapper starts its 100-millisecond timer, then calls the
delay wrapper. The delay waits for two seconds, but the timeout cancels it
first, producing `too slow`. Underneath both wrappers is the default TCP dialer;
in this case, the delay is cancelled before TCP dialing begins. The `|`
character describes composition, not a choice between strategies.

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

## Step 2: Register and use the custom types

Create `main.go` in the `configurl-example` directory and paste this complete
program into it:

```go
package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"log"
	"net"
	"net/url"
	"time"

	"golang.getoutline.org/sdk/transport"
	"golang.getoutline.org/sdk/x/configurl"
)

func registerDelay(providers *configurl.ProviderContainer) {
	providers.StreamDialers.RegisterType("delay", func(ctx context.Context, config *configurl.Config) (transport.StreamDialer, error) {
		// In "delay:200ms", URL.Opaque is "200ms".
		duration, err := time.ParseDuration(config.URL.Opaque)
		if err != nil || duration <= 0 {
			return nil, errors.New("delay: expected a positive duration, such as 200ms")
		}
		base, err := providers.StreamDialers.NewInstance(ctx, config.BaseConfig)
		if err != nil {
			return nil, err
		}
		return transport.FuncStreamDialer(func(ctx context.Context, address string) (transport.StreamConn, error) {
			timer := time.NewTimer(duration)
			defer timer.Stop()
			select {
			case <-ctx.Done():
				return nil, ctx.Err()
			case <-timer.C:
				return base.DialStream(ctx, address)
			}
		}), nil
	})
}

func registerTimeout(providers *configurl.ProviderContainer) {
	providers.StreamDialers.RegisterType("timeout", func(ctx context.Context, config *configurl.Config) (transport.StreamDialer, error) {
		// In "timeout:t=1s&error=too+slow", parse the key=value options.
		options, err := url.ParseQuery(config.URL.Opaque)
		if err != nil {
			return nil, fmt.Errorf("timeout: invalid options: %w", err)
		}
		duration, err := time.ParseDuration(options.Get("t"))
		if err != nil || duration <= 0 {
			return nil, errors.New("timeout: t must be a positive duration, such as 1s")
		}
		message := options.Get("error")
		if message == "" {
			return nil, errors.New("timeout: error must not be empty")
		}
		timeoutErr := errors.New(message)
		base, err := providers.StreamDialers.NewInstance(ctx, config.BaseConfig)
		if err != nil {
			return nil, err
		}
		return transport.FuncStreamDialer(func(ctx context.Context, address string) (transport.StreamConn, error) {
			// Apply a fresh timeout and error cause for each dial.
			dialCtx, cancel := context.WithTimeoutCause(ctx, duration, timeoutErr)
			defer cancel()
			conn, err := base.DialStream(dialCtx, address)
			if err != nil && context.Cause(dialCtx) == timeoutErr {
				return nil, timeoutErr
			}
			return conn, err
		}), nil
	})
}

func main() {
	configText := flag.String("transport", "delay:200ms|timeout:t=1s&error=too+slow", "configurl configuration")
	flag.Parse()
	log.SetFlags(0)

	providers := configurl.NewDefaultProviders()
	registerDelay(providers)
	registerTimeout(providers)
	dialer, err := providers.NewStreamDialer(context.Background(), *configText)
	if err != nil {
		log.Fatal(err)
	}

	// A local listener lets us try opening a TCP connection without a server setup.
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()
	conn, err := dialer.DialStream(context.Background(), listener.Addr().String())
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	fmt.Println("connected")
}
```

### Parse your configuration

Each builder receives a parsed [`configurl.Config`][config]:

- `config.URL` describes the current part. For `delay:200ms`, its `Scheme` is
  `delay` and its `Opaque` field is `200ms`.
- For `timeout:t=1s&error=too+slow`, `Opaque` holds `t=1s&error=too+slow`.
  `url.ParseQuery(config.URL.Opaque)` turns that text into options. Both `t`
  (a positive duration) and `error` (a nonempty message) are required here.
  These options follow the colon directly; there is no `?`, so `URL.Query()`
  would not read them.
- `config.BaseConfig` describes the parts to the left. Passing it to
  [`StreamDialers.NewInstance`][new-instance] preserves composition. When there
  are no parts to the left, it is `nil`, and the provider returns its default
  TCP dialer.

The `error` option uses URL query encoding: `too+slow` becomes `too slow`.
Encode literal `&`, `|`, and `+` in values as `%26`, `%7C`, and `%2B`, respectively,
so they do not become separators or spaces. When creating configurations in Go,
use `url.Values.Encode()` to encode the option values.

Use [`providers.NewStreamDialer`][new-stream-dialer] for a configuration
**string** and [`NewInstance`][new-instance] for an already parsed
`*configurl.Config`. Inside a builder, pass `config.BaseConfig`, not `config`
itself: passing the current config would call the same builder again indefinitely.

### Apply the behavior when dialing

`transport.FuncStreamDialer` turns a Go function into a stream dialer. Its
function runs on every dial and uses that call's context. The delay selects
between its timer and context cancellation; using `time.Sleep` here would make
it wait out the entire delay even after the timeout expires.

The timeout uses `context.WithTimeoutCause` to associate the configured error
with its deadline. When that deadline interrupts the underlying dialer, the
wrapper returns the custom error. The cause check keeps caller cancellation
and earlier caller deadlines from being relabeled with our message.

Both wrappers affect opening a connection; they do not delay data transfer or
set read or write deadlines on the returned connection. The underlying dialer
must honor its context for the timeout to take effect. The local listener is
only used to complete the TCP handshake; the example does not send application
data.

## Step 3: Run it and trigger a timeout

From the same directory, run:

```sh
go mod tidy
go run .
```

The default configuration waits 200 milliseconds before opening a local TCP
connection, within the one-second timeout. It prints:

```text
connected
```

Now make the delay longer than the timeout:

```sh
go run . -transport 'delay:2s|timeout:t=100ms&error=too+slow'
```

After about 100 milliseconds of dialing (excluding compilation time), the
timeout interrupts the delay. The program prints your decoded error message
and exits unsuccessfully:

```text
too slow
exit status 1
```

Quote configurations containing `|` or `&` so your shell passes the entire
string to the program.

### See why order matters

Put the delay outside the timeout:

```sh
go run . -transport 'timeout:t=1s&error=too+slow|delay:2s'
```

This prints `connected` after about two seconds. The delay wrapper runs first;
only after it finishes does it call the timeout wrapper, starting the
one-second timer for the local TCP connection. To include the delay in the time
limit, put the timeout to its right, as in the previous example.

### Reject invalid options early

```sh
go run . -transport 'timeout:t=invalid&error=too+slow'
```

The builder rejects the configuration before any connection is opened:

```text
timeout: t must be a positive duration, such as 1s
exit status 1
```

## Use the pattern in your application

Keep the provider container you configured and use it to build your dialers.
Registration belongs to that container: a new `NewDefaultProviders()` call
does not inherit your custom types, and registering here does not add `delay`
or `timeout` to other applications or prebuilt SDK tools. Register types during
application setup, before any goroutines use the providers. Use a distinct
lowercase name; registering an existing name replaces its builder.

These examples register stream dialers only. For datagram connections, register
a builder returning `transport.PacketDialer` with `providers.PacketDialers`;
packet listeners have a separate `providers.PacketListeners` registry. A stream
registration does not automatically enable the same name in those registries.

To implement your own strategy, replace the option parsing and wrappers with
your configuration format and dialer implementation. For wrappers, keep the
`BaseConfig` call so they compose with existing strategies. For the complete
API, see [Defining custom strategies](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Defining_custom_strategies)
and the [SDK's dialer concepts](/sdk/concepts#dialers).

[new-default-providers]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#NewDefaultProviders
[provider-container]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#ProviderContainer
[register-type]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#ExtensibleProvider.RegisterType
[build-func]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#BuildFunc
[config]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#Config
[new-instance]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#ExtensibleProvider.NewInstance
[new-stream-dialer]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#ProviderContainer.NewStreamDialer
