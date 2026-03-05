---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

En esta guía se explica cómo utilizar [Caddy](https://caddyserver.com/), un servidor web potente y fácil de usar, para mejorar la configuración de tu servidor de Outline. Las funciones [HTTPS automáticas](https://caddyserver.com/docs/automatic-https) y la configuración flexible de Caddy la convierten en una opción excelente para ofrecer tu servidor de Outline, especialmente cuando se usa un transporte de WebSocket.

## ¿Qué es Caddy?

Caddy es un servidor web de software libre conocido por su facilidad de uso, sus HTTPS automáticas y su compatibilidad con varios protocolos. Permite simplificar la configuración de servidores web y ofrece características como las siguientes:

- **HTTPS automáticas:** Caddy obtiene y renueva automáticamente los certificados TLS para asegurar que las conexiones sean seguras.

- **Compatibilidad con HTTP/3:** Caddy admite el protocolo HTTP/3 más reciente para proporcionar un tráfico web más rápido y eficiente.

- **Ampliable con complementos:** Caddy puede ampliarse mediante complementos para admitir diversas funciones, como los proxys inversos y el balanceo de carga.

## Paso 1: Requisitos previos

- Descarga e instala [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Paso 2: Configuración de tu dominio

Antes de empezar a usar Caddy, comprueba que el nombre de tu dominio se haya configurado correctamente de forma que dirija a la dirección IP de tu servidor.

- **Configura registros A o AAAA:** inicia sesión en tu proveedor de DNS y configura registros A y AAAA para que tu dominio dirija a las direcciones IPv4 e IPv6 de tu servidor, respectivamente.

- 

**Verifica los registros DNS:** verifica que tus registros DNS estén correctamente configurados mediante una búsqueda autorizada:

## Paso 3: Desarrollo y ejecución de una compilación personalizada de Caddy

Si usas `xcaddy`, puedes desarrollar un binario `caddy` personalizado que incluya el módulo de servidores principales de Outline y otros módulos de extensiones de servidor necesarios.

## Paso 4: Configuración y ejecución del servidor Caddy con Outline

Crea un archivo `config.yaml` con la siguiente configuración:

Esta configuración se corresponde con una estrategia de Shadowsocks a través de WebSockets con un servidor web que escucha en el puerto `443`, mientras se acepta el tráfico envuelto de Shadowsocks de TCP y UDP en las rutas `TCP_PATH` y `UDP_PATH`, respectivamente.

Ejecuta el servidor de Caddy ampliado con Outline usando la configuración creada:

Puedes encontrar más configuraciones de ejemplo en nuestro [repositorio de GitHub outline-ss-server/outlinecaddy](https://github.com/Jigsaw-Code/outline-ss-server/tree/master/outlinecaddy/examples).

## Paso 5: Creación de una clave de acceso dinámica

Genera un archivo YAML de clave de acceso de cliente para tus usuarios utilizando el formato de [configuración avanzada](../management/config) e incluye los endpoints de WebSocket que has definido previamente del lado del servidor:

Después de generar el archivo YAML de la clave de acceso dinámica, debes enviárselo a tus usuarios. Puedes alojar el archivo en un servicio de alojamiento web estático o generarlo de forma dinámica. [Más información sobre cómo usar claves de acceso dinámicas](../management/dynamic-access-keys)

## Paso 6: Conexión con el cliente de Outline

Utiliza una de las aplicaciones oficiales de [cliente de Outline](../../download-links) (versiones 1.15.0 y posteriores) y añade la clave de acceso dinámica que acabas de crear como entrada de servidor. Haz clic en **Conectar** para empezar la tunelización a tu servidor usando la configuración de Shadowsocks a través de Websocket.

Utiliza una herramienta como [IPInfo](https://ipinfo.io) para verificar que tienes acceso a Internet mediante tu servidor de Outline.
