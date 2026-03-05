---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline SDK si basa su concetti fondamentali rappresentati da interfacce interoperabili, progettate per la componibilità e per essere facilmente riutilizzabili.

## Connessioni

Le connessioni consentono la comunicazione tra due endpoint attraverso un trasporto astratto. Esistono due tipi di connessioni:

- `transport.StreamConn`: connessione basata su stream, come TCP, e tipo di socket Posix `SOCK_STREAM`.

- `transport.PacketConn`: connessione basata su datagrammi, come UDP, e tipo di socket Posix `SOCK_DGRAM`.
Utilizziamo "Packet" anziché "Datagram" perché questa è la convenzione nella libreria Go standard.

Le connessioni possono essere aggregate in modo da creare connessioni nidificate su un nuovo trasporto.
Ad esempio, tra le varie opzioni per una `StreamConn` ci possono essere la connessione su TCP, su TLS su TCP, su HTTP su TLS su TCP o su QUIC.

## Dialer

I dialer consentono di creare connessioni a partire da un indirizzo host:porta, incapsulando il protocollo di trasporto o proxy sottostante.
I tipi `StreamDialer` e `PacketDialer` creano rispettivamente connessioni `StreamConn` e `PacketConn` a partire da un indirizzo. Anche i dialer possono essere nidificati.
Ad esempio, uno Stream Dialer TLS può usare un dialer TCP per creare una `StreamConn` basata su TCP e quindi creare una `StreamConn` TLS appoggiata sulla connessione `StreamConn` TCP. Un dialer SOCKS5 su TLS potrebbe utilizzare il dialer TLS per creare la `StreamConn` TLS al proxy prima di effettuare la connessione SOCKS5 all'indirizzo di destinazione.

## Resolver

I resolver (`dns.Resolver`) consentono di rispondere alle domande DNS incapsulando l'algoritmo o il protocollo sottostante.
I resolver vengono usati principalmente per mappare i nomi di dominio a indirizzi IP.
