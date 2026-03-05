---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline fournit des métriques de performance détaillées dans [Prometheus](https://prometheus.io/) qui vous permettent de mieux analyser l'utilisation et l'état de votre serveur. Ce guide vous explique comment récupérer et afficher ces métriques.

**Remarque importante** : Dans ce guide, nous partons du principe que vous maîtrisez les bases de Prometheus et de PromQL. Si vous ne connaissez pas Prometheus, n'hésitez pas à consulter sa documentation et suivre ses tutoriels avant d'explorer les métriques d'Outline.

## Prérequis

- **Serveur Outline avec Prometheus activé** : vérifiez que les métriques Prometheus sont activées sur votre serveur Outline (il s'agit en général de la configuration par défaut).

- **Accès SSH à votre serveur** : vous avez besoin d'un accès SSH pour transférer le port Prometheus.

## Instructions

1. **Transférer le port Prometheus**

Connectez-vous à votre serveur via SSH et transférez le port 9090.

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **Accéder à l'interface Web de Prometheus**

Ouvrez votre navigateur Web et accédez à la page <http://localhost:9090/graph>.

3. **Interroger les métriques Prometheus**
Utilisez des requêtes PromQL pour retrouver les métriques qui vous intéressent.

### Exemples de requêtes PromQL

#### Utilisation

- **Octets de données (par clé d'accès, protocole et direction) :**

`increase(shadowsocks_data_bytes[1d])`

- **Octets de données (agrégés par clé d'accès) :**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Octets de données (pour le calcul des limites de données) :**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Octets de données (par emplacement, protocole et direction) :**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Clés d'accès actives

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### Connexions TCP

- **Connexions TCP (par clé d'accès, emplacement et état) :**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **Connexions TCP (par emplacement) :**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **Paquets UDP (par emplacement et état) :**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **Associations UDP (sans répartition) :**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Performances

- **Utilisation du processeur (par processus) :**

`rate(process_cpu_seconds_total[10m])`

- **Utilisation de la mémoire (par processus) :**

`process_virtual_memory_bytes`

#### Informations sur les builds

- **Prometheus :**

`prometheus_build_info`

- **outline-ss-server :**

`shadowsocks_build_info`

- **Node.js :**

`nodejs_version_info`

Vous trouverez la liste complète des métriques disponibles dans le [code source](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) d'`outline-ss-server`.
