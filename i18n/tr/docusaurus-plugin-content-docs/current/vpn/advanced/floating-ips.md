---
title: "Kayan IP'ler ile engellemeye dirençli sunucular oluşturma"
sidebar_label: "Kayan IP'ler ile engellemeye dirençli sunucular oluşturma"
---

## Giriş {#introduction}

Outline sunucuları, yüksek seviyede sansürlenen ağlar tarafından keşfedilip engellenme sorunuyla karşılaşabilir. Düzgün şekilde kurulmuşsa engellenmiş bir sunucuyu çok zorlanmadan kurtarabilirsiniz. Bunun için DNS'i (`getoutline.org` gibi alan adlarını `216.239.36.21` gibi fiziksel IP adreslerine çeviren internet teknolojisi) ve kayan IP'leri (bir Outline sunucusuna birden fazla IP adresi atamanıza olanak tanıyan bulut özelliği) kullanacağız.

## Şartlar {#requirements}

Bu kılavuzdaki talimatlara uymak için düşük seviyede teknik becerinizin olması gerekmektedir. Temel seviyede DNS bilgisi önerilir ama zorunlu değildir. Alan adlarıyla ilgili temel bilgileri edinmek için [MDN](https://developer.mozilla.org/docs/Learn/Common_questions/What_is_a_domain_name) kılavuzunu inceleyin.

Somut örnekler verebilmek için DigitalOcean ve Google Domains'i kullanacağız. Ancak IP adreslerinin atanabildiği herhangi bir bulut sağlayıcı (ör. Google Cloud veya [AWS Lightsail](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/lightsail-create-static-ip)) ve herhangi bir alan kayıt operatörü (ör. [AWS Route 53](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-using-route-53-to-point-a-domain-to-an-instance)) de işe yarayacaktır.

## Talimatlar {#instructions}

1. Aşağıdaki listede, bir sunucunun IP adresini değiştirme adımları özetlenmiştir:

2. Alan adı satın alın.

3. Alan adını sunucumuzun IP adresine yönlendirin.

4. Alan adını kullanarak erişim anahtarları oluşturun.

5. Sunucunun Droplet'ine bir kayan IP atayın.

6. Alan adını yeni IP adresine yönlendirin.

## DigitalOcean'da Outline sunucusu oluşturma {#create_an_outline_server_on_digitalocean}

Çalışan bir DigitalOcean sunucunuz varsa sonraki adıma geçin.

1. Outline Manager'ı açın ve sol alttaki "+" simgesini tıklayarak sunucu oluşturma ekranını açın.

2. "DigitalOcean" bölümündeki "Sunucu oluştur" düğmesini tıklayın ve uygulamadaki talimatları izleyin.

![Sunucu oluştur](/images/create-DO-server.png)

## Sunucunuz için ana makine adı oluşturma {#make_a_hostname_for_your_server}

1. [Google Domains](https://domains.google.com/m/registrar/)'e gidin ve "Mükemmel alanı bul"u tıklayın.

2. Arama çubuğuna bir alan adı yazın ve bir adı seçin. Örnek olarak `outlinedemo.info` adını kullandık.

3. Google Domains'de DNS sekmesine gidin. "Özel kaynak kayıtları" bölümünde, "IPV4 adresi" adlı alana sunucunuzun IP adresini yazın.

4. Outline Manager'da sunucunuzun "Ayarlar" sekmesine gidin. "Ana makine adı" bölümünde, satın aldığınız ana makine adını yazın ve "KAYDET"i tıklayın. Bu sayede, gelecekteki tüm erişim anahtarları, sunucunun IP adresi yerine bu ana makine adını kullanacak.

![Ana makine adını belirleme](/images/set-hostname.png)

## Sunucunun IP adresini değiştirme {#change_the_servers_ip_address}

1. DigitalOcean'ın "Droplets" (Droplet'ler) sayfasında sunucunuza gidin.

2. Pencerenin sağ üst köşesinde, "Floating IP"nin (Kayan IP) yanındaki "Enable Now"ı (Şimdi etkinleştir) tıklayın.

![Kayan IP&#39;yi etkinleştirme](/images/floating-ip-DO.png)

1. Droplet listesinde sunucunuzu bulun ve "Assign Floating IP"yi (Kayan IP ata) tıklayın.

![Kayan IP atama](/images/assign-floating-ip-DO.png)

1. Google Domains'deki DNS sekmesine dönün.

2. Önceden olduğu gibi IP adresini değiştirin ama bu sefer yeni kayan IP adresini kullanın. Etkinleşmesi 48 saati bulabilir ama genellikle yalnızca birkaç dakika sürer.

3. [Google'ın online DNS aracına](https://toolbox.googleapps.com/apps/dig/#A/) gidin ve son adımdaki değişikliğin ne zaman yapıldığını görmek için alan adınızı girin.

![Google DNS aracında alanınızı arama](/images/google-dns.png)

Bu değişiklik uygulandıktan sonra istemciler artık yeni IP adresine bağlanır. Yeni bir anahtarla sunucunuza bağlanabilir ve <https://ipinfo.io> adresinde sunucunuzun yeni IP adresini doğrulayabilirsiniz.

Sonuç
Bir sunucunun engelini kaldırıp tekrar istemcilerin hizmetine açmak için Outline sunucusunun IP adreslerini kolayca değiştirebilirsiniz. Sorularınız varsa [duyuru gönderisine](https://redd.it/hrbhz4) yorum yapabilir, [Outline destek sayfasına](https://support.getoutline.org/) gidebilir veya [doğrudan bizimle iletişime geçebilirsiniz](https://support.getoutline.org/s/contactsupport).
