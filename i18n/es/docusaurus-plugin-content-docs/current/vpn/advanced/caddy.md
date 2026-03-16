---
title: "HTTPS automático con Caddy"
sidebar_label: "HTTPS automático con Caddy"
---

En esta guía se explica cómo utilizar [Caddy](https://caddyserver.com/), un servidor web potente y fácil de usar, para mejorar la configuración de tu servidor de Outline. Las funciones [HTTPS automáticas](https://caddyserver.com/docs/automatic-https) y la configuración flexible de Caddy la convierten en una opción excelente para ofrecer tu servidor de Outline, especialmente cuando se usa un transporte de WebSocket.

## ¿Qué es Caddy? {#what_is_caddy}

Caddy es un servidor web de software libre conocido por su facilidad de uso, sus HTTPS automáticas y su compatibilidad con varios protocolos. Permite simplificar la configuración de servidores web y ofrece características como las siguientes:

- **HTTPS automáticas:** Caddy obtiene y renueva automáticamente los certificados TLS para asegurar que las conexiones sean seguras.

- **Compatibilidad con HTTP/3:** Caddy admite el protocolo HTTP/3 más reciente para proporcionar un tráfico web más rápido y eficiente.

- **Ampliable con complementos:** Caddy puede ampliarse mediante complementos para admitir diversas funciones, como los proxys inversos y el balanceo de carga.

## Paso 1: Requisitos previos {#step_1_prerequisites}

- Descarga e instala [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Paso 2: Configuración de tu dominio {#step_2_configure_your_domain}

Antes de empezar a usar Caddy, comprueba que el nombre de tu dominio se haya configurado correctamente de forma que dirija a la dirección IP de tu servidor.

- **Configura registros A o AAAA:** inicia sesión en tu proveedor de DNS y configura registros A y AAAA para que tu dominio dirija a las direcciones IPv4 e IPv6 de tu servidor, respectivamente.

- **Verifica los registros DNS:** verifica que tus registros DNS estén correctamente configurados mediante una búsqueda autorizada:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## Paso 3: Desarrollo y ejecución de una compilación personalizada de Caddy {#build-and-run}

Si usas `xcaddy`, puedes desarrollar un binario `caddy` personalizado que incluya el módulo de servidores principales de Outline y otros módulos de extensiones de servidor necesarios.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## Paso 4: Configuración y ejecución del servidor Caddy con Outline {#step_4_configure_and_run_the_caddy_server_with_outline}

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

Esta configuración se corresponde con una estrategia de Shadowsocks a través de WebSockets con un servidor web que escucha en el puerto `443`, mientras se acepta el tráfico envuelto de Shadowsocks de TCP y UDP en las rutas `TCP_PATH` y `UDP_PATH`, respectivamente.

Ejecuta el servidor de Caddy ampliado con Outline usando la configuración creada:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

Puedes encontrar más configuraciones de ejemplo en nuestro [repositorio de GitHub outline-ss-server/outlinecaddy](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples).

## Paso 5: Creación de una clave de acceso dinámica {#step_5_create_a_dynamic_access_key}

Genera un archivo YAML de clave de acceso de cliente para tus usuarios utilizando el formato de [configuración avanzada](../management/config) e incluye los endpoints de WebSocket que has definido previamente del lado del servidor:

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

Después de generar el archivo YAML de la clave de acceso dinámica, debes enviárselo a tus usuarios. Puedes alojar el archivo en un servicio de alojamiento web estático o generarlo de forma dinámica. [Más información sobre cómo usar claves de acceso dinámicas](../management/dynamic-access-keys)

## Paso 6: Conexión con el cliente de Outline {#step_6_connect_with_the_outline_client}

Utiliza una de las aplicaciones oficiales de [cliente de Outline](../../download-links) (versiones 1.15.0 y posteriores) y añade la clave de acceso dinámica que acabas de crear como entrada de servidor. Haz clic en **Conectar** para empezar la tunelización a tu servidor usando la configuración de Shadowsocks a través de Websocket.

Utiliza una herramienta como [IPInfo](https://ipinfo.io) para verificar que tienes acceso a Internet mediante tu servidor de Outline.
