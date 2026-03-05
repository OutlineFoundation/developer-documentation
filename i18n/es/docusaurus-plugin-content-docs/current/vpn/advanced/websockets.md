---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Versión 1.15.0 o posterior del cliente de Outline.*

Este tutorial es una guía detallada para ayudarte a implementar Shadowsocks a través de WebSockets, una técnica eficaz para sortear la censura en los entornos en los que las conexiones de Shadowsocks normales estén bloqueadas. Al encapsular el tráfico de Shadowsocks en WebSockets, puedes hacerlo pasar por tráfico web estándar, lo que mejora la resiliencia y la accesibilidad.

## Paso 1: Configura y ejecuta un servidor de Outline

Crea un archivo `config.yaml` con la siguiente configuración:

Descarga la última versión de [`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases) y ejecútala con la configuración que has creado:

## Paso 2: Expón el servidor web

Para que se pueda acceder a tu servidor web de WebSocket de forma pública, deberás exponerlo en Internet y configurar [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
Tienes varias formas de hacerlo. Puedes usar un servidor web local, como [Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) o [Apache](https://httpd.apache.org/) (asegurándote de que tenga un certificado TLS válido) o usar un servicio de tunelización, como [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) o [ngrok](https://ngrok.com/).

### Ejemplo con TryCloudflare

En este ejemplo, vamos a hacer una demo con [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) de cómo crear un túnel rápido. Este método te permite exponer tu servidor web local de una forma conveniente y segura sin abrir puertos de entrada.

1. Descarga e instala [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. Crea un túnel que dirija al puerto de tu servidor web local:

Cloudflare proporcionará un subdominio (por ejemplo, `acids-iceland-davidson-lb.trycloudflare.com`) para acceder a tu endpoint de WebSocket y gestionar automáticamente TLS. Apunta el subdominio para consultarlo más tarde.

## Paso 3: Crea una clave de acceso dinámica

Genera un archivo YAML de clave de acceso de cliente para tus usuarios utilizando el formato de la página [Configuración de claves de acceso](../management/config) e incluye los endpoints de WebSocket que has configurado previamente del lado del servidor:

Después de generar el archivo YAML de la clave de acceso dinámica, debes enviárselo a tus usuarios. Puedes alojar el archivo en un servicio de alojamiento web estático o generarlo de forma dinámica. [Más información sobre cómo usar claves de acceso dinámicas](../management/dynamic-access-keys)

## Paso 4: Conéctate con el cliente de Outline

Utiliza una de las aplicaciones oficiales del [cliente de Outline](../../download-links) (versión 1.15.0 y posteriores) y añade la clave de acceso dinámica que acabas de crear como entrada del servidor. Haz clic en **Conectar** para empezar la tunelización a tu servidor usando la configuración de Shadowsocks a través de Websockets.

Utiliza una herramienta como [IPInfo](https://ipinfo.io) para comprobar que estés navegando por Internet mediante tu servidor de Outline.
