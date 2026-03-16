---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

Ce guide explique comment utiliser [Caddy](https://caddyserver.com/), un serveur Web performant et convivial, pour améliorer la configuration de votre serveur Outline. Avec ses fonctionnalités [HTTPS automatiques](https://caddyserver.com/docs/automatic-https) et sa configuration flexible, Caddy est un excellent choix pour faire fonctionner votre serveur Outline, en particulier si vous utilisez un transport WebSocket.

## Qu'est-ce que Caddy ? {#what_is_caddy}

Caddy est un serveur Web Open Source connu pour sa facilité d'utilisation, ses fonctionnalités HTTPS automatiques et sa compatibilité avec de nombreux protocoles. Il permet de simplifier la configuration des serveurs Web et offre notamment les fonctionnalités suivantes :

- **HTTPS automatique** : Caddy obtient et renouvelle automatiquement les certificats TLS pour sécuriser les connexions.

- **Compatibilité HTTP/3** : Caddy prend en charge le dernier protocole HTTP/3, pour un trafic Web plus rapide et efficace.

- **Extensibilité** : Caddy peut être amélioré avec des plug-ins offrant différentes fonctionnalités comme le proxy inverse et l'équilibrage de charge.

## Étape 1 : Prérequis {#step_1_prerequisites}

- Téléchargez et installez [`xcaddy`](https://github.com/caddyserver/xcaddy).

## Étape 2 : Configurez votre domaine {#step_2_configure_your_domain}

Avant de lancer Caddy, vérifiez que votre nom de domaine est correctement configuré pour pointer vers l'adresse IP de votre serveur.

- **Configurez les enregistrements A/AAAA** : connectez-vous à votre fournisseur DNS et configurez les enregistrements A et AAAA afin que votre domaine pointe respectivement vers les adresses IPv4 et IPv6 de votre serveur.

- **Vérifiez les enregistrements DNS** : vérifiez que vos enregistrements DNS sont configurés correctement avec une recherche faisant autorité :

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## Étape 3 : Compilez et exécutez un build Caddy personnalisé {#build-and-run}

Avec `xcaddy`, vous pouvez compiler un serveur `caddy` binaire personnalisé qui inclut le module de serveur principal Outline et d'autres modules d'extension de serveur indispensables.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/Jigsaw-Code/outline-ss-server/outlinecaddy
```

## Étape 4 : Configurez et exécutez le serveur Caddy avec Outline {#step_4_configure_and_run_the_caddy_server_with_outline}

Créez un fichier `config.yaml` avec la configuration suivante :

```yaml
apps:
  http:
    servers:
      server1:
        listen:
          - ":443"
        routes:
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<TCP_PATH>
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<UDP_PATH>
            handle:
              - handler: websocket2layer4
                type: packet
                connection_handler: ss1
  outline:
    shadowsocks:
      replay_history: 10000
    connection_handlers:
      - name: ss1
        handle:
          handler: shadowsocks
          keys:
            - id: user-1
              cipher: chacha20-ietf-poly1305
              secret: <SHADOWSOCKS_SECRET>
```

Cette configuration représente une stratégie Shadowsocks-over-WebSockets avec un serveur Web écoutant le port `443`, qui accepte le trafic Shadowsocks TCP et UDP encapsulé respectivement aux chemins `TCP_PATH` et `UDP_PATH`.

Exécutez le serveur Caddy amélioré avec Outline à l'aide de la configuration créée :

```sh
caddy run --config config.yaml --adapter yaml --watch
```

Vous trouverez d'autres exemples de configuration dans notre [dépôt GitHub outline-ss-server/outlinecaddy](https://github.com/Jigsaw-Code/outline-ss-server/tree/master/outlinecaddy/examples).

## Étape 5 : Créez une clé d'accès dynamique {#step_5_create_a_dynamic_access_key}

Générez un fichier YAML de clé d'accès client pour vos utilisateurs à l'aide du format de [configuration avancée](../management/config) et indiquez les points de terminaison WebSocket configurés précédemment côté serveur :

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

Après avoir généré le fichier YAML de clé d'accès dynamique, vous devez le fournir à vos utilisateurs. Vous pouvez héberger le fichier sur un service d'hébergement Web statique ou le générer de façon dynamique. En savoir plus sur les [clés d'accès dynamiques](../management/dynamic-access-keys)

## Étape 6 : Connectez-vous au client Outline {#step_6_connect_with_the_outline_client}

Utilisez l'une des applications officielles du [client Outline](../../download-links)
(version 1.15.0 ou versions ultérieures) et ajoutez la clé d'accès dynamique que vous venez de créer comme entrée de serveur. Cliquez sur **Connecter** pour activer la tunnelisation vers votre serveur à l'aide de la configuration Shadowsocks-over-Websocket.

Utilisez un outil comme [IPInfo](https://ipinfo.io) pour vérifier que vous naviguez désormais sur Internet via votre serveur Outline.
