---
title: "Extending the Smart Dialer"
sidebar_label: "Smart Dialer Extensions"
---

# Extending the Smart Dialer

The [Smart Dialer](/sdk/reference/smart-dialer-config) tests the strategies
listed in a YAML config and picks one that reaches your test domains. You can
make your own components available to it in two ways:

- **Config URL types** are the `configurl` configuration types, such as
  `delay` and `timeout` from [Adding Custom Components](/sdk/extend-configurl).
  Once registered, they can appear in `tls` entries and in `fallback` strings.
- **Fallback types** read structured YAML under their own key in the
  `fallback` list. The SDK's optional Psiphon fallback works this way.

Start from the module you built in Adding Custom Components. You will run the
Smart Dialer from a Go program, then expose the same registrations to Android
and iOS apps with [Go Mobile](https://go.dev/wiki/Mobile). The examples need
internet access to reach a test domain.

## How the Smart Dialer uses your registrations

The Smart Dialer searches in phases. It races the `dns` entries and keeps the
first resolver that resolves every test domain. It then races the `tls`
entries, which are config URLs, on top of that resolver. Only if no DNS
resolver works, or no TLS entry works on the selected resolver, does it race
the `fallback` entries, which are complete dialers such as proxies.

Apps usually run the Smart Dialer through the SDK's
[`mobileproxy`](https://pkg.go.dev/golang.getoutline.org/sdk/x/mobileproxy)
package, which is designed for Go Mobile: it wraps the Smart Dialer and a local
proxy in types that Kotlin and Swift can call.
[`mobileproxy.SmartDialerOptions`][smart-dialer-options] holds a configurl
registry. [`ConfigURLRegistry()`][config-url-registry] returns it, already
populated with the built-in types; register your config URL types there. Each
kind of entry uses that registry differently:

| Config entry | How it is built |
|---|---|
| `tls: ["delay:100ms\|tlsfrag:1"]` | With a registry whose default stream dialer connects through the selected DNS resolver. |
| `fallback: ["delay:100ms\|split:2"]` | With the options' registry and its default stream dialer (direct TCP, unless you replace it), regardless of which DNS resolver was selected. |
| `fallback: [{paced: {...}}]` | By the fallback parser registered for the key `paced`. |

The default stream dialer is what `NewFromConfig` returns for a `nil` config,
at the left end of every config URL. For TLS tests, the Smart Dialer wraps
your registry to substitute the selected resolver's dialer as that default.
That is why parsers must build dependencies with the `registry` they receive,
as [Adding Custom Components](/sdk/extend-configurl#parse-your-configuration)
explains: a captured registry would bypass the resolver being tested. The
selected TLS strategy applies to connections on ports 443 and 853; other ports
use the selected resolver without it. A selected fallback applies to every
port.

A **fallback parser** is a [`smart.FallbackParser`][fallback-parser]. Each
fallback entry is a YAML object with exactly one key, the fallback type. The
parser receives the value under that key as a [`smart.YAMLNode`][yaml-node]:
`map[string]any` for an object, `[]any` for a list, or a `string`, `bool`, Go
number, or `nil`. It returns a stream dialer and a short **signature** that
identifies the entry in the Smart Dialer's logs. A fallback parser has no
registry parameter, so to build nested config URLs it uses a registry it
captured at registration time. As with config URL parsers, its `ctx` is for
construction only and is cancelled when the search ends.

## Step 1: Update the module

In your `configurl-example` directory, run:

<!-- RELEASE BLOCKER: Before merging, replace the pseudo-version below with a
released x module version containing OutlineFoundation/outline-sdk#649, then
rerun the examples and verify the Go doc links. -->

```sh
go get golang.getoutline.org/sdk/x@v0.2.3-0.20261106052654-c60acdb5f6f7
mkdir mobilecomponents smartdialer
```

This pins a version of the `x` module that includes the Smart Dialer
registration APIs. You will add three Go files and two configs:

```text
configurl-example/
├── components/
│   ├── delay.go          # From Adding Custom Components
│   ├── timeout.go        # From Adding Custom Components
│   └── paced.go          # New: paced fallback parser
├── mobilecomponents/
│   └── mobilecomponents.go  # New: registration helpers for mobile apps
├── smartdialer/
│   └── main.go           # New: app that runs the Smart Dialer
├── smart.yaml            # New: Smart Dialer config with TLS strategies
├── fallback.yaml         # New: Smart Dialer config that needs a fallback
└── main.go               # From Adding Custom Components
```

## Step 2: Add a fallback type

The `paced` fallback reads three options, builds the `transport` config URL with
the registry, and wraps the result with the delay and timeout constructors from
the component library:

```yaml
fallback:
  - paced:
      transport: "split:2"
      delay: 100ms
      timeout: 2s
```

Create `components/paced.go`:

```go title="components/paced.go"
package components

import (
	"context"
	"errors"
	"fmt"
	"time"

	"golang.getoutline.org/sdk/transport"
	"golang.getoutline.org/sdk/x/configurl"
	"golang.getoutline.org/sdk/x/smart"
)

// NewPacedFallbackParser returns a Smart Dialer fallback parser for entries such as
//
//	paced: {transport: "split:2", delay: 100ms, timeout: 2s}
//
// It builds transport with registry, then adds a delay and a timeout around it.
func NewPacedFallbackParser(registry configurl.Registry) smart.FallbackParser {
	parse := func(ctx context.Context, node smart.YAMLNode) (transport.StreamDialer, string, error) {
		options, ok := node.(map[string]any)
		if !ok {
			return nil, "", errors.New("paced: expected an object with transport, delay, and timeout")
		}
		for key := range options {
			if key != "transport" && key != "delay" && key != "timeout" {
				return nil, "", fmt.Errorf("paced: unknown option %q", key)
			}
		}
		transportConfig, ok := options["transport"].(string)
		if !ok {
			return nil, "", errors.New("paced: transport must be a config URL string")
		}
		delayText, _ := options["delay"].(string)
		delay, err := time.ParseDuration(delayText)
		if err != nil {
			return nil, "", errors.New("paced: delay must be a duration, such as 100ms")
		}
		timeoutText, _ := options["timeout"].(string)
		timeout, err := time.ParseDuration(timeoutText)
		if err != nil {
			return nil, "", errors.New("paced: timeout must be a duration, such as 2s")
		}
		base, err := configurl.New[transport.StreamDialer](ctx, registry, transportConfig)
		if err != nil {
			return nil, "", err
		}
		delayed, err := NewDelayDialer(base, delay)
		if err != nil {
			return nil, "", err
		}
		dialer, err := NewTimeoutDialer(delayed, timeout, "paced: timed out")
		if err != nil {
			return nil, "", err
		}
		// The Smart Dialer logs this signature after the fallback type name.
		signature := fmt.Sprintf("transport=%q delay=%v timeout=%v", transportConfig, delay, timeout)
		return dialer, signature, nil
	}
	return parse
}
```

The parser rejects unknown options so that a misspelled key fails instead of
being ignored. YAML reads `100ms` and `2s` as strings, so the parser converts
them with `time.ParseDuration`; `transport: ""` selects the registry's default
dialer. The Smart Dialer logs the signature, so leave out secrets, such as
passwords, that your own options carry.

`NewPacedFallbackParser` takes a [`configurl.Registry`][registry] rather than
Smart Dialer options, so Go apps can use it with any registry. The next step
connects it to the options.

## Step 3: Add registration helpers for mobile apps

Go Mobile skips generic functions, such as `configurl.Register`, and functions
that take Go function values, so Kotlin and Swift can't call them. It does bind
exported functions whose parameters are supported types, including types from
other packages bound at the same time. By convention, a component library
therefore publishes helpers shaped like
`RegisterCustomComponent(opts *mobileproxy.SmartDialerOptions, name string)`,
which perform the registration in Go. The SDK's Psiphon fallback provides
`psiphon.RegisterFallbackParser(opts, name)` in the same way.

Publish these helpers in their own package, such as `yourlib/mobile`, next to
your library's Go API. Go-only users then don't depend on `mobileproxy`, and
gomobile sees only functions it can bind. In this example, that package is
`mobilecomponents`. Create `mobilecomponents/mobilecomponents.go`:

```go title="mobilecomponents/mobilecomponents.go"
// Package mobilecomponents registers the example components on Smart Dialer options.
// Bind it with gomobile alongside mobileproxy.
package mobilecomponents

import (
	"example.com/configurl-example/components"
	"golang.getoutline.org/sdk/x/mobileproxy"
)

// RegisterDelay adds the delay config URL type under name.
func RegisterDelay(opts *mobileproxy.SmartDialerOptions, name string) {
	components.RegisterDelay(opts.ConfigURLRegistry(), name)
}

// RegisterTimeout adds the timeout config URL type under name.
func RegisterTimeout(opts *mobileproxy.SmartDialerOptions, name string) {
	components.RegisterTimeout(opts.ConfigURLRegistry(), name)
}

// RegisterPacedFallback adds the paced fallback type under name.
func RegisterPacedFallback(opts *mobileproxy.SmartDialerOptions, name string) {
	opts.RegisterFallbackParser(name, components.NewPacedFallbackParser(opts.ConfigURLRegistry()))
}
```

`RegisterPacedFallback` passes the options' registry to the fallback parser.
A `paced` entry can then use your custom types and any default dialer
registered there, for example `transport: "delay:50ms|split:2"`. Go apps that
use [`smart.FinderConfig`][finder-config] directly can call the `components`
functions instead; see
[Use the Smart Dialer without mobileproxy](#use-the-smart-dialer-without-mobileproxy).

## Step 4: Run the Smart Dialer

Create `smartdialer/main.go`. It uses the same `mobileproxy` API that the
mobile app will use:

```go title="smartdialer/main.go"
package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"os"

	"example.com/configurl-example/mobilecomponents"
	"golang.getoutline.org/sdk/x/mobileproxy"
)

func main() {
	configPath := flag.String("config", "smart.yaml", "Smart Dialer YAML config")
	domain := flag.String("domain", "www.google.com", "test domain with HTTPS on port 443")
	flag.Parse()
	log.SetFlags(0)

	config, err := os.ReadFile(*configPath)
	if err != nil {
		log.Fatal(err)
	}
	testDomains := mobileproxy.NewListFromLines(*domain)
	opts := mobileproxy.NewSmartDialerOptions(testDomains, string(config))
	opts.SetLogWriter(mobileproxy.NewStderrLogWriter())

	// highlight-start
	// Register the custom config URL types and fallback type before searching.
	mobilecomponents.RegisterDelay(opts, "delay")
	mobilecomponents.RegisterTimeout(opts, "timeout")
	mobilecomponents.RegisterPacedFallback(opts, "paced")
	// highlight-end

	dialer, err := opts.NewStreamDialer()
	if err != nil {
		log.Fatal(err)
	}
	conn, err := dialer.DialStream(context.Background(), *domain+":443")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	fmt.Println("connected to", *domain)
}
```

Create `smart.yaml` at the module root. Its first TLS strategy always fails,
because its two-second delay sits inside a 100-millisecond timeout. The second
strategy waits 100 milliseconds and then fragments the TLS ClientHello:

```yaml title="smart.yaml"
dns:
  - system: {}
tls:
  - "delay:2s|timeout:t=100ms&error=too+slow"
  - "delay:100ms|tlsfrag:1"
```

Run the program:

```sh
go mod tidy
go run ./smartdialer
```

The Smart Dialer writes its search log to standard error. Durations and IP
addresses vary; this excerpt shows the relevant lines:

```text
🏆 selected DNS resolver system: {}
...
🏁 failed to dial: 'delay:2s|timeout:t=100ms&error=too+slow' (domain: www.google.com.), duration=100.977376ms, dial_error=too slow ❌
...
🏁 success: 'delay:100ms|tlsfrag:1' (domain: www.google.com.), duration=266.759578ms, status=ok ✅
🏆 selected TLS strategy 'delay:100ms|tlsfrag:1' in 0.37s

connected to www.google.com
```

If `www.google.com` is unreachable from your network, pass another domain that
serves HTTPS on port 443 with `-domain`.

## Step 5: Fall back to the custom fallback type

Create `fallback.yaml`. Its DNS resolver works, but its only TLS strategy
fails, so the Smart Dialer moves on to the fallbacks:

```yaml title="fallback.yaml"
dns:
  - system: {}
tls:
  - "delay:2s|timeout:t=100ms&error=too+slow"
fallback:
  - paced:
      transport: "split:2"
      delay: 100ms
      timeout: 2s
```

Run the program with it:

```sh
go run ./smartdialer -config fallback.yaml
```

After the TLS strategy fails, the Smart Dialer passes the `paced` value to your
fallback parser and tests the dialer it returns. The log shows the signature
after the fallback type name:

```text
🏁 failed to dial: 'delay:2s|timeout:t=100ms&error=too+slow' (domain: www.google.com.), duration=100.659136ms, dial_error=too slow ❌
...
🏆 selected fallback 'paced:transport="split:2" delay=100ms timeout=2s' in 0.28s

connected to www.google.com
```

If the app forgets to register a type, the log shows the failed entry and the
search moves on. For example, without `RegisterPacedFallback`, the log shows
`❌ Failed to create fallback[0]: ... unsupported fallback type: paced`, and an
unregistered config URL type in a TLS entry shows `❌ Failed to create tls[N]`.
When every entry fails, `NewStreamDialer` returns an error.

## Step 6: Use the helpers in a mobile app

An app can include only one library generated by Go Mobile, because each one
embeds the Go runtime. A component library therefore doesn't ship its own
Android Archive or iOS framework, and a prebuilt `mobileproxy` library can't
gain new types. Instead, the app runs one `gomobile bind` that lists
`mobileproxy` and the helper packages of every component library it uses.
Binding them together also lets them share the generated `SmartDialerOptions`
type.

Add Go Mobile to the module as a tool, pinning the version the SDK uses, and
build its commands. As a tool dependency, it stays in `go.mod` when you run
`go mod tidy`:

```sh
go get -tool golang.org/x/mobile/cmd/gomobile@v0.0.0-20240520174638-fa72addaaa1b
go get -tool golang.org/x/mobile/cmd/gobind@v0.0.0-20240520174638-fa72addaaa1b
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

Then generate the library for your platform. These commands replace the
`gomobile bind` step in
[Add Outline SDK to your mobile app](/sdk/mobile-app-integration#step-1-building-mobileproxy-mobile-libraries).
Building for Android requires the Android SDK and NDK (`ANDROID_HOME` and
`ANDROID_NDK_HOME`); building for iOS requires Xcode on macOS:

```sh
# Android
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" golang.getoutline.org/sdk/x/mobileproxy example.com/configurl-example/mobilecomponents
# iOS
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" golang.getoutline.org/sdk/x/mobileproxy example.com/configurl-example/mobilecomponents
```

Add the generated library to your app as that guide describes. The iOS
framework's Swift module is named after the `-o` file, here `Mobileproxy`, and
contains both packages.

Call the helpers after creating the options and before creating the dialer.
`newStreamDialer` runs network tests and can take several seconds, so call it
off the main thread:

```kotlin title="Android (Kotlin)"
import mobilecomponents.Mobilecomponents
import mobileproxy.Mobileproxy

// Run on a background thread, for example with Dispatchers.IO.
val testDomains = Mobileproxy.newListFromLines("www.google.com")
val config = "..." // Smart Dialer YAML, such as fallback.yaml.
val options = Mobileproxy.newSmartDialerOptions(testDomains, config)
Mobilecomponents.registerDelay(options, "delay")
Mobilecomponents.registerTimeout(options, "timeout")
Mobilecomponents.registerPacedFallback(options, "paced")

try {
    val dialer = options.newStreamDialer()
    // Use port zero to let the system pick an open port for you.
    val proxy = Mobileproxy.runProxy("localhost:0", dialer)
    // Configure your networking library with proxy.address().
} catch (e: Exception) {
    // No strategy worked, or the proxy could not start.
}
```

```swift title="iOS (Swift)"
import Mobileproxy

// Run in a background task.
func startSmartProxy() throws -> MobileproxyProxy? {
    let testDomains = MobileproxyNewListFromLines("www.google.com")
    let config = "..." // Smart Dialer YAML, such as fallback.yaml.
    guard let options = MobileproxyNewSmartDialerOptions(testDomains, config) else { return nil }
    MobilecomponentsRegisterDelay(options, "delay")
    MobilecomponentsRegisterTimeout(options, "timeout")
    MobilecomponentsRegisterPacedFallback(options, "paced")

    let dialer = try options.newStreamDialer()
    var proxyError: NSError?
    // Use port zero to let the system pick an open port for you.
    let proxy = MobileproxyRunProxy("localhost:0", dialer, &proxyError)
    if let proxyError { throw proxyError }
    return proxy
}
```

When you publish a component library, document its helper names, the YAML or
config URL syntax of each type, and the package paths that apps must add to
their `gomobile bind` command.

## Registration rules

- Register everything before calling `NewStreamDialer`. Each call copies the
  fallback registrations when it starts but shares the registry, so don't
  change the registry while dialers are being built or used.
- To replace the default stream dialer, for example with one that protects
  sockets on Android, write a bound Go helper, such as
  `RegisterProtectedBase(opts, protector)`, that calls
  [`configurl.RegisterBase`][register-base] on `opts.ConfigURLRegistry()`. To
  keep `system` DNS entries working, the parser must return a
  `*transport.TCPDialer`; set its `Dialer.Control` field to protect sockets.
  If your config uses `udp` DNS entries or packet dialers, also register a
  `transport.PacketDialer` base the same way.
- [`SetConfigURLRegistry`][set-config-url-registry] replaces the registry and
  is available only from Go. If you use it, call it before every `Register*`
  helper: the helpers register on, or capture, the registry in place when they
  run.
- Registrations belong to one `SmartDialerOptions` value. Other options, and
  `mobileproxy.NewStreamDialerFromConfig`, don't see them. To use custom types
  without the Smart Dialer on mobile, write a bound helper that builds a dialer
  from your own registry and returns it as a `*mobileproxy.StreamDialer`.
- The Smart Dialer builds dialers for several entries concurrently and doesn't
  close the ones that lose. A fallback parser that starts background work, such
  as a tunnel, must handle concurrent and abandoned instances.
- With [`SetStrategyCache`][set-strategy-cache], the winning entry is replayed
  on the next search, so keep its types registered under the same names.
  Registering an existing fallback name replaces its parser.

## Use the Smart Dialer without mobileproxy

Go apps can configure a [`smart.Finder`][finder] directly with
[`smart.NewFinderConfig`][new-finder-config]. Register components on a registry,
pass it to the finder config, and register fallback parsers that capture the
same registry:

```go
func newSmartDialer(ctx context.Context, testDomains []string, config []byte) (transport.StreamDialer, error) {
	registry := configurl.NewDefaultRegistry()
	components.RegisterDelay(registry, "delay")
	components.RegisterTimeout(registry, "timeout")
	finder, err := smart.NewFinderConfig().
		SetConfigURLRegistry(registry).
		RegisterFallbackParser("paced", components.NewPacedFallbackParser(registry)).
		New()
	if err != nil {
		return nil, err
	}
	return finder.NewDialer(ctx, testDomains, config)
}
```

`New` checks the settings without network access; `NewDialer` runs the search.
A finder doesn't modify the registry, so several finders can share one after
registration is complete.

[smart-dialer-options]: https://pkg.go.dev/golang.getoutline.org/sdk/x/mobileproxy#SmartDialerOptions
[config-url-registry]: https://pkg.go.dev/golang.getoutline.org/sdk/x/mobileproxy#SmartDialerOptions.ConfigURLRegistry
[set-config-url-registry]: https://pkg.go.dev/golang.getoutline.org/sdk/x/mobileproxy#SmartDialerOptions.SetConfigURLRegistry
[set-strategy-cache]: https://pkg.go.dev/golang.getoutline.org/sdk/x/mobileproxy#SmartDialerOptions.SetStrategyCache
[fallback-parser]: https://pkg.go.dev/golang.getoutline.org/sdk/x/smart#FallbackParser
[yaml-node]: https://pkg.go.dev/golang.getoutline.org/sdk/x/smart#YAMLNode
[registry]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#Registry
[register-base]: https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#RegisterBase
[finder]: https://pkg.go.dev/golang.getoutline.org/sdk/x/smart#Finder
[finder-config]: https://pkg.go.dev/golang.getoutline.org/sdk/x/smart#FinderConfig
[new-finder-config]: https://pkg.go.dev/golang.getoutline.org/sdk/x/smart#NewFinderConfig
