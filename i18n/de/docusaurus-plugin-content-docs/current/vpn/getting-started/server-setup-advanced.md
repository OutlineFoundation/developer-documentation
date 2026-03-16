---
title: "Über ein Installationsskript bereitstellen"
sidebar_label: "Über ein Installationsskript bereitstellen"
---

In diesem Leitfaden werden Sie Schritt für Schritt durch die Einrichtung eines Outline-Servers geführt, um einen sicheren und uneingeschränkten Internetzugriff bereitzustellen.

## Sie benötigen: {#prerequisites}

- Einen Server (physisch oder virtuell) mit einem unterstützten Betriebssystem (Ubuntu 20.04 LTS oder Debian 10)

- Einen Root- oder sudo-Zugriff auf den Server

## Anleitung {#instructions}

1. Laden Sie das Installationsskript für Outline herunter und führen sie es aus.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Folgen Sie anschließend der Anleitung auf dem Bildschirm.
