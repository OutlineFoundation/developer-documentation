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

You can also test a strategy without a remote server. For example, restart the
proxy with [TLS fragmentation](https://developer.getoutline.org/sdk/command-line-debugging/#try-a-transport-configuration):

```sh
go run golang.getoutline.org/sdk/x/tools/http2transport@latest \
  -localAddr 127.0.0.1:8080 -transport 'tlsfrag:1'
```

Config URL components can be composed with `|`; quote the full configuration.
See the [config URL reference](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl)
for supported stream transports.

## What the Proxy Can Test

Configure an application's HTTP proxy setting to `http://127.0.0.1:8080` to send
its supported traffic through this listener. Starting the tool does not change
your system's proxy settings.

This proxy carries TCP streams. It does not provide a UDP tunnel for HTTP/3.
Use [`fetch -proto h3`](https://developer.getoutline.org/sdk/command-line-debugging/#compare-http-versions) to test
QUIC directly. To compare results from different networks, see
[Remote Measurement](remote-measurement.md).
