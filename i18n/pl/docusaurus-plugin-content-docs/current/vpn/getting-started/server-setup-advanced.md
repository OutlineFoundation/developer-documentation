---
title: "Deploy Using an Installation Script"
sidebar_label: "Using Installation Script"
---

Ten przewodnik przeprowadzi Cię przez proces konfigurowania serwera Outline w celu zapewnienia bezpiecznego i nieograniczonego dostępu do internetu.

## Wymagania wstępne {#prerequisites}

- Serwer (fizyczny lub wirtualny) z obsługiwanym systemem operacyjnym (Ubuntu 20.04 LTS lub Debian 10)

- Dostęp na poziomie roota lub sudo do serwera

## Instrukcje {#instructions}

1. Pobierz i uruchom skrypt instalacyjny Outline.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Postępuj zgodnie z instrukcjami wyświetlanymi na ekranie.
