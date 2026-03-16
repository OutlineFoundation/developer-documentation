---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline SDK 基于一些基本概念构建，这些概念被定义为可互操作的接口，可搭配组合，且便于重复使用。

## 连接 {#connections}

连接可使两个端点通过抽象传输层进行通信。连接分为两种类型：

- `transport.StreamConn`：基于数据流的连接，如 TCP 和 `SOCK_STREAM` Posix 套接字类型。

- `transport.PacketConn`：基于数据报的连接，如 UDP 和 `SOCK_DGRAM` Posix 套接字类型。我们使用的是数据包而非数据报，因为这是 Go 标准库中的惯例。

可通过对连接进行封装来创建基于新传输层的嵌套连接。例如，`StreamConn` 连接可通过以下任意一种协议创建：TCP、TLS over TCP、HTTP over TLS over TCP、QUIC 以及其他选项。

## 拨号器 {#dialers}

拨号器可根据 host:port 地址创建连接，同时封装底层传输或代理协议。`StreamDialer` 和 `PacketDialer` 类型可根据地址分别创建 `StreamConn` 和 `PacketConn` 连接。拨号器也可以嵌套。例如，TLS 数据流拨号器可以使用 TCP 拨号器创建一个由 TCP 连接提供支持的 `StreamConn`，然后再创建一个由 TCP `StreamConn` 提供支持的 TLS `StreamConn`。SOCKS5-over-TLS 拨号器可以使用 TLS 拨号器创建与代理服务器之间的 TLS `StreamConn`，然后再创建与目标地址的 SOCKS5 连接。

## 解析器 {#resolvers}

解析器 (`dns.Resolver`) 可在封装底层算法或协议的同时响应 DNS 问题。解析器主要用于将域名映射到 IP 地址。
