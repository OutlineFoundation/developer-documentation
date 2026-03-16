---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Com o [Prometheus](https://prometheus.io/), o Outline mostra métricas de performance
detalhadas para você ter insights melhores sobre
o uso e a integridade do seu servidor. Este guia vai acompanhar você ao longo do processo de
recuperação e visualização dessas métricas.

**Observação importante**: este guia pressupõe que você tem noções básicas sobre o
Prometheus e o PromQL. Se você não tiver familiaridade com o Prometheus,
leia a documentação e assista aos tutoriais antes de se aprofundar nas métricas do Outline.

## Pré-requisitos {#prerequisites}

- **Servidor do Outline com o Prometheus ativado**: verifique se as métricas do Prometheus
estão ativadas no servidor do Outline. Essa geralmente é a configuração padrão.

- **Acesso SSH ao servidor**: você precisará de acesso SSH para encaminhar a
porta do Prometheus.

## Instruções {#instructions}

1. **Encaminhar a porta do Prometheus**

Conecte-se ao seu servidor usando SSH e encaminhe a porta 9090:

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **Acessar a interface da Web do Prometheus**

Abra o navegador da Web e acesse: <http://localhost:9090/graph>. 
Consultar as métricas do Prometheus

3. **Use as consultas PromQL para ver as métricas que você quiser.**

### Exemplo de consultas PromQL {#example_promql_queries}

#### Uso {#usage}

- **Bytes de dados (por chave de acesso, protocolo e rotas)**:

`increase(shadowsocks_data_bytes[1d])`

- **Bytes de dados (agregados por chave de acesso)**:

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Bytes de dados (para o cálculo dos limites de dados)**:

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Bytes de dados (por local, protocolo e rotas)**:

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Chaves de acesso ativas {#active_access_keys}

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### Conexões TCP {#tcp_connections}

- **Conexões TCP (por chave de acesso, local e status)**:

`increase(shadowsocks_tcp_connections_closed[1d])`

- **Conexões TCP (por local)**:

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP {#udp}

- **Pacotes UDP (por local e status)**:

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **Associações UDP (sem detalhamento)**:

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Performance {#performance}

- **Uso da CPU (por processo)**:

`rate(process_cpu_seconds_total[10m])`

- **Memória (por processo)**:

`process_virtual_memory_bytes`

#### Informações sobre a versão {#build_information}

- **Prometheus**:

`prometheus_build_info`

- **outline-ss-server**:

`shadowsocks_build_info`

- **Node.js**:

`nodejs_version_info`

A lista completa das métricas está disponível no
[código-fonte](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) `outline-ss-server`.
