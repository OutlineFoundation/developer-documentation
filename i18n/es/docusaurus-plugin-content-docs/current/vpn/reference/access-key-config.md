---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## Túneles

### TunnelConfig

Los túneles son los objetos de nivel superior en una configuración de Outline e indican cómo debe configurarse la VPN.

**Formato:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**Formato:** *struct*

**Campos:**

- `transport` ([TransportConfig](#transportconfig)): transporte que debe usarse para intercambiar paquetes con el destino.

- `error` (*struct*): información que debe comunicarse al usuario si hay un error de servicio (por ejemplo, si la clave ha caducado o la cuota se ha agotado).

    - `message` (*cadena*): mensaje legible que se mostrará al usuario.

    - `details` (*cadena*): mensaje que se mostrará cuando el usuario despliegue los detalles del error. Sirve para solucionar problemas.

Los campos `error` y `transport` se excluyen entre sí.

Ejemplo de operación correcta:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Ejemplo de error:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Transportes

### TransportConfig

Objeto que especifica cómo deben intercambiarse los paquetes con el destino.

**Formato:** [Interface](#interface)

Tipos de Interface admitidos:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

TCPUDPConfig permite configurar estrategias de TCP y UDP por separado.

**Formato:** *struct*

**Campos:**

- `tcp` ([DialerConfig](#dialerconfig)): marcador de flujos que debe usarse para las conexiones TCP.

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): agente de escucha de paquetes que debe usarse para los paquetes UDP.

Ejemplo de envío de TCP y UDP a distintos endpoints:

```yaml
tcp:
  $type: shadowsocks
  endpoint: ss.example.com:80
  <<: &cipher
    cipher: chacha20-ietf-poly1305
    secret: SECRET
  prefix: "POST "

udp:
  $type: shadowsocks
  endpoint: ss.example.com:53
  <<: *cipher
```

## Endpoints

Los endpoints establecen conexiones con un endpoint fijo. Son preferibles a los marcadores porque permiten hacer optimizaciones específicas del endpoint. Hay dos tipos: endpoints de flujos y de paquetes.

### EndpointConfig

**Formato:** *cadena* | [Interface](#interface)

La *cadena* del endpoint es la dirección host:puerto del endpoint seleccionado. La conexión se establece usando el valor predeterminado del marcador.

Tipos de Interface admitidos para endpoints de flujos y de paquetes:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

Establece las conexiones marcando una dirección fija. Puede usarse un marcador, lo que permite componer estrategias.

**Formato:** *struct*

**Campos:**

- `address` (*cadena*): la dirección del endpoint que se debe marcar.

- `dialer` ([DialerConfig](#dialerconfig)): el marcador que debe usarse para marcar la dirección.

### WebsocketEndpointConfig

Tuneliza las conexiones de flujos y de paquetes dirigidos a un endpoint a través de Websockets.

En el caso de las conexiones de flujos, cada escritura se convierte en un mensaje de Websocket. En el caso de las conexiones de paquetes, cada paquete se convierte en un mensaje de Websocket.

**Formato:** *struct*

**Campos:**

- `url` (*cadena*): URL del endpoint de Websocket. El esquema debe ser `https` o `wss` para Websocket a través de TLS, y `http` o `ws` para Websocket de texto sin formato.

- `endpoint` ([EndpointConfig](#endpointconfig)): endpoint del servidor web con el que se va a establecer la conexión. Si no se encuentra, se conecta a la dirección especificada de la URL.

## Marcadores

Los marcadores establecen conexiones cuando se indica la dirección de un endpoint. Hay dos tipos: marcadores de flujos y de paquetes.

### DialerConfig

**Formato:** *nulo* | [Interface](#interface)

El valor *nulo* (no se encuentra) del marcador es el marcador predeterminado, que usa conexiones TCP directas para conexiones de flujos y conexiones UDP directas para paquetes.

Tipos de Interface admitidos para marcadores de flujos y de paquetes:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Agentes de escucha de paquetes

Los agentes de escucha de paquetes establecen conexiones de paquetes no delimitadas que pueden usarse para enviar paquetes a varios destinos.

### PacketListenerConfig

**Formato:** *nulo* | [Interface](#interface)

El valor *nulo* (no se encuentra) del agente de escucha de paquetes es el agente predeterminado, concretamente, un agente de escucha de paquetes UDP.

Tipos de Interface admitidos:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Estrategias

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig representa un túnel que usa Shadowsocks como transporte. Implementa el formato antiguo para la retrocompatibilidad.

**Formato:** *struct*

**Campos:**

- `server` (*cadena*): host con el que se va a establecer la conexión.

- `server_port` (*número*): número de puerto con el que se va a establecer la conexión.

- `method` (*cadena*): el [algoritmo de cifrado de AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) que debe usarse.

- `password` (*cadena*): utilizado para generar la clave de cifrado.

- `prefix` (*cadena*): la [ocultación de prefijo](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) que se debe usar.
Se admite en conexiones de flujos y de paquetes.

Ejemplo:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

LegacyShadowsocksURI representa un túnel que usa Shadowsocks como transporte.
Implementa el formato antiguo de la URL para la retrocompatibilidad.

**Formato:** *cadena*

Consulta el [formato antiguo del URI de Shadowsocks](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) y el [esquema del URI de SIP002](https://shadowsocks.org/doc/sip002.html). No admitimos los complementos.

Ejemplo:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

ShadowsocksConfig puede representar marcadores de flujos o de paquetes, además de un agente de escucha de paquetes que usa Shadowsocks.

**Formato:** *struct*

**Campos:**

- `endpoint` ([EndpointConfig](#endpointconfig)): el endpoint de Shadowsocks con el que se va a establecer la conexión.

- `cipher` (*cadena*): el [algoritmo de cifrado de AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) que debe usarse.

- `secret` (*cadena*): utilizado para generar la clave de cifrado.

- `prefix` (*cadena*, opcional): la [ocultación de prefijo](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) que se debe usar.
Se admite en conexiones de flujos y de paquetes.

Ejemplo:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Metadefiniciones

### FirstSupportedConfig

Usa la primera configuración admitida por la aplicación. De esta forma, se incorporan configuraciones nuevas y, a la vez, se mantiene la retrocompatibilidad con las antiguas.

**Formato:** *struct*

**Campos:**

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)): lista de opciones que deben tenerse en cuenta.

Ejemplo:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface

Los objetos Interface permiten elegir una implementación de entre muchas. Utiliza el campo `$type` para especificar el tipo que esa configuración representa.

Ejemplo:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
