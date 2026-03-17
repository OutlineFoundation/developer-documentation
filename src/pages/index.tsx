import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';

function Hero(): JSX.Element {
  return (
    <header className={styles.hero}>
      <div className={styles.heroInner}>
        <h1 className={styles.heroTitle}>
          <Translate id="homepage.hero.title">
            Build censorship-resilient apps with the power of Outline
          </Translate>
        </h1>
        <p className={styles.heroSubtitle}>
          <Translate id="homepage.hero.subtitle">
            Help your users overcome censorship barriers and access the open
            internet, no matter where they are.
          </Translate>
        </p>
      </div>
    </header>
  );
}

function Cards(): JSX.Element {
  return (
    <section className={styles.cards}>
      <div className={styles.card}>
        <img
          src="/images/landing-guides.png"
          alt=""
          className={styles.cardImage}
        />
        <h2 className={styles.cardTitle}>
          <Translate id="homepage.vpn.title">
            Get Started with Outline
          </Translate>
        </h2>
        <p className={styles.cardDescription}>
          <Translate id="homepage.vpn.description">
            Learn how to deploy, configure, and manage your own VPN server.
          </Translate>
        </p>
        <Link className={styles.cardButton} to="/why-outline">
          <Translate id="homepage.vpn.button">Start now</Translate>
        </Link>
      </div>
      <div className={styles.card}>
        <img
          src="/images/landing-reference.png"
          alt=""
          className={styles.cardImage}
        />
        <h2 className={styles.cardTitle}>
          <Translate id="homepage.sdk.title">
            Build with Outline SDK
          </Translate>
        </h2>
        <p className={styles.cardDescription}>
          <Translate id="homepage.sdk.description">
            Integrate Outline&#39;s advanced strategies into your applications
            and services.
          </Translate>
        </p>
        <Link className={styles.cardButton} to="/sdk/what-is-the-sdk">
          <Translate id="homepage.sdk.button">Explore the SDK</Translate>
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
