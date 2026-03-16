import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const SUPPORTED_LOCALES = [
  'en', 'ar', 'de', 'es', 'es-419', 'fa', 'fr', 'it', 'ja', 'ko',
  'nl', 'pl', 'pt-BR', 'ru', 'th', 'tr', 'zh-CN', 'zh-TW',
];

function buildLocaleConfigs(): Record<string, {label: string; direction: 'ltr' | 'rtl'}> {
  const configs: Record<string, {label: string; direction: 'ltr' | 'rtl'}> = {};
  for (const locale of SUPPORTED_LOCALES) {
    const label = new Intl.DisplayNames([locale], {type: 'language'}).of(locale) ?? locale;
    const {direction} = (new Intl.Locale(locale) as Intl.Locale & {textInfo: {direction: 'ltr' | 'rtl'}}).textInfo;
    configs[locale] = {label, direction};
  }
  return configs;
}

const config: Config = {
  title: 'Outline Developer Documentation',
  tagline: 'Build tools for internet freedom',
  favicon: 'images/outline-favicon.png',

  future: {
    v4: true,
  },

  url: 'https://developer.getoutline.org',
  baseUrl: '/',

  organizationName: 'OutlineFoundation',
  projectName: 'developer-documentation',
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',

  markdown: {
    format: 'md',
  },

  i18n: {
    defaultLocale: 'en',
    locales: SUPPORTED_LOCALES,
    localeConfigs: buildLocaleConfigs(),
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
          editUrl:
            'https://github.com/OutlineFoundation/developer-documentation/edit/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        gtag: {
          trackingID: 'G-0J7RG8K8MY',
          anonymizeIP: true,
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'images/outline-logo.png',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Outline',
      logo: {
        alt: 'Outline Logo',
        src: 'images/outline-logo.png',
      },
      items: [
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://getoutline.org',
          label: 'Outline',
          position: 'right',
        },
        {
          href: 'https://github.com/OutlineFoundation/?q=outline',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Product Info',
          items: [
            {
              label: 'Download Outline',
              href: 'https://getoutline.org/',
            },
            {
              label: 'Terms of Service',
              href: 'https://s3.amazonaws.com/outline-vpn/static_downloads/Outline-Terms-of-Service.html',
            },
            {
              label: 'Data Collection Policy',
              href: 'https://support.google.com/outline/answer/14915905',
            },
            {
              label: 'Branding Guidelines',
              href: 'https://support.google.com/outline/answer/15331625',
            },
          ],
        },
        {
          title: 'Get Help',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/OutlineFoundation/?q=outline',
            },
            {
              label: 'Reddit',
              href: 'https://www.reddit.com/r/outlinevpn/',
            },
            {
              label: 'Help Center',
              href: 'https://support.getoutline.org/',
            },
            {
              label: 'Contact Us',
              href: 'https://support.getoutline.org/s/contactsupport',
            },
          ],
        },
      ],
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
