import { defaultTheme } from '@vuepress/theme-default'
import { defineUserConfig } from 'vuepress/cli'
import { viteBundler } from '@vuepress/bundler-vite'

export default defineUserConfig({
  lang: 'zh-CN',

  title: 'SyncFile',
  description: '由元素提供的文件同步工具',

  theme: defaultTheme({
    logo: '/logo_transparent.png',
    repo: 'https://github.com/ECSDevs/SyncFile',
    navbar: [
      {text: '首页', link: '/'},
      {text: '快速上手', link: '/quick-guide.html'},
      {
        text: '文档', 
        prefix: '/reference/',
        children: [
          {text: '参考介绍', link: 'introduction.html'},
          {text: '服务端参考', link: 'server_config.html'},
          {text: '客户端参考', link: 'client_config.html'}
        ]
      },
      {text: '贡献手册', link: 'communicate.html'}
    ],

    sidebar: false,
  }),

  bundler: viteBundler(),
})
