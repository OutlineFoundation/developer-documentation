---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline 使用基于 YAML 的配置来定义 VPN 参数并处理 TCP/UDP 流量。该配置支持多个级别的可组合性，可实现灵活且可扩展的设置。

顶级配置指定了 [TunnelConfig](../reference/access-key-config#tunnelconfig)。

## 示例

典型的 Shadowsocks 配置如下所示：

请注意，我们现在可以让 TCP 和 UDP 在不同的端口或端点上运行，并使用不同的前缀。

您可以使用 YAML 锚标记和 `<<` 合并键来避免重复：

现在可以组合策略并执行多跳：

如果 Shadowsocks 等“隐形”协议被屏蔽，您可以使用 Shadowsocks-over-WebSocket。如需了解如何部署，请参阅[服务器示例配置](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)。客户端配置如下所示：

请注意，WebSocket 端点反过来也可以采用端点，利用端点可绕过基于 DNS 的屏蔽：

为了确保不同 Outline 客户端版本之间的兼容性，应在配置中使用 `first-supported` 选项。随着在 Outline 中添加新的策略和功能，这一点尤为重要，因为并非所有用户都已更新到最新的客户端软件。通过使用 `first-supported`，您可以提供一个可在各种平台和客户端版本中无缝运行的单一配置，从而确保向后兼容性和一致的用户体验。
