---
title: "Configurer Smart Dialer"
sidebar_label: "Configurer Smart Dialer"
---

**Smart Dialer** recherche une stratégie qui débloque les protocoles DNS et TLS pour une liste spécifique de domaines de test. Il part d'une configuration décrivant plusieurs stratégies pour faire son choix.

## Configuration YAML pour Smart Dialer {#yaml_config_for_the_smart_dialer}

La configuration que Smart Dialer utilise est au format YAML. Voici un exemple :

```yaml
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1

fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

### Configuration DNS {#dns_configuration}

- Le champ `dns` spécifie une liste de résolveurs DNS à tester.

- Chaque résolveur DNS peut être de l'un des types suivants :

    - `system` : utilisation du résolveur du système. Il est spécifié avec un objet vide.

    - `https` : utilisation d'un résolveur DNS-over-HTTPS (DoH) chiffré.

    - `tls` : utilisation d'un résolveur DNS-over-TLS (DoT) chiffré.

    - `udp` : utilisation d'un résolveur UDP.

    - `tcp` : utilisation d'un résolveur TCP.

#### Résolveur DNS-over-HTTPS (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name` : nom de domaine du serveur DoH.

- `address` : adresse hôte:port du serveur DoH. La valeur par défaut est `name`:443.

#### Résolveur DNS-over-TLS (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name` : nom de domaine du serveur DoT.

- `address` : adresse hôte:port du serveur DoT. La valeur par défaut est `name`:853.

#### Résolveur UDP {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address` : adresse hôte:port du résolveur UDP.

#### Résolveur TCP {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address` : adresse hôte:port du résolveur TCP.

### Configuration TLS {#tls_configuration}

- Le champ `tls` spécifie une liste de transports TLS à tester.

- Chaque transport TLS est une chaîne qui spécifie le transport à utiliser.

- Par exemple, `override:host=cloudflare.net|tlsfrag:1` spécifie un transport qui utilise le domain fronting avec Cloudflare et la fragmentation TLS. Consultez la [documentation sur la configuration](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Config_Format) pour en savoir plus.

### Configuration de remplacement {#fallback_configuration}

Une configuration de remplacement est utilisée si aucune des stratégies sans proxy ne parvient à établir une connexion. Par exemple, elle peut spécifier un serveur proxy de secours pour tenter de connecter l'utilisateur. Le lancement de la stratégie de remplacement prend plus de temps, puisque les autres stratégies DNS ou TLS doivent avoir échoué ou expiré d'abord.

Les chaînes de la configuration de remplacement doivent respecter ces caractéristiques :

- Être des chaînes de configuration `StreamDialer` valides, telles que définies dans [`configurl`](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl#hdr-Proxy_Protocols)

- Être des objets de configuration Psiphon valides, en tant qu'éléments enfants d'un champ `psiphon`

#### Exemple de serveur Shadowsocks {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### Exemple de serveur SOCKS5 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Exemple de configuration Psiphon {#psiphon_config_example}

Pour utiliser le réseau [Psiphon](https://psiphon.ca/) :

1. Contactez l'équipe Psiphon pour obtenir une configuration qui vous donne accès à son réseau. Un contrat peut être nécessaire.

2. Ajoutez la configuration Psiphon reçue à la section `fallback` de votre configuration Smart Dialer. Puisque JSON est compatible avec YAML, vous pouvez copier et coller votre configuration Psiphon directement dans la section `fallback`, comme suit :

```yaml
fallback:
  - psiphon: {
      "PropagationChannelId": "FFFFFFFFFFFFFFFF",
      "SponsorId": "FFFFFFFFFFFFFFFF",
      "DisableLocalSocksProxy" : true,
      "DisableLocalHTTPProxy" : true,
      ...
    }
```


:::note
: Le codebase Psiphon est sous licence GPL, ce qui peut imposer des restrictions de licence à votre propre code. Vous pouvez envisager d'obtenir une licence spéciale auprès de Psiphon.
:::

### Comment utiliser Smart Dialer {#how_to_use_the_smart_dialer}

Pour utiliser Smart Dialer, créez un objet `StrategyFinder` et appelez la méthode `NewDialer`, en donnant la liste de domaines de test et la configuration YAML.
La méthode `NewDialer` renvoie un `transport.StreamDialer`, qui peut être utilisé pour établir des connexions à l'aide de la stratégie trouvée. Par exemple :

```go
finder := &smart.StrategyFinder{
    TestTimeout:  5 * time.Second,
    LogWriter:   os.Stdout,
    StreamDialer: &transport.TCPDialer{},
    PacketDialer: &transport.UDPDialer{},
}

configBytes := []byte(`
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
`)

dialer, err := finder.NewDialer(
  context.Background(),
  []string{"www.google.com"},
  configBytes
)
if err != nil {
    // Handle error.
}

// Use dialer to create connections.
```

Il s'agit d'un exemple basique. Vous devrez peut-être l'adapter à votre cas d'utilisation.
