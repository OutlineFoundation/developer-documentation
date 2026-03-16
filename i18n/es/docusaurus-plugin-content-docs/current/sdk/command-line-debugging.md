---
title: "Caracterización y omisión remota de interferencias de red con el SDK de Outline"
sidebar_label: "Caracterización y omisión remota de interferencias de red con el SDK de Outline"
---

En esta guía, se muestra cómo usar las herramientas de línea de comandos del SDK de Outline para comprender y evitar la interferencia de red desde una perspectiva remota. Aprenderás a usar las herramientas del SDK para medir la interferencia de la red, probar estrategias de elusión y analizar los resultados. En esta guía, nos centraremos en las herramientas `resolve`, `fetch` y `http2transport`.

## Primeros pasos con las herramientas del SDK de Outline

Puedes comenzar a usar las herramientas del SDK de Outline directamente desde la línea de comandos.

### Resolver DNS

La herramienta `resolve` te permite realizar búsquedas de DNS con un agente de resolución especificado.

Para resolver el registro A de un dominio, haz lo siguiente:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

Para resolver un registro CNAME, sigue estos pasos:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### Cómo recuperar una página web

La herramienta `fetch` se puede usar para recuperar el contenido de una página web.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

También puede forzar la conexión para que use QUIC.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### Usa un proxy local

La herramienta `http2transport` crea un proxy local para enrutar tu tráfico.
Para iniciar un proxy local con un transporte de Shadowsocks, haz lo siguiente:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

Luego, puedes usar este proxy con otras herramientas, como curl:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## Especifica estrategias de elusión

El SDK de Outline permite especificar varias estrategias de elusión que se pueden combinar para evitar diferentes formas de interferencia de red. La especificación de estas estrategias se encuentra en la [documentación de Go](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x@v0.0.3/configurl).

### Estrategias componibles

Estas estrategias se pueden combinar para crear técnicas de elusión más sólidas.

* **DNS-over-HTTPS con fragmentación de TLS**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5 a través de TLS con Domain Fronting**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Enrutamiento de varios saltos con Shadowsocks**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## Acceso y medición remotos

Para medir la interferencia de la red tal como se experimenta en diferentes regiones, puedes usar proxies remotos. Puedes buscar o crear proxies remotos para conectarte.

### Opciones de acceso remoto

Con la herramienta `fetch`, puedes probar las conexiones de forma remota de varias maneras.

#### Servidor de Outline

Conéctate de forma remota a un servidor de Outline estándar con un transporte de Shadowsocks.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 a través de SSH

Crea un proxy SOCKS5 con un túnel SSH.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

Conéctate a ese túnel con fetch

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## Caso de éxito: Cómo eludir el bloqueo de YouTube en Irán

Este es un ejemplo práctico para detectar y evitar la interferencia de la red.

### Cómo detectar el bloqueo

Cuando se intenta recuperar la página principal de YouTube a través de un proxy iraní, se agota el tiempo de espera de la solicitud, lo que indica un bloqueo.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

Este comando falla con un tiempo de espera agotado.

### Bypass con fragmentación de TLS

Si agregamos la fragmentación de TLS al transporte, podemos omitir este bloqueo.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Este comando recupera correctamente el título de la página principal de YouTube, que es `<title>YouTube</title>`.

### Bypass con fragmentación de TLS y DNS-over-HTTPS

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Esto también devuelve `<title>YouTube</title>` correctamente.

### Cómo omitir la censura con un servidor de Outline

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Esto también devuelve `<title>YouTube</title>`.

## Análisis y recursos adicionales

Para ver debates y preguntas, visita el [grupo de debate del SDK de Outline](https://github.com/OutlineFoundation/outline-sdk/discussions).
