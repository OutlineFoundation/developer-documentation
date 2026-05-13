---
title: "Deploy Using an AI Agent"
sidebar_label: "Using an AI Agent"
---

# Deploy using an AI Agent

This guide walks you through deploying an Outline Server with the help of an
AI agent (such as Claude Code, Codex, or Gemini CLI) using the experimental
[Outline Skills](https://github.com/OutlineFoundation/outline-skills).

:::warning
Outline Skills is experimental. Use at your own risk and please share feedback
in the project's
[Discussions](https://github.com/OutlineFoundation/outline-skills/discussions).
:::

## Prerequisites

- An AI agent CLI that supports skills, such as
  [Claude Code](https://claude.com/claude-code),
  [Codex](https://github.com/openai/codex), or
  [Gemini CLI](https://github.com/google-gemini/gemini-cli).
- An account with a supported cloud provider (currently
  [DigitalOcean](https://www.digitalocean.com/)).

## Instructions

1. Install Outline Skills in your AI agent.

    ```sh
    npx skills add https://github.com/OutlineFoundation/outline-skills
    ```

1. Start your AI agent and ask it to deploy an Outline server. For example:

    > Deploy an Outline VPN server to DigitalOcean.

1. Follow the agent's prompts. It will ask you for the credentials it needs
   (such as a DigitalOcean API token), confirm the deployment details with
   you, and run the install.

1. Once finished, the agent will provide a management URL you can add to the
   Outline Manager to share access with your users.
