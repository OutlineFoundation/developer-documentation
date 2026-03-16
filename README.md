# Outline Developer Documentation

Developer documentation for [Outline](https://getoutline.org), built with [Docusaurus](https://docusaurus.io/).

Live site: https://developer.getoutline.org

## Prerequisites

- [Node.js](https://nodejs.org/) >= 20

## Getting Started

Install dependencies:

```sh
npm install
```

Start the local development server (English only):

```sh
npm start
```

This opens `http://localhost:3000` with hot-reloading enabled.

To start the dev server in a specific locale:

```sh
npm start -- --locale ru
```

## Building

Build the site for all locales:

```sh
npm run build
```

Build for a single locale (much faster, useful for testing):

```sh
npm run build -- --locale en
```

Preview the production build locally:

```sh
npm run serve
```

## Deployment

The site deploys to GitHub Pages via:

```sh
npm run deploy
```

This builds all 18 locales and pushes to the `gh-pages` branch, which is served at https://developer.getoutline.org.