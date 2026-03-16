---
title: "インストール スクリプトを使用してデプロイする"
sidebar_label: "インストール スクリプトを使用してデプロイする"
---

このガイドでは、無制限の安全なインターネット アクセスを提供するように Outline サーバーを設定するプロセスについて説明します。

## 前提条件 {#prerequisites}

- サポートされているオペレーティング システム（Ubuntu
20.04 LTS または Debian 10）を実行しているサーバー（物理または仮想）

- サーバーへの root または sudo アクセス権

## 手順 {#instructions}

1. Outline インストール スクリプトをダウンロードして実行します。

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. 画面の指示に従います。
