---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

Les clés d'accès sont compatibles avec l'option "prefix" à partir de la version 1.9.0 du client Outline. L'option "prefix" correspond aux premiers octets utilisés pour le [salage](https://shadowsocks.org/guide/aead.html) d'une connexion TCP Shadowsocks.
La connexion peut ainsi ressembler à un protocole autorisé sur le réseau et ainsi contourner les pare-feu rejetant les protocoles non reconnus.

## Quand dois-je utiliser un préfixe ?

Si vous pensez que l'accès des utilisateurs de votre serveur Outline est toujours bloqué, vous pouvez essayer d'utiliser différents préfixes.

## Instructions

Les préfixes ne doivent pas dépasser 16 octets. Des préfixes plus longs peuvent générer des collisions de salage, ce qui peut compromettre la sécurité du chiffrement et entraîner la détection des connexions. Utilisez le préfixe le plus court possible pour contourner le blocage rencontré.

Le port que vous utilisez doit correspondre au protocole que votre préfixe prétend être.
L'IANA tient un [registre des numéros de port pour les protocoles de transport](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) qui liste les protocoles et les numéros de port associés.

Voici des exemples de préfixes efficaces ressemblant à des protocoles courants :

Port recommandé
Encodé au format JSON
Encodé au format URL

Requête HTTP
80 (http)
`"POST "`
`POST%20`

Réponse HTTP
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

Requête DNS sur TCP
53 (DNS)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

ClientHello TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

Données d'application TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

ServerHello TLS
443 (https), 463 (smtps), 563 (nntps), 636 (ldaps), 989 (ftps-data), 990 (ftps), 993 (imaps), 995 (pop3s), 5223 (Apple APN), 5228 (Play Store), 5349 (turns)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh), 830 (netconf-ssh), 4334 (netconf-ch-ssh), 5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### Clés d'accès dynamiques

Pour utiliser des préfixes avec les [clés d'accès dynamiques](../management/dynamic-access-keys) (`ssconf://`),
ajoutez une clé "prefix" à l'objet JSON et définissez la valeur **encodée au format JSON** de votre choix (voir les exemples dans le tableau ci-dessus). Vous pouvez utiliser des codes d'échappement (\u00FF, par exemple) pour représenter les points de code Unicode non imprimables dans la plage `U+0` à `U+FF`. Par exemple :

### Clés d'accès statiques

Pour utiliser des préfixes avec les **clés d'accès statiques** (ss://), vous devrez modifier votre clé existante avant de la distribuer. Si vous possédez une clé d'accès statique générée par Outline Manager, ajoutez une version **encodée au format URL** de votre préfixe (voir les exemples dans le tableau ci-dessus) à la fin de votre clé d'accès comme suit :

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

Si vous êtes expérimenté, vous pouvez utiliser la fonction `encodeURIComponent()` de votre navigateur pour convertir votre préfixe **encodé au format JSON** en préfixe **encodé au format URL**. Pour ce faire, ouvrez la console de l'outil d'inspection Web (sur Chrome : Outils de développement > Console Web JavaScript), et saisissez ce qui suit :

Appuyez sur "Entrée". La valeur générée correspond à la version encodée au format URL. Par exemple :
