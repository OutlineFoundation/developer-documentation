---
title: "Share Management Access"
sidebar_label: "Share Management Access"
---

Als je Outline-service groeit, wil je andere mensen die je vertrouwt misschien beheerverantwoordelijkheden geven. In dit document vind je uitleg over de verschillende methoden waarmee je andere mensen beheertoegang kunt geven.

Hoe je beheertoegang geeft, hangt af van hoe je je Outline-server in eerste instantie hebt geïmplementeerd.

## Implementatie op cloudproviders

Voor Outline-servers die zijn geïmplementeerd op cloudplatforms zoals DigitalOcean, AWS of Google Cloud geef je beheertoegang meestal via de geïntegreerde functies voor identiteits- en toegangsbeheer (IAM) van de provider. Dit biedt meer beveiliging en controle dan de configuratie handmatig delen.

### DigitalOcean

DigitalOcean biedt de krachtige functie **Teams** waarmee je andere DigitalOcean-gebruikers kunt uitnodigen om samen te werken aan je projecten. Dit is de aanbevolen manier om beheertoegang te geven tot je Outline-server als die is gehost op het platform van DigitalOcean.

#### 1. Teamtoegang instellen

De meest effectieve manier om beheertoegang te geven tot je Outline-server als die is gehost op het platform van DigitalOcean is door de functie **Teams** van DigitalOcean te gebruiken.

- Log in op je DigitalOcean-account.

- Ga naar het gedeelte **Teams**.

- Maak een nieuw team (als je nog geen team hebt) of nodig bestaande DigitalOcean-gebruikers uit voor je team.

- Als je leden uitnodigt, kun je ze specifieke rollen geven en ze toegang geven tot specifieke resources, inclusief je Droplets die Outline uitvoeren.

#### 2. Rechten beheren

Bepaal zorgvuldig welke rechten je teamleden geeft. Voor het beheer van de Outline-server kun je ze lees- en schrijftoegang geven tot de specifieke Droplet. Ze kunnen dan het volgende doen:

- De details van de Droplet (IP-adres, status, etc.) bekijken.

- De console van de Droplet openen (indien nodig voor probleemoplossing).

- Eventueel acties uitvoeren zoals het opnieuw opstarten van de Droplet (afhankelijk van de rechten die ze hebben gekregen).

Gebruikers die Outline Manager koppelen aan hun DigitalOcean-account kunnen nu alle Outline-servers die zijn gekoppeld aan dat account bekijken en beheren.

## Handmatige installaties

Als je Outline handmatig hebt geïnstalleerd op je eigen server via het [installatiescript](../getting-started/server-setup-advanced), is de primaire manier om beheertoegang te geven door de **toegangsconfiguratie** te delen.

De Outline Manager-app heeft een specifieke configuratietekenreeks nodig om verbinding te maken met een Outline-server en deze te beheren. Deze configuratietekenreeks bevat alle nodige informatie, inclusief het serveradres, de poort en een geheime sleutel voor verificatie.

### 1. Zoek het `access.txt`-bestand

Ga op de server waarop Outline is geïnstalleerd naar de Outline-directory. De exacte locatie kan verschillen, afhankelijk van je installatiemethode, maar dit zijn enkele veelgebruikte locaties:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- In het Docker-volume dat wordt gebruikt door de Outline-servercontainer.

### 2. Haal de toegangsconfiguratie op

Nadat je het `access.txt`-bestand hebt gevonden, converteer je het naar json. Dit is de indeling die Outline Manager verwacht in de volgende stap.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

De uitvoer bevat de zelfondertekende vingerafdruk van het certificaat (`certSha256`) en het eindpunt van de beheer-API op de server (`apiUrl`):

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```

### 3. Deel de toegangsconfiguratie op een beveiligde manier

Kopieer de uitvoer en deel deze beveiligd met de nieuwe Outline-beheerder. Stuur de uitvoer niet via onversleutelde kanalen zoals gewone e-mail of instant messaging.
We raden je aan de functie voor beveiligd delen van een wachtwoordmanager of een andere versleutelde communicatiemethode te gebruiken.

Als de nieuwe beheerder de ontvangen **toegangsconfiguratie** in Outline Manager plakt, kan deze de Outline-server toevoegen en daarna beheren via de app-interface. Je vindt meer hulp voor het gebruik van Outline Manager in het [Helpcentrum van Outline](https://support.google.com/outline).
