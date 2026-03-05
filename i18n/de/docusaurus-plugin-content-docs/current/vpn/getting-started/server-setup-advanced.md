---
title: "Deploy Using an Installation Script"
sidebar_label: "Using Installation Script"
---

In diesem Leitfaden werden Sie Schritt für Schritt durch die Einrichtung eines Outline-Servers geführt, um einen sicheren und uneingeschränkten Internetzugriff bereitzustellen.

## Sie benötigen:

- Einen Server (physisch oder virtuell) mit einem unterstützten Betriebssystem (Ubuntu 20.04 LTS oder Debian 10)

- Einen Root- oder sudo-Zugriff auf den Server

## Anleitung

1. Laden Sie das Installationsskript für Outline herunter und führen sie es aus.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Folgen Sie anschließend der Anleitung auf dem Bildschirm.
