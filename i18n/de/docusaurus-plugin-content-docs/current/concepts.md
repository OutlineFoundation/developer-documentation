---
title: "Concepts"
sidebar_label: "Concepts"
---

Mit Outline erhalten Nutzer ungehinderten Zugang zum offenen Internet. Hier sind einige Schlüsselkonzepte zur Erklärung:

## Serviceprovider und Endnutzer

Im Outline-System gibt es zwei Hauptrollen: **Serviceprovider**, die die Server verwalten, und **Endnutzer**, die über das Internet auf diese Server zugreifen.

- **Serviceprovider** erstellen die Outline-Server, generieren die **Zugriffsschlüssel**
und **verteilen die Schlüssel** an die Endnutzer, zum Beispiel über die App **Outline-Manager**.

- **Endnutzer** installieren die App **Outline-Client**, fügen den erhaltenen **Zugriffsschlüssel** ein und **verbinden** sich über einen sicheren Tunnel.

## Zugriffsschlüssel

Die Zugriffsschlüssel sind die Anmeldedaten, mit denen Nutzer eine Verbindung zu einem Outline-Server herstellen können. Sie enthalten alle Informationen, die der Online-Client benötigt, um eine verschlüsselte Verbindung aufzubauen. Es gibt zwei Arten von Zugriffsschlüsseln:

- 

**Statische Zugriffsschlüssel** codieren alle für die Verbindung notwendigen Serverinformationen, wie Serveradresse, Port, Passwort und Verschlüsselungsmethode. So wird verhindert, dass die Zugangsinformationen geändert werden können. Nutzer fügen diesen Schlüssel in den Outline-Client ein.

Beispiel:

- 

Mit einem **dynamischen Zugriffsschlüssel** können Serviceprovider die Informationen für den Serverzugriff aus der Ferne hosten. So können Provider die Serverkonfiguration – Serveradresse, Port, Passwörter, Verschlüsselungsmethode – aktualisieren, ohne neue Zugriffsschlüssel an die Endnutzer ausstellen zu müssen. Weitere Informationen finden Sie unter [Dynamische Zugriffsschlüssel](vpn/management/dynamic-access-keys).
