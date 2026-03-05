---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline utilise une configuration YAML pour définir les paramètres VPN et gérer le trafic TCP/UDP. Cette configuration permet une composabilité multiniveau, pour des configurations flexibles et extensibles.

L'élément [TunnelConfig](../reference/access-key-config#tunnelconfig) est indiqué dans la configuration de premier niveau.

## Exemples

Voici à quoi ressemble généralement une configuration Shadowsocks :

Les protocoles TCP et UDP peuvent désormais être exécutés sur différents ports ou points de terminaison, et avec différents préfixes.

Vous pouvez utiliser des ancres YAML et la clé de fusion `<<` pour éviter la duplication :

Il est maintenant possible de composer des stratégies et de faire des multisauts.

En cas de protocoles bloquants ou difficiles à identifier comme Shadowsocks, vous pouvez utiliser Shadowsocks-over-Websockets. Découvrez un [exemple de configuration de serveur](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)
et comment le déployer. Voici à quoi ressemble une configuration client :

Le point de terminaison Websocket peut à son tour prendre un point de terminaison, lequel peut être utilisé pour contourner un blocage DNS :

Pour permettre une compatibilité avec différentes versions de client Outline, utilisez l'option `first-supported` dans votre configuration. C'est particulièrement important lorsque de nouvelles stratégies et fonctionnalités sont ajoutées à Outline, car tous les utilisateurs n'ont peut-être pas la dernière version du logiciel client. En utilisant `first-supported`, vous pouvez fournir une configuration unique qui fonctionne sur différentes plates-formes et versions de client, afin d'assurer une bonne rétrocompatibilité et une expérience utilisateur cohérente.
