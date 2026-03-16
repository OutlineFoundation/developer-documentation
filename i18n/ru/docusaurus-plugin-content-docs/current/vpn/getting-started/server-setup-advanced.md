---
title: "Deploy Using an Installation Script"
sidebar_label: "Using Installation Script"
---

Это руководство поможет вам настроить сервер Outline для защищенного и неограниченного доступа к интернету.

## Требования {#prerequisites}

- Физический или виртуальный сервер, работающий на поддерживаемой операционной системы (Ubuntu 20.04 LTS или Debian 10).

- Корневой доступ к серверу или доступ с привилегиями администратора.

## Инструкции {#instructions}

1. Скачайте и запустите скрипт установки Outline.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Следуйте инструкциям на экране.
