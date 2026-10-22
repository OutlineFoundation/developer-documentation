---
title: "Running a Local HTTP Proxy"
sidebar_label: "Local HTTP Proxy"
---

Use the Outline SDK's `http2transport` tool to connect an HTTP proxy client, such
as curl, to an Outline transport. The tool listens locally and makes outgoing
connections using the strategy you choose.

Install [Go](https://go.dev/doc/install), then inspect the available flags:

```sh
go run golang.getoutline.org/sdk/x/tools/http2transport@latest -help
```

Despite its name, `http2transport` means HTTP-to-transport; it is not an HTTP/2
protocol selector.

## Start the Proxy

Start a proxy on your computer's loopback interface:

```sh
go run golang.getoutline.org/sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080
```

Leave it running. In another terminal, use curl to fetch the Cloudflare trace
endpoint through it:

```sh
curl --proxy http://127.0.0.1:8080 https://getoutline.org/cdn-cgi/trace
```

For HTTPS URLs, curl creates a CONNECT tunnel through the proxy and performs TLS
with the destination. Without `-transport`, the proxy connects directly. Press
Ctrl+C in the proxy terminal to stop it.

## Choose an Outgoing Transport

The `-transport` flag accepts a [config URL](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).
For this example, you need an existing Outline server and its `ss://` access key;
see [Set Up an Outline Server](/vpn/getting-started/server-setup-manager) if
you need to create one. Stop the previous proxy and restart it with that key in
place of the placeholder:

```sh
TRANSPORT='ss://YOUR_OUTLINE_ACCESS_KEY'
go run golang.getoutline.org/sdk/x/tools/http2transport@latest \
  -localAddr 127.0.0.1:8080 -transport "$TRANSPORT"
```

Run the curl command again. The trace's `ip` field should now show the remote
server's exit address.

Config URL components can be composed with `|`; quote the full configuration.
See the [config URL reference](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl)
for supported stream transports.

## Proxyless Evasion with Encrypted DNS and TLS Fragmentation

For an [Intra](https://getintra.org/)-style experiment, combine encrypted DNS with
TLS fragmentation. This can help with DNS manipulation and some forms of TLS
handshake blocking. Here, **proxyless** means that website traffic connects
directly from your computer, with no remote proxy server or access key. The local
HTTP proxy lets your applications use the strategy.

Stop the previous listener with Ctrl+C, then start it with this configuration:

```sh
TRANSPORT='tlsfrag:1|doh:name=cloudflare-dns.com&address=1.1.1.1:443'
go run golang.getoutline.org/sdk/x/tools/http2transport@latest \
  -localAddr 127.0.0.1:8080 -transport "$TRANSPORT"
```

The two components work together:

- `tlsfrag:1` splits the initial TLS ClientHello into two TLS records, with one
  payload byte in the first and the remaining bytes in the second.
- `doh:name=cloudflare-dns.com&address=1.1.1.1:443` resolves destination hostnames
  using [Cloudflare DNS over HTTPS](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/).
  `name` supplies the resolver's TLS server name and HTTP hostname. `address`
  supplies its connection address, avoiding a local DNS lookup to find the
  resolver itself.

Order matters: placing `tlsfrag:1` **before** `doh:...` applies fragmentation to
both the resolver's TLS connection and the website's TLS connection. With
`doh:...|tlsfrag:1`, only the website's TLS connection gets fragmented.

In another terminal, compare a direct request with one through the local proxy:

```sh
curl --max-time 15 --write-out '\nHTTP %{http_code}\n' \
  --noproxy '*' https://getoutline.org/cdn-cgi/trace
curl --max-time 15 --write-out '\nHTTP %{http_code}\n' \
  --noproxy '' --proxy http://127.0.0.1:8080 https://getoutline.org/cdn-cgi/trace
```

`--noproxy '*'` bypasses proxy settings for the baseline; `--noproxy ''` makes the
second request use the local proxy even if you have proxy-bypass rules. Curl
passes `getoutline.org` to the proxy, which resolves it over HTTPS. Website
traffic still leaves through your own network's public IP.

On an unrestricted connection, both requests should succeed and their trace
output may look alike. Trace does not report DNS encryption or TLS record
boundaries. To investigate interference, repeat the comparison with an affected
HTTPS URL and compare success, status, and errors. You can also restart the proxy
with only `tlsfrag:1` or only the `doh:...` component to isolate which change helps.

The resolver and destination IP addresses must be reachable. TLS fragmentation
does not encrypt SNI or enable ECH; it changes the handshake's record boundaries.
Only applications configured to use the local HTTP proxy get this behavior.

## What the Proxy Can Test

Configure an application's HTTP proxy setting to `http://127.0.0.1:8080` to send
its supported traffic through this listener. Starting the tool does not change
your system's proxy settings.

This proxy carries TCP streams. It does not provide a UDP tunnel for HTTP/3.
Use [`fetch -proto h3`](https://developer.getoutline.org/sdk/command-line-debugging/#compare-http-versions) to test
QUIC directly. To compare results from different networks, see
[Remote Measurement](remote-measurement.md).
