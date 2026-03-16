---
title: "Conceptos"
sidebar_label: "Conceptos"
---

El SDK de Outline se basa en unos cuantos conceptos básicos definidos como interfaces interoperables que permiten la componibilidad y una reutilización sencilla.

## Conexiones {#connections}

Las conexiones posibilitan la comunicación entre dos endpoints por un transporte abstracto. Hay dos tipos de conexiones:

- `transport.StreamConn`: conexión basada en flujos, como TCP y el tipo de socket POSIX `SOCK_STREAM`.

- `transport.PacketConn`: conexión basada en datagramas, como UDP y el tipo de socket POSIX `SOCK_DGRAM`.
Usamos "Packet" en vez de "Datagram" porque es la convención que se emplea en la biblioteca estándar de Go.

Las conexiones se pueden envolver para crear conexiones anidadas a través de otro transporte.
Por ejemplo, `StreamConn` puede ir a través de TCP, a través de TLS por TCP, a través de HTTP por TLS por TCP o a través de QUIC, entre otras opciones.

## Marcadores {#dialers}

Los marcadores permiten crear conexiones a partir de una dirección host:puerto a la vez que encapsulan el protocolo subyacente de transporte o proxy.
Los tipos `StreamDialer` y `PacketDialer` crean conexiones `StreamConn` y `PacketConn`, respectivamente, a partir de una dirección. Los marcadores también se pueden anidar.
Por ejemplo, un marcador de flujos TLS puede usar un marcador TCP para crear una conexión `StreamConn` basada en una conexión TCP y, luego, crear una conexión `StreamConn` TLS basada en la conexión `StreamConn` TCP. Un marcador SOCKS5 a través de TLS puede usar el marcador TLS para crear la conexión `StreamConn` TLS al proxy antes de realizar la conexión SOCKS5 a la dirección de destino.

## Resoluciones {#resolvers}

Las resoluciones (`dns.Resolver`) permiten responder las preguntas de DNS a la vez que encapsulan el algoritmo o el protocolo subyacentes.
Las resoluciones se usan principalmente para asociar nombres de dominio a direcciones IP.
