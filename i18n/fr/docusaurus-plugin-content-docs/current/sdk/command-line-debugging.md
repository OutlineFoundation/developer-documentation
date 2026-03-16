---
title: "Command Line Debugging"
sidebar_label: "Command Line Debugging"
---

Ce guide explique comment utiliser les outils de ligne de commande du SDK Outline pour comprendre et contourner les interférences réseau à distance. Vous apprendrez à utiliser les outils du SDK pour mesurer les interférences réseau, tester les stratégies de contournement et analyser les résultats. Ce guide se concentre sur les outils `resolve`, `fetch` et `http2transport`.

## Premiers pas avec les outils du SDK Outline

Vous pouvez commencer à utiliser les outils du SDK Outline directement à partir de la ligne de commande.

### Résoudre le DNS

L'outil `resolve` vous permet d'effectuer des recherches DNS avec un résolveur spécifique.

Pour résoudre l'enregistrement A d'un domaine :

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

Pour résoudre un enregistrement CNAME :

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### Récupérer une page Web

L'outil `fetch` peut être utilisé pour récupérer le contenu d'une page Web.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest https://example.com
```

Il peut également forcer la connexion à utiliser QUIC.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### Utiliser un proxy local

L'outil `http2transport` crée un proxy local pour acheminer votre trafic.
Pour démarrer un proxy local avec un transport Shadowsocks :

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

Vous pouvez ensuite utiliser ce proxy avec d'autres outils tels que curl :

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## Spécifier des stratégies de contournement

Le SDK Outline permet de spécifier différentes stratégies de contournement qui peuvent être combinées pour contourner différentes formes d'interférences réseau. La spécification de ces stratégies se trouve dans la [documentation Go](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x@v0.0.3/configurl).

### Stratégies composables

Ces stratégies peuvent être combinées pour créer des techniques de contournement plus robustes.

* **DNS-over-HTTPS avec fragmentation TLS** : `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5-over-TLS avec domain fronting** : `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Routage multisaut avec Shadowsocks** : `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## Accès et mesure à distance

Pour mesurer les interférences réseau telles qu'elles sont ressenties dans différentes régions, vous pouvez utiliser des proxys à distance. Vous pouvez rechercher ou créer des proxys distants auxquels vous connecter.

### Options d'accès à distance

L'outil `fetch` vous permet de tester les connexions à distance de différentes manières.

#### Serveur Outline

Connectez-vous à distance à un serveur Outline standard avec un transport Shadowsocks.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 sur SSH

Créez un proxy SOCKS5 à l'aide d'un tunnel SSH.

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

Se connecter à ce tunnel à l'aide de fetch

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## Étude de cas : contourner le blocage de YouTube en Iran

Voici un exemple pratique de détection et de contournement des interférences réseau.

### Détecter le bloc

Lorsque vous essayez de récupérer la page d'accueil YouTube via un proxy iranien, la requête expire, ce qui indique un blocage.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

Cette commande échoue en raison d'un délai d'attente dépassé.

### Contournement avec la fragmentation TLS

En ajoutant la fragmentation TLS au transport, nous pouvons contourner ce blocage.

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Cette commande récupère le titre de la page d'accueil YouTube, qui est `<title>YouTube</title>`.

### Contournement avec la fragmentation TLS et DNS-over-HTTPS

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Cette opération renvoie également `<title>YouTube</title>`.

### Contourner la censure avec un serveur Outline

```sh
go run github.com/Jigsaw-Code/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

Cette opération renvoie également `<title>YouTube</title>`.

## Ressources et analyses supplémentaires

Pour les discussions et les questions, consultez le [groupe de discussion du SDK Outline](https://github.com/Jigsaw-Code/outline-sdk/discussions).
