// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://carbonproject.ai',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'auto' },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/contact/received'),
      changefreq: 'monthly',
      lastmod: new Date(),
    }),
  ],
  compressHTML: true,
  prefetch: { prefetchAll: true, defaultStrategy: 'hover' },
});
