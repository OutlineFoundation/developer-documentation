---
title: "Config"
sidebar_label: "Config"
---

## Túneles {#tunnels}

### TunnelConfig {#tunnelconfig}

Túnel es el objeto de nivel superior en una configuración de Outline y especifica cómo debe
configurarse la VPN.

**Formato:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig {#explicittunnelconfig}

**Formato:** *struct*

**Campos:**

- `transport` ([TransportConfig](#transportconfig)): Es el transporte que se utilizará para
intercambiar paquetes con el destino objetivo.

- `error` (*struct*): Contiene información que recibirá el usuario si se produce
un error en el servicio (p. ej., si venció la clave o se agotó la cuota).

    - `message` (*string*): Es un mensaje fácil de entender que verá el usuario.

    - `details` (*string*): Es el mensaje que verá el usuario cuando abra los
detalles del error. Debe ser útil para solucionar problemas.

Los campos `error` y `transport` son mutuamente excluyentes.

Ejemplo sin errores:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Ejemplo con errores:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Transportes {#transports}

### TransportConfig {#transportconfig}

Especifica cómo deben intercambiarse los paquetes con el destino objetivo.

**Formato:** [Interface](#interface)

Tipos de Interfaces admitidos:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig {#tcpudpconfig}

Permite establecer estrategias distintas para TCP y UDP.

**Formato:** *struct*

**Campos:**

- `tcp` ([DialerConfig](#dialerconfig)): Es el marcador de paquete que se usará para las conexiones
TCP.

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): Es el objeto de escucha de paquete
que se usará para los paquetes UDP.

Ejemplo de envío TCP y UDP a diferentes extremos:

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

## Extremos {#endpoints}

Los Extremos establecen conexiones con un extremo fijo. Se prefieren sobre los
marcadores, ya que permiten optimizaciones específicas para cada extremo. Existen Extremos
de transmisión y de paquete.

### EndpointConfig {#endpointconfig}

**Formato:** *string* | [Interface](#interface)

El Extremo *string* es la dirección host:puerto del extremo seleccionado. La
conexión se establece a través del Marcador predeterminado.

Tipos de Interfaces admitidos para los Extremos de transmisión y de paquete:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig {#dialendpointconfig}

Establece conexiones marcando una dirección fija. Puede llevar un marcador, lo que
permite combinar estrategias.

**Formato:** *struct*

**Campos:**

- `address` (*string*): Es la dirección del extremo que se debe marcar.

- `dialer` ([DialerConfig](#dialerconfig)): Es el marcador que se usará para marcar la
dirección.

### WebsocketEndpointConfig {#websocketendpointconfig}

Tuneliza conexiones de transmisión y de paquete hacia un extremo a través de WebSockets.

Para las conexiones de transmisión, cada escritura se convierte en un mensaje de WebSocket. En el caso de
las conexiones de paquetes, cada paquete se convierte en un mensaje de WebSocket.

**Formato:** *struct*

**Campos:**

- `url` (*string*): Es la URL del extremo de WebSocket. El esquema debe ser
`https` o `wss` para WebSocket sobre TLS, y `http` o `ws` en el caso de WebSocket
con texto simple.

- `endpoint` ([EndpointConfig](#endpointconfig)): Es el extremo del servidor web al
que hay que conectarse. Si no existe, se conecta a la dirección especificada en la URL.

## Marcadores {#dialers}

Los Marcadores establecen conexiones a partir de una dirección de extremo. Hay Marcadores de transmisión y de paquete.

### DialerConfig {#dialerconfig}

**Formato:** *null* | [Interface](#interface)

El Marcador *null* (ausente) corresponde al Dialer predeterminado, que usa conexiones TCP
directas para transmisión y conexiones UDP directas para paquetes.

Tipos de Interfaces admitidos para Marcadores de transmisión y de paquete.

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Objetos de escucha de paquete {#packet_listeners}

Un objeto de escucha de paquete establece una conexión de paquetes no delimitada que puede usarse para
enviar paquetes a múltiples destinos.

### PacketListenerConfig {#packetlistenerconfig}

**Formato:** *null* | [Interface](#interface)

El objeto de escucha de paquete *null* (ausente) corresponde al objeto de escucha de paquete predeterminado,
que funciona con UDP.

Tipos de Interfaces admitidos:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Estrategias {#strategies}

### Shadowsocks {#shadowsocks}

#### LegacyShadowsocksConfig {#legacyshadowsocksconfig}

LegacyShadowsocksConfig representa un túnel que utiliza Shadowsocks como
transporte. Implementa el formato heredado por motivos de retrocompatibilidad.

**Formato:** *struct*

**Campos:**

- `server` (*string*): Es el host al que hay que conectarse.

- `server_port` (*number*): Es el número del puerto al que hay que conectarse.

- `method` (*string*): Es el [algoritmo de cifrado
de AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) que hay que usar.

- `password` (*string*): Se usa para generar la clave de encriptación.

- `prefix` (*string*): Es el [enmascaramiento
del prefijo](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) que hay que usar.
Se admite en conexiones de transmisiones y de paquetes.

Ejemplo:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI {#legacyshadowsocksuri}

LegacyShadowsocksURI representa un túnel que utiliza Shadowsocks como
transporte.
Implementa el formato de URL heredado por motivos de retrocompatibilidad.

**Formato:** *string*

Consulta el [formato LegacyShadowsocksURI](https://shadowsocks.org/doc/configs.html#uri-and-qr-code)
y el [esquema de
URI SIP002](https://shadowsocks.org/doc/sip002.html). No admitimos complementos.

Ejemplo:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig {#shadowsocksconfig}

ShadowsocksConfig puede representar a Dialers de transmisión o de paquete, así como a un objeto de escucha de paquete que usa Shadowsocks.

**Formato:** *struct*

**Campos:**

- `endpoint` ([EndpointConfig](#endpointconfig)): Es el extremo de Shadowsocks al
que hay que conectarse.

- `cipher` (*string*): Es el [algoritmo de cifrado
de AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) que hay que usar.

- `secret` (*string*): Se usa para generar la clave de encriptación.

- `prefix` (*string*, opcional): Es el [enmascaramiento
del prefijo](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) que hay que usar.
Se admite en conexiones de transmisiones y de paquetes.

Ejemplo:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Metadefiniciones {#meta_definitions}

### FirstSupportedConfig {#firstsupportedconfig}

Usa el primer parámetro de configuración que admite la app. Es una forma de
incorporar nuevos parámetros sin dejar de admitir los anteriores.

**Formato:** *struct*

**Campos:**

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)): Es la lista de opciones que
se consideran.

Ejemplo:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface {#interface}

Las Interfaces permiten elegir una implementación entre varias. Usa el
campo `$type` para especificar el tipo que representa ese parámetro de configuración.

Ejemplo:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
