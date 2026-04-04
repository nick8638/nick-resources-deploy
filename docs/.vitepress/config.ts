// @ts-nocheck
import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

function getSidebarItems(dir: string) {
  const files = fs.readdirSync(path.join(__dirname, '../', dir))
    .filter(file => file.endsWith('.md') && file !== 'index.md')
    .sort()

  return files.map(file => {
    const name = path.basename(file, '.md')
    return {
      text: name,
      link: `/${dir}/${name}`
    }
  })
}

// https://vitepress.vuejs.org/config/app-configs
export default defineConfig({
  base: '/',
  title: "超过 100T 的资源",
  titleTemplate: ":title - 尼克的资源收集站 | 免费资源下载",
  lang: 'zh-CN',
  lastUpdated: false,
  cleanUrls: false,
  trailingSlash: false,
  sitemap: {
    hostname: 'https://nick88.top'
  },
  vite: {
    assetsInclude: ['**/*.png', '**/*.jpg', '**/*.jpeg', '**/*.gif', '**/*.svg'],
    server: {
      fs: {
        allow: ['..']
      }
    }
  },
  description: "超过100T免费资源下载站，包含AI知识、书籍资料、跨境电商、自媒体、教育、健康、影视、工具等海量资源，持续更新中",
  head: [
    ['link', { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    ['link', { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' }],
    ['link', { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' }],
    ['link', { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' }],
    ['link', { rel: 'manifest', href: '/site.webmanifest' }],
    ['meta', { name: 'theme-color', content: '#ffffff' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: '尼克的资源收集站 | 超过 100T+ 资源' }],
    ['meta', { property: 'og:description', content: '超过100T免费资源下载站，包含AI知识、书籍资料、跨境电商、自媒体、教育、健康、影视、工具等海量资源' }],
    ['meta', { property: 'og:url', content: 'https://nick88.top' }],
    ['meta', { name: 'keywords', content: '免费资源下载,AI知识,书籍资料,跨境电商,自媒体,教育资源,健康养生,影视资源,工具软件,100T资源' }],
    ['meta', { name: 'author', content: '尼克的资源收集站' }],
    [
      'script',
      { async: true, src: 'https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js' }
    ],
  ],
  themeConfig: {
    socialLinks: [
      { icon: 'qq', link: 'https://qm.qq.com/q/gOI5eLKk70', ariaLabel: 'QQ群' }
    ],
    nav: [
      { text: '首页', link: '/' },
      { text: '📂 资源', link: '/AIknowledge/' },
      { text: '点击加入QQ群：1095830226', link: 'https://qm.qq.com/q/gOI5eLKk70' }
    ],
    search: {
      provider: 'local'
    },
    sidebar: [
      {
        text: '资源分类',
        items: [
          {
            text: 'AI 知识',
            collapsed: true,
            items: [
              { text: 'AI 知识主页', link: '/AIknowledge/' },
              ...getSidebarItems('AIknowledge')
            ]
          },
          {
            text: '书籍资料',
            collapsed: true,
            items: [
              { text: '书籍资料主页', link: '/book/' },
              ...getSidebarItems('book')
            ]
          },
          {
            text: '传统文化',
            collapsed: true,
            items: [
              { text: '传统文化主页', link: '/chinese-traditional/' },
              ...getSidebarItems('chinese-traditional')
            ]
          },
          {
            text: '跨境电商',
            collapsed: true,
            items: [
              { text: '跨境电商主页', link: '/cross-border/' },
              ...getSidebarItems('cross-border')
            ]
          },
          {
            text: '课程资料',
            collapsed: true,
            items: [
              { text: '课程资料主页', link: '/curriculum/' },
              ...getSidebarItems('curriculum')
            ]
          },
          {
            text: '教育知识',
            collapsed: true,
            items: [
              { text: '教育知识主页', link: '/edu-knowlege/' },
              ...getSidebarItems('edu-knowlege')
            ]
          },
          {
            text: '健康养生',
            collapsed: true,
            items: [
              { text: '健康养生主页', link: '/healthy/' },
              ...getSidebarItems('healthy')
            ]
          },
          {
            text: '影视媒体',
            collapsed: true,
            items: [
              { text: '影视媒体主页', link: '/movies/' },
              ...getSidebarItems('movies')
            ]
          },
          {
            text: '自媒体',
            collapsed: true,
            items: [
              { text: '自媒体主页', link: '/self-media/' },
              ...getSidebarItems('self-media')
            ]
          },
          {
            text: '工具合集',
            collapsed: true,
            items: [
              { text: '工具合集主页', link: '/tools/' },
              ...getSidebarItems('tools')
            ]
          },
        ]
      }
    ],
    footer: {
      message: "<a href=\"https://qm.qq.com/q/gOI5eLKk70\" target=\"_blank\">QQ群交流</a> | <a href=\"/disclaimer\">免责声明</a> | 如有侵权，请联系删除。<br><span id=\"busuanzi_container_site_uv\">访客数 <span id=\"busuanzi_value_site_uv\"></span> 人次</span>，<span id=\"busuanzi_container_site_pv\">本站总访问量 <span id=\"busuanzi_value_site_pv\"></span> 次</span>",
      copyright: 'Copyright © 2025-present 尼克的资源收集站'
    }
  }
})
