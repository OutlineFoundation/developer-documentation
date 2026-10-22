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
