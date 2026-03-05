---
title: "Deploy Using an Installation Script"
sidebar_label: "Using Installation Script"
---

سنتعرف في هذا الدليل على عملية إعداد خادم Outline
لتوفير إمكانية وصول إلى الإنترنت آمنة وغير مقيّدة.

## المتطلّبات الأساسية

- خادم (افتراضي أو فعلي) يعمل عليه نظام تشغيل متوافق (مثل Ubuntu
20.04 LTS أو Debian 10)

- إذن وصول من النوع الجذري أو النوع sudo إلى الخادم

## التعليمات

1. يجب تنزيل نص تثبيت Outline البرمجي وتشغيله.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. يجب تنفيذ الطلبات التي تظهر على الشاشة.
