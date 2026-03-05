---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline SDK 的設計基於幾項基本概念，這些概念以可互通的介面為核心，介面能靈活組合，並方便重複使用。

## 連線

連線讓兩個端點能透過抽象的傳輸方式互相通訊，主要分為兩種：

- `transport.StreamConn`：以串流為基礎的連線，例如 TCP 和 `SOCK_STREAM` Posix 通訊端類型。

- `transport.PacketConn`：以資料元為基礎的連線，例如 UDP 和 `SOCK_DGRAM` Posix 通訊端類型。「封包」是 Go 標準程式庫的慣用稱呼，所以我們選擇用這個詞，而不是「資料元」。

連線可透過封裝疊加新的傳輸層，形成巢狀連線。舉例來說，`StreamConn` 可以是 TCP，也可以是基於 TCP 的 TLS，或是在 TLS 上再疊加 HTTP，甚至 QUIC 或其他可能組合。

## 撥號器

撥號器可根據 <主機>:<通訊埠> 位址建立連線，同時封裝底層的傳輸方式或 Proxy 通訊協定。`StreamDialer` 和 `PacketDialer` 類型分別能根據位址建立 `StreamConn` 和 `PacketConn` 連線。撥號器也可以是巢狀結構。舉例來說，TLS 串流撥號器可先用 TCP 撥號器建立以 TCP 連線為基礎的 `StreamConn`，再建立由 TCP `StreamConn` 支援的 TLS `StreamConn`。或者，SOCKS5-over-TLS 撥號器可用 TLS 撥號器建立連到 Proxy 的 TLS `StreamConn`，接著再透過該連線與目標位址進行 SOCKS5 通訊。

## 解析器

解析器 (`dns.Resolver`) 負責回應 DNS 查詢，並封裝底層的演算法或通訊協定，主要用於將網域名稱解析成 IP 位址。
