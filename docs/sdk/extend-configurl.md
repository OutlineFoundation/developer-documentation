---
title: "Adding Custom Components"
sidebar_label: "Custom Components"
---

# Adding Custom Components

You can build components for the Outline SDK and share them as a Go library in
your own repository. A component provider—the author of that library—can expose
`Register*` functions that apps call to add configuration types to the SDK's
[`configurl` package](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).
This makes your components easy for other apps in the Outline ecosystem to use.

Also expose constructors or types for direct use. An app should be able to
create your components with ordinary Go arguments, without parsing configuration
strings. Keep the component behavior in those constructors or types, and let
the registration functions handle configuration parsing and call them.

In this guide, you will write a component library and an app that imports it.
The library provides two dialers and their configuration types:

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
configuration. This runtime provider is distinct from the component author who
publishes the library. [`configurl.NewDefaultProviders()`][new-default-providers]
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
mkdir components
```

This guide uses version `v0.2.2` of the SDK's `x` module. The `x` APIs are
experimental, so pin a version when using them. Use the `golang.getoutline.org`
import paths shown here, including for the core `transport` package; older
examples may use GitHub import paths.

For a runnable example, the library and app live in one module, with the library
in a separate Go package. Keep each component in its own file:

```text
configurl-example/
├── go.mod
├── components/
│   ├── delay.go       # Component library: delay dialer and registration
│   └── timeout.go     # Component library: timeout dialer and registration
└── main.go            # App: imports the library and registers its components
```

When publishing your library, the `components` package can live in its own
repository and Go module. Apps then add that module as a dependency and import
its published package path instead of the local example path used below.

## Step 2: Write the component library

The library exposes a constructor and a registration function for each
component. The constructors take Go values and implement the behavior; the
registration functions turn configurl text into constructor arguments.

### Delay component

Create `components/delay.go`:

```go title="components/delay.go"
package components

import (
	"context"
	"errors"
	"time"

	"golang.getoutline.org/sdk/transport"
	"golang.getoutline.org/sdk/x/configurl"
)

// NewDelayDialer waits before opening each connection through base.
func NewDelayDialer(base transport.StreamDialer, duration time.Duration) (transport.StreamDialer, error) {
	if base == nil {
		return nil, errors.New("delay: base dialer must not be nil")
	}
	if duration <= 0 {
		return nil, errors.New("delay: duration must be positive")
	}
	dialStream := func(ctx context.Context, address string) (transport.StreamConn, error) {
		timer := time.NewTimer(duration)
		defer timer.Stop()
		select {
		case <-ctx.Done():
			return nil, ctx.Err()
		case <-timer.C:
			return base.DialStream(ctx, address)
		}
	}
	return transport.FuncStreamDialer(dialStream), nil
}

// RegisterDelay adds the "delay:<duration>" configuration type.
func RegisterDelay(providers *configurl.ProviderContainer) {
	newInstance := func(ctx context.Context, config *configurl.Config) (transport.StreamDialer, error) {
		// In "delay:200ms", URL.Opaque is "200ms".
		duration, err := time.ParseDuration(config.URL.Opaque)
		if err != nil {
			return nil, errors.New("delay: expected a duration, such as 200ms")
		}
		base, err := providers.StreamDialers.NewInstance(ctx, config.BaseConfig)
		if err != nil {
			return nil, err
		}
		return NewDelayDialer(base, duration)
	}
	providers.StreamDialers.RegisterType("delay", newInstance)
}
```

### Timeout component

Create `components/timeout.go` in the same package:

```go title="components/timeout.go"
package components

import (
	"context"
	"errors"
	"fmt"
	"net/url"
	"time"

	"golang.getoutline.org/sdk/transport"
	"golang.getoutline.org/sdk/x/configurl"
)

// NewTimeoutDialer limits how long opening a connection through base can take.
func NewTimeoutDialer(base transport.StreamDialer, duration time.Duration, message string) (transport.StreamDialer, error) {
	if base == nil {
		return nil, errors.New("timeout: base dialer must not be nil")
	}
	if duration <= 0 {
		return nil, errors.New("timeout: duration must be positive")
	}
	if message == "" {
		return nil, errors.New("timeout: error must not be empty")
	}
	timeoutErr := errors.New(message)
	dialStream := func(ctx context.Context, address string) (transport.StreamConn, error) {
		// Apply a fresh timeout and error cause for each dial.
		dialCtx, cancel := context.WithTimeoutCause(ctx, duration, timeoutErr)
		defer cancel()
		conn, err := base.DialStream(dialCtx, address)
		if err != nil && context.Cause(dialCtx) == timeoutErr {
			return nil, timeoutErr
		}
		return conn, err
	}
	return transport.FuncStreamDialer(dialStream), nil
}

// RegisterTimeout adds the "timeout:t=<duration>&error=<message>" configuration type.
func RegisterTimeout(providers *configurl.ProviderContainer) {
	newInstance := func(ctx context.Context, config *configurl.Config) (transport.StreamDialer, error) {
		// In "timeout:t=1s&error=too+slow", parse the key=value options.
		options, err := url.ParseQuery(config.URL.Opaque)
		if err != nil {
			return nil, fmt.Errorf("timeout: invalid options: %w", err)
		}
		duration, err := time.ParseDuration(options.Get("t"))
		if err != nil {
			return nil, errors.New("timeout: t must be a duration, such as 1s")
		}
		base, err := providers.StreamDialers.NewInstance(ctx, config.BaseConfig)
		if err != nil {
			return nil, err
		}
		return NewTimeoutDialer(base, duration, options.Get("error"))
	}
	providers.StreamDialers.RegisterType("timeout", newInstance)
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

## Step 3: Import and register the components in your app

Create `main.go` at the module root, alongside the `components` directory. The
app imports the library and calls its exported `Register*` functions on the
app's provider container before building a dialer:

```go title="main.go"
package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"

	"example.com/configurl-example/components"
	"golang.getoutline.org/sdk/x/configurl"
)

func main() {
	configText := flag.String("transport", "delay:200ms|timeout:t=1s&error=too+slow", "configurl configuration")
	flag.Parse()
	log.SetFlags(0)

	providers := configurl.NewDefaultProviders()

	// highlight-start
	// Register the "delay" and "timeout" configuration types.
	components.RegisterDelay(providers)
	components.RegisterTimeout(providers)
	// highlight-end

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

## Step 4: Run it and trigger a timeout

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
timeout: t must be a duration, such as 1s
exit status 1
```

## Use components directly

Expose components for direct use as well as through configuration. For example,
this helper constructs the same stack as the app's default configuration using
Go arguments. It belongs in application code that imports your `components`
package, `time`, and `golang.getoutline.org/sdk/transport`:

```go
func newDialer() (transport.StreamDialer, error) {
	delayed, err := components.NewDelayDialer(&transport.TCPDialer{}, 200*time.Millisecond)
	if err != nil {
		return nil, err
	}
	return components.NewTimeoutDialer(delayed, time.Second, "too slow")
}
```

An app can call this helper in place of creating a provider container and
parsing a configurl string. Both approaches use the same component
implementations and validation.

## Share your components with the ecosystem

Publish your component package as a Go module in your own repository, with
exported constructors and `Register*` functions like the ones above. Apps add
your module as a dependency, import your package, and call its registration
functions on their provider container. The component code and registration
helpers stay in your library; each app chooses which components to register.
This lets you make components available to the Outline ecosystem independently
of SDK releases.

Document the supported configuration syntax alongside the direct Go API. Keep
constructors usable on their own so apps that build their transport stacks in
Go can use the same components without configuration strings. A configuration
string can only select components that an app has included and registered;
it does not download a library or register new code automatically.

### Registration scope

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
