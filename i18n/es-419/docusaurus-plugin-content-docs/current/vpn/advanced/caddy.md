---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

En esta guía, se explica cómo usar [Caddy](https://caddyserver.com/), un servidor web
potente y fácil de usar, para mejorar la configuración del servidor de Outline. Las funciones de
[HTTPS automático](https://caddyserver.com/docs/automatic-https) de Caddy y
su configuración flexible lo convierten en una excelente opción para entregar servidores de Outline,
sobre todo cuando se utiliza el transporte con WebSocket.

## ¿Qué es Caddy?

Caddy es un servidor web de código abierto conocido por su facilidad de uso, HTTPS automático
y compatibilidad con diversos protocolos. Simplifica la configuración de servidores web y
ofrece funciones como las siguientes:

- **HTTPS automático:** Caddy obtiene y renueva automáticamente los certificados TLS,
lo que garantiza conexiones seguras.

- **Compatibilidad con HTTP/3:** Caddy es compatible con el protocolo HTTP/3 más reciente para brindar un
tráfico web más rápido y eficiente.

- **Complementos:** Caddy puede extenderse con complementos para
ofrecer diversas funciones, como proxy inverso y balanceo de cargas.

## Paso 1: Requisitos

- Descarga e instala [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Paso 2: Configura el dominio

Antes de iniciar Caddy, asegúrate de que tu nombre de dominio esté correctamente configurado para que apunte
a la dirección IP de tu servidor.

- **Configura los registros A y AAAA:** Accede a tu proveedor de DNS y configura los registros A y AAAA
de tu dominio para que apunten a las direcciones IPv4 e IPv6 de tu servidor,
respectivamente.

- **Verifica los registros DNS:** Comprueba que tus registros DNS estén correctamente configurados con una
búsqueda autorizada.

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## Paso 3: Crea y ejecuta una compilación personalizada de Caddy

Con `xcaddy`, puedes compilar un objeto binario personalizado de `caddy` que incluya el módulo principal
del servidor de Outline y otros módulos de extensión del servidor necesarios.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/Jigsaw-Code/outline-ss-server/outlinecaddy
```

## Paso 4: Configura y ejecuta el servidor de Caddy con Outline

Crea un archivo `config.yaml` con la siguiente configuración:

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

Esta configuración representa una estrategia de Shadowsocks sobre WebSockets. Hay un servidor
web que escucha en el puerto `443` y acepta tráfico de TCP y UDP encapsulado con Shadowsocks
en las rutas `TCP_PATH` y `UDP_PATH`,
respectivamente.

Ejecuta el servidor de Caddy extendido con Outline usando la configuración creada:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

Puedes encontrar más ejemplos de configuración en nuestro [repo de GitHub,
outline-ss-server/outlinecaddy](https://github.com/Jigsaw-Code/outline-ss-server/tree/master/outlinecaddy/examples).

## Paso 5: Crea una clave de acceso dinámica

Genera un archivo YAML de clave de acceso de cliente para tus usuarios utilizando el formato de [configuración
avanzada](../management/config) y, luego, incluye los extremos de WebSocket
previamente configurados en el servidor:

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

Después de generar el archivo YAML de clave de acceso dinámica, debes enviárselo a los
usuarios. Puedes alojar el archivo en un servicio de hosting web estático o generarlo
dinámicamente. Obtén más información para usar [claves de acceso
dinámicas](../management/dynamic-access-keys).

## Paso 6: Conecta el servidor con el cliente de Outline

Usa una de las aplicaciones oficiales del [cliente de Outline](../../download-links)
(versión 1.15.0 como mínimo) y agrega la clave de acceso dinámica que acabas de crear como
entrada de servidor. Haz clic en **Conectar** para iniciar una tunelización hacia el servidor utilizando la
configuración de Shadowsocks sobre WebSocket.

Usa una herramienta como [IPInfo](https://ipinfo.io) para verificar que ahora estás navegando por
Internet a través del servidor de Outline.
