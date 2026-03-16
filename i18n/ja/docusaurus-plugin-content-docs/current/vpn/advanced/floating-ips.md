---
title: "フローティング IP を使用してブロック機能回避サーバーを設定する"
sidebar_label: "フローティング IP を使用してブロック機能回避サーバーを設定する"
---

## はじめに {#introduction}

Outline サーバーが検閲の厳しいネットワークで検出され、ブロックされるという問題に遭遇することは多々ありますが、サーバーが正しく設定されていれば、ブロックされても解除は可能であり、それほど難しくもありません。これを行うために、DNS とフローティング IP を使用します。DNS は、ドメイン名（`getoutline.org` など）を物理 IP アドレス（`216.239.36.21` など）に変換するインターネット テクノロジーであり、フローティング IP は、1 つの Outline サーバーに複数の IP アドレスを割り当てることができるクラウド機能です。

## 要件 {#requirements}

このガイドに従うには、低いレベルの技術スキルが必要です。DNS の基本事項を理解していることは役立ちますが、必須ではありません。概要については、ドメイン名の [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name) ガイドをご覧ください。

具体的な例を示すために、DigitalOcean と Google Domains を使用しますが、IP アドレスを割り当てることができるどのクラウド プロバイダ（Google Cloud や [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip) など）でも、またどのドメイン登録事業者（[AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance) など）でも使用できます。

## 手順 {#instructions}

1. 次のリストは、サーバーの IP アドレスをローテーションする手順を要約したものです。

2. ドメイン名を購入します。

3. ドメイン名がサーバーの IP アドレスを指すようにします。

4. ドメイン名を使用してアクセスキーを発行します。

5. フローティング IP をサーバーの Droplet に割り当てます。

6. 新しい IP アドレスを指すようにドメイン名を変更します。

## DigitalOcean 上で Outline サーバーを作成する {#create_an_outline_server_on_digitalocean}

実行中の DigitalOcean サーバーがある場合は、次のステップに進みます。

1. Outline マネージャーを開き、左下の [+] をクリックしてサーバー作成画面を表示します。

2. [DigitalOcean] ボタンで [サーバーを作成] をクリックし、アプリの指示に従います。

![サーバーを作成](/images/create-DO-server.png)

## サーバーのホスト名を指定する {#make_a_hostname_for_your_server}

1. [Google Domains](https://domains.google.com/m/registrar/) に移動し、[最適なドメインを検索] をクリックします。

2. 検索バーにドメイン名を入力し、名前を選択します。例として `outlinedemo.info` を使用しています。

3. Google Domains の [DNS] タブに移動します。[カスタム リソース レコード] で、[IPV4 アドレス] と表示されているフィールドにサーバーの IP アドレスを入力します。

4. Outline マネージャーでサーバーの [設定] タブに移動します。[ホスト名] タブに、購入したホスト名を入力し、[保存] をクリックします。これで、今後のすべてのアクセスキーで、サーバーの IP アドレスではなく、このホスト名が使用されるようになります。

![ホスト名を設定](/images/set-hostname.png)

## サーバーの IP アドレスを変更する {#change_the_servers_ip_address}

1. DigitalOcean の [Droplets] ページでサーバーに移動します。

2. ウィンドウの右上（[Floating IP] の横）の [Enable Now] をクリックします。

![フローティング IP を有効にする](/images/floating-ip-DO.png)

1. Droplets のリストでサーバーを見つけて、[Assign Floating IP] をクリックします。

![フローティング IP を割り当てる](/images/assign-floating-ip-DO.png)

1. Google Domains の [DNS] タブに戻ります。

2. 前と同じように IP アドレスを変更しますが、今回は新しいフローティング IP アドレスを使用します。変更が反映されるまで最大 48 時間かかることもありますが、数分程度しかかからない場合がほとんどです。

3. [Google のオンライン DNS ツール](https://toolbox.googleapps.com/apps/dig/#A/)に移動し、ドメイン名を入力して、前のステップの変更がいつ行われたかを確認します。

![Google DNS ツールでドメインを検索](/images/google-dns.png)

この変更が反映されると、クライアントが新しい IP アドレスに接続します。新しいキーでサーバーに接続し、<https://ipinfo.io> を開いて、サーバーの新しい IP アドレスが表示されていることを確認できます。

まとめ
Outline サーバーの IP アドレスをローテーションすると、すばやくサーバーのブロックを解除し、クライアントへのサービスを復元することができます。ご不明な点については、お気軽に[お知らせの投稿](https://redd.it/hrbhz4)にコメントしてください。また、[Outline のサポート ページ](https://support.getoutline.org/)をご覧になるか、[直接お問い合わせ](https://support.getoutline.org/s/contactsupport)いただくことも可能です。
