---
title: "Share Management Access"
sidebar_label: "Share Management Access"
---

Wenn Ihr Outline-Dienst wächst, kann es erforderlich werden, anderen vertrauenswürdigen Personen Verwaltungsaufgaben zu übertragen. In diesem Dokument werden die verschiedenen Methoden beschrieben, die für die gemeinsame Nutzung des Verwaltungszugangs mit anderen Managern zur Verfügung stehen.

Die Methode für die Freigabe des Verwaltungszugriffs ist davon abhängig, wie Ihr Outline-Server ursprünglich bereitgestellt wurde.

## Bereitstellung bei Cloud-Anbietern {#cloud_provider_deployments}

Bei Outline-Servern, die auf Cloud-Plattformen wie DigitalOcean, AWS oder Google Cloud bereitgestellt wurden, erfolgt der Verwaltungszugriff normalerweise über die integrierte Identitäts- und Zugriffsverwaltung (IAM) des Anbieters. Dieser Ansatz ist sicherer und kontrollierter als eine manuelle Konfigurationsfreigabe.

### DigitalOcean {#digitalocean}

DigitalOcean bietet eine solide **Teams**-Funktion, mit der Sie andere DigitalOcean-Nutzer zur Zusammenarbeit an Ihren Projekten einladen können. Dieses Verfahren wird empfohlen, um anderen Verwaltungszugriff auf Ihren Outline-Server zu gewähren, der auf deren Plattform gehostet wird.

#### 1. Teamzugang gewähren {#1_grant_team_access}

Die effektivste Möglichkeit, die Verwaltung Ihres auf DigitalOcean gehosteten Outline-Servers freizugeben, ist die Nutzung der **Teams**-Funktion.

- Melden Sie sich in Ihrem DigitalOcean-Konto an.

- Gehen Sie zum Bereich **Teams**.

- Erstellen Sie ein neues Team (wenn nicht bereits erfolgt) oder laden Sie bestehende DigitalOcean-Nutzer in Ihr Team ein.

- Wenn Sie Mitglieder einladen, können Sie Ihnen spezifische Rollen zuweisen und ihnen Zugriff auf bestimmte Ressourcen gewähren, einschließlich Ihres oder Ihrer Droplets mit Outline.

#### 2. Berechtigungen festlegen {#2_control_permissions}

Überlegen Sie sich, welche Berechtigungen Sie den Teammitgliedern erteilen. Zur Verwaltung des Outline-Servers können Sie ihnen Lese- und Schreibzugriff auf das entsprechende Droplet gewähren. Dadurch können sie Folgendes:

- die Details des Droplets einsehen (IP-Adresse, Status usw.)

- auf die Droplet-Konsole zugreifen (falls für die Fehlerbehebung erforderlich)

- potenziell Aktionen wie den Neustart des Droplets ausführen (abhängig von den gewährten Berechtigungen)

Nutzer, die den Outline-Manager mit ihrem DigitalOcean-Konto verbinden, können jetzt alle Outline-Server einsehen und verwalten, die mit diesem Konto verknüpft sind.

## Manuelle Installationen {#manual_installations}

Wenn Outline mithilfe des [Installationsskripts](../getting-started/server-setup-advanced) manuell auf eigenen Servern installiert wurde, besteht die primäre Möglichkeit, Verwaltungszugriff zu gewähren, darin, die **access config** freizugeben.

Die Outline-Manager-Anwendung braucht einen bestimmten Konfigurationsstring, um sich mit einem Outline-Server zu verbinden und ihn zu verwalten. Dieser String enthält alle notwendigen Informationen, einschließlich der Serveradresse, des Ports und eines geheimen Schlüssels zur Authentifizierung.

### 1. Die `access.txt`-Datei suchen {#1_locate_the_accesstxt_file}

Gehen Sie auf dem Server, auf dem Outline installiert ist, zum Outline-Verzeichnis. Der genaue Ort kann je nach Ihrer Installationsmethode leicht variieren, ist aber häufig hier zu finden:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- In dem vom Outline-Servercontainer verwendeten Docker-Volume.

### 2. Die access config abrufen {#2_retrieve_the_access_config}

Wenn Sie die `access.txt`-Datei gefunden haben, konvertieren Sie diese in JSON, das Format, das der Outline-Manager im nächsten Schritt erwartet.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

Die Ausgabe enthält den selbst signierten Zertifikat-Fingerabdruck (`certSha256`) und den Endpunkt der Management API auf dem Server (`apiUrl`):

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```

### 3. Die access config sicher weitergeben {#3_share_the_access_config_securely}

Kopieren Sie die Ausgabe und geben Sie sie sicher an den neuen Outline-Manager weiter. Versenden Sie sie möglichst nicht über unverschlüsselte Kanäle wie einfache E-Mail oder Chat.
Nach Möglichkeit sollten Sie die sichere Freigabefunktion eines Passwortmanagers oder eine andere verschlüsselte Kommunikationsmethode nutzen.

Durch Einfügen der bereitgestellten **access config** in den Outline-Manager kann der neue Verwalter den Outline-Server hinzufügen und anschließend über die Benutzeroberfläche der Anwendung verwalten. Zusätzlicher Support für die Verwendung des Outline-Managers ist in der [Outline-Hilfe](https://support.google.com/outline) verfügbar.
