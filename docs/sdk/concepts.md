---
title: "Concepts"
sidebar_label: "Concepts"
---

# Concepts

The Outline SDK is built upon some basic concepts, defined as interoperable
interfaces that allow for composition and easy reuse.

## Connections

Connections enable communication between two endpoints over an abstract
transport. There are two types of connections:

- `transport.StreamConn`: stream-based connection,
  like TCP and the `SOCK_STREAM` Posix socket type.
- `transport.PacketConn`: datagram-based connection,
  like UDP and the `SOCK_DGRAM` Posix socket type.
  We use "Packet" instead of "Datagram" because that is the convention in the
  Go standard library.

Connections can be wrapped to create nested connections over a new transport.
For example, a `StreamConn` could be over TCP, over TLS over TCP, over HTTP over
TLS over TCP, over QUIC, among other options.

## Dialers

Dialers enable the creation of connections given a host:port address while
encapsulating the underlying transport or proxy protocol.
The `StreamDialer` and `PacketDialer` types create `StreamConn` and `PacketConn`
connections, respectively, given an address. Dialers can also be nested.
For example, a TLS Stream Dialer can use a TCP dialer to create a `StreamConn`
backed by a TCP connection, then create a TLS `StreamConn` backed by the TCP
`StreamConn`. A SOCKS5-over-TLS Dialer could use the TLS Dialer to create the
TLS `StreamConn` to the proxy before doing the SOCKS5 connection to the target
address.

## Resolvers

Resolvers (`dns.Resolver`) enable the answering of DNS questions while
encapsulating the underlying algorithm or protocol.
Resolvers are primarily used to map domain names to IP addresses.
