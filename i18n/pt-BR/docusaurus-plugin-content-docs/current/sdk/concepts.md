---
title: "Concepts"
sidebar_label: "Concepts"
---

O SDK Outline foi desenvolvido com base em conceitos simples, definidos como interfaces
interoperáveis que permitem combinações variadas e uma fácil reutilização.

## Conexões {#connections}

As conexões permitem a comunicação entre dois endpoints sobre um transporte
abstrato. Existem dois tipos de conexões:

- `transport.StreamConn`: conexão com base em stream,
como TCP e o tipo de soquete Posix `SOCK_STREAM`.

- `transport.PacketConn`: conexão com base em datagram,
como UDP e o tipo de soquete Posix `SOCK_DGRAM`.
Usamos "Packet" em vez de "Datagram" porque essa é a convenção na
biblioteca padrão do Go.

As conexões podem ser unidas para criar conexões aninhadas sobre um novo transporte.
Por exemplo, um `StreamConn` pode ser sobre TCP, sobre TLS sobre TCP, sobre HTTP sobre
TLS sobre TCP, sobre QUIC, entre outras opções.

## Discadores {#dialers}

Os discadores permitem a criação de conexões para certo endereço de host:porta e, ao mesmo tempo,
encapsulam os protocolos de proxy ou transporte.
Os tipos `StreamDialer` e `PacketDialer` criam conexões `StreamConn` e `PacketConn`
respectivamente quando um endereço é fornecido. Discadores também podem ser aninhados.
Por exemplo, um Discador Stream de TLS pode usar um discador de TCP para criar uma `StreamConn`
que tenha o apoio de uma conexão TCP. Depois pode criar uma `StreamConn` TLS que tenha o apoio de uma
`StreamConn` TCP. Um discador de SOCKS5 sobre TLS poderia usar um discador de TLS para criar a
`StreamConn` TLS para o proxy antes de fazer a conexão de SOCKS5 com o endereço-alvo.

## Resolvedores {#resolvers}

Os resolvedores (`dns.Resolver`) permitem responder a perguntas de DNS e, ao mesmo tempo,
encapsulam o protocolo ou algoritmo.
Eles são usados principalmente para associar nomes de domínio a endereços IP.
