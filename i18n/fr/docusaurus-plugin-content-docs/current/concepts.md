---
title: "Concepts"
sidebar_label: "Concepts"
---

Outline permet aux utilisateurs de contourner les restrictions d'accès à Internet. Voici quelques concepts clés à connaître pour comprendre son fonctionnement :

## Fournisseurs de services et utilisateurs finaux

Le système Outline implique deux rôles principaux : des **fournisseurs de services**, qui gèrent les serveurs, et des **utilisateurs finaux**, qui accèdent à Internet par le biais de ces serveurs.

- Les **fournisseurs de services** créent les serveurs Outline, génèrent les **clés d'accès** et **distribuent ces clés** aux utilisateurs finaux. Pour cela, ils peuvent par exemple utiliser l'application **Outline Manager**.

- Les **utilisateurs finaux** installent l'application du **client Outline**, collent dans celle-ci la **clé d'accès** qu'ils ont reçue, puis **se connectent** à un tunnel sécurisé.

## Clés d'accès

Les clés d'accès sont des identifiants grâce auxquels les utilisateurs peuvent se connecter à un serveur Outline. Elles contiennent les informations permettant au client Outline d'établir une connexion sécurisée. Il existe deux types de clés d'accès :

- Les **clés d'accès statiques** qui encodent les informations concernant le serveur nécessaires pour se connecter (adresse du serveur, port, mot de passe, méthode de chiffrement), ce qui empêche la modification des informations d'accès. Les utilisateurs collent cette clé dans le client Outline.

Exemple :

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo1UkVmeFRqbHR6Mkw@outline-server.example.com:17178/?outline=1
```

- Les **clés d'accès dynamiques** qui permettent à un fournisseur de services d'héberger à distance les informations d'accès au serveur. Les fournisseurs peuvent ainsi modifier la configuration de leur serveur (adresse du serveur, port, mots de passe, méthode de chiffrement) sans avoir à distribuer de nouvelles clés d'accès aux utilisateurs finaux. Pour accéder à une documentation plus détaillée, consultez [Clés d'accès dynamiques](vpn/management/dynamic-access-keys).
