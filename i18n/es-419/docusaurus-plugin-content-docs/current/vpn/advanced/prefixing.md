---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

A partir de la versión 1.9.0 del cliente de Outline, las claves de acceso admiten la opción "prefijo". El
"prefijo" es una lista de bytes que se usan como los primeros de la 
[sal](https://shadowsocks.org/guide/aead.html) de una conexión TCP de Shadowsocks.
Esto puede hacer que la conexión parezca un protocolo que se permite en la
red y, así, eludir firewalls que rechazan protocolos que no reconocen.

## ¿Cuándo debo probar esta opción?

Si sospechas que aún se bloquea a los usuarios de tu implementación de Outline, recomendamos
que pruebes algunos prefijos diferentes.

## Instrucciones

El prefijo no debe exceder los 16 bytes. Los prefijos más largos pueden causar colisiones
de sal, que pueden comprometer la seguridad de la encriptación y provocar que se detecten
las conexiones. Usa el prefijo más corto para evitar el bloqueo
que enfrentas.

El puerto que uses deberá coincidir con el protocolo que pretende simular tu prefijo.
IANA mantiene un [registro de números de puertos de protocolo de transporte](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
que asigna protocolos y números de puertos.

Algunos ejemplos de prefijos eficaces son similares a protocolos comunes:

Puerto recomendado
Codificado con JSON
Codificado con URL

Solicitud HTTP
80 (HTTP)
`"POST "`
`POST%20`

Respuesta HTTP
80 (HTTP)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

Solicitud de DNS por TCP
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443 (https), 463 (smtp), 563 (nntp), 636 (ldap), 989 (ftp-data), 990 (ftp), 993 (imap), 995 (pop3), 5223 (Apple APN), 5228 (Play Store), 5349 (turn)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

Datos de aplicación de TLS
443 (https), 463 (smtp), 563 (nntp), 636 (ldap), 989 (ftp-data), 990 (ftp), 993 (imap), 995 (pop3), 5223 (Apple APN), 5228 (Play Store), 5349 (turn)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

TLS ServerHello
443 (https), 463 (smtp), 563 (nntp), 636 (ldap), 989 (ftp-data), 990 (ftp), 993 (imap), 995 (pop3), 5223 (Apple APN), 5228 (Play Store), 5349 (turn)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh), 830 (netconf-ssh), 4334 (netconf-ch-ssh), 5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### Claves de acceso dinámicas

Para usar la función de prefijo con [claves de acceso dinámicas](../management/dynamic-access-keys) (`ssconf://`),
agrega una clave de "prefijo" al objeto JSON, con un valor **codificado con JSON** que represente el prefijo que quieres (revisa los ejemplos en la tabla de arriba). Puedes
usar códigos de escape (como \u00FF) para representar puntos de código Unicode en
el rango de `U+0` a `U+FF`. Por ejemplo:

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### Claves de acceso estáticas

Para usar prefijos con **claves de acceso estáticas** (ss://), deberás modificar tu
clave existente antes de distribuirla. Si tienes una clave de acceso estática generada
por Outline Manager, toma una versión **codificada con URL** de tu prefijo (revisa ejemplos
de estos en la tabla de arriba) y agrégala al final de la clave de acceso como se muestra aquí:

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Para los usuarios avanzados, puedes usar la función `encodeURIComponent()` de tu navegador
para convertir tu prefijo **codificado con JSON** a uno **codificado con URL**. Para hacerlo,
abre la consola de tu inspector web
(*Desarrollador > Consola web de JavaScript *en Chrome) y escribe lo siguiente:

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

Presiona Intro. El valor que se produzca será la *versión *codificada con URL. Por ejemplo:

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
