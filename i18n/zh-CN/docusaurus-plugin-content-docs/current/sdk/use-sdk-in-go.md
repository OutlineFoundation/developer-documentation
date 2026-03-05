---
title: "Add Outline SDK to Your Go Code"
sidebar_label: "Go Integration"
---

本指南详细介绍了如何设置 Go 环境以及在 Go 代码中使用 Outline SDK。

我们将创建一个名为 `splitfetch` 的示例应用以展示 SDK 的一项功能。此应用会提取一个网页，然后**使用 Outline SDK 将初始 TCP 数据流拆分成两个独立的数据包**，而非以单个网络数据包发送请求。这有助于绕过某些形式的网络干预。

您可以在 **Linux、Mac 和 Windows** 上运行此应用。如需与移动应用集成，请参阅[将 Outline SDK 添加到移动应用](mobile-app-integration)。

## 第 1 步：设置 Go

首先，您需要使用 [Go 编程语言](https://go.dev/)。如果您已安装 Go（1.21 或更高版本），可以跳到下一步。

安装时，您可以按照[官方指南](https://go.dev/doc/install)操作，或者，如果您使用的是软件包管理系统，可以按照以下说明操作：

### Linux

按照 [Go Wiki: Ubuntu](https://go.dev/wiki/Ubuntu) 中的步骤操作。

### Mac

### Windows

Go 安装完成后，您可以在终端运行以下命令来验证是否已正确安装：

## 第 2 步：创建 `splitfetch` 应用

创建 `splitfetch` 项目。首先，创建项目目录并初始化 Go 模块：

接下来，添加 Outline SDK 并创建 `main.go` 文件：

## 第 3 步：在应用中使用 Outline SDK

在您常用的代码编辑器中打开 `main.go` 文件，然后粘贴以下代码。此代码包含 `splitfetch` 应用所需的所有逻辑。

保存代码后，在终端运行以下命令，确保 `go.mod` 文件已正确更新。

## 第 4 步：运行应用

代码编写完成后便可以运行 `splitfetch` 应用。

在终端中进入 `splitfetch` 目录，运行以下命令，将网址作为参数进行传递：

此命令将编译并运行应用，从而显示网页的 HTML 内容。

如果您想创建并发布一个无需 `go` 即可运行的独立程序，请使用 `go build` 命令：

### Linux 和 Mac

### Windows

构建完成后，您便可以发布和运行应用。例如：
