---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

Ce document explique comment intégrer le SDK Outline à des applications mobiles et se concentre sur la bibliothèque `MobileProxy` afin de simplifier la gestion des proxys locaux.

`MobileProxy` est une bibliothèque basée sur Go conçue pour simplifier l'intégration de fonctionnalités de proxy dans les applications mobiles. Elle utilise [Go Mobile](https://go.dev/wiki/Mobile) pour générer des bibliothèques mobiles. Vous pouvez ainsi configurer les bibliothèques réseau de vos applications pour acheminer le trafic via un proxy local.

**Application sans MobileProxy**

![Application de contenu sans MobileProxy](/images/mobileproxy-before.png)

**Application avec MobileProxy**

![Application de contenu avec MobileProxy](/images/mobileproxy-after.png)

## Étape 1 : Créer des bibliothèques mobiles MobileProxy

Utilisez [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) pour compiler le code Go en bibliothèques pour Android et iOS.

1. Clonez le dépôt du SDK Outline :

2. Créez les binaires Go Mobile avec [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) :

#### Ajouter la compatibilité Psiphon

Vous pouvez rendre possible l'utilisation du réseau [Psiphon](https://psiphon.ca/) en suivant ces étapes :

    - Contactez l'équipe Psiphon pour obtenir une configuration qui vous donne accès à son réseau. Un contrat peut être nécessaire.

    - Ajoutez la configuration Psiphon reçue à la section `fallback` de votre configuration `SmartDialer`.

    - Créez le MobileProxy à l'aide de l'option `-tags psiphon` :

L'option `-tags psiphon` est nécessaire, car le codebase Psiphon est sous licence GPL, ce qui peut imposer des restrictions de licence à votre propre code. Vous pouvez envisager d'obtenir une licence spéciale auprès de Psiphon.

3. Générez les bibliothèques mobiles et ajoutez-les à votre projet :

### Android

Dans Android Studio, sélectionnez **File > Import Project** (Fichier > Importer un projet) pour importer le bundle `out/mobileproxy.aar` généré. Pour en savoir plus, consultez la section sur [la création et le déploiement sur Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) de la documentation Go Mobile.

### iOS

Faites glisser le bundle `out/mobileproxy.xcframework` dans le projet Xcode. Pour en savoir plus, consultez la section sur [la création et le déploiement sur iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) de la documentation Go Mobile.

## Étape 2 : Exécuter le MobileProxy

Initialisez et lancez le proxy local `MobileProxy` dans l'environnement d'exécution de votre application.
Vous pouvez utiliser une configuration de transport statique ou le Smart Proxy pour sélectionner une stratégie de façon dynamique.

- **Configuration de transport statique** : utilisez la fonction `RunProxy` en incluant une adresse locale et une configuration de transport.

### Android

### iOS

- **Smart Proxy** : le Smart Proxy sélectionne des stratégies DNS et TLS de façon dynamique en fonction des domaines de test spécifiés. Vous devez spécifier la stratégie de configuration au format YAML ([exemple](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## Étape 3 : Configurer les clients HTTP et les bibliothèques réseau

Configurez vos bibliothèques réseau pour qu'elles utilisent l'adresse et le port du proxy local.

### HttpClient Dart/Flutter

Configurez le proxy avec [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

Configurez le proxy avec [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### JVM (Java, Kotlin)

Configurez le proxy avec les [propriétés système](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html) :

### WebView Android

Appliquez une configuration de proxy à toutes les vues Web de votre application avec la bibliothèque [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController) :

### WebView iOS

À partir d'iOS 17, vous pouvez ajouter une configuration de proxy à une `WKWebView` en utilisant sa [propriété `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) :

## Options avancées : générer une bibliothèque mobile personnalisée

Pour les cas d'utilisation avancés, vous pouvez générer vos propres bibliothèques mobiles :

1. **Créez une bibliothèque Go** : créez un package Go réunissant les fonctionnalités de SDK nécessaires.

2. **Générez des bibliothèques mobiles** : utilisez `gomobile bind` pour créer des archives Android (AAR) et des frameworks Apple. Exemples :

    - [Archive Android Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Framework Apple Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Intégrez-les à votre application** : ajoutez les bibliothèques générées à votre application mobile.
