---
title: "Ocultación de prefijo de conexión"
sidebar_label: "Ocultación de prefijo de conexión"
---

Desde la versión 1.9.0 del cliente de Outline, las claves de acceso admiten la opción "prefix". Esta opción es una lista de bytes que sirven como los primeros bytes de la [salt](https://shadowsocks.org/guide/aead.html) de una conexión TCP de Shadowsocks.
De esta forma, la conexión puede parecer un protocolo permitido en la red, lo que le permite eludir los cortafuegos que rechazan los protocolos desconocidos.

## ¿Cuándo debería optar por esta opción? {#when_should_i_try_this}

Si sospechas que se sigue bloqueando a los usuarios de tu despliegue de Outline, te recomendamos probar distintos prefijos.

## Instrucciones {#instructions}

El prefijo no debe tener más de 16 bytes. Los prefijos más largos pueden provocar colisiones en la salt, lo que puede poner en riesgo la seguridad del cifrado y hacer que las conexiones se detecten. Usa el prefijo más corto posible para sortear el bloqueo que te hayas encontrado.

El puerto que uses debe coincidir con el protocolo que esté simulando el prefijo.
La IANA tiene un [registro de los números de puerto de los protocolos de transporte](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) que asocia protocolos y números de puerto.

Estos son algunos ejemplos de prefijos eficaces que parecen protocolos habituales:

Puerto recomendado
Codificado como JSON
Codificado como URL

Solicitud HTTP
80 (http)
`"POST "`
`POST%20`

Respuesta HTTP
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

Solicitud DNS-over-TCP
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

TLS Application Data
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

TLS ServerHello
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh), 830 (netconf-ssh), 4334 (netconf-ch-ssh), 5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### Claves de acceso dinámicas {#dynamic_access_keys}

Para usar la opción de prefijo con las [claves de acceso dinámicas](../management/dynamic-access-keys) (`ssconf://`), añade una clave "prefix" al objeto JSON, con un valor **codificado como JSON** que represente el prefijo que quieras (consulta algunos ejemplos en la tabla de arriba). Puedes usar códigos de escape (como \u00FF) para representar puntos de código Unicode no imprimibles en el intervalo de `U+0` a `U+FF`. Por ejemplo:

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### Claves de acceso estáticas {#static_access_keys}

Para usar prefijos con las **claves de acceso estáticas** (ss://), debes modificar tu clave antes de distribuirla. Si tienes una clave de acceso estática generada por Administrador de Outline, consigue una versión de tu prefijo **codificada como URL** (consulta algunos ejemplos en la tabla de arriba) y añádela al final de la clave de acceso de esta forma:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Si eres un usuario avanzado, puedes usar la función `encodeURIComponent()` de tu navegador para convertir tu prefijo **codificado como JSON** en uno **codificado como URL**. Para ello, abre la pestaña Consola del inspector web (*Desarrollador > consola web de JavaScript* en Chrome) y escribe lo siguiente:

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Pulsa Intro. El valor que se genera es la versión *codificada como URL*. Por ejemplo:

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
