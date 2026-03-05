---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline utiliza una configuración basada en YAML para definir los parámetros VPN y gestionar
el tráfico TCP/UDP. La configuración admite la componibilidad en múltiples niveles,
lo que permite establecer parámetros de configuración flexibles y extensibles.

La configuración de nivel superior especifica una
[TunnelConfig](../reference/access-key-config#tunnelconfig).

## Ejemplos

Una configuración habitual de Shadowsocks se vería de la siguiente manera:

Observa cómo ahora podemos tener los protocolos TCP y UDP ejecutándose en diferentes puertos o extremos
con prefijos diferentes.

Puedes usar anclas YAML y la clave de combinación `<<` para evitar la duplicación:

Ahora puedes crear estrategias y saltos múltiples:

En caso de bloqueo de protocolos "look-like-nothing" como Shadowsocks, puedes
usar Shadowsocks sobre WebSockets. Consulta la [configuración de ejemplo del
servidor](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)
para saber cómo implementarla. Una configuración del cliente se vería de la siguiente manera:

Ten en cuenta que el extremo de WebSocket puede, a su vez, tomar un extremo, que se puede
aprovechar para evitar el bloqueo basado en DNS:

Para garantizar la compatibilidad entre las distintas versiones del cliente de Outline, usa la opción
`first-supported` en la configuración. Esto es muy importante
a medida que se agregan nuevas estrategias y funciones a Outline, ya que es posible que no todos los usuarios
actualicen a la versión más reciente del software del cliente. Con `first-supported`, puedes
proporcionar una única configuración que funcione sin problemas en diversas plataformas
y versiones de clientes, lo que garantiza la retrocompatibilidad y una experiencia del usuario
coherente.
