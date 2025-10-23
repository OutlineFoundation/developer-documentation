Project: /outline/_project.yaml
Book: /outline/_book.yaml

# Remotely Characterizing and Bypassing Network Interference with the Outline SDK

This guide demonstrates how to use the Outline SDK's command line tools to
understand and circumvent network interference from a remote perspective. You
will learn how to use the SDK's tools to measure network interference, test
circumvention strategies, and analyze the results. This guide will focus on the
`resolve`, `fetch`, and `http2transport` tools.

## Getting Started with Outline SDK Tools

You can start using the Outline SDK tools directly from the command line.

### Resolve DNS

The `resolve` tool lets you perform DNS lookups with a specified resolver.

To resolve a domain's A record:

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

To resolve a CNAME record:

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### Fetch a Webpage

The `fetch` tool can be used to retrieve the content of a webpage.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest https://example.com
```

It can also force the connection to use QUIC.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### Use a Local Proxy

The `http2transport` tool creates a local proxy to route your traffic through.
To start a local proxy with a Shadowsocks transport:

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

You can then use this proxy with other tools like curl:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## Specify Circumvention Strategies

The Outline SDK allows for the specification of various circumvention strategies
that can be combined to bypass different forms of network interference. The
specification for these strategies is in the [go documentation](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x@v0.0.3/configurl).

### Composable Strategies

These strategies can be combined to create more robust circumvention techniques.

* **DNS-over-HTTPS with TLS Fragmentation**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`
* **SOCKS5-over-TLS with Domain Fronting**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`
* **Multi-hop Routing with Shadowsocks**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## Remote Access and Measurement

To measure network interference as it's experienced in different regions, you
can use remote proxies. You can find or create remote proxies to connect to.

### Remote Access Options

Using the `fetch` tool you can test connections remotely in various ways.

#### Outline Server

Connect remotely to a standard Outline server with a Shadowsocks transport.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 over SSH

Create a SOCKS5 proxy using an SSH tunnel.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

Connect to that tunnel using fetch

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## Case Study: Bypassing YouTube Blocking in Iran

Here's a practical example of detecting and bypassing network interference.

### Detect the Block

When trying to fetch the YouTube homepage through an Iranian proxy, the request
times out, indicating a block.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

This command fails with a timeout.

### Bypass with TLS Fragmentation

By adding TLS fragmentation to the transport, we can bypass this block.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

This command successfully retrieves the title of the YouTube homepage, which is
`<title>YouTube</title>`.

### Bypass with TLS Fragmentation and DNS-over-HTTPS

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

This also successfully returns `<title>YouTube</title>`.

### Bypass with an Outline Server

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

This too returns `<title>YouTube</title>`.

## Further Analysis and Resources

For discussions and questions, visit the [Outline SDK Discussion Group](https://github.com/Jigsaw-Code/outline-sdk/discussions).

