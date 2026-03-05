---
title: "Concepts"
sidebar_label: "Concepts"
---

Le SDK Outline repose sur certains concepts de base, définis comme des interfaces interopérables qui permettent de moduler les composants et de les réutiliser facilement.

## Connexions

Les connexions permettent la communication entre deux points de terminaison par le biais d'un transport abstrait. Il existe deux types de connexions :

- `transport.StreamConn` : connexion basée sur des flux, comme TCP et le type de socket POSIX `SOCK_STREAM`.

- `transport.PacketConn` : connexion basée sur des datagrammes, comme UDP et le type de socket POSIX `SOCK_DGRAM`.
Nous utilisons "Packet" au lieu de "Datagram", conformément à la bibliothèque Go standard.

Des connexions peuvent être encapsulées afin de créer des connexions imbriquées sur un nouveau transport.
Par exemple, une `StreamConn` pourrait se faire sur TCP, sur TLS sur TCP, sur HTTP sur TLS sur TCP ou sur QUIC, par exemple.

## Dialers

Les dialers permettent de créer des connexions en fonction d'une adresse hôte:port tout en encapsulant le protocole de proxy ou de transport sous-jacent.
Les types `StreamDialer` et `PacketDialer` créent respectivement des connexions `StreamConn` et `PacketConn` en fonction d'une adresse. Les dialers peuvent également être imbriqués.
Par exemple, un dialer de flux TLS peut utiliser un dialer TCP pour créer une `StreamConn` appuyée par une connexion TCP, puis créer une `StreamConn` TLS appuyée par la `StreamConn` TCP. Un dialer SOCKS5-over-TLS pourrait utiliser le dialer TLS pour créer la `StreamConn` TLS au proxy avant d'effectuer la connexion SOCKS5 à l'adresse cible.

## Résolveurs

Les résolveurs (`dns.Resolver`) permettent de répondre aux questions DNS tout en encapsulant l'algorithme ou le protocole sous-jacent.
Ils sont principalement utilisés pour associer des noms de domaines à des adresses IP.
