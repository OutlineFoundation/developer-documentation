---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

# Shadowsocks-over-WebSockets

_Outline Client v1.15.0+._

This tutorial provides a detailed walkthrough to help you implement
Shadowsocks-over-WebSockets, a powerful technique for bypassing censorship in
environments where regular Shadowsocks connections are blocked. By encapsulating
Shadowsocks traffic within WebSockets, you can disguise it as standard web
traffic, enhancing resilience and accessibility.

:::note
Shadowsocks-over-WebSockets is only supported on the Outline clients
v1.15.0+. You must maintain your existing configurations to support older client
versions.
:::

## Step 1: Configure and Run an Outline Server

Create a new `config.yaml` file with the following configuration:

```yaml
web:
  servers:
    - id: server1
        listen: 127.0.0.1:<WEB_SERVER_PORT>

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
Keep the `path` secret to avoid probing. It acts as a secret endpoint. A
long, randomly generated path is recommended.
:::

Download the latest
[`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases)
and run it using the created configuration:

```sh
outline-ss-server -config=config.yaml
```

## Step 2: Expose the Web Server

To make your WebSocket web server publicly accessible, you'll need to expose it
to the internet and configure
[TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
You have several options for achieving this. You can use a local web server like
[Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) or
[Apache](https://httpd.apache.org/), ensuring it has a valid TLS certificate, or
employ a tunneling service such as [Cloudflare
Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
or [ngrok](https://ngrok.com/).

### Example using TryCloudflare

:::caution
TryCloudflare is intended for demos and testing only.
:::

For this example, we'll demonstrate using
[TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/)
to create a quick tunnel. This provides a convenient and secure way to expose
your local web server without opening inbound ports.

1.  Download and install
    [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

1.  Create a tunnel pointing to your local web server port:

    ```sh
    cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
    ```

Cloudflare will provide a subdomain (e.g.,
`acids-iceland-davidson-lb.trycloudflare.com`) to access your WebSocket endpoint
and automatically handle TLS. Make note of this subdomain, as you'll need it
later.

## Step 3: Create a Dynamic Access Key

Generate a client access key YAML file for your users using the [Access Key
Configuration](../management/config) format and include the WebSocket endpoints previously
configured on the server side:

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

After generating the dynamic access key YAML file, you need to get it to your
users. You can host the file on a static web hosting service or dynamically
generate it. Learn more about how to use [Dynamic Access
Keys](../management/dynamic-access-keys).

## Step 4: Connect with the Outline Client

Use one of the official [Outline Client](../../download-links.md)
applications (versions 1.15.0+) and add your newly created dynamic access key as
a server entry. Click **Connect** to start tunneling to your server using the
Shadowsocks-over-Websocket configuration.

Use a tool like [IPInfo](https://ipinfo.io) to verify you are now browsing the
internet via your Outline server.