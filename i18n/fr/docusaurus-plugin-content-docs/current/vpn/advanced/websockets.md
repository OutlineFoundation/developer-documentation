---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Client Outline v1.15.0 et versions ultérieures*

Ce tutoriel détaillé vous aidera à implémenter Shadowsocks-over-WebSockets, une technique puissante utilisée pour contourner la censure dans les environnements où les connexions Shadowsocks standards sont bloquées. En encapsulant le trafic Shadowsocks dans des WebSockets, vous pouvez le déguiser en trafic Web standard pour plus de résilience et d'accessibilité.

## Étape 1 : Configurez et exécutez un serveur Outline

Créez un fichier `config.yaml` avec la configuration suivante :

Téléchargez le dernier
[`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases)
et exécutez-le avec la configuration créée :

## Étape 2 : Révélez le serveur Web

Pour rendre votre serveur Web WebSocket accessible au public, vous devez le révéler sur Internet et configurer le protocole
[TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
Il existe plusieurs façons de procéder. Vous pouvez utiliser un serveur Web local comme
[Caddy](https://caddyserver.com/), [nginx](https://nginx.org/) ou
[Apache](https://httpd.apache.org/) (en vous assurant qu'il comporte un certificat TLS valide), ou
faire appel à un service de tunnelisation comme [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
ou [ngrok](https://ngrok.com/).

### Exemple avec TryCloudflare

Dans cet exemple, nous allons utiliser
[TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/)
pour créer un tunnel rapide. C'est un moyen pratique et sécurisé de révéler votre serveur Web local sans ouvrir de ports d'entrée.

1. 

Téléchargez et installez [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. 

Créez un tunnel pointant vers le port de votre serveur Web local :

Cloudflare fournira un sous-domaine (exemple :
`acids-iceland-davidson-lb.trycloudflare.com`) pour accéder à votre point de terminaison WebSocket et gérer automatiquement le protocole TLS. Notez le nom de ce sous-domaine, car vous en aurez besoin ultérieurement.

## Étape 3 : Créez une clé d'accès dynamique

Générez un fichier YAML de clé d'accès client pour vos utilisateurs à l'aide du format de [configuration de la clé d'accès](../management/config) et indiquez les points de terminaison WebSocket configurés précédemment côté serveur :

Après avoir généré le fichier YAML de clé d'accès dynamique, vous devez le fournir à vos utilisateurs. Vous pouvez héberger le fichier sur un service d'hébergement Web statique ou bien le générer de façon dynamique. En savoir plus sur les [clés d'accès dynamiques](../management/dynamic-access-keys)

## Étape 4 : Connectez-vous au client Outline

Utilisez l'une des applications [client Outline](../../download-links)
officielles (version 1.15.0 ou versions ultérieures) et ajoutez la clé d'accès dynamique que vous venez de créer comme entrée de serveur. Cliquez sur **Connecter** pour activer la tunnelisation vers votre serveur à l'aide de la configuration Shadowsocks-over-Websocket.

Utilisez un outil comme [IPInfo](https://ipinfo.io) pour vérifier que vous naviguez désormais sur Internet depuis votre serveur Outline.
