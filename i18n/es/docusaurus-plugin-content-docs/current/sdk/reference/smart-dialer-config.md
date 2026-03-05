---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

El **marcador inteligente** busca una estrategia que desbloquee DNS y TLS en la lista proporcionada de dominios de prueba. Necesita una configuración que describa varias estrategias entre las que elegir.

## Configuración de YAML para el marcador inteligente

El marcador inteligente necesita una configuración en formato YAML. Aquí tienes un ejemplo:

### Configuración de DNS

- El campo `dns` especifica la lista de resoluciones de DNS que se deben probar.

- Las resoluciones de DNS pueden ser de uno de estos tipos:

    - `system`: usa la resolución del sistema. Se especifica con un objeto vacío.

    - `https`: usa una resolución de DNS‑over‑HTTPS (DoH) cifrada.

    - `tls`: usa una resolución de DNS a través de TLS cifrada.

    - `udp`: usa una resolución de UDP.

    - `tcp`: usa una resolución de TCP.

#### Resolución de DNS‑over‑HTTPS (DoH)

- `name`: nombre de dominio del servidor de DoH.

- `address`: host:puerto del servidor de DoH. El valor predeterminado es `name`:443.

#### Resolución de DNS a través de TLS (DoT)

- `name`: nombre de dominio del servidor de DoT.

- `address`: host:puerto del servidor de DoT. El valor predeterminado es `name`:853.

#### Resolución de UDP

- `address`: host:puerto de la resolución de UDP.

#### Resolución de TCP

- `address`: host:puerto de la resolución de TCP.

### Configuración de TLS

- El campo `tls` especifica la lista de transportes TLS que se deben probar.

- Cada transporte TLS es una cadena que especifica qué transporte se debe usar.

- Por ejemplo, `override:host=cloudflare.net|tlsfrag:1` especifica un transporte que usa ocultación de dominios con Cloudflare y fragmentación de TLS. Para obtener más información, consulta la [documentación sobre la configuración](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format).

### Configuración de respaldo

Si ninguna de las estrategias sin proxy logra conectar, se usa una configuración de respaldo. Por ejemplo, se puede especificar que un servidor proxy de copia de seguridad intente establecer la conexión del usuario. El método de respaldo tarda más en iniciarse, ya que antes deben fallar o agotar el tiempo de espera las demás estrategias de DNS o TLS.

Las cadenas de respaldo deben ser lo siguiente:

- Una cadena de configuración `StreamDialer` válida, tal como se defina en [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols).

- Un objeto de configuración de Psiphon válido que sea un elemento secundario de un campo `psiphon`.

#### Ejemplo de servidor Shadowsocks

#### Ejemplo de servidor SOCKS5

#### Ejemplo de configuración de Psiphon

Para usar la red [Psiphon](https://psiphon.ca/), debes hacer lo siguiente:

1. Ponerte en contacto con el equipo de Psiphon para obtener una configuración que te dé acceso a su red. Puede que tengas que firmar un contrato.

2. Añadir la configuración de Psiphon que recibas a la sección `fallback` de la configuración de tu marcador inteligente. JSON es compatible con YAML, así que puedes copiar y pegar la configuración de Psiphon directamente en la sección `fallback`, como en este ejemplo:

### Cómo usar el marcador inteligente

Para usar el marcador inteligente, crea un objeto `StrategyFinder` y llama al método `NewDialer` pasando la lista de dominios de prueba y la configuración de YAML.
El método `NewDialer` devuelve un objeto `transport.StreamDialer` que sirve para crear conexiones empleando la estrategia encontrada. Por ejemplo:

Este es un ejemplo básico que quizá debas adaptar a tu caso práctico específico.
