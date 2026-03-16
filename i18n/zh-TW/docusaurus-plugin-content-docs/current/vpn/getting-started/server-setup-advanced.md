---
title: "使用安裝指令碼部署"
sidebar_label: "使用安裝指令碼部署"
---

本指南將逐步引導您設定 Outline 伺服器，讓您可以安全且不受限制地存取網際網路。

## 事前準備 {#prerequisites}

- 一部實體或虛擬伺服器，搭載支援的作業系統 (Ubuntu 20.04 LTS 或 Debian 10)

- 該伺服器的 root 或 sudo 存取權

## 操作說明 {#instructions}

1. 下載並執行 Outline 安裝指令碼。

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. 按照畫面上的提示操作。
