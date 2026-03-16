---
title: "Concepts"
sidebar_label: "Concepts"
---

De Outline SDK is gemaakt aan de hand van enkele basisconcepten, beschreven als interoperabele interfaces die makkelijk kunnen worden aangepast en hergebruikt.

## Verbindingen {#connections}

Verbindingen maken communicatie tussen 2 eindpunten via een abstracte transportmanier mogelijk. Er zijn 2 soorten verbindingen:

- `transport.StreamConn`: Streamgebaseerde verbinding, zoals TCP en het type Posix-netwerkverbinding `SOCK_STREAM`.

- `transport.PacketConn`: Datagramgebaseerde verbinding, zoals UDP en het type Posix-netwerkverbinding `SOCK_DGRAM`.
We gebruiken het woord Packet in plaats van Datagram, omdat dat de conventie is in de standaard Go-bibliotheek.

Je kunt verbindingen verpakken om geneste verbindingen mogelijk te maken via een nieuwe transportmanier.
Een `StreamConn` kan bijvoorbeeld worden gestuurd over TCP, over TLS over TCP, over HTTP over TLS over TCP of over QUIC.

## Dialers {#dialers}

Dialers zorgen dat er verbinding kan worden gemaakt als je een host:port-adres opgeeft terwijl het onderliggende transport of proxyprotocol wordt ingekapseld.
De typen `StreamDialer` en `PacketDialer` zorgen respectievelijk voor `StreamConn`- en `PacketConn`-verbindingen als je een adres opgeeft. Je kunt dialers ook nesten.
Een TLS Stream Dialer kan bijvoorbeeld een TCP Dialer gebruiken om een `StreamConn` te maken die wordt ondersteund door een TCP-verbinding, en dan een TLS `StreamConn` maken die wordt ondersteund door de TCP `StreamConn`. Een SOCKS5-over-TLS Dialer kan de TLS Dialer gebruiken om de TLS `StreamConn` te maken voor de proxy voordat de SOCKS5-verbinding met het doeladres wordt gemaakt.

## Resolvers {#resolvers}

Resolvers (`dns.Resolver`) zorgen dat DNS-vragen kunnen worden beantwoord terwijl het onderliggende algoritme of protocol wordt ingekapseld.
Resolvers worden voornamelijk gebruikt om domeinnamen toe te wijzen aan IP-adressen.
