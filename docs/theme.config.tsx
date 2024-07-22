import React from "react";
import { DocsThemeConfig, useConfig } from "nextra-theme-docs";

const config: DocsThemeConfig = {
  logo: 'RVC CLI',
  search: {
    placeholder: "What are you looking for? 🧐",
  },
  project: {
    link: "https://github.com/blaisewf/rvc_cli",
  },
  chat: {
    link: "https://discord.gg/iahispano",
  },
  docsRepositoryBase: "https://github.com/blaisewf/rvc_cli/tree/main/docs",
  footer: {
    text: (
      <span>
        made w ❤️ by blaisewf
      </span>
    ),
  },
  nextThemes: {
    defaultTheme: "dark",
  },
  feedback: {
    content: "Do you think we should improve something? Let us know!",

  },
  editLink: {
    component: null,
  },
  faviconGlyph: "favicon.ico",
  logoLink: "/",
  primaryHue: 317,
  head: () => {
    const { frontMatter } = useConfig();

    return (
      <>
      <meta name="msapplication-TileColor" content="#fff" />
      <meta name="theme-color" content="#111" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta httpEquiv="Content-Language" content="en" />
      <meta
        name="description"
        content="🚀 RVC + UVR = A perfect set of tools for voice cloning, easily and free!"
      />
      <meta
        name="og:description"
        content="🚀 RVC + UVR = A perfect set of tools for voice cloning, easily and free!"
      />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site:domain" content="https://rvc-cli.pages.dev/" />
      <meta name="twitter:url" content="https://rvc-cli.pages.dev/" />
      <meta
        name="og:title"
        content={frontMatter.title || 'RVC CLI'}
      />
      <meta name="apple-mobile-web-app-title" content="RVC CLI" />
      <link rel="icon" href="/favicon.ico" sizes="any" />
    </>
    );
  },
  useNextSeoProps() {
    return {
      titleTemplate: `%s - RVC CLI`,
    };
  },
};

export default config;