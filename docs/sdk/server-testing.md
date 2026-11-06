---
title: "Testing Outline Servers"
sidebar_label: "Test Outline Servers"
---

Use the Outline SDK's command-line tools to understand your Outline server's
connectivity and troubleshoot TCP and UDP forwarding. Test plain Shadowsocks
and Shadowsocks over WebSockets without installing the Outline Client, then
repeat the tests from another network to see where your server is reachable.

Install [Go](https://go.dev/doc/install) and use a POSIX shell, such as Bash or
Zsh. `go run` downloads and compiles the tool on its first run. See
[Fetch](https://developer.getoutline.org/sdk/command-line-debugging/) for
`-help`, verbose output, and HTTP options, or [DNS Lookups](dns-debugging.md) for
`resolve`. The `-transport` flag accepts a
[config URL](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).

## Choose Your Server Configuration

Set `SERVER` to the connection configuration using **one** of the following
options, then run the tests below in the same terminal. To compare deployments,
change `SERVER` and repeat the same commands.

### Shadowsocks

Use an existing server's `ss://` access key, or
[set up an Outline server](/vpn/getting-started/server-setup-manager). Set
`ACCESS_KEY` to the complete key: replace the entire sample URI below,
including the bracketed placeholders, with your key including its `ss://` prefix.

```sh
ACCESS_KEY='ss://[credentials]@[host]:[port]'
SERVER="$ACCESS_KEY"
```

For plain Shadowsocks, the access key itself is the connection configuration.
The server must accept both TCP and UDP on the access key's port, including in
its host and cloud firewall rules, and be able to forward both to the internet.

### Shadowsocks over WebSockets

This option requires an existing
[Shadowsocks-over-WebSockets deployment](/vpn/advanced/websockets) with both
TCP and UDP WebSocket endpoints. The linked setup guide provides a server
configuration and an access-key YAML containing the values you need:

- `YOUR_CIPHER` and `YOUR_SECRET`: the Shadowsocks cipher and secret. The setup
  guide uses `chacha20-ietf-poly1305` as its cipher.
- `YOUR_WS_HOST`: the hostname from your public `wss://` endpoint. Use its
  actual TLS port if it differs from 443.
- `/YOUR_TCP_PATH` and `/YOUR_UDP_PATH`: the two WebSocket paths, including each
  leading `/`. This example uses the same hostname, port, and credentials for
  both endpoints, as in the setup guide.

```sh
SS_USERINFO=$(printf '%s' 'YOUR_CIPHER:YOUR_SECRET' | base64 | tr '/+' '_-' | tr -d '=\n')
SERVER="tls|ws:tcp_path=/YOUR_TCP_PATH&udp_path=/YOUR_UDP_PATH|ss://${SS_USERINFO}@YOUR_WS_HOST:443"
```

The first line encodes `cipher:secret` as unpadded URL-safe Base64. In `SERVER`,
`tls` secures the WebSocket connection, `ws` selects the TCP or UDP endpoint,
and `ss` supplies the Shadowsocks credentials and WebSocket hostname and port.
This converts the values from the Outline Client's YAML into a CLI config URL.
Keep the entire config quoted so the shell does not interpret `|` or `&`.

## Test TCP and UDP with Fetch

Run both requests with your chosen `SERVER`. HTTP/2 tests TCP forwarding;
HTTP/3 uses QUIC to test UDP forwarding:

```sh
# TCP: fetch over HTTP/2.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$SERVER" https://getoutline.org/cdn-cgi/trace

# UDP: fetch over HTTP/3.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h3 -timeout 15 -transport "$SERVER" https://getoutline.org/cdn-cgi/trace
```

Look for an HTTP 200 response, `HTTP Proto version=HTTP/2.0` or
`HTTP Proto version=HTTP/3.0` in verbose output, and the corresponding `http`
field in the trace. The `ip` field reports your server's exit address as seen
by Cloudflare. TCP and UDP, or IPv4 and IPv6, can use different exit addresses.

| Server configuration | HTTP/2 tests | HTTP/3 tests |
|---|---|---|
| Shadowsocks (`ss://`) | Shadowsocks TCP forwarding | Shadowsocks UDP forwarding |
| Shadowsocks over WebSockets (`tls\|ws\|ss`) | The `tcp_path` endpoint | The `udp_path` endpoint |

With plain Shadowsocks, the UDP test sends UDP packets to your server. With
WebSockets, **both tests connect to the WebSocket endpoint over TLS and TCP**;
the UDP endpoint carries packets inside WebSocket messages. The server still
sends UDP to `getoutline.org`. Successful HTTP/3 over WebSockets therefore
confirms UDP forwarding through that endpoint, but does not demonstrate native
UDP reachability from your computer to the server.

## Test TCP and UDP with DNS

To check forwarding independently of HTTPS and QUIC, query a public DNS
resolver through the same `SERVER`. Use `-tcp` for TCP; omitting it selects UDP:

```sh
# TCP DNS through the server.
go run golang.getoutline.org/sdk/x/tools/resolve@latest \
  -v -tcp -timeout 10 -transport "$SERVER" -resolver 1.1.1.1 -type A getoutline.org

# UDP DNS through the server.
go run golang.getoutline.org/sdk/x/tools/resolve@latest \
  -v -timeout 10 -transport "$SERVER" -resolver 1.1.1.1 -type A getoutline.org
```

Both commands should print IPv4 addresses for `getoutline.org`; `-v` also
prints the DNS response details. With the WebSocket configuration, these
commands test `tcp_path` and `udp_path`, respectively. The resolver's numeric
address avoids a local DNS lookup for the resolver, although a hostname in
your server configuration may still need resolution.

The server must be able to reach the resolver on port 53. If necessary, repeat
with another reachable resolver, such as `-resolver 8.8.8.8`. A successful UDP
DNS query confirms that small UDP exchanges work; it does not guarantee that
QUIC will work, with its different packet sizes and destination port.

## Test from Another Network

First get the tests above working from your computer. Then follow
[Remote Measurement](remote-measurement.md) to set `TUNNEL` to a working
connection into the network you want to measure. Use an independent tunnel;
`SERVER` remains the Outline server under test.

Set both `SERVER` and `TUNNEL` in the terminal where you run the tests. If you
use SSH, keep the SSH command running in a separate terminal, then set `TUNNEL`
in your original terminal alongside `SERVER`.

```sh
# Baseline: the measurement tunnel can reach the test website.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$TUNNEL" https://getoutline.org/cdn-cgi/trace

# TCP forwarding through the Outline server, reached from the remote network.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "${TUNNEL}|${SERVER}" https://getoutline.org/cdn-cgi/trace

# UDP forwarding through the same server, subject to the tunnel support below.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h3 -timeout 15 -transport "${TUNNEL}|${SERVER}" https://getoutline.org/cdn-cgi/trace
```

The combined configuration takes the path **your computer → measurement tunnel
→ Outline server → getoutline.org**. Cloudflare sees the Outline server's exit
address. The `|` inside the quoted config composes the connections.

For **plain Shadowsocks UDP**, `TUNNEL` must also support UDP: use an Outline
server with UDP support or a SOCKS5 proxy with a reachable UDP relay. SSH's
SOCKS listener cannot carry this test. Check the tunnel's UDP baseline by
repeating the first command with `-proto h3` before testing the chain.

For **Shadowsocks over WebSockets**, a TCP-only tunnel, including SSH, can
carry both tests: the connection to either WebSocket endpoint uses TCP. A
direct HTTP/3 request through that TCP-only tunnel would fail, so use the
HTTP/2 tunnel baseline shown above.

You can also repeat the DNS tests with `-transport "${TUNNEL}|${SERVER}"`;
the same TCP/UDP requirements apply. This measures the tunnel's exit network,
which may differ from the access networks your users are on.

## Interpret Failures

If both local server tests and the relevant tunnel baseline succeed, but a
chained request fails, investigate the path from the remote network to your
server. Repeat the baselines and compare verbose errors before attributing a
failure to interference.

If TCP succeeds but UDP fails, check UDP forwarding and firewall rules for
plain Shadowsocks, or the UDP WebSocket path and server listener for
WebSockets. If UDP DNS succeeds but HTTP/3 fails, check the QUIC path and local
DNS too: `fetch` resolves the destination locally for HTTP/3. A timeout alone
does not identify the cause, and success against one destination does not
establish reachability of every site.

Record the tool release, time, measurement network, server configuration,
protocol, and errors with each result. Keep access keys, secrets, and private
WebSocket paths out of shared records. To repeat a test with the same release,
replace `@latest` with a version such as `@v0.2.2`.
