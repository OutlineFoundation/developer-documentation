---
title: "Share Management Access"
sidebar_label: "Share Management Access"
---

Man mano che il tuo servizio Outline si espande, può essere necessario delegare le responsabilità di gestione ad altre persone fidate. Questo documento illustra i vari metodi disponibili per condividere l'accesso in gestione con altre persone.

Il metodo da usare per condividere l'accesso in gestione varia in base al modo in cui è stato eseguito il deployment iniziale del server Outline.

## Distribuzioni in provider cloud

Per i server Outline distribuiti su piattaforme cloud, come DigitalOcean, AWS o Google Cloud, l'accesso in gestione viene in genere amministrato attraverso le funzionalità integrate di gestione di identità e accessi (IAM) del provider, che offrono un approccio più sicuro e controllato rispetto alla condivisione manuale della configurazione.

### DigitalOcean

DigitalOcean offre una valida funzionalità per i **team ** che consente di invitare altri utenti di DigitalOcean a collaborare ai tuoi progetti. Questo è il modo consigliato per concedere l'accesso in gestione al tuo server Outline ospitato sulla piattaforma DigitalOcean.

#### 1. Concedi l'accesso al team

Il modo più efficiente per condividere la gestione del tuo server Outline ospitato su DigitalOcean è utilizzare la funzionalità **Teams** della piattaforma.

- Accedi al tuo account DigitalOcean.

- Vai alla sezione **Teams**.

- Crea un nuovo team (se non l'hai già fatto) o invita utenti di DigitalOcean esistenti nel tuo team.

- Puoi assegnare ai membri che inviti nel team ruoli precisi e concedergli l'accesso a risorse specifiche, comprese le droplet che eseguono Outline.

#### 2. Controlla le autorizzazioni

Valuta con attenzione le autorizzazioni da concedere ai membri del team. Per gestire il server Outline puoi concedere l'accesso in lettura e scrittura alla specifica droplet. Questo consentirà ai membri di:

- Visualizzare i dettagli della droplet (indirizzo IP, stato e così via).

- Accedere alla console della droplet (se necessario per la risoluzione dei problemi).

- Potenzialmente, eseguire azioni come il riavvio della droplet (a seconda delle autorizzazioni concesse).

A questo punto gli utenti che collegano Outline Manager al proprio account DigitalOcean saranno in grado di visualizzare e gestire tutti i server Outline collegati a quell'account.

## Installazioni manuali

Per chi ha installato manualmente Outline sul proprio server utilizzando lo [script di installazione](../getting-started/server-setup-advanced), il metodo principale per concedere l'accesso in gestione consiste nel condividere la **configurazione di accesso**.

L'applicazione Outline Manager ha bisogno di una specifica stringa di configurazione per eseguire la connessione a un server Outline e gestirlo. Questa stringa di configurazione contiene tutte le informazioni necessarie, tra cui l'indirizzo del server, la porta e una chiave segreta per l'autenticazione.

### 1. Individua il file `access.txt`

Sul server in cui è installato Outline, vai alla directory di Outline. La posizione esatta può variare leggermente in base al metodo di installazione, ma le posizioni comuni sono:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Nel volume Docker usato dal contenitore del server Outline

### 2. Recupera la configurazione di accesso

Dopo aver trovato il file `access.txt`, convertilo in JSON, il formato previsto da Outline Manager nel passaggio successivo.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

L'output conterrà il fingerprint del certificato autofirmato (`certSha256`) e l'endpoint dell'API di gestione sul server (`apiUrl`):

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```

### 3. Condividi la configurazione di accesso in modo sicuro

Copia l'output e condividilo in modo sicuro con il nuovo gestore di Outline. Evita di inviarlo tramite canali non crittografati, ad esempio email in testo normale o messaggistica immediata.
Valuta la possibilità di utilizzare la funzionalità di condivisione sicura di un gestore delle password o un altro metodo di comunicazione crittografato.

Una volta incollata la **configurazione di accesso** fornita in Outline Manager, il nuovo gestore potrà aggiungere e successivamente gestire il server Outline attraverso l'interfaccia dell'applicazione. Ulteriore assistenza per l'utilizzo di Outline Manager è disponibile nel [Centro assistenza Outline](https://support.google.com/outline).
