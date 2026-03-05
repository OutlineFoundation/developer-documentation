---
title: "Deploy Using an Installation Script"
sidebar_label: "Using Installation Script"
---

Deze handleiding leidt je door het proces om een Outline-server in te stellen zodat je mensen beveiligde, onbeperkte internettoegang kunt geven.

## Vereisten

- Een server (fysiek of virtueel) met een ondersteund besturingssysteem (Ubuntu 20.04 LTS of Debian 10)

- Root- of sudo-toegang tot de server

## Instructies

1. Download het Outline-installatiescript en voer het uit.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Volg de aanwijzingen op het scherm.
