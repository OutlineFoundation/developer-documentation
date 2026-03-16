---
title: "Use a Domain Name with Floating IPs"
sidebar_label: "Domain with Floating IPs"
---

## Einführung {#introduction}

Gelegentlich können Outline-Server von stark zensierten Netzwerken erkannt und blockiert werden. Wenn ein blockierter Server korrekt eingestellt wurde, kann die Konnektivität relativ einfach wiederhergestellt werden. Wir nutzen dafür DNS, die Internettechnologie, die Domainnamen wie `getoutline.org` in physische IP-Adressen wie `216.239.36.21` übersetzt, und Floating-IP-Adressen, eine Cloud-Funktion, mit der man Outline-Servern mehr als eine IP-Adresse zuweisen kann.

## Voraussetzungen {#requirements}

Um die folgenden Anleitungen umsetzen zu können, ist nur ein geringes Maß an technischen Fähigkeiten erforderlich. Grundlegende Kenntnisse zu DNS sind hilfreich, aber nicht notwendig. Im [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name)-Leitfaden zu Domains finden Sie eine Einführung.

Als konkretes Beispiel nutzen wir Domains von DigitalOcean und Google. Jeder Cloud-Anbieter, der eine Zuweisung von IP-Adressen zulässt (wie Google Cloud oder [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip)), und jeder Domainregistrar (z. B. [AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)) bietet sich aber genauso dafür an.

## Anleitung {#instructions}

1. Mit den folgenden Schritten können Sie einen Server periodisch zwischen mehreren IP‑Adressen umschalten lassen:

2. Erwerben Sie einen Domainnamen.

3. Lassen Sie den Domainnamen auf die IP-Adresse unseres Servers verweisen.

4. Verteilen Sie unter Verwendung des Domainnamens Zugriffsschlüssel.

5. Weisen Sie dem Droplet des Servers eine Floating-IP-Adresse zu.

6. Ändern Sie den Domainnamen, sodass er auf die neue IP-Adresse verweist.

## Einen Outline-Server bei DigitalOcean erstellen {#create_an_outline_server_on_digitalocean}

Wenn Sie bereits einen laufenden DigitalOcean-Server haben, überspringen Sie den nächsten Schritt.

1. Öffnen Sie den Outline-Manager und klicken Sie unten links auf die Schaltfläche „+“, um zum Bildschirm zum Erstellen eines Servers zu gelangen.

2. Klicken Sie auf der Schaltfläche „DigitalOcean“ auf „Server erstellen“ und folgen Sie den Anweisungen in der App.

![Server erstellen](/images/create-DO-server.png)

## Einen Hostnamen für Ihren Server festlegen {#make_a_hostname_for_your_server}

1. Gehen Sie zu [Google Domains](https://domains.google.com/m/registrar/) und klicken Sie auf „Sichern Sie sich die perfekte Domain“.

2. Geben Sie in der Suchleiste einen Domainnamen ein und wählen Sie einen Namen aus. Für unser Beispiel nutzen wir `outlinedemo.info` als Namen.

3. Gehen Sie auf „Google Domains“ zum DNS-Tab. Tippen Sie unter „Benutzerdefinierte Ressourceneinträge“ im Feld „IPv4-Adresse“ die IP-Adresse Ihres Servers ein.

4. Gehen Sie im Outline-Manager zum Tab „Einstellungen“ für Ihren Server. Geben Sie unter „Hostname“ den von Ihnen gekauften Hostnamen ein und klicken SIe auf „Speichern“. Dadurch nutzen alle zukünftigen Zugriffsschlüssel anstelle der IP-Adresse des Servers diesen Hostnamen.

![Den Hostnamen festlegen](/images/set-hostname.png)

## Die IP-Adresse des Servers ändern {#change_the_servers_ip_address}

1. Gehen Sie auf der Seite „Droplets“ bei DigitalOcean auf Ihren Server.

2. Klicken Sie rechts oben neben „Floating-IP-Adressen“ auf „Jetzt aktivieren“.

![Floating-IP-Adresse aktivieren](/images/floating-ip-DO.png)

1. Suchen Sie in der Liste mit den Droplets nach Ihrem Server und klicken Sie auf „Floating-IP-Adresse zuweisen“.

![Floating-IP-Adresse zuweisen](/images/assign-floating-ip-DO.png)

1. Gehen Sie auf Google Domains zurück auf den DNS-Tab.

2. Ändern Sie wie zuvor die IP-Adresse. Ersetzen Sie sie diesmal durch die neue Floating-IP-Adresse. Bis zur Änderung könnte es 48 dauern; oft vergehen aber nur ein paar Minuten.

3. Gehen Sie auf [Das Online-DNS-Tool von Google](https://toolbox.googleapps.com/apps/dig/#A/) und geben SIe Ihren Domainnamen ein. Nachfolgend wird Ihnen angezeigt, wann die Änderung im letzten Schritt stattgefunden hat.

![Suchen Sie mit dem DNS-Tool von Google nach Ihrer Domain.](/images/google-dns.png)

Sobald die Änderung übernommen wurde, werden sich Kunden mit der neuen IP-Adresse verbinden. Wenn Sie sich über einen neuen Schlüssel mit Ihrem Server verbinden und <https://ipinfo.io> aufrufen, können Sie die neue IP-Adresse Ihres Servers sehen.

Fazit
Durch „rotieren“ der IP-Adresse eines Outline-Servers können Sie Blockierungen eines Servers umgehen und die Konnektivität für Clients wiederherstellen. Wenn Sie weitere Fragen haben, können Sie [hier einen Kommentar hinzufügen](https://redd.it/hrbhz4), die [Supportseite von Outline aufrufen](https://support.getoutline.org/) oder [uns direkt kontaktieren](https://support.getoutline.org/s/contactsupport).
