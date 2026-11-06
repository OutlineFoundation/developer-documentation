---
title: "Adding Custom Components"
sidebar_label: "Custom Components"
---

# Adding Custom Components

You can build components for the Outline SDK and share them as a Go library in
your own repository. As the author of that library, you can expose `Register*`
functions that apps call to add configuration types to their registry for the
SDK's [`configurl` package](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).
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
that opens a connection, such as TCP. A **registry** maps each configuration
type name, such as `delay`, to a **parser** for a given component type: a
function that reads that part of
the configuration and builds the component.
[`configurl.NewDefaultRegistry()`][new-default-registry] creates a
[`MutableRegistry`][mutable-registry] with the
[built-in configuration types][built-in] already registered. A
[`Registry`][registry] only looks up parsers; `MutableRegistry` adds
registration. Parsers receive the read-only `Registry`.

Each part of a configuration string is parsed as a URL with Go's `net/url`.
The type name is the URL scheme, and for `delay:200ms`, the text after the
colon, `200ms`, is the URL's opaque part.

To add a type, call [`configurl.Register`][register] with the registry, a name,
and a parser function of type [`configurl.Parser`][parser]. For `delay:200ms`,
the name is `delay`, and the parser reads the duration, builds the dialer it
wraps, and returns the wrapper. A registry stores parsers by Go result type and
name, so `delay` for `transport.StreamDialer` and `delay` for
`transport.PacketDialer` are separate entries. `Register` infers the result
type from the parser's signature, and the type argument of
`configurl.New[T]` selects which entry to use.

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

<!-- RELEASE BLOCKER: Before merging, replace the pseudo-version below with a
released x module version containing OutlineFoundation/outline-sdk#647, then
rerun the examples and verify the Go doc links. -->

Run these commands in a terminal:

```sh
mkdir configurl-example
cd configurl-example
go mod init example.com/configurl-example
go get golang.getoutline.org/sdk/x/configurl@v0.2.3-0.20261030210620-71f60768ef4c
mkdir components
```

This guide pins a version of the SDK's `x` module. Its APIs are experimental,
so keep the version pinned when using them. Use the `golang.getoutline.org`
import paths shown here, including for the core `transport` package; older
examples may use GitHub import paths.

For a runnable example, the library and app live in one module, with the library
in a separate Go package. Keep each component in its own file:

```text
configurl-example/
├── go.mod
├── components/
│   ├── delay.go       # Component library: delay dialer, parser, and registration
│   └── timeout.go     # Component library: timeout dialer, parser, and registration
└── main.go            # App: imports the library and registers its components
```

When publishing your library, the `components` package can live in its own
repository and Go module. Apps then add that module as a dependency and import
its published package path instead of the local example path used below.

## Step 2: Write the component library

The library exposes a constructor and a registration function for each
component. The constructors take Go values and implement the behavior. Each
registration function registers a parser, which turns a configuration string
into constructor arguments.

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

func parseDelayDialer(ctx context.Context, registry configurl.Registry, config *configurl.Config) (transport.StreamDialer, error) {
	// In "delay:200ms", URL.Opaque is "200ms".
	duration, err := time.ParseDuration(config.URL.Opaque)
	if err != nil {
		return nil, errors.New("delay: expected a duration, such as 200ms")
	}
	base, err := configurl.NewFromConfig[transport.StreamDialer](ctx, registry, config.BaseConfig)
	if err != nil {
		return nil, err
	}
	return NewDelayDialer(base, duration)
}

// RegisterDelay adds the "<name>:<duration>" configuration type, such as "delay:200ms".
func RegisterDelay(registry configurl.MutableRegistry, name string) {
	configurl.Register(registry, name, parseDelayDialer)
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

func parseTimeoutDialer(ctx context.Context, registry configurl.Registry, config *configurl.Config) (transport.StreamDialer, error) {
	// In "timeout:t=1s&error=too+slow", parse the key=value options.
	options, err := url.ParseQuery(config.URL.Opaque)
	if err != nil {
		return nil, fmt.Errorf("timeout: invalid options: %w", err)
	}
	duration, err := time.ParseDuration(options.Get("t"))
	if err != nil {
		return nil, errors.New("timeout: t must be a duration, such as 1s")
	}
	base, err := configurl.NewFromConfig[transport.StreamDialer](ctx, registry, config.BaseConfig)
	if err != nil {
		return nil, err
	}
	return NewTimeoutDialer(base, duration, options.Get("error"))
}

// RegisterTimeout adds the "<name>:t=<duration>&error=<message>" configuration type,
// such as "timeout:t=1s&error=too+slow".
func RegisterTimeout(registry configurl.MutableRegistry, name string) {
	configurl.Register(registry, name, parseTimeoutDialer)
}
```

### Parse your configuration

Each parser receives a context, a registry, and a parsed
[`configurl.Config`][config]:

- `config.URL` describes the current part. For `delay:200ms`, its `Scheme` is
  `delay` and its `Opaque` field is `200ms`.
- For `timeout:t=1s&error=too+slow`, `Opaque` holds `t=1s&error=too+slow`.
  `url.ParseQuery(config.URL.Opaque)` turns that text into options. Both `t`
  (a positive duration) and `error` (a nonempty message) are required here.
  These options follow the colon directly; there is no `?`, so `URL.Query()`
  would not read them.
- `config.BaseConfig` describes the parts to the left. Passing it to
  [`configurl.NewFromConfig`][new-from-config] builds the dialer that your
  wrapper uses, which preserves composition. When there are no parts to the
  left, it is `nil`, and the registry returns its default TCP dialer.

The `error` option uses URL query encoding: `too+slow` becomes `too slow`.
Encode literal `&`, `|`, and `+` in values as `%26`, `%7C`, and `%2B`, respectively,
so they do not become separators or spaces. Also encode `?`, `#`, and `%`: URL
parsing removes text after an unencoded `?` or `#` from the opaque part. When
creating configurations in Go, use `url.Values.Encode()` to encode the option
values.

Use [`configurl.New`][new] for a configuration **string** and
[`NewFromConfig`][new-from-config] for an already parsed `*configurl.Config`.
The type argument, `transport.StreamDialer` here, selects which kind of
component to build. Inside a parser, pass `config.BaseConfig`, not `config`
itself: passing the current config would call the same parser again
indefinitely.

Build dependencies with the `registry` and `ctx` your parser receives, never a
registry captured when you registered. An app's registry customizations, such
as a different default dialer, then also apply to your dependencies. The
context is for construction only: the returned dialer uses the context of each
`DialStream` call.

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
must honor its context for the timeout to take effect.

## Step 3: Import and register the components in your app

Create `main.go` at the module root, alongside the `components` directory. The
app imports the library and calls its exported `Register*` functions on the
app's registry before building a dialer. The app chooses each configuration
type's name, which lets it avoid collisions with built-in types or other
libraries:

```go title="main.go"
package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"

	"example.com/configurl-example/components"
	"golang.getoutline.org/sdk/transport"
	"golang.getoutline.org/sdk/x/configurl"
)

func main() {
	configText := flag.String("transport", "delay:200ms|timeout:t=1s&error=too+slow", "configurl configuration")
	flag.Parse()
	log.SetFlags(0)

	registry := configurl.NewDefaultRegistry()

	// highlight-start
	// Register the "delay" and "timeout" configuration types.
	components.RegisterDelay(registry, "delay")
	components.RegisterTimeout(registry, "timeout")
	// highlight-end

	dialer, err := configurl.New[transport.StreamDialer](context.Background(), registry, *configText)
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

An app can call this helper in place of creating a registry and
parsing a configuration string. Both approaches use the same component
implementations and validation.

## Share your components with the ecosystem

Publish your component package as a Go module in your own repository, with
exported constructors and `Register*` functions like the ones above. Apps add
your module as a dependency, import your package, and call its registration
functions on their registry. The component code and registration
helpers stay in your library; each app chooses which components to register.
This lets you make components available to the Outline ecosystem independently
of SDK releases.

Document the supported configuration syntax alongside the direct Go API. Keep
constructors usable on their own so apps that build their transport stacks in
Go can use the same components without configuration strings. A configuration
string can only select components that an app has included and registered;
it does not download a library or register new code automatically.

### Registration scope

Registration belongs to the registry you configured: a new `NewDefaultRegistry()` call
does not inherit your custom types, and registering here does not add `delay`
or `timeout` to other applications or prebuilt SDK tools. Register types during
application setup, before building or using components from the registry. Use
a distinct lowercase name: URL parsing lowercases schemes, so a type registered
as `Delay` never matches. Registering an existing name for the same result type
replaces its parser.

To replace a default base underneath every configuration (the TCP stream
dialer, UDP packet dialer, or UDP packet listener), for example with one that
protects sockets on Android, call [`configurl.RegisterBase`][register-base]
with a parser for that result type. See
[Custom base components](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Custom_base_components).

If a configuration names a type that the registry doesn't have,
`configurl.New` returns an error matching `errors.ErrUnsupported`, which you
can check with `errors.Is`. Malformed options return your parser's error
instead.

These examples register stream dialers only. Registrations are specific to a
parser's Go result type. For datagram connections, write a parser that returns
`transport.PacketDialer` or `transport.PacketListener` and register it with the
same `configurl.Register` function. A stream registration does not enable the
same name for packet dialers or packet listeners.

To implement your own strategy, replace the option parsing and wrappers with
your configuration format and dialer implementation. For wrappers, keep the
`NewFromConfig` call on `BaseConfig` so they compose with existing strategies. For the complete
API, see [Defining custom strategies](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Defining_custom_strategies)
and the [SDK's dialer concepts](/sdk/concepts#dialers).

[new-default-registry]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#NewDefaultRegistry
[built-in]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Built_in_components
[registry]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#Registry
[register-base]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#RegisterBase
[mutable-registry]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#MutableRegistry
[register]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#Register
[parser]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#Parser
[config]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#Config
[new-from-config]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#NewFromConfig
[new]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#New
