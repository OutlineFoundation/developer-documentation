# Automatic HTTPS with Caddy

This guide explains how to use [Caddy](https://caddyserver.com/), a powerful and
user-friendly web server, to enhance your Outline server setup. Caddy's
[automatic HTTPS](https://caddyserver.com/docs/automatic-https) capabilities and
flexible configuration make it an excellent choice for serving your Outline
server, especially when using a WebSocket transport.

## What is Caddy?

Caddy is an open-source web server known for its ease of use, automatic HTTPS,
and support for various protocols. It simplifies web server configuration and
offers features like:

-   **Automatic HTTPS:** Caddy automatically obtains and renews TLS
    certificates, ensuring secure connections.
-   **HTTP/3 Support:** Caddy supports the latest HTTP/3 protocol for faster and
    more efficient web traffic.
-   **Extensible with Plugins:** Caddy can be extended with plugins to support
    various functionalities, including reverse proxying and load balancing.

## Step 1: Prerequisites

-   Download and install [`xcaddy`](https://github.com/caddyserver/xcaddy)

## Step 2: Configure Your Domain

Before starting Caddy, ensure your domain name is correctly configured to point
to your server's IP address.

-   **Set A/AAAA records:** Sign in to your DNS provider and set the A and AAAA
    records for your domain to point to your server's IPv4 and IPv6 addresses,
    respectively.
-   **Verify DNS records:** Verify your DNS records are set correctly with an
    authoritative lookup:

    ```sh
    curl "https://cloudflare-dns.com/dns-query?name=<var>DOMAIN_NAME</var>&type=A" \
      -H "accept: application/dns-json"
    ```

## Step 3: Build and Run a Custom Caddy Build

Using `xcaddy`, you can build a custom `caddy` binary that includes the Outline
core server module and other needed server extension modules.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/Jigsaw-Code/outline-ss-server/outlinecaddy
```

## Step 4: Configure and Run the Caddy Server with Outline

Create a new `config.yaml` file with the following configuration:

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
              - '<var>DOMAIN_NAME</var>'
            - path:
              - "/<var>TCP_PATH</var>"
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - '<var>DOMAIN_NAME</var>'
            - path:
              - "/<var>UDP_PATH</var>"
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
              secret: <var>SHADOWSOCKS_SECRET</var>
```

Important: Keep the `path` secret to avoid probing. It acts as a secret
endpoint. A long, randomly generated path is recommended.

This configuration represents a Shadowsocks-over-WebSockets strategy with a web
server listening on port `443`, accepting TCP and UDP Shadowsocks wrapped
traffic at paths {{ '<VAR>TCP_PATH</VAR>' }} and {{ '<VAR>UDP_PATH</VAR>' }}
respectively.

Run the Caddy server extended with Outline using the created configuration:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

Note: The example uses YAML because it's more readable and easier to annotate,
but you can also use JSON (Caddy's native config language) directly. If you use
that, you can run without the `--adapter yaml` flag and remove the YAML adapter
dependency in the [build and run step](#build-and-run).

You can find more example configs in our [outline-ss-server/outlinecaddy GitHub
repo](https://github.com/Jigsaw-Code/outline-ss-server/tree/master/outlinecaddy/examples).

## Step 5: Create a Dynamic Access Key

Generate a client access key YAML file for your users using the [advanced
configuration](advanced-config) format and include the WebSocket endpoints
previously configured on the server side:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://{{"<var>"}}DOMAIN_NAME{{"</var>"}}/{{"<var>"}}TCP_PATH{{"</var>"}}
    cipher: chacha20-ietf-poly1305
    secret: {{"<var>"}}SHADOWSOCKS_SECRET{{"</var>"}}

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://{{"<var>"}}DOMAIN_NAME{{"</var>"}}/{{"<var>"}}UDP_PATH{{"</var>"}}
    cipher: chacha20-ietf-poly1305
    secret: {{"<var>"}}SHADOWSOCKS_SECRET{{"</var>"}}
```

After generating the dynamic access key YAML file, you need to get it to your
users. You can host the file on a static web hosting service or dynamically
generate it. Learn more about how to use [Dynamic Access
Keys](dynamic-access-keys).

## Step 6: Connect with the Outline Client

Use one of the official [Outline Client](../../download-links.md)
applications (versions 1.15.0+) and add your newly created dynamic access key as
a server entry. Click **Connect** to start tunneling to your server using the
Shadowsocks-over-Websocket configuration.

Use a tool like [IPInfo](https://ipinfo.io) to verify you are now browsing the
internet via your Outline server.