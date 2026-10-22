---
title: "Fetching Webpages from the Command Line"
sidebar_label: "Fetch"
---

The Outline SDK is a library for building network connections with configurable
strategies, such as proxies and TLS fragmentation. Its command-line tools let you
try those strategies without writing an application: keep the request the same,
change how it connects, and compare the result.

Start with `fetch` to inspect a connection to `getoutline.org`, then try HTTP/3
over QUIC, encrypt the TLS server name with Encrypted Client Hello (ECH), and
experiment with custom transports. You only need Go and an internet connection
for this guide; no Outline server or account is required.

For other tasks, see [DNS Lookups](dns-debugging.md),
[Local HTTP Proxy](local-http-proxy.md), and
[Remote Measurement](remote-measurement.md).

## Get Started

Install [Go](https://go.dev/doc/install), then run:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest https://getoutline.org/cdn-cgi/trace
```

`go run` downloads and runs the tool; the first run may take longer while Go
compiles it. These examples use a POSIX shell, such as Bash or Zsh.

The response is a short connection report from Cloudflare. Find `http` to see
the HTTP version and `ip` to see your public IP address. Later, you will change
the protocol and enable ECH, then see the differences in this same report.
To fetch the site's HTML instead, use `https://getoutline.org` as the URL.

Use `-help` to see all flags and their defaults:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest -help
```

Put flags **before** the URL. To repeat a measurement with the same tool version,
replace `@latest` with a specific release, such as `@v0.2.2`.

## Inspect the Response

Enable verbose output with `-v`. Use `-method HEAD` to request headers without
downloading the response body:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest -v -method HEAD https://getoutline.org
```

Verbose output includes the HTTP version, status, and response headers. The tool
writes diagnostics to standard error and the response body to standard output,
so you can save them separately:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest -v https://getoutline.org \
  > page.html 2> fetch.log
```

The default request timeout is five seconds. Use `-timeout 15` for a slower
connection. `fetch` does not follow redirects: inspect the status and `Location`
header, then request the new URL if needed. A completed request can return an
HTTP error status, so check the status as well as the tool's exit code.

### Inspect the Connection with Cloudflare Trace

`getoutline.org` uses Cloudflare, whose
[`/cdn-cgi/trace` endpoint](https://developers.cloudflare.com/fundamentals/reference/cdn-cgi-endpoint/)
returns connection details in a small text response:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest -v https://getoutline.org/cdn-cgi/trace
```

Look for these fields in the response body:

| Field | What to check |
|---|---|
| `http` | HTTP version used for the request |
| `tls` | Negotiated TLS version |
| `sni` | Whether the server name was sent in plaintext or encrypted |
| `ip` | Client IP address as seen by Cloudflare; a proxy's exit IP when using one |
| `colo` | Cloudflare data center serving the request |
| `loc` | Country associated with the client IP address |

Use a GET request here (the default): `HEAD` omits the body containing these
fields. Remove the `ip` value before sharing output if you do not want to disclose
that address.

## Compare HTTP Versions

Select the protocol with `-proto`. The default is `h1` (HTTP/1.1):

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest -v -proto h1 https://getoutline.org/cdn-cgi/trace
go run golang.getoutline.org/sdk/x/tools/fetch@latest -v -proto h2 https://getoutline.org/cdn-cgi/trace
go run golang.getoutline.org/sdk/x/tools/fetch@latest -v -proto h3 https://getoutline.org/cdn-cgi/trace
```

HTTP/1.1 and HTTP/2 use TCP for these HTTPS requests. HTTP/3 uses QUIC over UDP.
Check the reported HTTP version and the trace's `http` field. If HTTP/3 fails
while HTTP/2 succeeds, check UDP reachability and any proxy's UDP support; a
timeout alone does not establish blocking.

With `-v`, an HTTP/3 request also reports the negotiated QUIC version. QUIC
versions are distinct from HTTP versions; the HTTP version here is HTTP/3.

## Use Encrypted Client Hello (ECH)

ECH encrypts the part of the TLS ClientHello that carries the destination server
name. It requires a configuration published by the site. `fetch` accepts this
configuration through `-ech-config`; it does not retrieve it automatically.

Use `dig` to query the site's HTTPS DNS record. On Debian and Ubuntu, `dig` is
provided by the `dnsutils` package.

```sh
dig +short getoutline.org HTTPS
```

Find the base64 value of the `ech` parameter. Retrieve a fresh value rather than
reusing one from an old example, since configurations can change. This shell
snippet extracts the first advertised value and runs the request only if it
found one:

```sh
ECH_CONFIG=$(dig +short getoutline.org HTTPS | sed -nE 's/.* ech="?([^"[:space:]]+)"?.*/\1/p' | head -n 1)
if [ -n "$ECH_CONFIG" ]; then
  go run golang.getoutline.org/sdk/x/tools/fetch@latest \
    -v -proto h2 -ech-config "$ECH_CONFIG" https://getoutline.org/cdn-cgi/trace
else
  printf '%s\n' 'No ECH configuration found in the HTTPS record.' >&2
fi
```

Check for `sni=encrypted` in the trace response. You can also use `-proto h3` in
this command to try ECH over QUIC. If the configuration is rejected, retrieve the
HTTPS record again and retry. An empty lookup may mean the resolver does not
return HTTPS records or the site is not advertising ECH.

ECH does not hide the destination IP address or encrypt DNS lookups. See
[DNS Lookups](dns-debugging.md) for resolver experiments and
[Cloudflare's ECH documentation](https://developers.cloudflare.com/ssl/edge-certificates/ech/)
for how Cloudflare uses ECH.

## Try a Transport Configuration

The `-transport` flag accepts a [config URL](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).
A config URL describes a connection strategy, such as a proxy or TLS
fragmentation. Components separated by `|` build on the transport to their left.
Quote the entire value so the shell does not interpret `|` or `&`.

For example, `tlsfrag:1` splits the initial TLS ClientHello into two TLS records:
the first carries one byte of the original record's payload, and the second
carries the rest. Try it with HTTP/2:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest -v -proto h2 \
  -transport 'tlsfrag:1' https://getoutline.org/cdn-cgi/trace
```

Compare success or failure with the direct HTTP/2 request above. On a working
connection, the response can look identical: you changed the handshake's
structure, not the HTTP request. On a network that interferes with TLS handshakes,
that change may affect whether the request succeeds.

For HTTP/3, `quicprelude` sends extra datagrams before packets that may carry a
QUIC ClientHello. Compare the result with the direct HTTP/3 request above:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest -v -proto h3 \
  -transport 'quicprelude' https://getoutline.org/cdn-cgi/trace
```

Transport components must support the kind of connection being tested:
`tlsfrag` operates on TCP streams, while `quicprelude` operates on UDP packets.
The [config URL reference](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl)
lists available components and their parameters.

To test these strategies from another network, continue with
[Remote Measurement](remote-measurement.md).
