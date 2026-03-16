---
title: "Concepts"
sidebar_label: "Concepts"
---

El SDK de Outline se basa en ciertos conceptos fundamentales definidos como interfaces
interoperables que permiten la composición y una reutilización sencilla.

## Conexiones {#connections}

Las conexiones permiten la comunicación entre dos extremos a través de un transporte
abstracto. Las hay de dos tipos:

- `transport.StreamConn`: Es una conexión basada en transmisiones,
como TCP y el tipo de socket `SOCK_STREAM` de POSIX.

- `transport.PacketConn`: Es una conexión basada en datagramas,
como UDP y el tipo de socket `SOCK_DGRAM` de POSIX.
Usamos "Packet" en vez de "Datagram" porque seguimos la convención de la
biblioteca estándar de Go.

Las conexiones se pueden unir para crear conexiones anidadas a través de un nuevo transporte.
Por ejemplo, una `StreamConn` podría funcionar por TCP, por TLS sobre TCP, por HTTP sobre
TLS sobre TCP o por QUIC, entre otras opciones.

## Marcadores {#dialers}

Los marcadores permiten crear conexiones si se proporciona una dirección host:puerto
y encapsulan el protocolo de proxy o transporte subyacente.
Los tipos `StreamDialer` y `PacketDialer` crean conexiones `StreamConn` y `PacketConn`,
respectivamente, si se proporciona una dirección. Los marcadores también pueden anidarse.
Por ejemplo, un marcador de transmisión TLS puede usar un marcador TCP para crear una `StreamConn`
respaldada por una conexión TCP y, luego, crear una `StreamConn` TLS respaldada por la `StreamConn`
TCP. Un marcador SOCKS5 sobre TLS podría usar el marcador TLS para crear la
`StreamConn` TLS al proxy antes de realizar la conexión SOCKS5 a la dirección de
destino.

## Agentes de resolución {#resolvers}

Los agentes de resolución (`dns.Resolver`) permiten responder las preguntas del DNS
y encapsulan el algoritmo o protocolo subyacente.
Se usan principalmente para asignar nombres de dominio a direcciones IP.
