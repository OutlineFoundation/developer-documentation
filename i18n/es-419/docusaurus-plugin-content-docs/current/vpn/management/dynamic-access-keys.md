---
title: "Dynamic Access Keys"
sidebar_label: "Dynamic Access Keys"
---

Outline ofrece dos tipos de claves de acceso: estáticas y dinámicas. Las estáticas codifican
toda la información de conexión en sí mismas, mientras que las dinámicas codifican
la ubicación de la información de conexión, lo que permite almacenar esos
datos de forma remota y cambiarlos si es necesario. Esto significa que puedes actualizar la
configuración del servidor sin tener que generar nuevas claves ni distribuirlas a los
usuarios. En este documento, se explica cómo usar claves de acceso dinámicas para administrar
el servidor de Outline con mayor flexibilidad y eficiencia.

Existen tres formatos para especificar la información de acceso que utilizarán
tus claves de acceso dinámicas:

### Usa un vínculo `ss://`

*Cliente de Outline 1.8.1 y versiones posteriores*

Puedes usar directamente un vínculo `ss://` que ya tengas. Este método es ideal si no
necesitas cambiar el servidor, el puerto o el método de encriptación con frecuencia, pero aún quieres
disponer de flexibilidad para actualizar la dirección del servidor.

**Ejemplo:**

### Usa un objeto JSON

*Cliente de Outline 1.8.0 y versiones posteriores.*

Este método ofrece más flexibilidad para administrar todos los aspectos de la
conexión de Outline de los usuarios. Puedes actualizar el servidor, el puerto, la contraseña y el método de encriptación
de esta manera.

**Ejemplo:**

- **server:** Es el dominio o la dirección IP del servidor de VPN.

- **server_port:** Es el número de puerto en el que se ejecuta el servidor de VPN.

- **password:** Es la contraseña obligatoria para conectarse a la VPN.

- **method:** Es el método de encriptación que usa la VPN. Consulta los
[algoritmos de cifrado de AEAD](https://shadowsocks.org/doc/aead.html) que admite Shadowsocks.

### Usa un objeto YAML

*Cliente de Outline 1.15.0 y versiones posteriores.*

Este método es similar al método JSON anterior, pero agrega aún más
flexibilidad aprovechando el formato de configuración avanzada de Outline. Puedes
actualizar el servidor, el puerto, la contraseña, el método de encriptación y mucho más.

**Ejemplo:**

- **transport:** Define los protocolos de transporte que se usarán (TCP y UDP en
este caso).

- **tcp/udp:** Especifica la configuración para cada protocolo.

    - **$type:** Indica el tipo de configuración (que en este caso es shadowsocks).

    - **endpoint:** Es el dominio o la dirección IP y el puerto del servidor de VPN.

    - **secret:** Es la contraseña obligatoria para conectarse a la VPN.

    - **cipher:** Es el método de encriptación que usa la VPN. Consulta los
[algoritmos de cifrado de AEAD](https://shadowsocks.org/doc/aead.html)
que admite Shadowsocks.

Consulta [Configuración de las claves de acceso](config) y conoce todas maneras en las que puedes
configurar el acceso a tu servidor de Outline, incluidos transportes, extremos,
marcadores y objetos de escucha de paquetes.

## Extrae información de acceso de una clave estática

Si ya tienes una clave de acceso estática, puedes extraer su información para
crear una clave de acceso dinámica basada en JSON o YAML. Las claves de acceso estáticas siguen
este patrón:

Ejemplo:

- **Servidor:** `outline-server.example.com`

- **Puerto del servidor:** `8388`

- **Información del usuario:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl`; se decodifica como
[base64](https://en.wikipedia.org/wiki/Base64) con soluciones como [Codificar/Decodificar de la Caja de herramientas para administradores de Google](https://toolbox.googleapps.com/apps/encode_decode/)

    - **Método**: `chacha20-ietf-poly1305`

    - **Contraseña**: `example`

## Elige una plataforma de hosting

Ahora que sabes crear claves de acceso dinámicas, es importante
elegir una plataforma de hosting adecuada para la configuración de las claves de acceso. Cuando
tomes esta decisión, considera factores como la confiabilidad,
la seguridad, la facilidad de uso y la resistencia a la censura de la plataforma. ¿La plataforma entregará de manera coherente
la información de las claves de acceso sin tiempos de inactividad? ¿Ofrece medidas
de seguridad adecuadas para proteger la configuración? ¿Qué tan fácil es administrar
la información de las claves de acceso en la plataforma? ¿Se puede acceder a la plataforma en regiones
donde se censura Internet?

Para situaciones en las que el acceso a la información pueda estar restringido, considera alojarlas
en plataformas resistentes a la censura, como [Google Drive](https://drive.google.com),
[pad.riseup.net](https://pad.riseup.net/), [Amazon
S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html)
(con acceso con estilo de ruta),
[Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96),
o [gists de GitHub
secretos](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
Evalúa las necesidades específicas de tu implementación y elige una plataforma que se ajuste
a tus requisitos de accesibilidad y seguridad.
