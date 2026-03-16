---
title: "Yükleme komut dosyası kullanarak dağıtma"
sidebar_label: "Yükleme komut dosyası kullanarak dağıtma"
---

Bu kılavuzda, internet erişimini güvenli ve sınırsız hale getirmek için Outline sunucusu kurma işlemi anlatılmaktadır.

## Ön hazırlık {#prerequisites}

- Desteklenen işletim sisteminde (Ubuntu 20.04 LTS veya Debian 10) çalışan bir sunucu (fiziksel veya sanal)

- Sunucuya kök veya sudo erişimi

## Talimatlar {#instructions}

1. Outline yükleme komut dosyasını indirip çalıştırın.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. Ekranda gösterilen adımları izleyin.
