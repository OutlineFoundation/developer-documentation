---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline, VPN parametrelerini tanımlamak ve TCP/UDP trafiğini işlemek için YAML tabanlı bir yapılandırma kullanır. Yapılandırma, birden fazla düzeyde birleştirilebilirliği destekler. Böylece esnek ve genişletilebilir kurumlara olanak tanır.

Üst düzey yapılandırmada [TunnelConfig](../reference/access-key-config#tunnelconfig) kullanılır.

## Örnekler

Standart bir Shadowsocks yapılandırması şöyle olur:

TCP ve UDP'nin artık farklı bağlantı noktalarında veya uç noktalarda ve farklı öneklerle nasıl çalıştığına dikkat edin.

Yinelemeyi önlemek için YAML anchor'larını ve `<<` birleştirme anahtarını kullanabilirsiniz:

Artık strateji oluşturabilir ve birden çok aşamalı işlemler yapabilirsiniz:

Shadowsocks gibi trafiği değiştiren protokollerin engellenmesi durumunda, Shadowsocks-over-Websockets kullanabilirsiniz. Nasıl dağıtılacağına ilişkin [sunucu örneği](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml) yapılandırmasına bakın. Bir istemci yapılandırması şöyle olur:

Websocket uç noktasının da bir uç noktaya bağlanabileceğini unutmayın. Bu yöntem, DNS tabanlı engellemeyi atlamak için kullanılabilir:

Farklı Outline istemci sürümleri arasında uyumluluğu sağlamak için yapılandırmanızda `first-supported` seçeneğini kullanın. Bu yöntem, kullanıcıların tamamı en yeni istemci yazılımına güncelleme yapmamış olabileceğinden, Outline'a yeni stratejiler ve özellikler eklendikçe özellikle önemlidir. `first-supported` kullanarak, çeşitli platformlarda ve istemci sürümlerinde sorunsuz bir şekilde çalışan tek bir yapılandırma sunabilirsiniz. Böylece geriye dönük uyumluluk ve tutarlı bir kullanıcı deneyimi sağlayabilirsiniz.
