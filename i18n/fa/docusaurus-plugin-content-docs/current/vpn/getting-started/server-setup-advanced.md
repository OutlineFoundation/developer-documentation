---
title: "Deploy Using an Installation Script"
sidebar_label: "Using Installation Script"
---

این راهنما شما را در فرایند راه‌اندازی «سرور Outline» همراهی می‌کند تا
دسترسی به اینترنت ایمن و بدون محدودیت را ارائه کند.

## پیش‌نیازها {#prerequisites}

- سیستم‌عامل (Ubuntu 20.04 LTS یا Debian 10) را یک سرور (فیزیکی یا مجازی) اجرا یا پشتیبانی می‌کند

- دسترسی sudo یا ریشه به سرور

## دستورالعمل‌ها {#instructions}

1. دستورگان نصب Outline را بارگیری و اجرا کنید.

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. پیام‌واره‌های روی صفحه را دنبال کنید.
