---
title: "Shadowsocks-over-WebSocket"
sidebar_label: "Shadowsocks-over-WebSocket"
---

Outline 客户端 1.15.0 及以上版本。**

本教程提供了详细的操作步骤，可帮助您实现 Shadowsocks-over-WebSocket，这是一种强大的技术，可在常规 Shadowsocks 连接被屏蔽的环境中绕过审查。通过将 Shadowsocks 流量封装在 WebSocket 中，您可以将其伪装成标准 Web 流量，从而提高弹性和可访问性。


:::note
只有 Outline 客户端 1.15.0 及以上版本支持 Shadowsocks-over-WebSocket。您必须保留现有配置，才能支持较低的客户端版本。
:::

## 第 1 步：配置并运行 Outline 服务器 {#step_1_configure_and_run_an_outline_server}

创建一个包含以下配置的新 `config.yaml` 文件：

```yaml
web:
  servers:
    - id: server1
      listen:
        - "127.0.0.1:<WEB_SERVER_PORT>"

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

:::tip
确保 `path` 的机密性，以免被探测。它充当秘密端点。建议使用随机生成的长路径。
:::


下载最新的 [`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases)，并使用创建的配置来运行它：

```sh
outline-ss-server -config=config.yaml
```

## 第 2 步：公开 Web 服务器 {#step_2_expose_the_web_server}

若要让 WebSocket Web 服务器可公开访问，您需要将其公开到互联网并配置 [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security)。您可以通过多种方式实现此目的。您可以使用 [Caddy](https://caddyserver.com/)、[nginx](https://nginx.org/) 或 [Apache](https://httpd.apache.org/) 等本地 Web 服务器，确保它具有有效的 TLS 证书，也可以使用 [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) 或 [ngrok](https://ngrok.com/) 等隧道服务。

### 使用 TryCloudflare 的示例 {#example_using_trycloudflare}


:::caution
TryCloudflare 仅用于演示和测试。
:::

在本示例中，我们将演示如何使用 [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) 创建快速隧道。这样，您就可以安全便捷地公开本地 Web 服务器，而无需打开入站端口。

1. 下载并安装 [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)。

2. 创建指向本地 Web 服务器端口的隧道：

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Cloudflare 将提供一个子网域（例如 `acids-iceland-davidson-lb.trycloudflare.com`）来访问您的 WebSocket 端点并自动处理 TLS。记下此子网域，您稍后需要用到它。

## 第 3 步：创建动态访问密钥 {#step_3_create_a_dynamic_access_key}

使用[访问密钥配置](../management/config)格式为用户生成客户端访问密钥 YAML 文件，并在其中添加之前在服务器端配置的 WebSocket 端点：

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

生成动态访问密钥 YAML 文件后，您需要将其提供给用户。您可以将文件托管在静态网站托管服务上，也可以动态生成文件。详细了解如何使用[动态访问密钥](../management/dynamic-access-keys)。

## 第 4 步：连接到 Outline 客户端 {#step_4_connect_with_the_outline_client}

使用某个官方 [Outline 客户端](../../download-links)应用（1.15.0 及更高版本），将新创建的动态访问密钥添加为服务器条目。点击**连接**，开始使用 Shadowsocks-over-WebSocket 配置通过隧道连接到服务器。

使用 [IPInfo](https://ipinfo.io) 等工具验证您目前是否在通过 Outline 服务器浏览互联网。
