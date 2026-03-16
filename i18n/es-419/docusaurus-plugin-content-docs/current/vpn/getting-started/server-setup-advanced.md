---
title: "Implementa el servidor con una secuencia de comandos de instalación"
sidebar_label: "Implementa el servidor con una secuencia de comandos de instalación"
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
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Sigue las indicaciones que aparecen en pantalla.
