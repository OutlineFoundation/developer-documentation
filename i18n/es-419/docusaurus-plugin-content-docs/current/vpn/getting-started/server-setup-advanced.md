---
title: "Deploy Using an Installation Script"
sidebar_label: "Using Installation Script"
---

En esta guía, se explica el proceso para configurar un servidor de Outline para
proporcionar acceso a Internet seguro y sin restricciones.

## Requisitos previos {#prerequisites}

- Un servidor (físico o virtual) que ejecute un sistema operativo compatible (Ubuntu
20.04 LTS o Debian 10)

- Acceso raíz o sudo al servidor

## Instrucciones {#instructions}

1. Descarga y ejecuta la secuencia de comandos de instalación de Outline.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Sigue las indicaciones que aparecen en pantalla.
