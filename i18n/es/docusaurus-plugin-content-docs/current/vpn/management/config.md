---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline usa una configuración basada en YAML para definir los parámetros de la VPN y gestionar el tráfico TCP/UDP. La configuración admite la componibilidad en varios niveles, por lo que es flexible y ampliable.

La configuración de nivel superior especifica [TunnelConfig](../reference/access-key-config#tunnelconfig).

## Ejemplos

Este es el aspecto de una configuración típica de Shadowsocks:

Fíjate en que ahora TCP y UDP pueden ejecutarse en puertos o endpoints distintos y con prefijos diferentes.

Puedes usar los anclas YAML y la clave de fusión `<<` para evitar los duplicados:

Ahora puedes redactar estrategias y hacer varios saltos:

Si se bloquean los protocolos que no se parecen a nada en particular como Shadowsocks, puedes usar la técnica Shadowsocks a través de Websockets. Consulta el [ejemplo de configuración del servidor](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) para saber cómo implementarlo. Este es el aspecto de la configuración del cliente:

El endpoint de Websocket puede, a su vez, tomar un endpoint, que puede servir para sortear el bloqueo basado en DNS:

Para asegurar la compatibilidad entre las distintas versiones del cliente de Outline, usa la opción `first-supported` en tu configuración. Esto cobra especial importancia a medida que se añaden nuevas estrategias y funciones a Outline, ya que es posible que no todos los usuarios hayan actualizado a la versión más reciente del software cliente. Si usas `first-supported`, puedes ofrecer una configuración que funcione a la perfección en las distintas plataformas y versiones del cliente, lo que garantiza la retrocompatibilidad y una experiencia de usuario coherente.
