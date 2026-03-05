---
title: "Use a Domain Name with Floating IPs"
sidebar_label: "Domain with Floating IPs"
---

## Introduzione

A volte i server Outline possono trovarsi ad affrontare il problema di essere scoperti e bloccati
da reti altamente censurate. È possibile e non troppo difficile recuperare
un server bloccato se è stato configurato correttamente. Lo faremo utilizzando il DNS, la
tecnologia internet che traduce i nomi di dominio (come `getoutline.org`) in
indirizzi IP fisici (come `216.239.36.21`), e gli IP mobile, una funzionalità cloud
che consente di assegnare più indirizzi IP a un server Outline.

## Requisiti

Per seguire questa guida è richiesta una bassa competenza tecnica. Una conoscenza
di base del DNS è utile, ma non obbligatoria. Per un'introduzione, consulta la guida
[MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name)
sui nomi di dominio.

Per fare un esempio concreto useremo DigitalOcean e Google Domains, ma funzionerà altrettanto bene qualsiasi
provider cloud che consenta l'assegnazione di indirizzi IP (ad esempio Google Cloud o
[AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip))
e qualsiasi registrar di domini (ad esempio
[AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)).

## Istruzioni

1. L'elenco seguente riassume i passaggi per ruotare l'indirizzo IP di un server:

2. Acquista un nome di dominio.

3. Indirizza il nome di dominio all'indirizzo IP del nostro server.

4. Emetti delle chiavi di accesso utilizzando il nome di dominio.

5. Assegna un IP mobile alla droplet del server.

6. Cambia il nome di dominio in modo che rimandi al nuovo indirizzo IP.

## Crea un server Outline su DigitalOcean

Se disponi di un server DigitalOcean in esecuzione, vai al passaggio successivo.

1. Apri Outline Manager e fai clic su "+" in basso a sinistra per entrare nella schermata
di creazione del server.

2. Fai clic su "Crea server" sul pulsante "DigitalOcean" e segui le istruzioni
nell'app.

![Crea server](/images/create-DO-server.png)

## Crea un nome host per il tuo server

1. Vai su [Google Domains](https://domains.google.com/m/registrar/) e
fai clic su "Trova il dominio perfetto".

2. Inserisci un nome di dominio nella barra di ricerca e scegli un nome. Abbiamo usato
`outlinedemo.info` come esempio.

3. Vai alla scheda DNS su Google Domains. In "Record di risorse personalizzati",
digita l'indirizzo IP del tuo server nel campo contrassegnato "Indirizzo IPV4".

4. Vai alla scheda "Impostazioni" del tuo server in Outline Manager. In "Nome host",
digita il nome host che hai acquistato e fai clic su "SALVA". Ciò farà sì che
tutte le future chiavi di accesso utilizzino questo nome host anziché l'indirizzo IP del server.

![Imposta il nome host](/images/set-hostname.png)

## Cambia l'indirizzo IP del server

1. Accedi al tuo server nella pagina "Droplets" di DigitalOcean.

2. Fai clic su "Enable Now" (Abilita ora) in alto a destra nella finestra accanto a "Floating IP" (IP mobile).

![Abilita IP mobile](/images/floating-ip-DO.png)

1. Trova il tuo server nell'elenco delle droplet e fai clic su "Assign Floating IP" (Assegna IP mobile).

![Assegna IP mobile](/images/assign-floating-ip-DO.png)

1. Torna alla scheda DNS su Google Domains.

2. Cambia l'indirizzo IP come prima, ma questa volta con il nuovo indirizzo IP
mobile. L'operazione potrebbe richiedere fino a 48 ore, ma spesso bastano
solo pochi minuti.

3. Vai allo [strumento DNS online di Google](https://toolbox.googleapps.com/apps/dig/#A/)
e inserisci il tuo nome di dominio per vedere quando è avvenuta la modifica nell'ultimo
passaggio.

![Cerca il tuo dominio sullo strumento DNS di Google](/images/google-dns.png)

Una volta propagata questa modifica, i client si connetteranno al nuovo indirizzo IP. Puoi
connetterti al tuo server con una nuova chiave e aprire <https://ipinfo.io> per assicurarti
di vedere il nuovo indirizzo IP del tuo server.

Conclusione
La rotazione degli indirizzi IP di un server Outline può essere un modo rapido per sbloccare un server
e ripristinare il servizio per i client. Per ulteriori domande, commenta il
[post dell'annuncio](https://redd.it/hrbhz4), visita
la [pagina dell'assistenza di Outline](https://support.getoutline.org/) o
[contattaci direttamente](https://support.getoutline.org/s/contactsupport).
