---
title: "Configuration"
sidebar_label: "Configuration"
---

## Tunnels {#tunnels}

### TunnelConfig {#tunnelconfig}

Tunnel est l'objet de premier niveau dans une configuration Outline. Il indique comment le VPN doit être configuré.

**Format** : [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig {#explicittunnelconfig}

**Format** : *struct*

**Champs** :

- `transport` ([TransportConfig](#transportconfig)) : transport à utiliser pour échanger des paquets avec la destination cible

- `error` (*struct*) : informations à communiquer à l'utilisateur en cas d'erreur du service (par exemple : clé expirée, quota épuisé)

    - `message` (*string*) : message convivial à afficher pour l'utilisateur

    - `details` (*string*) : message à afficher lorsque l'utilisateur ouvre les détails de l'erreur afin de faciliter le dépannage

Les champs `error` et `transport` s'excluent mutuellement.

Exemple de réussite :

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

Exemple d'erreur :

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## Transports {#transports}

### TransportConfig {#transportconfig}

TransportConfig indique comment les paquets doivent être échangés avec la destination cible

**Format** : [Interface](#interface)

Types d'Interface compatibles :

- `tcpudp` : [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig {#tcpudpconfig}

TCPUDPConfig permet de configurer des stratégies TCP et UDP distinctes.

**Format** : *struct*

**Champs** :

- `tcp` ([DialerConfig](#dialerconfig)) : Stream Dialer à utiliser pour les connexions TCP

- `udp` ([PacketListenerConfig](#packetlistenerconfig)) : Packet Listener à utiliser pour les paquets UDP

Exemple avec un envoi TCP et UDP vers différents points de terminaison :

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

Les Endpoints établissent des connexions vers un point de terminaison fixe. Ils sont préférables aux dialers, car ils permettent des optimisations spécifiques aux points de terminaison. Il existe des Endpoints Stream et des Endpoints Packet.

### EndpointConfig {#endpointconfig}

**Format** : *string* | [Interface](#interface)

Le Endpoint *string* est l'adresse hôte:port du point de terminaison sélectionné. La connexion est établie à l'aide du dialer par défaut.

Types d'interface acceptés pour les Endpoints Stream et Packet :

- `dial` : [DialEndpointConfig](#dialendpointconfig)

- `first-supported` : [FirstSupportedConfig](#firstsupportedconfig)

- `websocket` : [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks` : [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig {#dialendpointconfig}

DialEndpointConfig permet d'établir des connexions en composant une adresse fixe. Un dialer peut être ajouté pour associer plusieurs stratégies.

**Format** : *struct*

**Champs** :

- `address` (*string*) : adresse du point de terminaison à composer

- `dialer` ([DialerConfig](#dialerconfig)) : dialer à utiliser pour composer l'adresse

### WebsocketEndpointConfig {#websocketendpointconfig}

WebsocketEndpointConfig tunnelise les connexions de flux et de paquets vers un point de terminaison sur Websockets.

Pour les connexions de flux, chaque message est transformé en message Websocket. Pour les connexions de paquets, chaque paquet est transformé en message Websocket.

**Format** : *struct*

**Champs** :

- `url` (*string*) : URL du point de terminaison Websocket. Le schéma doit être
`https` ou `wss` pour Websocket sur TLS, et `http` ou `ws` pour Websocket en texte brut.

- `endpoint` ([EndpointConfig](#endpointconfig)) : point de terminaison du serveur Web auquel se connecter. S'il n'est pas indiqué, la connexion s'effectue à l'adresse indiquée dans l'URL.

## Dialers {#dialers}

Les dialers établissent des connexions à une adresse de point de terminaison. Il existe des Dialers Stream et Dialers Packet.

### DialerConfig {#dialerconfig}

**Format** : *null* | [Interface](#interface)

Le Dialer *null* (absent) est le dialer par défaut, qui utilise des connexions TCP directes pour Stream et des connexions UDP directes pour Packets.

Types d'interface acceptés pour les Dialers Stream et Packet :

- `first-supported` : [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks` : [ShadowsocksConfig](#shadowsocksconfig)

## Packet Listeners {#packet_listeners}

Un Packet Listener établit une connexion de paquet illimitée qui peut être utilisée pour envoyer des paquets vers de multiples destinations.

### PacketListenerConfig {#packetlistenerconfig}

**Format** : *null* | [Interface](#interface)

Le Packet Listener *null* (absent) est le Packet Listener par défaut, c'est-à-dire le Packet Listener UDP.

Types d'interface compatibles :

- `first-supported` : [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks` : [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## Strategies {#strategies}

### Shadowsocks {#shadowsocks}

#### LegacyShadowsocksConfig {#legacyshadowsocksconfig}

LegacyShadowsocksConfig représente un Tunnel qui utilise Shadowsocks comme transport. Il implémente l'ancien format pour assurer la rétrocompatibilité.

**Format** : *struct*

**Champs** :

- `server` (*string*) : hôte auquel se connecter

- `server_port` (*number*) : numéro de port auquel se connecter

- `method` (*string*) : [algorithme de chiffrement AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) à utiliser

- `password` (*string*) : utilisé pour générer la clé de chiffrement

- `prefix` (*string*) : méthode de [dissimulation des préfixes](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) à utiliser
(compatible avec les connexions de flux et de paquets)

Exemple :

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI {#legacyshadowsocksuri}

LegacyShadowsocksURI représente un Tunnel qui utilise Shadowsocks comme transport.
Il implémente l'ancien format d'URL pour assurer la rétrocompatibilité.

**Format** : *string*

Voir l'[ancien format d'URI Shadowsocks](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) et le [schéma d'URI SIP002](https://shadowsocks.org/doc/sip002.html). Les plug-ins ne sont pas compatibles.

Exemple :

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig {#shadowsocksconfig}

ShadowsocksConfig peut représenter des Stream Dialers ou des Packet Dialers, ainsi qu'un Packet Listener qui utilise Shadowsocks.

**Format** : *struct*

**Champs** :

- `endpoint` ([EndpointConfig](#endpointconfig)) : point de terminaison Shadowsocks auquel se connecter

- `cipher` (*string*) : [algorithme de chiffrement AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) à utiliser

- `secret` (*string*) : utilisé pour générer la clé de chiffrement

- `prefix` (*string*, facultatif) : méthode de [dissimulation des préfixes](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) à utiliser
(compatible avec les connexions de flux et de paquets)

Exemple :

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## Meta Definitions {#meta_definitions}

### FirstSupportedConfig {#firstsupportedconfig}

FirstSupportedConfig utilise la première configuration acceptée par l'application. Cela permet d'incorporer de nouvelles configurations tout en maintenant la rétrocompatibilité avec les anciennes.

**Format** : *struct*

**Champs** :

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)) : liste d'options à prendre en compte

Exemple :

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface {#interface}

Les Interfaces permettent de choisir une implémentation parmi plusieurs. Le champ `$type` est utilisé pour indiquer le type de configuration représentée.

Exemple :

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
