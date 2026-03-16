---
title: "ทำให้ใช้งานได้ด้วยการใช้สคริปต์การติดตั้ง"
sidebar_label: "ทำให้ใช้งานได้ด้วยการใช้สคริปต์การติดตั้ง"
---

คู่มือนี้จะอธิบายกระบวนการตั้งค่าเซิร์ฟเวอร์ Outline เพื่อการเข้าถึงอินเทอร์เน็ตที่ปลอดภัยและไม่จำกัด

## สิ่งที่ต้องมี {#prerequisites}

- เซิร์ฟเวอร์ (แบบกายภาพหรือระบบเสมือนจริง) ที่ใช้ระบบปฏิบัติการที่รองรับ (Ubuntu 20.04 LTS หรือ Debian 10)

- สิทธิ์เข้าถึงเซิร์ฟเวอร์แบบรูทหรือ sudo

## วิธีการ {#instructions}

1. ดาวน์โหลดและเรียกใช้สคริปต์การติดตั้ง Outline

```sh
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/OutlineFoundation/outline-apps/master/server_manager/install_scripts/install_server.sh)"
```

2. ทำตามคำแนะนำบนหน้าจอ
