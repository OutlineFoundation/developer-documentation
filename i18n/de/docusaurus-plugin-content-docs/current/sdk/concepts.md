---
title: "Konzepte"
sidebar_label: "Konzepte"
---

Das Outline SDK basiert auf einigen grundlegenden Konzepten, die als interoperable Schnittstellen definiert sind, die eine Kombination und einfache Wiederverwendung ermöglichen.

## Verbindungen {#connections}

Verbindungen ermöglichen die Kommunikation zwischen zwei Endpunkten über einen abstrakten Transport. Es gibt zwei Arten von Verbindungen:

- `transport.StreamConn`: streambasierte Verbindungen wie TCP und den `SOCK_STREAM` Posix Socket-Typ.

- `transport.PacketConn`: datagram-basierte Verbindungen wie UDP und den `SOCK_DGRAM` Posix Socket-Typ.
Wir verwenden „Packet“ anstelle von „Datagram“, weil dies die Konvention in der Go-Standard-Bibliothek ist.

Verbindungen können zusammengefasst werden, um verschachtelte Verbindungen über eine neue Transportmethode zu erstellen.
Eine `StreamConn` könnte z. B. per TCP, per TLS über TCP, per HTTP über TLS über TCP, per QUIC und andere Optionen erfolgen.

## Dialer {#dialers}

Dialer ermöglichen den Aufbau von Verbindungen mit einer Host:Port-Adresse, wobei sie das zugrunde liegende Transport- oder Proxy-Protokoll kapseln.
Die `StreamDialer`- und `PacketDialer`-Typen erstellen `StreamConn`- und `PacketConn`-Verbindungen mit jeweils einer Adresse. Dialer können auch verschachtelt werden.
Ein TLS-Stream-Dialer kann z. B. einen TCP-Dialer zum Erstellen einer `StreamConn` verwenden, der mit einer TCP-Verbindung gesichert ist. Anschließend kann er eine TLS-`StreamConn` erstellen, die von der TCP-`StreamConn` gesichert wird. Ein SOCKS5-over-TLS-Dialer kann den TLS-Dialer zum Erstellen der TLS-`StreamConn` zum Proxy verwenden, bevor er die SOCKS5-Verbindung zur Zieladresse herstellt.

## Resolver {#resolvers}

Resolver (`dns.Resolver`) ermöglichen die Beantwortung von DNS-Fragen, während sie den zugrunde liegenden Algorithmus oder das Protokoll kapseln.
Resolver werden hauptsächlich zur Zuordnung von Domainnamen zu IP-Adressen verwendet.
