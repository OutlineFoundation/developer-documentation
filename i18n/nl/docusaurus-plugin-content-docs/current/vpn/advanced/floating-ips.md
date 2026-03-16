---
title: "Een server maken die niet kan worden geblokkeerd met zwevende IP-adressen"
sidebar_label: "Een server maken die niet kan worden geblokkeerd met zwevende IP-adressen"
---

## Introductie {#introduction}

Outline-servers worden soms ontdekt en geblokkeerd voor sterk gecensureerde netwerken. Het is mogelijk en niet al te moeilijk om een geblokkeerde server te herstellen als die juist was ingesteld. Je doet dit met DNS, de internettechnologie die domeinnamen (zoals `getoutline.org`) vertaalt in fysieke IP-adressen (zoals `216.239.36.21`), en zwevende IP's, een cloudfunctie waarmee je meerdere IP-adressen kunt toewijzen aan één Outline-server.

## Vereisten {#requirements}

Je hebt niet veel technische kennis nodig om deze handleiding te kunnen volgen. Wat basiskennis van DNS is nuttig, maar niet vereist. Ga naar de [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name)-handleiding over domeinnamen voor een introductie.

We gebruiken DigitalOcean en Google Domains om een concreet voorbeeld te geven, maar elke cloudprovider waarbij je IP-adressen kunt toewijzen (zoals Google Cloud of [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip)) en elke domeinregistreerder (zoals [AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)) werken ook gewoon.

## Instructies {#instructions}

1. Dit zijn de stappen om het IP-adres van een server te roteren:

2. Koop een domeinnaam.

3. Stel in dat de domeinnaam naar het IP-adres van onze server verwijst.

4. Geef toegangssleutels uit met de domeinnaam.

5. Wijs een zwevend IP-adres toe aan de Droplet van de server.

6. Wijzig de domeinnaam zodat deze verwijst naar het nieuwe IP-adres.

## Een Outline-server maken via DigitalOcean {#create_an_outline_server_on_digitalocean}

Als je een bestaande DigitalOcean-server hebt, sla je deze stap over.

1. Open Outline Manager en klik linksonder op het plusje (+) om het scherm te openen waarin je servers maakt.

2. Klik bij de knop DigitalOcean op Server maken en volg de aanwijzingen in de app.

![Server maken](/images/create-DO-server.png)

## Een hostnaam maken voor je server {#make_a_hostname_for_your_server}

1. Ga naar [Google Domains](https://domains.google.com/m/registrar/) en klik op Perfecte zoeken.

2. Voer in de zoekbalk een domeinnaam in en kies een naam. We gebruiken `outlinedemo.info` als voorbeeld.

3. Ga in Google Domains naar het tabblad DNS. Typ onder Aangepaste resourcerecords het IP-adres van je server in het veld IPv4-adres.

4. Ga in Outline Manager naar het tabblad Instellingen voor je server. Typ onder Hostnaam de hostnaam die je hebt gekocht en klik op OPSLAAN. Alle toekomstige toegangssleutels gebruiken dan deze hostnaam in plaats van het IP-adres van de server.

![De hostnaam instellen](/images/set-hostname.png)

## Het IP-adres van de server wijzigen {#change_the_servers_ip_address}

1. Ga op de pagina Droplets van DigitalOcean naar je server.

2. Klik rechtsboven, naast Floating IP (Zwevend IP-adres), op Enable Now (Nu aanzetten).

![Zwevend IP-adres aanzetten](/images/floating-ip-DO.png)

1. Zoek je server in de lijst met Droplets en klik op Assign Floating IP (Zwevend IP-adres toewijzen).

![Zwevend IP-adres toewijzen](/images/assign-floating-ip-DO.png)

1. Ga terug naar het tabblad DNS in Google Domains.

2. Wijzig het IP-adres op dezelfde manier als eerst, maar voeg dit keer het nieuwe zwevende IP-adres toe. Het kan 48 uur duren voordat dit is doorgevoerd, maar meestal duurt het maar een paar minuten.

3. Ga naar de [online DNS-tool van Google](https://toolbox.googleapps.com/apps/dig/#A/) en voer je domeinnaam in om te controleren of de wijziging in de laatste stap is doorgevoerd.

![Je domein zoeken in de DNS-tool van Google](/images/google-dns.png)

Nadat deze wijziging is doorgevoerd, maken clients verbinding met het nieuwe IP-adres. Je kunt met een nieuwe sleutel verbinding maken met je server en <https://ipinfo.io> openen om te controleren of het nieuwe IP-adres van je server wordt getoond.

Conclusie
Het IP-adres van een server roteren kan een snelle manier zijn om de blokkade van een server op te heffen en weer toegang te geven tot clients. Als je meer vragen hebt, kun je reageren op de [aankondigingspost](https://redd.it/hrbhz4), naar [de supportpagina van Outline](https://support.getoutline.org/) gaan of [rechtstreeks contact met ons opnemen](https://support.getoutline.org/s/contactsupport).
