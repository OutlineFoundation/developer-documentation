---
title: "Concepts"
sidebar_label: "Concepts"
---

Met Outline kunnen gebruikers toegangsbeperkingen tot het open internet omzeilen. Hieronder vind je informatie over hoe het werkt:

## Serviceproviders en eindgebruikers

Het Outline-systeem bestaat uit 2 partijen: **serviceproviders** die de servers beheren en **eindgebruikers** die via die servers toegang krijgen tot het internet.

- **Serviceproviders** maken de Outline-servers, genereren **toegangssleutels** en **geven de sleutels uit** aan eindgebruikers. Dit kan onder andere met de app
**Outline Manager**.

- **Eindgebruikers** installeren de **Outline-client**, voeren de ontvangen **toegangssleutel** in en **maken verbinding** met een beveiligde tunnel.

## Toegangssleutels

Toegangssleutels zijn de inloggegevens waarmee gebruikers verbinding kunnen maken met een Outline-server. Ze bevatten de nodige informatie voor de Outline-client om een beveiligde verbinding te maken. Er zijn 2 typen toegangssleutels:

- **Statische toegangssleutels** coderen alle serverinformatie die nodig is om verbinding te maken (serveradres, poort, wachtwoord, versleutelingsmethode), wat ertoe leidt dat de toegangsinformatie niet gewijzigd kan worden. Gebruikers plakken deze sleutel in de Outline-client.

Voorbeeld:

- **Dynamische toegangssleutels**: Hiermee kan een serviceprovider de toegangsinformatie tot de server op afstand hosten. Zo kunnen providers hun serverconfiguratie updaten (serveradres, poort, wachtwoorden, versleutelingsmethode) zonder nieuwe toegangssleutels te hoeven uitgeven aan eindgebruikers. Ga naar [dynamische toegangssleutels](vpn/management/dynamic-access-keys) voor meer informatie.
