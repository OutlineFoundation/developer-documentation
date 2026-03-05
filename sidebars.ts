import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'why-outline',
    'concepts',
    {
      type: 'category',
      label: 'Outline VPN',
      items: [
        {
          type: 'category',
          label: 'Get Started',
          items: [
            'vpn/getting-started/server-setup-manager',
            'vpn/getting-started/server-setup-advanced',
            'vpn/getting-started/share-access',
          ],
        },
        {
          type: 'category',
          label: 'Manage & Scale',
          items: [
            'vpn/management/share-management-access',
            'vpn/management/dynamic-access-keys',
            'vpn/management/config',
            'vpn/management/metrics',
          ],
        },
        {
          type: 'category',
          label: 'Resilience Against Blocking',
          items: [
            'vpn/advanced/floating-ips',
            'vpn/advanced/prefixing',
            'vpn/advanced/websockets',
          ],
        },
        {
          type: 'category',
          label: 'Advanced Deployments',
          items: [
            'vpn/advanced/caddy',
          ],
        },
        {
          type: 'category',
          label: 'Reference',
          items: [
            'vpn/reference/access-key-config',
            {
              type: 'link',
              label: 'Management API',
              href: 'https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/shadowbox/server/api.yml',
            },
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Outline SDK',
      items: [
        {
          type: 'category',
          label: 'Discover',
          items: [
            'sdk/what-is-the-sdk',
            'sdk/concepts',
          ],
        },
        {
          type: 'category',
          label: 'Integrate',
          items: [
            'sdk/mobile-app-integration',
            'sdk/use-sdk-in-go',
          ],
        },
        {
          type: 'category',
          label: 'Tools',
          items: [
            'sdk/command-line-debugging',
          ],
        },
        {
          type: 'category',
          label: 'Reference',
          items: [
            'sdk/reference/smart-dialer-config',
            {
              type: 'link',
              label: 'Go API Reference',
              href: 'https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk',
            },
          ],
        },
      ],
    },
    'download-links',
  ],
};

export default sidebars;
