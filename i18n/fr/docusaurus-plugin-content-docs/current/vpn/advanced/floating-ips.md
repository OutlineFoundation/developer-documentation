---
title: "Use a Domain Name with Floating IPs"
sidebar_label: "Domain with Floating IPs"
---

## Introduction {#introduction}

Les serveurs Outline peuvent parfois être détectés et bloqués sur des réseaux très censurés. Cependant, s'ils ont été correctement configurés, ils peuvent être récupérés assez facilement. Pour cela, nous utilisons un DNS, une technologie Internet qui traduit les noms de domaine (comme `getoutline.org`) en adresses IP physiques (comme `216.239.36.21`), et des adresses IP flottantes, une fonctionnalité cloud qui vous permet d'attribuer plusieurs adresses IP à un serveur Outline.

## Conditions requises {#requirements}

Seules de simples compétences techniques sont nécessaires pour suivre ce guide. Avoir des connaissances de base sur les DNS est utile, mais n'est pas obligatoire. Consultez le guide [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name) sur les noms de domaine pour en savoir plus.

Nous allons vous présenter un exemple concret en utilisant DigitalOcean et Google Domains. Cependant, vous pouvez tout aussi bien utiliser d'autres fournisseurs de services cloud qui permettent d'attribuer des adresses IP (Google Cloud ou [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip), par exemple) et bureaux d'enregistrement de noms de domaine ([AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance), par exemple).

## Instructions {#instructions}

1. Voici la liste des étapes à suivre pour effectuer une rotation de l'adresse IP d'un serveur :

2. Achetez un nom de domaine.

3. Pointez le nom de domaine vers l'adresse IP de notre serveur.

4. Générez des clés d'accès en utilisant le nom de domaine.

5. Attribuez une adresse IP flottante au Droplet du serveur.

6. Modifiez le nom de domaine pour qu'il pointe vers la nouvelle adresse IP.

## Créer un serveur Outline sur DigitalOcean {#create_an_outline_server_on_digitalocean}

Si vous disposez déjà d'un serveur DigitalOcean opérationnel, passez à l'étape suivante.

1. Ouvrez Outline Manager et cliquez sur + en bas à gauche pour accéder à l'écran de création de serveurs.

2. Cliquez sur le bouton "Créer un serveur" dans la section "DigitalOcean" et suivez les instructions affichées dans l'application.

![Créer un serveur](/images/create-DO-server.png)

## Créer un nom d'hôte pour votre serveur {#make_a_hostname_for_your_server}

1. Accédez à [Google Domains](https://domains.google.com/m/registrar/) et cliquez sur "Trouver le domaine idéal".

2. Saisissez un nom de domaine dans la barre de recherche et sélectionnez celui de votre choix dans la liste. Nous utilisons ici `outlinedemo.info` comme exemple.

3. Dans Google Domains, accédez à l'onglet "DNS". Sous "Enregistrements de ressources personnalisés", saisissez l'adresse IP de votre serveur dans le champ "Adresse IPv4".

4. Dans Outline Manager, accédez à l'onglet "Paramètres" de votre serveur. Dans le champ "Nom d'hôte", saisissez le nom d'hôte que vous avez acheté, puis cliquez sur ENREGISTRER. Toutes les clés d'accès qui seront générées utiliseront maintenant ce nom d'hôte au lieu de l'adresse IP du serveur.

![Définir le nom d&#39;hôte](/images/set-hostname.png)

## Modifier l'adresse IP du serveur {#change_the_servers_ip_address}

1. Accédez à votre serveur sur la page "Droplets" de DigitalOcean.

2. En haut à droite de la fenêtre, cliquez sur "Enable Now" (Activer maintenant) à côté de "Floating IP" (Adresse IP flottante).

![Activer l&#39;adresse IP flottante](/images/floating-ip-DO.png)

1. Recherchez votre serveur dans la liste des Droplets et cliquez sur "Assign Floating IP" (Attribuer une adresse IP flottante).

![Attribuer une adresse IP flottante](/images/assign-floating-ip-DO.png)

1. Revenez à l'onglet "DNS" dans Google Domains.

2. Modifiez l'adresse IP comme précédemment, mais en utilisant cette fois la nouvelle adresse IP flottante. L'application de la modification prend quelques minutes, mais parfois jusqu'à 48 heures.

3. Accédez à l'[outil DNS en ligne de Google](https://toolbox.googleapps.com/apps/dig/#A/) et saisissez votre nom de domaine pour afficher la date à laquelle cette dernière modification a été appliquée.

![Rechercher votre domaine dans l&#39;outil DNS de Google](/images/google-dns.png)

Une fois la modification appliquée, les clients se connectent à la nouvelle adresse IP. Vous pouvez vous connecter à votre serveur avec une nouvelle clé et accéder à <https://ipinfo.io> pour vérifier que la nouvelle adresse IP de votre serveur s'affiche.

ConclusionEn effectuant la rotation des adresses IP d'un serveur Outline, vous pouvez rapidement le débloquer rapidement et rétablir le service pour les clients. Si vous avez d'autres questions, n'hésitez pas à laisser un commentaire sur le [post d'annonce](https://redd.it/hrbhz4), à consulter la [page d'assistance d'Outline](https://support.getoutline.org/) ou à [nous contacter directement](https://support.getoutline.org/s/contactsupport).
