---
title: "Concetti"
sidebar_label: "Concetti"
---

Outline aiuta gli utenti a bypassare le restrizioni per accedere alla rete internet aperta. Ecco alcuni concetti chiave per capire come funziona:

## Fornitori di servizi e utenti finali {#service_providers_and_end_users}

Il sistema Outline coinvolge due ruoli principali: i **fornitori di servizi**, che gestiscono i server, e gli **utenti finali**, che accedono a internet tramite questi server.

- I **fornitori di servizi** creano i server Outline, generano **chiavi di accesso** e **distribuiscono le chiavi** agli utenti finali. Un modo per farlo è mediante l'applicazione **Outline Manager**.

- Gli **utenti finali** installano l'applicazione **client Outline**, incollano la **chiave di accesso** ricevuta e **si connettono** a un tunnel sicuro.

## Chiavi di accesso {#access-keys}

Le chiavi di accesso sono le credenziali che consentono agli utenti di connettersi a un server Outline. Contengono le informazioni necessarie affinché il client Outline stabilisca una connessione sicura. Esistono due tipi di chiavi di accesso:

- Le **chiavi di accesso statiche** codificano tutte le informazioni del server necessarie per connettersi (indirizzo del server, porta, password, metodo di crittografia), impedendo che le informazioni di accesso vengano modificate. Gli utenti incollano questa chiave nel client Outline.

Esempio:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo1UkVmeFRqbHR6Mkw@outline-server.example.com:17178/?outline=1
```

- Le **chiavi di accesso dinamiche** consentono a un fornitore di servizi di ospitare le informazioni di accesso al server in remoto. Ciò consente ai fornitori di aggiornare la configurazione del server (indirizzo del server, porta, password, metodo di crittografia) senza dover riemettere nuove chiavi di accesso per gli utenti finali. Per una documentazione più dettagliata, consulta [Chiavi di accesso dinamiche](vpn/management/dynamic-access-keys).
