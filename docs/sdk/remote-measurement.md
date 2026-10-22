---
title: "Measuring Connections from a Remote Network"
sidebar_label: "Remote Measurement"
---

A remote proxy lets you test a connection from another network. Use it with the
Outline SDK's `fetch` tool to compare a direct connection, a connection through
the proxy, and a connection with an additional circumvention strategy.

Start with [Fetch](https://developer.getoutline.org/sdk/command-line-debugging/) for installation, `-help`, verbose
output, HTTP versions, and ECH. For separate tasks, see
[DNS Lookups](dns-debugging.md) and [Local HTTP Proxy](local-http-proxy.md).
The `-transport` examples below use the
[config URL format](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).

## Connect Through an Outline Server

This option requires an existing Outline server and its `ss://` access key.
You can [set up a server](/vpn/getting-started/server-setup-manager), or use
[SSH](#connect-through-ssh) if you already have access to a remote machine.
Replace the placeholder with the access key:

```sh
TUNNEL='ss://YOUR_OUTLINE_ACCESS_KEY'
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -timeout 15 -transport "$TUNNEL" https://getoutline.org/cdn-cgi/trace
```

Compare the trace's `ip`, `loc`, and `colo` fields with a direct request. The `ip`
field identifies the exit address seen by Cloudflare. `loc` is IP geolocation;
it does not establish which access network or subscriber experience you are
measuring. Remove the IP address before sharing output if needed.

## Connect Through SSH

If you have SSH access to a remote machine, start a local SOCKS5 listener. Replace
the user, host, and port with your SSH connection details:

```sh
ssh -N -D 127.0.0.1:1080 -p 22 USER@HOST
```

Leave SSH running. In a second terminal:

```sh
TUNNEL='socks5://127.0.0.1:1080'
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -timeout 15 -transport "$TUNNEL" https://getoutline.org/cdn-cgi/trace
```

An SSH dynamic forward carries TCP connections, so use it with `-proto h1` or
`-proto h2`. It does not support the UDP traffic needed for HTTP/3. Stop the SSH
command with Ctrl+C when finished.

## Identify the Exit IP and Network

Cloudflare trace is usually the best starting point: it reports the exit IP
together with HTTP, TLS, ECH, and serving-data-center details. The website you
ultimately want to test does not have to use Cloudflare. Send a separate request
through the same transport to identify the proxy's exit, then test your target.

Other IP lookup services can add network-operator and location information or
provide an alternative when Cloudflare is unreachable. These examples use
`TUNNEL` from one of the preceding sections. Omit `-transport "$TUNNEL"`
to check your own connection. Install [jq](https://jqlang.org/download/) to format
the JSON, or omit `| jq` to see the raw response.

### IPinfo and SOAX

[IPinfo](https://ipinfo.io/json) returns fields such as `ip`, `org` (ASN and
operator), `city`, `region`, and `country`:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$TUNNEL" https://ipinfo.io/json | jq
```

Keep an alternative for measurements from Iran or China, where IPinfo may be
unreachable. IPinfo [documents GCP infrastructure restrictions affecting Iranian
IP addresses](https://community.ipinfo.io/t/getting-403-forbidden-when-accessing-the-ipinfo-api-and-website/303);
local filtering can also affect access. A failure to reach this service does not
by itself mean the proxy is broken.

The [SOAX checker](https://checker.soax.com/api/ipinfo) returns details inside a
`data` object, including `ip`, `asn`, `aso` (AS operator), `isp`, `carrier`, `city`,
`region`, and country information:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$TUNNEL" https://checker.soax.com/api/ipinfo | jq
```

For just the exit IP, replace `jq` with `jq -r '.ip'` for IPinfo or
`jq -r '.data.ip'` for SOAX. To remove the IP and postal code from SOAX output
before sharing, use `jq 'del(.data.ip, .data.zip)'`.

### An HTTP/3 Alternative

[`ident.me/json`](https://api.ident.me/) is an independent IP lookup service with
JSON fields for the IP, ASN, operator, and location. It also worked over HTTP/3
in a direct test on October 22, 2026:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h3 -timeout 15 -transport "$TUNNEL" https://ident.me/json | jq
```

Use a UDP-capable transport for this command; the SSH SOCKS listener above cannot
carry HTTP/3. Check `HTTP Proto version=HTTP/3.0` in verbose output and the `ip`
field in the JSON. The `asn` and `aso` fields identify the network, and `cc` and
`country` describe its geolocation.

In the same direct checks, IPinfo also returned HTTP/3 successfully; SOAX
returned HTTP/2 successfully but its HTTP/3 request timed out. Treat protocol
support and reachability as properties to check from your measurement network.
These checks do not establish availability from Iran or China.

A lookup reports the address used for that request. A rotating proxy, different
IPv4/IPv6 routes, or different TCP/UDP exits can produce another address for the
next request. Use a stable proxy session when comparing results, and treat
operator and geolocation fields as database estimates.

## Testing Outline Servers

You can use a remote network to check whether people there can reach your
Outline server. Keep two configurations separate: `TUNNEL` is your working
connection to that network, and `SERVER` is the Outline server you want to test.
Use an independent, working tunnel so a failure to reach the server does not
also cut off your measurement path.

### Test a Shadowsocks Server

Set `SERVER` to the `ss://` access key for the server under test. Keep `TUNNEL`
set to one of the working proxies above. Run these commands in the same terminal:

```sh
SERVER='ss://YOUR_SERVER_ACCESS_KEY'

# Baseline: the measurement tunnel can reach the test website.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$TUNNEL" https://getoutline.org/cdn-cgi/trace

# Your computer can reach the Outline server and fetch through it.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$SERVER" https://getoutline.org/cdn-cgi/trace

# The remote network can reach the Outline server and fetch through it.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "${TUNNEL}|${SERVER}" https://getoutline.org/cdn-cgi/trace
```

The last command takes the path **your computer → measurement tunnel → Outline
server → getoutline.org**. The `|` inside the quoted config URL composes the two
connections; it is not a shell pipe. On success, Cloudflare's `ip` field reports
the Outline server's exit address, rather than the measurement tunnel's exit.

If both baselines succeed but the chained request fails, investigate the path
from the remote network to your Outline server. Repeat the tests and compare
verbose errors; a timeout alone does not identify the cause. This tests the
tunnel's exit network, which may differ from the networks your users are on.

### Test Shadowsocks over WebSockets

If your server already offers [Shadowsocks over WebSockets](/vpn/advanced/websockets),
you can test that endpoint through the same measurement tunnel. You need its
public TLS hostname, TCP WebSocket path, and the `cipher` and `secret` from its
server configuration or access-key YAML. An ordinary Outline server needs the
linked WebSocket setup before this example will work.

Replace `YOUR_CIPHER` and `YOUR_SECRET` with those values (the setup guide uses
`chacha20-ietf-poly1305` as its cipher). Replace `YOUR_WS_HOST` with the hostname
from your `wss://` endpoint, and `/YOUR_TCP_PATH` with its TCP path, including the
leading `/`. Use the actual TLS port if it differs from 443. Keep `TUNNEL` set to
your working measurement tunnel:

```sh
SS_USERINFO=$(printf '%s' 'YOUR_CIPHER:YOUR_SECRET' | base64 | tr '/+' '_-' | tr -d '=\n')
SERVER="tls|ws:tcp_path=/YOUR_TCP_PATH|ss://${SS_USERINFO}@YOUR_WS_HOST:443"

# Test the WebSocket endpoint from your computer.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$SERVER" https://getoutline.org/cdn-cgi/trace

# Test the same endpoint from the remote network.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "${TUNNEL}|${SERVER}" https://getoutline.org/cdn-cgi/trace
```

The first line encodes `cipher:secret` as unpadded URL-safe Base64. In `SERVER`,
`tls` secures the WebSocket connection, `ws` selects the server's TCP WebSocket
path, and `ss` supplies the Shadowsocks credentials and WebSocket hostname and
port. This converts the values from the Outline Client's YAML configuration
into the CLI's [config URL format](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl).

These HTTP/2 commands test the TCP WebSocket endpoint. To experiment with
HTTP/3 through this server, configure its UDP WebSocket endpoint too and add
`&udp_path=/YOUR_UDP_PATH` to the `ws:` component. UDP packets are then carried
inside WebSocket connections; successful HTTP/3 here does not show that the
measurement network permits native QUIC traffic to your server.

## Compare Other Connection Strategies

Keep the destination, HTTP version, and timeout the same while changing the
transport. For example, with `TUNNEL` set to one of the proxies above:

```sh
# Direct connection from your computer.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 https://getoutline.org/cdn-cgi/trace

# Connection through the remote proxy.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$TUNNEL" https://getoutline.org/cdn-cgi/trace

# Same proxy, with TLS fragmentation toward the destination.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "${TUNNEL}|tlsfrag:1" https://getoutline.org/cdn-cgi/trace
```

The fragmenting transport wraps the connection provided by the proxy.
`tlsfrag:1` splits the initial TLS ClientHello into two TLS records, with one
payload byte in the first and the rest in the second. The HTTP request stays
the same, so compare whether it succeeds and what status it returns.

A timeout can result from an unreachable proxy, DNS failure, a blocked path, or a
slow server. Check that the proxy itself works, repeat the baseline, and record
the HTTP status and error output before attributing a failure to interference.
A successful request to `getoutline.org` is a useful connectivity check; it does
not establish reachability of other sites.

### Control Where DNS Resolution Happens

For HTTP/1.1 and HTTP/2, the SOCKS5 and Shadowsocks transports can pass the target
hostname to the proxy for resolution. To test a particular IP address instead,
resolve it on your computer and supply it with `-address`. This example uses
`dig`, provided by the `dnsutils` package on Debian and Ubuntu:

```sh
TARGET_IP=$(dig +short getoutline.org A | sed -n '/^[0-9][0-9.]*$/p' | head -n 1)
if [ -n "$TARGET_IP" ]; then
  go run golang.getoutline.org/sdk/x/tools/fetch@latest \
    -v -proto h2 -timeout 15 -transport "$TUNNEL" \
    -address "$TARGET_IP" https://getoutline.org/cdn-cgi/trace
else
  printf '%s\n' 'No IPv4 address found for getoutline.org.' >&2
fi
```

The URL still supplies the HTTP hostname and TLS server name. This experiment
uses local DNS results, which can differ from the remote network's results.
For HTTP/3, `fetch` resolves the destination locally before sending UDP packets.
See [DNS Lookups](dns-debugging.md) to query a specific resolver through a proxy.

### Try ECH and QUIC

Use the [ECH example](https://developer.getoutline.org/sdk/command-line-debugging/#use-encrypted-client-hello-ech)
with `-transport "$TUNNEL"` to test ECH through a proxy. The `dig` query in that
example runs locally; ECH does not move DNS resolution to the remote network.

To test HTTP/3, use an Outline server with UDP support or a SOCKS5 service that
supports UDP ASSOCIATE with a reachable UDP relay. Set `TUNNEL` to that service
first; the SSH listener above will not work. Compare the ordinary request with a
QUIC prelude:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h3 -timeout 15 -transport "$TUNNEL" https://getoutline.org/cdn-cgi/trace

go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h3 -timeout 15 -transport "${TUNNEL}|quicprelude" https://getoutline.org/cdn-cgi/trace
```

Record the tool release, time, proxy exit, destination address, protocol, and
configuration with each result, keeping access keys out of shared records.
Strategies that help on one path may have no effect on another.
