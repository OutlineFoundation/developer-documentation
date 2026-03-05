---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

Ce guide vous explique comment configurer votre environnement Go et utiliser le SDK Outline dans votre code Go.

Nous allons créer un exemple d'application nommée `splitfetch`, qui présente une fonctionnalité du SDK. Cette application récupère une page Web, mais au lieu d'envoyer la requête en un seul paquet réseau, **elle se sert du SDK Outline pour diviser le flux TCP initial en deux paquets distincts**. Cela peut permettre de contourner certaines formes d'interventions sur le réseau.

Vous pouvez exécuter l'application sur **Linux, Mac et Windows**.
Pour intégrer le SDK à des applications mobiles, consultez la page [Ajouter le SDK Outline à votre application mobile](mobile-app-integration).

## Étape 1 : Configurer Go

Tout d'abord, vous avez besoin du [langage de programmation Go](https://go.dev/).
Si vous avez déjà installé Go (version 1.21 ou ultérieure), vous pouvez passer à l'étape suivante.

Pour installer Go, vous pouvez suivre le [guide officiel](https://go.dev/doc/install) ou procéder comme suit si vous utilisez un gestionnaire de paquets :

### Linux

Suivez les étapes figurant sur [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### Mac

### Windows

Une fois l'installation terminée, vous pouvez vérifier que Go est bien installé en exécutant la commande suivante dans un terminal :

## Étape 2 : Créer l'application `splitfetch`

Pour configurer le projet `splitfetch`, commencez par créer le répertoire du projet et initialiser un module Go :

Ensuite, ajoutez le SDK Outline et créez votre fichier `main.go` :

## Étape 3 : Utiliser le SDK Outline dans l'application

Ouvrez le fichier `main.go` dans l'éditeur de code de votre choix et collez-y le code ci-dessous. Ce code contient toute la logique pour notre application `splitfetch`.

Une fois le code enregistré, exécutez la commande suivante dans votre terminal pour vous assurer que le fichier `go.mod` a bien été mis à jour.

## Étape 4 : Exécuter l'application

Maintenant que le code est prêt, vous pouvez exécuter l'application `splitfetch`.

Depuis le répertoire `splitfetch`, exécutez la commande suivante dans votre terminal, en utilisant une URL comme argument :

Cette commande compile et exécute l'application, en affichant le contenu HTML de la page Web.

Si vous souhaitez créer et partager un programme autonome exécutable sans `go`, utilisez la commande `go build` :

### Linux et Mac

### Windows

Une fois la compilation terminée, vous pouvez partager et exécuter votre application.
Par exemple :
