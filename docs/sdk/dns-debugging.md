---
title: "Looking Up DNS Records"
sidebar_label: "DNS Lookups"
---

Use the Outline SDK's `resolve` tool to compare DNS responses across resolvers
and transports. Install [Go](https://go.dev/doc/install) before running these
commands. For a general introduction to running the tools, see [Fetch](https://developer.getoutline.org/sdk/command-line-debugging/).

## Discover the Options

```sh
go run golang.getoutline.org/sdk/x/tools/resolve@latest -help
```

Put flags before the domain name. `-v` prints the DNS response details to standard
error, while matching answers go to standard output. The timeout defaults to two
seconds; use `-timeout 10` when testing a slower connection.

## Query a Resolver

Specify a recursive resolver with `-resolver`. The default port is 53. Query
Cloudflare's public resolver for the IPv4 and IPv6 addresses of `getoutline.org`:

```sh
go run golang.getoutline.org/sdk/x/tools/resolve@latest -resolver 1.1.1.1 -type A getoutline.org
go run golang.getoutline.org/sdk/x/tools/resolve@latest -resolver 1.1.1.1 -type AAAA getoutline.org
```

The tool supports `A`, `AAAA`, `CNAME`, `NS`, `SOA`, and `TXT` queries. A successful
query can have no answers of the requested type; for example, a name need not
have a CNAME record. Use `-v` to inspect the response.

Compare with another resolver by changing only `-resolver`:

```sh
go run golang.getoutline.org/sdk/x/tools/resolve@latest -v -resolver 8.8.8.8 -type A getoutline.org
```

Different answers do not by themselves indicate interference: DNS answers can
vary with location, caching, and load balancing.

## Compare UDP and TCP

Queries use UDP by default. Add `-tcp` to query the same resolver over TCP:

```sh
go run golang.getoutline.org/sdk/x/tools/resolve@latest -v -tcp -resolver 1.1.1.1 -type A getoutline.org
```

Both examples use plain DNS. Selecting TCP does not encrypt the query.

## Configure the Transport to the Resolver

The `-transport` flag accepts a [config URL](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl)
for the connection **to the DNS resolver**. For example, `split:20` writes the
first 20 bytes of the TCP stream separately from the remaining bytes:

```sh
go run golang.getoutline.org/sdk/x/tools/resolve@latest \
  -tcp -transport 'split:20' -resolver 1.1.1.1 -type A getoutline.org
```

Compare whether this query succeeds with the ordinary TCP query above. The DNS
answer may be unchanged; this experiment changes how the query is sent.

If you have an [Outline server](/vpn/getting-started/server-setup-manager),
you can also supply its access key as the transport. Replace the placeholder
with the server's `ss://` access key:

```sh
TRANSPORT='ss://YOUR_OUTLINE_ACCESS_KEY'
go run golang.getoutline.org/sdk/x/tools/resolve@latest \
  -tcp -transport "$TRANSPORT" -resolver 1.1.1.1 -type A getoutline.org
```

Use a resolver address reachable from the proxy. UDP queries need a transport
and server that support UDP; stream-only proxies require `-tcp`. See
[Remote Measurement](remote-measurement.md) for more on choosing a remote path.

## Look Up ECH Configurations

`resolve` does not currently support the HTTPS record type used to publish ECH
configurations. Use `dig` for that query (provided by `dnsutils` on Debian and
Ubuntu):

```sh
dig +short getoutline.org HTTPS
```

The [ECH example in Fetch](https://developer.getoutline.org/sdk/command-line-debugging/#use-encrypted-client-hello-ech)
shows how to pass the returned configuration to `fetch`.
