---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## Túneis {#tunnels}

### TunnelConfig {#tunnelconfig}

O túnel é o objeto de mais alto nível em uma configuração do Outline. Ele especifica como a
VPN deve ser configurada.

**Formato:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig {#explicittunnelconfig}

**Formato:** *struct*

**Campos:**

- `transport` ([TransportConfig](#transportconfig)): o transporte a ser usado para
trocar pacotes com o destino pretendido

- `error` (*struct*): informações a serem comunicadas ao usuário em caso de
erro de serviço (por exemplo, chave expirada, cota esgotada)

    - `message` (*string*): mensagem simples para exibir ao usuário

    - `details` (*string*): mensagem a ser exibida quando o usuário abrir os
detalhes do erro; útil para solução de problemas

Os campos `error` e `transport` são mutuamente exclusivos.

Exemplo bem-sucedido:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Exemplo de erro:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Transportes {#transports}

### TransportConfig {#transportconfig}

Especifica como os pacotes devem ser trocados com o destino pretendido.

**Formato:** [Interface](#interface)

Tipos de interface aceitos:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig {#tcpudpconfig}

O TCPUDPConfig permite definir estratégias TCP e UDP separadas.

**Formato:** *struct*

**Campos:**

- `tcp` ([DialerConfig](#dialerconfig)): o discador de fluxo a ser usado para
conexões TCP.

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): o listener de pacotes
a ser usado para pacotes UDP.

Exemplo de envio de TCP e UDP para diferentes endpoints:

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

## Endpoints {#endpoints}

Os endpoints estabelecem conexões com um endpoint fixo. São preferíveis aos discadores,
porque permitem otimizações específicas. Existem endpoints
de fluxo e de pacote.

### EndpointConfig {#endpointconfig}

**Formato:** *string* | [Interface](#interface)

O endpoint *string* é o endereço host:porta do endpoint selecionado. A
conexão é estabelecida usando o discador padrão.

Tipos de interface aceitos para endpoints de fluxo e pacote:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig {#dialendpointconfig}

Estabelece conexões discando um endereço fixo. Pode usar um discador, o que
permite a composição de estratégias.

**Formato:** *struct*

**Campos:**

- `address` (*string*): endereço do endpoint a discar

- `dialer` ([DialerConfig](#dialerconfig)): discador a ser usado para discar o
endereço

### WebsocketEndpointConfig {#websocketendpointconfig}

Conexões de fluxo e pacotes de túneis para um endpoint sobre Websockets.

Para conexões de fluxo, cada gravação é transformada em uma mensagem do Websocket. Para
conexões de pacotes, cada pacote é transformado em uma mensagem do Websocket.

**Formato:** *struct*

**Campos:**

- `url` (*string*): URL do endpoint do Websocket. O esquema precisa ser
`https` ou `wss` para Websocket sobre TLS e `http` ou `ws` para Websocket
em texto simples.

- `endpoint` ([EndpointConfig](#endpointconfig)): endpoint (do servidor da Web) para conexão. Se não houver um, ele se conectará ao endereço especificado no URL.

## Discadores {#dialers}

Os discadores estabelecem conexões de acordo com o endereço de um endpoint. Existem discadores de fluxo e
de pacotes.

### DialerConfig {#dialerconfig}

**Formato:** *null* | [Interface](#interface)

Um discador *null* (ausente) significa o discador padrão, que usa conexões diretas TCP
para fluxo e conexões diretas UDP para pacotes.

Tipos de interface aceitos para discadores de fluxo e de pacotes:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## Listeners de pacotes {#packet_listeners}

Um listener de pacotes estabelece uma conexão de pacotes ilimitada que pode ser usada para
enviar pacotes a vários destinos.

### PacketListenerConfig {#packetlistenerconfig}

**Formato:** *null* | [Interface](#interface)

Um listener de pacotes *null* (ausente) significa o listener de pacotes padrão, que é
um listener de pacotes UDP.

Tipos de interface aceitos:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Estratégias {#strategies}

### Shadowsocks {#shadowsocks}

#### LegacyShadowsocksConfig {#legacyshadowsocksconfig}

O LegacyShadowsocksConfig representa um túnel que usa o Shadowsocks como
transporte. Ele implementa o formato legado para compatibilidade com versões anteriores.

**Formato:** *struct*

**Campos:**

- `server` (*string*): o host para se conectar

- `server_port` (*number*): o número da porta para se conectar

- `method` (*string*): a [criptografia
AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) a ser usada (link em inglês)

- `password` (*string*): usada para gerar a chave de criptografia

- `prefix` (*string*): o [disfarce de
prefixo](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) a ser usado.
Compatível com conexões de pacotes e fluxo.

Exemplo:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI {#legacyshadowsocksuri}

O LegacyShadowsocksURI representa um túnel que usa o Shadowsocks como transporte.
Ele implementa o formato legado de URL para compatibilidade com versões anteriores.

**Formato:** *string*

Consulte [Formato de URI
legado do Shadowsocks](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) e [Esquema
de URI SIP002](https://shadowsocks.org/doc/sip002.html) (links em inglês). Não oferecemos suporte a plug-ins.

Exemplo:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig {#shadowsocksconfig}

O ShadowsocksConfig pode representar discadores de fluxo ou de pacotes, bem como um listener de pacotes que usa o Shadowsocks.

**Formato:** *struct*

**Campos:**

- `endpoint` ([EndpointConfig](#endpointconfig)): o endpoint do Shadowsocks para
se conectar

- `cipher` (*string*): a [criptografia
AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) a ser usada (link em inglês)

- `secret` (*string*): usada para gerar a chave de criptografia

- `prefix` (*string*, opcional): o [disfarce de
prefixo](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) a ser usado.
Compatível com conexões de pacotes e fluxo.

Exemplo:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Metadefinições {#meta_definitions}

### FirstSupportedConfig {#firstsupportedconfig}

Usa a primeira configuração aceita no aplicativo. Esta é uma maneira
de incorporar novas configurações e, ao mesmo tempo, manter compatibilidade com outras antigas.

**Formato:** *struct*

**Campos:**

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)): lista de opções
a considerar

Exemplo:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface {#interface}

As interfaces permitem escolher uma entre diversas implementações. Elas usam o campo
`$type` para especificar o tipo que a configuração representa.

Exemplo:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
