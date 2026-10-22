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
TRANSPORT='ss://YOUR_OUTLINE_ACCESS_KEY'
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -timeout 15 -transport "$TRANSPORT" https://getoutline.org/cdn-cgi/trace
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
TRANSPORT='socks5://127.0.0.1:1080'
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -timeout 15 -transport "$TRANSPORT" https://getoutline.org/cdn-cgi/trace
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
`TRANSPORT` from one of the preceding sections. Omit `-transport "$TRANSPORT"`
to check your own connection. Install [jq](https://jqlang.org/download/) to format
the JSON, or omit `| jq` to see the raw response.

### IPinfo and SOAX

[IPinfo](https://ipinfo.io/json) returns fields such as `ip`, `org` (ASN and
operator), `city`, `region`, and `country`:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$TRANSPORT" https://ipinfo.io/json | jq
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
  -v -proto h2 -timeout 15 -transport "$TRANSPORT" https://checker.soax.com/api/ipinfo | jq
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
  -v -proto h3 -timeout 15 -transport "$TRANSPORT" https://ident.me/json | jq
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

## Compare Connection Strategies

Keep the destination, HTTP version, and timeout the same while changing the
transport. For example, with `TRANSPORT` set to one of the proxies above:

```sh
# Direct connection from your computer.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 https://getoutline.org/cdn-cgi/trace

# Connection through the remote proxy.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "$TRANSPORT" https://getoutline.org/cdn-cgi/trace

# Same proxy, with TLS fragmentation toward the destination.
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h2 -timeout 15 -transport "${TRANSPORT}|tlsfrag:1" https://getoutline.org/cdn-cgi/trace
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
    -v -proto h2 -timeout 15 -transport "$TRANSPORT" \
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
with `-transport "$TRANSPORT"` to test ECH through a proxy. The `dig` query in that
example runs locally; ECH does not move DNS resolution to the remote network.

To test HTTP/3, use an Outline server with UDP support or a SOCKS5 service that
supports UDP ASSOCIATE with a reachable UDP relay. Set `TRANSPORT` to that service
first; the SSH listener above will not work. Compare the ordinary request with a
QUIC prelude:

```sh
go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h3 -timeout 15 -transport "$TRANSPORT" https://getoutline.org/cdn-cgi/trace

go run golang.getoutline.org/sdk/x/tools/fetch@latest \
  -v -proto h3 -timeout 15 -transport "${TRANSPORT}|quicprelude" https://getoutline.org/cdn-cgi/trace
```

Record the tool release, time, proxy exit, destination address, protocol, and
configuration with each result, keeping access keys out of shared records.
Strategies that help on one path may have no effect on another.
