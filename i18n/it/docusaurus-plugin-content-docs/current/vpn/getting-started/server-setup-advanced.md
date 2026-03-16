---
title: "Deploy Using an Installation Script"
sidebar_label: "Using Installation Script"
---

Questa guida ti illustra il processo di configurazione di un server Outline per
fornire un accesso a internet sicuro e senza limitazioni.

## Prerequisiti {#prerequisites}

- Un server (fisico o virtuale) che esegue un sistema operativo supportato (Ubuntu
20.04 LTS o Debian 10)

- Accesso root o sudo al server

## Istruzioni {#instructions}

1. Scarica ed esegui lo script di installazione di Outline.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Segui le istruzioni visualizzate sullo schermo.
