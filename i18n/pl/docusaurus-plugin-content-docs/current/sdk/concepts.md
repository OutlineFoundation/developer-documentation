---
title: "Concepts"
sidebar_label: "Concepts"
---

Pakiet Outline SDK jest oparty na podstawowych koncepcjach zdefiniowanych jako interfejsy interoperacyjne, które zapewniają kompozycyjność i możliwość łatwego ponownego wykorzystania.

## Połączenia {#connections}

Połączenia umożliwiają komunikację między 2 punktami końcowymi przez abstrakcyjny transport. Dostępne są 2 typy połączeń:

- `transport.StreamConn`: połączenie strumieniowe, takie jak TCP i gniazdo POSIX `SOCK_STREAM`.

- `transport.PacketConn`: połączenie oparte na datagramach, takie jak UDP i gniazdo POSIX `SOCK_DGRAM`.
W dokumentacji używamy terminu „pakiet” zamiast „datagram”, ponieważ taka konwencja jest stosowana w standardowej bibliotece Go.

Połączenia można opakowywać w celu tworzenia. połączeń zagnieżdżonych w ramach nowego transportu.
Na przykład `StreamConn` można realizować przez TCP, TLS-over-TCP, HTTP-over-TLS przez TCP, QUIC itd.

## Dialery {#dialers}

Dialery umożliwiają tworzenie połączeń z adresami w formacie host:port przy jednoczesnej hermetyzacji podstawowego protokołu transportu lub proxy.
Typy `StreamDialer` i `PacketDialer` tworzą odpowiednio połączenia `StreamConn` i `PacketConn` z podanym adresem. Dialery można także zagnieżdżać.
Na przykład dialer strumienia TLS może użyć dialera TCP do utworzenia połączenia `StreamConn` obsługiwanego przez połączenie TCP, a następnie utworzyć połączenie TLS `StreamConn` obsługiwane przez połączenie TCP `StreamConn`. Dialer SOCKS5 przez TLS może użyć dialera TLS do utworzenia połączenia TLS `StreamConn` z serwerem proxy przed nawiązaniem połączenia SOCKS5 z adresem docelowym.

## Resolvery {#resolvers}

Resolvery (`dns.Resolver`) umożliwiają odpowiadanie na zapytania DNS, jednocześnie hermetyzując podstawowy algorytm lub protokół.
Resolvery są używane głównie do mapowania nazw domen na adresy IP.
