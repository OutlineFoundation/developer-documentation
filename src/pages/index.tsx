import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';

// Import all locale translations for the landing page.
const allTranslations: Record<string, Record<string, string>> = {
  en: require('@site/i18n/en/landingpage.json'),
  ar: require('@site/i18n/ar/landingpage.json'),
  de: require('@site/i18n/de/landingpage.json'),
  es: require('@site/i18n/es/landingpage.json'),
  'es-419': require('@site/i18n/es-419/landingpage.json'),
  fa: require('@site/i18n/fa/landingpage.json'),
  fr: require('@site/i18n/fr/landingpage.json'),
  it: require('@site/i18n/it/landingpage.json'),
  ja: require('@site/i18n/ja/landingpage.json'),
  ko: require('@site/i18n/ko/landingpage.json'),
  nl: require('@site/i18n/nl/landingpage.json'),
  pl: require('@site/i18n/pl/landingpage.json'),
  'pt-BR': require('@site/i18n/pt-BR/landingpage.json'),
  ru: require('@site/i18n/ru/landingpage.json'),
  th: require('@site/i18n/th/landingpage.json'),
  tr: require('@site/i18n/tr/landingpage.json'),
  'zh-CN': require('@site/i18n/zh-CN/landingpage.json'),
  'zh-TW': require('@site/i18n/zh-TW/landingpage.json'),
};

function useTranslations(): Record<string, string> {
  const {i18n: {currentLocale}} = useDocusaurusContext();
  return allTranslations[currentLocale] ?? allTranslations.en;
}

function Hero(): JSX.Element {
  const t = useTranslations();
  return (
    <header className={styles.hero}>
      <div className={styles.heroInner}>
        <h1 className={styles.heroTitle}>{t['hero.title']}</h1>
        <p className={styles.heroSubtitle}>{t['hero.subtitle']}</p>
      </div>
    </header>
  );
}

function Cards(): JSX.Element {
  const t = useTranslations();
  return (
    <section className={styles.cards}>
      <div className={styles.card}>
        <div className={styles.cardImageWrapper}>
          <img
            src="/images/landing-guides.png"
            alt=""
            className={styles.cardImage}
          />
        </div>
        <h2 className={styles.cardTitle}>{t['vpn.title']}</h2>
        <p className={styles.cardDescription}>{t['vpn.description']}</p>
        <Link className={styles.cardButton} to="/why-outline">
          {t['vpn.button']}
        </Link>
      </div>
      <div className={styles.card}>
        <div className={styles.cardImageWrapper}>
          <img
            src="/images/landing-reference.png"
            alt=""
            className={styles.cardImage}
          />
        </div>
        <h2 className={styles.cardTitle}>{t['sdk.title']}</h2>
        <p className={styles.cardDescription}>{t['sdk.description']}</p>
        <Link className={styles.cardButton} to="/sdk/what-is-the-sdk">
          {t['sdk.button']}
        </Link>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout title={siteConfig.title} description={siteConfig.tagline}>
      <Hero />
      <main className={styles.main}>
        <Cards />
      </main>
    </Layout>
  );
}
