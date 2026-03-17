---
title: "使用 Caddy 实现自动 HTTPS"
sidebar_label: "使用 Caddy 实现自动 HTTPS"
---

本指南介绍了如何使用强大易用的 Web 服务器 [Caddy](https://caddyserver.com/) 来增强 Outline 服务器设置。Caddy 具有[自动 HTTPS](https://caddyserver.com/docs/automatic-https) 功能和灵活的配置，是为 Outline 服务器提供支持的理想选择，尤其适合使用 WebSocket 传输的应用场景。

## 什么是 Caddy？ {#what_is_caddy}

Caddy 是一种开源 Web 服务器，它易于使用、具备自动 HTTPS 功能且支持各种协议。该服务器简化了 Web 服务器配置，提供了以下实用功能：

- **自动 HTTPS**：Caddy 可自动获取和续订 TLS 证书，确保连接安全性。

- **HTTP/3 支持**：Caddy 支持最新 HTTP/3 协议，能够实现更快、更高效的网络流量传输。

- **支持插件扩展**：Caddy 可通过插件进行扩展，以支持各种功能，包括反向代理和负载均衡。

## 第 1 步：前提条件 {#step_1_prerequisites}

- 下载并安装 [`xcaddy`](https://github.com/caddyserver/xcaddy)

## 第 2 步：配置域名 {#step_2_configure_your_domain}

在启动 Caddy 之前，请务必正确配置域名，使其指向服务器的 IP 地址。

- **设置 A/AAAA 记录**：登录 DNS 提供商的网站，设置域名的 A 记录和 AAAA 记录，确保它们分别指向服务器的 IPv4 地址和 IPv6 地址。

- **验证 DNS 记录**：通过权威查找验证 DNS 记录是否设置正确：

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## 第 3 步：构建并运行自定义 Caddy build {#build-and-run}

使用 `xcaddy`，您可以构建自定义 `caddy` 二进制文件，并在其中添加 Outline 核心服务器模块和所需的其他服务器扩展模块。

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## 第 4 步：使用 Outline 配置并运行 Caddy 服务器 {#step_4_configure_and_run_the_caddy_server_with_outline}

创建一个包含以下配置的新 `config.yaml` 文件：

```yaml
apps:
  http:
    servers:
      server1:
        listen:
          - ":443"
        routes:
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<TCP_PATH>
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<UDP_PATH>
            handle:
              - handler: websocket2layer4
                type: packet
                connection_handler: ss1
  outline:
    shadowsocks:
      replay_history: 10000
    connection_handlers:
      - name: ss1
        handle:
          handler: shadowsocks
          keys:
            - id: user-1
              cipher: chacha20-ietf-poly1305
              secret: <SHADOWSOCKS_SECRET>
```

:::warning[Important]
请确保 `path` 的机密性，以免被探测。它将充当秘密端点。建议使用随机生成的长路径。
:::


此配置代表 Shadowsocks-over-WebSocket 策略，其中 Web 服务器监听端口 `443`，并分别在路径 `TCP_PATH` 和 `UDP_PATH` 接受 TCP 和 UDP Shadowsocks 封装的流量。

使用创建的配置运行使用 Outline 扩展的 Caddy 服务器：

```sh
caddy run --config config.yaml --adapter yaml --watch
```

:::note
以上示例使用的是更易于读取和注释的 YAML，您也可以直接使用 JSON（Caddy 的原生配置语言）。如果使用 JSON，您无需 `--adapter yaml` 标志即可运行 Caddy 服务器，并可在构建和运行步骤中移除 YAML 适配器依赖项。
:::


如需查看更多示例配置，请访问我们的 [outline-ss-server/outlinecaddy GitHub 仓库](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples)。

## 第 5 步：创建动态访问密钥 {#step_5_create_a_dynamic_access_key}

使用[高级配置](../management/config)格式为用户生成客户端访问密钥 YAML 文件，并在其中添加之前在服务器端配置的 WebSocket 端点：

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

生成动态访问密钥 YAML 文件后，您需要将其提供给用户。您可以将文件托管在静态网站托管服务中，也可以动态生成文件。详细了解如何使用[动态访问密钥](../management/dynamic-access-keys)。

## 第 6 步：连接到 Outline 客户端 {#step_6_connect_with_the_outline_client}

使用某个官方 [Outline 客户端](../../download-links)应用（1.15.0 及更高版本），将新创建的动态访问密钥添加为服务器条目。点击**连接**，开始使用 Shadowsocks-over-WebSocket 配置通过隧道技术连接到服务器。

使用 [IPInfo](https://ipinfo.io) 等工具验证您是否在通过 Outline 服务器浏览互联网。
