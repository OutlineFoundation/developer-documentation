---
title: "Clés d'accès dynamiques"
sidebar_label: "Clés d'accès dynamiques"
---

Outline propose deux types de clés d'accès : des clés statiques et des clés dynamiques. Les clés statiques encodent directement toutes les informations de connexion, tandis que les clés dynamiques encodent l'emplacement des informations de connexion, ce qui permet de stocker ces informations à distance et de les modifier si nécessaire. Vous pouvez ainsi modifier la configuration de votre serveur sans devoir générer de nouvelles clés ni les distribuer à vos utilisateurs. Ce document explique comment utiliser des clés d'accès dynamiques pour gérer votre serveur Outline de façon plus flexible et efficace.

Pour indiquer quelles informations d'accès vos clés d'accès dynamiques doivent utiliser, vous disposez de trois possibilités :

### Utiliser un lien `ss://` {#use_an_ss_link}

*Client Outline v1.8.1 et versions ultérieures*

Vous pouvez utiliser directement un lien `ss://` existant. Cette méthode est idéale si vous n'avez pas besoin de changer souvent de serveur, de port ou de méthode de chiffrement, mais que vous souhaitez tout de même pouvoir modifier l'adresse du serveur.

**Exemple :**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### Utiliser un objet JSON {#use_a_json_object}

*Client Outline v1.8.0 et versions ultérieures*

Cette méthode vous permet de gérer tous les aspects de la connexion Outline de vos utilisateurs avec plus de flexibilité. Vous pouvez modifier le serveur, le port, le mot de passe et la méthode de chiffrement.

**Exemple :**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server** : domaine ou adresse IP de votre serveur VPN

- **server_port** : numéro de port sur lequel le serveur VPN est exécuté

- **password** : mot de passe requis pour se connecter au VPN

- **method** : méthode de chiffrement utilisée par le VPN (consultez les [algorithmes de chiffrement AEAD](https://shadowsocks.org/doc/aead.html) acceptés par Shadowsocks)

### Utiliser un objet YAML {#use_a_yaml_object}

*Client Outline v1.15.0 et versions ultérieures*

Cette méthode est semblable à la méthode JSON décrite ci-dessus, mais elle offre encore plus de flexibilité, car elle utilise le format de configuration avancée d'Outline. Vous pouvez modifier le serveur, le port, le mot de passe, la méthode de chiffrement et plus encore.

**Exemple :**

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
  udp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
```

- **transport** : définit les protocoles de transport à utiliser (TCP et UDP dans ce cas)

- **tcp/udp** : précise la configuration pour chaque protocole

    - **$type** : indique le type de configuration (shadowsocks, dans notre cas)

    - **endpoint** : domaine ou adresse IP et port de votre serveur VPN

    - **secret** : mot de passe requis pour se connecter au VPN

    - **cipher** : méthode de chiffrement utilisée par le VPN (consultez les [algorithmes de chiffrement AEAD](https://shadowsocks.org/doc/aead.html) acceptés par Shadowsocks)

Consultez [Configuration de la clé d'accès](config) pour découvrir plus en détail les différentes méthodes permettant de configurer l'accès à votre serveur Outline (transports, points de terminaison, composeurs, écouteurs de paquets, etc.).

## Extraire les informations d'accès d'une clé statique {#extract_access_information_from_a_static_key}

Si vous avez déjà une clé d'accès statique, vous pouvez en extraire les informations pour créer une clé d'accès dynamique au format JSON ou YAML. Les clés d'accès statiques sont configurées comme ceci :

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

Exemple :

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **Serveur** : `outline-server.example.com`

- **Port du serveur** : `8388`

- **Informations utilisateur** : `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` décodé en [base64](https://en.wikipedia.org/wiki/Base64) à l'aide d'un outil comme [Google Admin Toolbox Encode/Decode](https://toolbox.googleapps.com/apps/encode_decode/)

    - **Méthode** : `chacha20-ietf-poly1305`

    - **Mot de passe** : `example`

## Choisir une plate-forme d'hébergement {#choose_a_hosting_platform}

Maintenant que vous savez comment créer des clés d'accès dynamiques, vous devez choisir une plate-forme d'hébergement adaptée à la configuration de votre clé d'accès. Pour sélectionner la bonne plate-forme, il faut prendre en compte sa fiabilité, le degré de sécurité qu'elle fournit, sa facilité d'utilisation et sa résistance à la censure. Livrera-t-elle systématiquement vos informations de clé d'accès sans temps d'arrêt ? A-t-elle mis en place les mesures de sécurité adéquates pour protéger votre configuration ? Permet-elle de gérer vos informations de clé d'accès facilement ? Est-elle accessible dans les régions appliquant des politiques de censure sur Internet ?

Pour les situations où l'accès aux informations peut être restreint, vous pouvez héberger votre serveur sur des plates-formes résistant à la censure comme [Google Drive](https://drive.google.com), [pad.riseup.net](https://pad.riseup.net/), [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) (avec un accès de type chemin d'accès), [Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96) ou les [gists secrets GitHub](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
Évaluez les besoins spécifiques de votre déploiement et choisissez une plate-forme adaptée à vos impératifs en termes d'accessibilité et de sécurité.
