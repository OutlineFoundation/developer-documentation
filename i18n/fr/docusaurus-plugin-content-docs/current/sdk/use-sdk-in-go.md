---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

Ce guide vous explique comment configurer votre environnement Go et utiliser le SDK Outline dans votre code Go.

Nous allons créer un exemple d'application nommée `splitfetch`, qui présente une fonctionnalité du SDK. Cette application récupère une page Web, mais au lieu d'envoyer la requête en un seul paquet réseau, **elle se sert du SDK Outline pour diviser le flux TCP initial en deux paquets distincts**. Cela peut permettre de contourner certaines formes d'interventions sur le réseau.

Vous pouvez exécuter l'application sur **Linux, Mac et Windows**.
Pour intégrer le SDK à des applications mobiles, consultez la page [Ajouter le SDK Outline à votre application mobile](mobile-app-integration).

## Étape 1 : Configurer Go {#step_1_set_up_go}

Tout d'abord, vous avez besoin du [langage de programmation Go](https://go.dev/).
Si vous avez déjà installé Go (version 1.21 ou ultérieure), vous pouvez passer à l'étape suivante.

Pour installer Go, vous pouvez suivre le [guide officiel](https://go.dev/doc/install) ou procéder comme suit si vous utilisez un gestionnaire de paquets :

### Linux {#linux}

Suivez les étapes figurant sur [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu).

### Mac {#mac}

```sh
brew install go
```

### Windows {#windows}

```powershell
winget install --id=GoLang.Go  -e
```

Une fois l'installation terminée, vous pouvez vérifier que Go est bien installé en exécutant la commande suivante dans un terminal :

```sh
go version
```

## Étape 2 : Créer l'application `splitfetch` {#step_2_create_the_splitfetch_application}

Pour configurer le projet `splitfetch`, commencez par créer le répertoire du projet et initialiser un module Go :

```sh
mkdir splitfetch
cd splitfetch
go mod init example/splitfetch
```

Ensuite, ajoutez le SDK Outline et créez votre fichier `main.go` :

```sh
go get github.com/OutlineFoundation/outline-sdk@latest
touch main.go
```

## Étape 3 : Utiliser le SDK Outline dans l'application {#step_3_use_outline_sdk_in_the_application}

Ouvrez le fichier `main.go` dans l'éditeur de code de votre choix et collez-y le code ci-dessous. Ce code contient toute la logique pour notre application `splitfetch`.

```go
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"os"

	"github.com/OutlineFoundation/outline-sdk/transport"
	"github.com/OutlineFoundation/outline-sdk/transport/split"
)

// The number of bytes to send in the first packet.
const splitPacketSize = 3

func main() {
	// 1. Get the URL from the command-line arguments.
	if len(os.Args) < 2 {
		log.Fatalf("Usage: %s <URL>", os.Args[0])
	}
	url := os.Args[1]

	// 2. Create a split dialer from the Outline SDK.
	// This dialer wraps a standard TCP dialer to add the splitting behavior.
	dialer, err := split.NewStreamDialer(&transport.TCPDialer{}, split.NewFixedSplitIterator(splitPacketSize))
	if err != nil {
		log.Fatalf("Failed to create split dialer: %v", err)
	}

	// 3. Configure an HTTP client to use our custom split dialer for TCP connections.
	httpClient := &http.Client{
		Transport: &http.Transport{
			DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
				return dialer.DialStream(ctx, addr)
			},
		},
	}

	// 4. Use the custom client to make the HTTP GET request.
	resp, err := httpClient.Get(url)
	if err != nil {
		log.Fatalf("HTTP request failed: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Failed to read response body: %v", err)
	}
	fmt.Println(string(body))
}
```

Une fois le code enregistré, exécutez la commande suivante dans votre terminal pour vous assurer que le fichier `go.mod` a bien été mis à jour.

```sh
go mod tidy
```

## Étape 4 : Exécuter l'application {#step_4_run_the_application}

Maintenant que le code est prêt, vous pouvez exécuter l'application `splitfetch`.

Depuis le répertoire `splitfetch`, exécutez la commande suivante dans votre terminal, en utilisant une URL comme argument :

```sh
go run . https://getoutline.org
```

Cette commande compile et exécute l'application, en affichant le contenu HTML de la page Web.

Si vous souhaitez créer et partager un programme autonome exécutable sans `go`, utilisez la commande `go build` :

### Linux et Mac {#linux-mac}

```sh
go build -o splitfetch .
```

### Windows {#windows_1}

```sh
go build -o splitfetch.exe .
```

Une fois la compilation terminée, vous pouvez partager et exécuter votre application.
Par exemple :

```sh
./splitfetch https://getoutline.org
```
