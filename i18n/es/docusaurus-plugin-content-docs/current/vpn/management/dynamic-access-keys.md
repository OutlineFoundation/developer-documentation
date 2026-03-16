---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

Outline ofrece dos tipos de claves de acceso: estáticas y dinámicas. Con las claves estáticas, toda la información de conexión se codifica en la misma clave. Con las claves dinámicas, se codifica la ubicación de la información de conexión, lo que te permite almacenar esa información de forma remota y modificarla si es necesario. Esto significa que puedes actualizar la configuración de tu servidor sin tener que generar ni distribuir claves nuevas a tus usuarios. En este documento se explica cómo puedes usar las claves de acceso dinámicas para gestionar tu servidor de Outline de una forma más flexible y eficiente.

Hay tres formatos para especificar la información de acceso que utilizarán tus claves de acceso dinámicas:

### Usar un enlace `ss://` {#use_an_ss_link}

*Versiones 1.8.1 o posteriores del cliente de Outline.*

Puedes usar un enlace `ss://` que ya tengas directamente. Este método es ideal si no necesitas cambiar con frecuencia el servidor, el puerto ni el método de cifrado, pero quieres tener flexibilidad para actualizar la dirección del servidor.

**Ejemplo:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### Usar un objeto JSON {#use_a_json_object}

*Versiones 1.8.0 o posteriores del cliente de Outline.*

Este método ofrece más flexibilidad para gestionar todos los aspectos de la conexión a Outline de tus usuarios. Te permite actualizar el servidor, el puerto, la contraseña y el método de cifrado.

**Ejemplo:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server:** la dirección IP o del dominio de tu servidor de VPN.

- **server_port:** el número de puerto en el que se ejecuta tu servidor de VPN.

- **password:** la contraseña necesaria para conectarse a la VPN.

- **method:** el método de cifrado que usa la VPN. Consulta los [algoritmos de cifrado de AEAD](https://shadowsocks.org/doc/aead.html) compatibles con Shadowsocks.

### Usar un objeto YAML {#use_a_yaml_object}

*Versiones 1.15.0 o posteriores del cliente de Outline.*

Este método es similar al método JSON anterior, pero añade aún más flexibilidad al aprovechar el formato de configuración avanzado de Outline. Puedes actualizar el servidor, el puerto, la contraseña, el método de cifrado y mucho más.

**Ejemplo:**

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
  udp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
```

- **transport:** define los protocolos de transporte que deben usarse (TCP y UDP en este caso).

- **tcp/udp:** especifica la configuración de cada protocolo.

    - **$type:** indica el tipo de configuración, que en este caso es Shadowsocks.

    - **endpoint:** la dirección IP o del dominio y el puerto de tu servidor de VPN.

    - **secret:** la contraseña necesaria para conectarse a la VPN.

    - **cipher:** el método de cifrado que usa la VPN. Consulta los [algoritmos de cifrado de AEAD](https://shadowsocks.org/doc/aead.html) compatibles con Shadowsocks.

Consulta el artículo [Configuración de claves de acceso](config) para obtener información sobre todos los métodos de configuración del acceso a tu servidor de Outline, incluidos los transportes, los endpoints, los marcadores y los procesadores de paquetes.

## Obtener información de acceso a partir de una clave estática {#extract_access_information_from_a_static_key}

Si tienes una clave de acceso estática, puedes obtener la información necesaria para crear una clave de acceso dinámica basada en JSON o YAML. Las claves de acceso estáticas siguen el siguiente patrón:

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Ejemplo:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Servidor:** `outline-server.example.com`

- **Puerto del servidor:** `8388`

- **Información del usuario:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` decodificado con el formato [base64](https://en.wikipedia.org/wiki/Base64) con una herramienta como [la codificación o la decodificación de Caja de herramientas de Google Admin](https://toolbox.googleapps.com/apps/encode_decode/)

    - **Método:** `chacha20-ietf-poly1305`

    - **Contraseña:** `example`

## Elegir una plataforma de alojamiento {#choose_a_hosting_platform}

Ahora que sabes cómo crear claves de acceso dinámicas, es importante que elijas una plataforma de alojamiento adecuada para la configuración de tus claves de acceso. Al tomar esta decisión, ten en cuenta factores como la fiabilidad, la seguridad, la facilidad de uso y la resistencia a la censura de la plataforma. Pregúntate lo siguiente: ¿la plataforma proporcionará de manera uniforme tu información de claves de acceso sin periodos de inactividad? ¿Ofrece medidas de seguridad adecuadas para proteger tu configuración? ¿Te resulta fácil gestionar tu información de claves de acceso en ella? ¿Es accesible en regiones que censuran Internet?

En los casos en que el acceso a la información podría estar restringido, te recomendamos alojar tus claves en plataformas resistentes a la censura como [Google Drive](https://drive.google.com), [pad.riseup.net](https://pad.riseup.net/), [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) (con acceso de estilo ruta), [Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) o los [gists secretos de GitHub](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
Evalúa las necesidades específicas de tu implementación y elige una plataforma que vaya en línea con tus requisitos de accesibilidad y seguridad.
