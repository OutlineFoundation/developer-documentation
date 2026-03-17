---
title: "Shadowsocks sobre WebSockets"
sidebar_label: "Shadowsocks sobre WebSockets"
---

*Cliente de Outline 1.15.0 y versiones posteriores.*

En este instructivo, se ofrece una explicación detallada para ayudarte a implementar
Shadowsocks sobre WebSockets, una potente técnica para evitar la censura en
entornos donde se bloquean las conexiones comunes de Shadowsocks. Encapsular
el tráfico de Shadowsocks en WebSockets puede disfrazarlo como tráfico web,
lo que mejora la resiliencia y la accesibilidad.


:::note
Shadowsocks sobre WebSockets solo es compatible con la versión 1.15.0 del cliente de Outline (y versiones posteriores). Debes mantener tus parámetros de configuración existentes para admitir las versiones anteriores del cliente.
:::

## Paso 1: Configura y ejecuta un servidor de Outline {#step_1_configure_and_run_an_outline_server}

Crea un archivo `config.yaml` con la siguiente configuración:

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
No reveles el valor de `path` para evitar sondeos, ya que actúa como extremo secreto. Se recomienda una ruta larga y generada aleatoriamente.
:::


Descarga la versión más reciente de
[`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases)
y ejecútala con la configuración que creaste:

```sh
outline-ss-server -config=config.yaml
```

## Paso 2: Expón el servidor web {#step_2_expose_the_web_server}

Para que tu servidor web WebSocket sea de acceso público, deberás exponerlo
a Internet y configurar
[TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
Para ello, tienes varias opciones: puedes usar un servidor web local (como
[Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) o
[Apache](https://httpd.apache.org/)) y asegurarte de que tenga un certificado TLS válido, o
utilizar un servicio de tunelización como [Cloudflare
Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
o [ngrok](https://ngrok.com/).

### Ejemplo de uso de TryCloudflare {#example_using_trycloudflare}


:::caution
TryCloudflare solo se diseñó para realizar demostraciones y pruebas.
:::

En este ejemplo, usaremos
[TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/)
para crear un túnel rápido, lo que brinda una forma conveniente y segura de exponer
servidores web locales sin abrir puertos entrantes.

1. Descarga e instala [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. Crea un túnel que apunte al puerto del servidor web local:

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Cloudflare proporcionará un subdominio (p. ej.,
`acids-iceland-davidson-lb.trycloudflare.com`) para acceder a tu extremo de WebSocket
y controlar TLS automáticamente. Anota este subdominio, ya que lo necesitarás más
adelante.

## Paso 3: Crea una clave de acceso dinámica {#step_3_create_a_dynamic_access_key}

Genera un archivo YAML de clave de acceso de cliente para tus usuarios usando el formato de [configuración de claves de
acceso](../management/config) y, luego, incluye los extremos de WebSocket previamente
configurados en el servidor:

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

Después de generar el archivo YAML de clave de acceso dinámica, debes enviárselo a los
usuarios. Puedes alojar el archivo en un servicio de hosting web estático o generarlo
dinámicamente. Obtén más información para usar [claves de acceso
dinámicas](../management/dynamic-access-keys).

## Paso 4: Conecta el servidor con el cliente de Outline {#step_4_connect_with_the_outline_client}

Usa una de las apps oficiales del [cliente de Outline](../../download-links)
(versión 1.15.0 como mínimo) y agrega la clave de acceso dinámica que acabas de crear como
entrada de servidor. Haz clic en **Conectar** para iniciar una tunelización hacia el servidor utilizando la
configuración de Shadowsocks sobre WebSocket.

Usa una herramienta como [IPInfo](https://ipinfo.io) para verificar que ahora estás navegando por
Internet a través del servidor de Outline.
