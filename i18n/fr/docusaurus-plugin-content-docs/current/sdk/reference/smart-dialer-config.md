---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

**Smart Dialer** recherche une stratégie qui débloque les protocoles DNS et TLS pour une liste spécifique de domaines de test. Il part d'une configuration décrivant plusieurs stratégies pour faire son choix.

## Configuration YAML pour Smart Dialer

La configuration que Smart Dialer utilise est au format YAML. Voici un exemple :

### Configuration DNS

- Le champ `dns` spécifie une liste de résolveurs DNS à tester.

- Chaque résolveur DNS peut être de l'un des types suivants :

    - `system` : utilisation du résolveur du système. Il est spécifié avec un objet vide.

    - `https` : utilisation d'un résolveur DNS-over-HTTPS (DoH) chiffré.

    - `tls` : utilisation d'un résolveur DNS-over-TLS (DoT) chiffré.

    - `udp` : utilisation d'un résolveur UDP.

    - `tcp` : utilisation d'un résolveur TCP.

#### Résolveur DNS-over-HTTPS (DoH)

- `name` : nom de domaine du serveur DoH.

- `address` : adresse hôte:port du serveur DoH. La valeur par défaut est `name`:443.

#### Résolveur DNS-over-TLS (DoT)

- `name` : nom de domaine du serveur DoT.

- `address` : adresse hôte:port du serveur DoT. La valeur par défaut est `name`:853.

#### Résolveur UDP

- `address` : adresse hôte:port du résolveur UDP.

#### Résolveur TCP

- `address` : adresse hôte:port du résolveur TCP.

### Configuration TLS

- Le champ `tls` spécifie une liste de transports TLS à tester.

- Chaque transport TLS est une chaîne qui spécifie le transport à utiliser.

- Par exemple, `override:host=cloudflare.net|tlsfrag:1` spécifie un transport qui utilise le domain fronting avec Cloudflare et la fragmentation TLS. Consultez la [documentation sur la configuration](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format) pour en savoir plus.

### Configuration de remplacement

Une configuration de remplacement est utilisée si aucune des stratégies sans proxy ne parvient à établir une connexion. Par exemple, elle peut spécifier un serveur proxy de secours pour tenter de connecter l'utilisateur. Le lancement de la stratégie de remplacement prend plus de temps, puisque les autres stratégies DNS ou TLS doivent avoir échoué ou expiré d'abord.

Les chaînes de la configuration de remplacement doivent respecter ces caractéristiques :

- Être des chaînes de configuration `StreamDialer` valides, telles que définies dans [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols)

- Être des objets de configuration Psiphon valides, en tant qu'éléments enfants d'un champ `psiphon`

#### Exemple de serveur Shadowsocks

#### Exemple de serveur SOCKS5

#### Exemple de configuration Psiphon

Pour utiliser le réseau [Psiphon](https://psiphon.ca/) :

1. Contactez l'équipe Psiphon pour obtenir une configuration qui vous donne accès à son réseau. Un contrat peut être nécessaire.

2. Ajoutez la configuration Psiphon reçue à la section `fallback` de votre configuration Smart Dialer. Puisque JSON est compatible avec YAML, vous pouvez copier et coller votre configuration Psiphon directement dans la section `fallback`, comme suit :

### Comment utiliser Smart Dialer

Pour utiliser Smart Dialer, créez un objet `StrategyFinder` et appelez la méthode `NewDialer`, en donnant la liste de domaines de test et la configuration YAML.
La méthode `NewDialer` renvoie un `transport.StreamDialer`, qui peut être utilisé pour établir des connexions à l'aide de la stratégie trouvée. Par exemple :

Il s'agit d'un exemple basique. Vous devrez peut-être l'adapter à votre cas d'utilisation.
