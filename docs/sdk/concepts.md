---
title: "Concepts"
sidebar_label: "Concepts"
---

# Concepts

The Outline SDK separates **how data is exchanged** from **how a destination is
chosen**. Streams carry a sequence of bytes; packets carry individual messages.
Dialers let the caller choose a destination; endpoints have the destination
configured in advance. These interfaces let applications use different transports
and proxy protocols without changing the code that reads and writes data.

## At a glance

The four core transport concepts are:

| Concept | What it does | Stream (like TCP) | Packet (like UDP) |
| --- | --- | --- | --- |
| **Connection** | Exchanges data with one destination. | [`StreamConn`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#StreamConn) | [`net.Conn`](https://pkg.go.dev/net#Conn) |
| **Dialer** | Creates a connection to an address supplied by the caller. Like a **forward proxy**. | [`StreamDialer`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#StreamDialer) | [`PacketDialer`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#PacketDialer) |
| **Endpoint** | Creates a connection to a destination configured in advance. Like a **reverse proxy**. | [`StreamEndpoint`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#StreamEndpoint) | [`PacketEndpoint`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#PacketEndpoint) |
| **Packet listener** | Creates a socket that can send to and receive from multiple destinations. | No stream listener interface in `transport`. | [`PacketListener`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#PacketListener), returning [`net.PacketConn`](https://pkg.go.dev/net#PacketConn) |

Except for the Go standard library's `net` types, the types in this table belong
to the SDK's `golang.getoutline.org/sdk/transport` package. Dialers and endpoints
create connections to one destination. Packet listeners create objects that send
and receive packets with multiple destinations.

## Connections

A connection provides two-way communication with one destination. The stream
and packet interfaces differ in how they treat the data:

- **Stream:** an ordered sequence of bytes, like TCP. Writes do not define message
  boundaries: one write may take several reads to consume, and a read may combine
  data from several writes. `transport.StreamConn` extends Go's `net.Conn` with
  `CloseRead` and `CloseWrite` for closing either direction independently
  (**half-close**). For example, you can finish sending data while continuing to
  read a response.
- **Packet:** individual messages, also called datagrams, like UDP. Each write
  sends one packet, and each read receives one packet; the receiving buffer must
  be large enough to hold it. Packet dialers and endpoints return a `net.Conn`
  associated with one remote destination, so reads and writes do not take an
  address. The SDK uses "packet" to follow Go's naming convention.

`net.Conn` does not imply a stream: Go uses that interface for both TCP and
connected UDP sockets. For UDP, "connected" means the socket has a selected
remote destination. It does not imply a handshake, reliable delivery, or ordered
delivery.

These interfaces describe the data your application exchanges, not the protocol
on the wire. A stream connection can use TCP directly, TLS over TCP, or a stream
carried over QUIC, for example.

## Dialers and endpoints {#dialers}

Both dialers and endpoints create connections. The key difference is **who
chooses the destination, and when**.

### Dialers: the caller chooses

A dialer takes a `host:port` address each time it creates a connection. For
example, the same dialer can connect to `example.com:443` on one call and
`example.org:443` on another:

- `DialStream(ctx, address)` returns a `StreamConn` and an error.
- `DialPacket(ctx, address)` returns a `net.Conn` and an error.

Here, `ctx` is a Go context used to control the connection setup, and the host
can be a domain name or an IP address. The dialer encapsulates how to reach the
requested destination, whether directly or through a proxy.

This is like a **forward proxy**: the client supplies the destination it wants
to reach. Each resulting connection is associated with that one destination;
choosing another destination means asking the dialer for another connection.

### Endpoints: the destination is configured

An endpoint already knows where to connect, so the caller supplies no address:

- `ConnectStream(ctx)` returns a `StreamConn` and an error.
- `ConnectPacket(ctx)` returns a `net.Conn` and an error.

This is like a **reverse proxy**: the destination is configured behind the
interface, rather than supplied by the caller on each connection. "Fixed" refers
to the configured destination, which might be a hostname whose IP address changes.
An endpoint is a reusable way to create connections, not an already-open
connection or just an address string.

The proxy analogies describe destination selection. Dialers and endpoints are
objects used by client code; neither interface requires running a proxy server.

You can turn a dialer into an endpoint by pairing it with an address using
[`StreamDialerEndpoint`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#StreamDialerEndpoint)
or [`PacketDialerEndpoint`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#PacketDialerEndpoint).

### Example: one proxy, many destinations

A Shadowsocks client uses both concepts:

1. A **stream endpoint** is configured to connect to the proxy server at
   `proxy.example:8388`.
2. A **Shadowsocks stream dialer** uses that endpoint. The application asks the
   dialer for a connection to `example.com:443`.
3. The dialer connects to the proxy through the endpoint and uses the Shadowsocks
   protocol to request the application's destination. The application reads and
   writes through the returned stream connection.

On a later call, the application can request `example.org:443` through the same
dialer and proxy endpoint. The **proxy server** is the endpoint's destination;
the **target website** is the destination passed to the dialer.

## Packet listeners

Use a `PacketListener` when you need to exchange packets with multiple
destinations through one socket. `ListenPacket(ctx)` returns a `net.PacketConn`
and an error. Unlike a packet dialer's `net.Conn`, this object takes an address
on each send and reports the sender on each receive:

- `WriteTo(packet, destination)` sends a packet to the supplied destination.
- `ReadFrom(buffer)` receives a packet and returns its source address along
  with the byte count and any error.

Think of an **unconnected UDP socket**. It has a local address, but it is not
tied to one remote destination. For example, a UDP client can send queries to
two different DNS servers through the same socket and identify which server
sent each reply.

Despite the name, this is not a server listener that waits for connections and
returns a new connection from `Accept`. `ListenPacket` creates the packet socket;
you send and receive packets on it directly. It is useful in clients as well as
servers, including when relaying UDP through a proxy.

The SDK's [`UDPListener`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#UDPListener)
creates a local UDP socket. Other implementations can carry packets through a
proxy while exposing the same `net.PacketConn` interface. If a caller needs a
single-destination connection instead, adapt a listener into a packet dialer
with [`PacketListenerDialer`](https://pkg.go.dev/golang.getoutline.org/sdk/transport#PacketListenerDialer).

## Composition

Components can build on these interfaces to add a transport layer or change
connection behavior. For example, a TLS stream dialer calls an underlying TCP
stream dialer, wraps the resulting connection with TLS, and returns another
`StreamConn`. The application still uses the same read and write methods.

Endpoints make it possible to change how a proxy is reached independently of
the proxy protocol. In the Shadowsocks example, replacing the proxy endpoint
changes the transport to the proxy while leaving the application's use of the
Shadowsocks dialer the same. The proxy server must support the chosen transport.

Packet listeners can also wrap other packet listeners to add behavior while
preserving the ability to send to multiple destinations. Composition works when
one component provides the interface the next component expects.

## Resolvers

A [`dns.Resolver`](https://pkg.go.dev/golang.getoutline.org/sdk/dns#Resolver)
answers DNS questions, most commonly to map domain names to IP addresses. Its
`Query` method hides how the answer is obtained, such as over UDP, TCP, or HTTPS.
This lets an application change its DNS strategy independently of the code
asking the question.
