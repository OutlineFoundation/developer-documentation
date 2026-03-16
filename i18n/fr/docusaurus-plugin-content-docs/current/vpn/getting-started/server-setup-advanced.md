---
title: "Déployer avec un script d&apos;installation"
sidebar_label: "Déployer avec un script d&apos;installation"
---

Ce guide vous explique comment configurer un serveur Outline pour fournir un accès sécurisé et sans restriction à Internet.

## Prérequis {#prerequisites}

- Un serveur (physique ou virtuel) exécutant un système d'exploitation compatible (Ubuntu 20.04 LTS ou Debian 10)

- Un accès root ou sudo au serveur

## Instructions {#instructions}

1. Téléchargez et exécutez le script d'installation d'Outline.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Suivez les instructions à l'écran.
