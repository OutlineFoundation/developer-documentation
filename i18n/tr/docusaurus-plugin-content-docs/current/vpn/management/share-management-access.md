---
title: "Share Management Access"
sidebar_label: "Share Management Access"
---

Outline hizmetiniz büyüdükçe, yönetim sorumluluklarını diğer güvenilir kişilere devretmeniz gerekebilir. Bu belgede, yönetici erişimini diğer yöneticilerle paylaşmak için kullanılabilecek çeşitli yöntemler açıklanmaktadır.

Yönetim erişimini paylaşma yöntemi, Outline sunucunuzun ilk dağıtım şekline göre farklılık gösterir.

## Bulut sağlayıcı dağıtımları {#cloud_provider_deployments}

DigitalOcean, AWS veya Google Cloud gibi bulut platformlarına dağıtılan Outline sunucuları için yönetim erişimi genellikle sağlayıcının entegre kimlik ve erişim yönetimi (IAM) özellikleri aracılığıyla yönetilir. Bu yöntem, manuel yapılandırma paylaşımına kıyasla daha güvenli ve kontrollü bir yaklaşım sağlar.

### DigitalOcean {#digitalocean}

DigitalOcean'da, diğer DigitalOcean kullanıcılarını projelerinizde birlikte çalışmaya davet etmenizi sağlayan güçlü bir **Teams** (Ekipler) özelliği bulunur. DigitalOcean platformunda barındırılan Outline sunucunuza erişim yönetimi vermek için bu yöntemi kullanmanız önerilir.

#### 1. Ekibe erişim izni verme {#1_grant_team_access}

DigitalOcean'da barındırılan Outline sunucunuzun yönetimini paylaşmak için en etkili yöntem, DigitalOcean'da bulunan **Teams** (Ekipler) özelliğidir.

- DigitalOcean hesabınızda oturum açın.

- **Teams** (Ekipler) bölümüne gidin.

- Henüz oluşturmadıysanız bir ekip oluşturun veya mevcut DigitalOcean kullanıcılarınızı ekibinizin üyesi olmaları için davet edin.

- Üyeleri davet ederken her birine belirli bir rol atayabilir ve Outline'ı çalıştıran droplet'leriniz gibi belirli kaynaklara erişim izni verebilirsiniz.

#### 2. Denetim izinleri {#2_control_permissions}

Ekip üyelerine vereceğiniz izinleri dikkatle değerlendirin. Outline sunucusunun yönetimi için üyelere ilgili droplet için "Okuma" ve "Yazma" izni verebilirsiniz. Bu sayede şunları yapabilirler:

- Droplet'in ayrıntılarını (IP adresi, durum vb.) görüntüleme

- Droplet'in konsoluna erişme (sorun giderme amacıyla gerekirse)

- Droplet'i yeniden başlatma gibi işlemleri (verilen izne bağlı olarak) gerçekleştirme

Outline Manager'ı DigitalOcean hesaplarına bağlayan kullanıcılar artık bu hesaba bağlı tüm Outline sunucularını görüntüleyip yönetebilir.

## Manuel yüklemeler {#manual_installations}

Outline'ı [yükleme komut dosyasını](../getting-started/server-setup-advanced) kullanarak kendi sunucunuza manuel olarak yüklediyseniz yönetim erişimi vermek için kullanılması gereken birincil yöntem **erişim yapılandırmasını** paylaşmaktır.

Outline Manager uygulamasının Outline sunucularına bağlanmak ve bu sunucuları yönetmek için özel bir yapılandırma dizesi gerekir. Bu onay dizesinde sunucu adresi, bağlantı noktası ve kimlik doğrulama için gizli anahtar gibi gerekli tüm bilgiler yer alır.

### 1. `access.txt` dosyasını bulma {#1_locate_the_accesstxt_file}

Outline'ın yüklü olduğu sunucuda Outline dizinine gidin. Dizinin konumu yükleme yönteminize göre biraz farklılık gösterebilir ancak genellikle şu gibi konumlarda bulunur:

- `/opt/outline/access.txt`

- `/etc/outline/access.txt`

- Outline sunucu kapsayıcısının kullandığı Docker birimi

### 2. Erişim yapılandırmasını alma {#2_retrieve_the_access_config}

`access.txt` dosyasını bulduğunuzda dosyayı JSON'a dönüştürün. Outline Manager bir sonraki adımda bu biçimi bekler.

```sh
sed -n '2s/^apiUrl://p; 1s/^certSha256://p' /opt/outline/access.txt | paste -d'\n' -s | sed 'H;1h;$!d;x;s/\n/", \"apiUrl\": \"/g; s/^/{"certSha256": \"/; s/$/\"}/'
```

Çıkışta kendinden imzalı sertifika parmak izi (`certSha256`) ve sunucudaki yönetim API'sinin uç noktası (`apiUrl`) bulunur:

```json
{"certSha256": "1DCC18CC9F6C34EBBB639255F4D1BC6984C2F6A47B15F7A49AA8AFB69B7E4DDE", "apiUrl": "https://1.1.1.1:12345/Fw-CkWFNSN7Ml8LLM8Pduw"}
```

### 3. Erişim yapılandırmasını güvenle paylaşma {#3_share_the_access_config_securely}

Çıkışı kopyalayıp yeni Outline yöneticisi ile güvenli bir şekilde paylaşın. Düz e-posta veya anlık mesajlaşma uygulamaları gibi şifrelenmemiş kanallardan göndermeyin.
Parola yöneticilerinin güvenli paylaşma özelliklerini veya başka bir şifrelenmiş iletişim yöntemi kullanabilirsiniz.

Sağlanan **erişim kodu** Outline Manager'a yapıştırıldığında, yeni yönetici Outline sunucusunu ekleyip uygulama arayüzünden yönetebilir. Outline Manager'ı kullanma hakkında daha fazla bilgiye [Outline Yardım Merkezi](https://support.google.com/outline)'nden ulaşılabilir.
