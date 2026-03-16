---
title: "Share Management Access"
sidebar_label: "Share Management Access"
---

À mesure que votre service Outline se développe, vous pouvez être amené à déléguer certaines tâches de gestion à des personnes de confiance. Ce document présente les diverses méthodes disponibles pour partager l'accès aux fonctionnalités de gestion avec d'autres administrateurs.

La méthode à utiliser dépendra de la façon dont votre serveur Outline a été initialement déployé.

## Déploiements via des fournisseurs de services cloud {#cloud_provider_deployments}

Pour les serveurs Outline déployés sur des plates-formes cloud comme DigitalOcean, AWS ou Google Cloud, l'accès aux fonctionnalités de gestion est généralement géré dans la solution de gestion de l'authentification et des accès (IAM) du fournisseur de services cloud. Cette approche vous offre davantage de contrôle et de sécurité que le partage manuel de la configuration.

### DigitalOcean {#digitalocean}

DigitalOcean propose une fonctionnalité **Teams** performante qui vous permet d'inviter d'autres utilisateurs DigitalOcean à collaborer sur vos projets. Nous vous recommandons d'utiliser cette méthode pour autoriser d'autres personnes à gérer votre serveur Outline hébergé sur cette plate-forme.

#### 1. Accorder l'accès à une équipe {#1_grant_team_access}

Le moyen le plus efficace de partager la gestion de votre serveur Outline hébergé sur DigitalOcean est d'utiliser la fonctionnalité **Teams** de la plate-forme.

- Connectez-vous à votre compte DigitalOcean.

- Accédez à la section **Teams** (Équipes).

- Créez une équipe (si ce n'est pas déjà fait) ou invitez d'autres utilisateurs DigitalOcean existants à rejoindre votre équipe.

- Lorsque vous invitez des membres, vous pouvez leur attribuer des rôles particuliers et leur accorder l'accès à des ressources précises, y compris les droplets qui exécutent Outline.

#### 2. Définir les autorisations {#2_control_permissions}

Réfléchissez bien aux autorisations que vous accordez aux membres de l'équipe. Pour la gestion du serveur Outline, vous pourriez leur accorder un accès en lecture et en écriture aux droplets concernés. Ainsi, ils pourront :

- consulter les informations sur le droplet (adresse IP, état, etc.) ;

- accéder à la console du droplet (si nécessaire pour résoudre des problèmes) ;

- éventuellement effectuer des actions comme redémarrer le droplet (en fonction des autorisations accordées).

Les utilisateurs qui connectent Outline Manager à leur compte DigitalOcean pourront désormais consulter et gérer tous les serveurs Outline associés à ce compte.

## Installations manuelles {#manual_installations}

Lorsque vous avez installé Outline manuellement sur vos propres serveurs à l'aide du [script d'installation](../getting-started/server-setup-advanced), la principale méthode pour accorder l'accès aux fonctionnalités de gestion est de partager la **configuration d'accès**.

L'application Outline Manager a besoin d'une chaîne de configuration spécifique pour se connecter à un serveur Outline et le gérer. Cette chaîne de configuration contient toutes les informations nécessaires, dont l'adresse du serveur, le port et une clé secrète pour l'authentification.

### 1. Trouver le fichier `access.txt` {#1_locate_the_accesstxt_file}

Sur le serveur où Outline est installé, accédez au répertoire Outline. L'emplacement exact du fichier peut varier légèrement selon la méthode d'installation utilisée, mais voici quelques emplacements courants :

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Dans le volume Docker utilisé par le conteneur du serveur Outline

### 2. Récupérer la configuration d'accès {#2_retrieve_the_access_config}

Lorsque vous avez trouvé le fichier `access.txt`, convertissez-le en JSON. Il s'agit du format attendu par Outline Manager à l'étape suivante.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

Le résultat contient l'empreinte du certificat autosigné (`certSha256`) et le point de terminaison de l'API de gestion sur le serveur (`apiUrl`) :

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```

### 3. Partager la configuration d'accès de façon sécurisée {#3_share_the_access_config_securely}

Copiez la sortie et partagez-la avec le nouvel administrateur Outline de façon sécurisée. Évitez de l'envoyer par le biais de canaux non chiffrés comme un simple e-mail ou message instantané.
Privilégiez la fonctionnalité de partage sécurisé d'un gestionnaire de mots de passe ou une autre méthode de communication chiffrée.

Le nouvel administrateur colle la **configuration d'accès** fournie dans Outline Manager afin d'ajouter le serveur Outline et de pouvoir le gérer dans l'interface de l'application. Pour en savoir plus sur l'utilisation d'Outline Manager, consultez le [Centre d'aide Outline](https://support.google.com/outline).
