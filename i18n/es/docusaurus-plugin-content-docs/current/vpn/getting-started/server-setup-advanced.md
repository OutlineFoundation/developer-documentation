---
title: "Implementar con una secuencia de comandos de instalación"
sidebar_label: "Implementar con una secuencia de comandos de instalación"
---

Esta guía explica el proceso de configurar un servidor de Outline para ofrecer acceso a Internet seguro y sin restricciones.

## Requisitos previos {#prerequisites}

- Un servidor (físico o virtual) con un sistema operativo compatible (Ubuntu 20.04 LTS o Debian 10)

- Acceso raíz o sudo al servidor

## Instrucciones {#instructions}

1. Descarga y ejecuta la secuencia de comandos de instalación de Outline.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Sigue las indicaciones que aparecen en pantalla.
