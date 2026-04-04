# 🚀 尼克资源站 - 项目迁移指南

> 最后更新：2026-04-04
>
> 本文档用于在新电脑上快速恢复开发环境。**所有关键信息都在这里，不再依赖某台特定电脑。**

---

## 📦 必须带走的资料（打包清单）

### 1️⃣ 核心项目代码（最重要！）
```
nick-fresh/          ← 整个目录都要（约983个文件）
├── docs/           ← VitePress 源文件（首页、配置、组件、资源md）
├── package.json    ← Node.js 依赖声明
├── .gitignore      ← Git忽略规则
└── scripts/        ← 工具脚本（fetch-commits.js等）
```

### 2️⃣ 自动化脚本（工作区根目录）
```
push-to-github.py   ← GitHub API 推送脚本（含token）
batch-replace.py    ← 批量链接替换脚本
parse-docx.py       ← Word文档解析脚本
cleanup-remaining.py ← 残留清理脚本
```

### 3️⃣ 数据文件
```
网盘转存名单.docx    ← 网盘链接映射表（已填写的版本）
网盘转存名单.md      ← 同上Markdown版（备用）
```

### 4️⃣ 参考备份（可选但建议带上）
```
mswnlz.github.io-main/  ← 原始参考站源码备份
```

### ❌ 不需要带走的
- `node_modules/` → 可通过 `npm install` 或 `pnpm install` 重新安装
- `docs/.vitepress/dist/` → 构建产物，可重新 `npm run build`
- `docs/.vitepress/cache/` → 缓存，自动生成

---

## 🔑 关键账号与 Token 信息

### GitHub
- **用户名**: `nick8638`
- **部署仓库**: `nick8638/nick-resources-deploy`
- **Fine-grained PAT Token**: `YOUR_GITHUB_PAT_TOKEN_HERE`  ← **替换为你的实际 token**
  - ⚠️ 认证格式：**`Bearer`**（不是 `token`）
  - 权限：Contents: **Read and write**
  - 仓库范围：仅 `nick8638/nick-resources-deploy`
  - ⚠️ 过期时间请自己在 GitHub Settings 查看并记录

### Vercel 部署
- **自定义域名**: https://www.nick88.top
- **Vercel 地址**: https://nick-resources-deploy.vercel.app
- 部署方式：GitHub 推送后 Vercel 自动构建部署

### 个人信息
- **联系邮箱**: s2622658510@163.com
- **QQ群**: 1095830226（https://qm.qq.com/q/gOI5eLKk70）

---

## 🖥️ 新电脑环境搭建步骤

### 第 1 步：安装基础软件
1. **Node.js**（推荐 v22.x）→ https://nodejs.org
2. **Python 3.13+** → 用于运行自动化脚本
3. **Git**（可选，我们用 API 推送不需要 git）

### 第 2 步：恢复项目代码
```bash
# 方式A：从GitHub拉取部署仓库（推荐）
# 这个仓库包含最新的 docs/ 全部源码
# 但注意：GitHub上的 nick-resources-deploy 只有 docs/ 目录
# 如果需要完整项目（含 node_modules 等），用打包的 nick-fresh/

# 方式B：直接复制打包的 nick-fresh/ 文件夹到新电脑
cd 你的工作目录
cp -r nick-fresh/* .
pnpm install        # 安装Node.js依赖
```

### 第 3 步：更新推送脚本中的路径
⚠️ **重要！push-to-github.py 中的路径是硬编码的旧电脑路径**
新电脑上必须修改：
```python
# push-to-github.py 第4行，改为你的实际路径：
docs_dir = r'C:\你的新路径\nick-fresh\docs'

# batch-replace.py 第5行 和第48行：
docx = r'C:\你的新路径\网盘转存名单.docx'
docs_dir = r'C:\你的新路径\nick-fresh\docs'
```

### 第 4 步：验证能否正常使用
```bash
# 启动本地开发服务器测试
pnpm dev
# 或者
npm run dev
```

### 第 5 步：修改代码后的推送流程
```bash
# 修改完文件后，执行推送：
python push-to-github.py
# 等输出 "Success: xxx, Errors: 0" 就说明成功了
# Vercel 会自动重新部署
```

---

## 🌐 云端化方案（推荐！彻底解决换电脑问题）

### 为什么需要云端化？
- 你经常换电脑，每次都要打包资料太麻烦
- token、配置、脚本分散在不同地方容易丢失
- WorkBuddy 本身有记忆功能，但项目代码不在云端

### 方案 A：将关键信息放到网站隐藏页面（推荐 ⭐）
在你的网站上创建一个 `/admin/` 或 `/dev/` 页面，存储以下信息：
- GitHub token（加密或混淆存储）
- 脚本模板代码
- 开发笔记和进度记录

**优点**：随时随地能访问，不依赖任何电脑

### 方案 B：使用 GitHub 作为唯一数据源
1. 把 `nick-fresh/docs/` 以外的工作区文件也建一个私有 GitHub 仓库
2. 新电脑只需 clone 两个仓库即可
3. 所有脚本、token 配置都在代码里

### 方案 C：利用 WorkBuddy 自带的记忆系统 ✅
当前已经在使用的方案：
- `MEMORY.md` 存储长期信息（账号、token、架构等）
- `YYYY-MM-DD.md` 存储每日工作记录
- 换电脑后 WorkBuddy 会自动读取这些记忆

**但限制**：项目代码本身不在记忆里，需要另外处理

---

## 📋 项目架构速查

```
nick-fresh/                          ← 主项目目录
├── docs/                            ← VitePress 文档根
│   ├── index.md                     ← 首页（12分类卡片+关键词+打赏）
│   ├── disclaimer.md                ← 免责声明
│   ├── support.md                   ← 打赏页
│   ├── public/                      ← 静态资源
│   │   ├── alipay.jpg / wechat.jpg  ← 收款码
│   │   ├── commits.json             ← 最新动态数据
│   │   └── {分类}/                  ← 各分类资源md文件
│   │       ├── AIknowledge/
│   │       ├── book/
│   │       ├── cross-border/
│   │       ├── curriculum/
│   │       ├── edu-knowlege/
│   │       ├── healthy/
│   │       ├── movies/
│   │       ├── self-media/
│   │       ├── tools/
│   │       ├── chinese-traditional/
│   │       └── auto/
│   └── .vitepress/                   ← VitePress 配置
│       ├── config.ts                 ← ★主配置（导航/SEO/统计/侧边栏）
│       ├── theme/
│       │   ├── style.css            ← 全局CSS样式
│       │   ├── components/          ← Vue组件
│       │   │   ├── Layout.vue       ← 自定义布局
│       │   │   ├── CommitHistory.vue← 最新动态滚动
│       │   │   ├── ResourceTabs.vue ← 资源选项卡
│       │   │   ├── SupportSection.vue ← 打赏组件
│       │   │   ├── VPFooter.vue     ← 页脚
│       │   │   ├── UpdateTime.vue   ← 更新时间
│       │   │   └── GitHubLink.vue   ← GitHub展示
│       │   └── index.ts             ← 主题入口
│       └── components/              ← 全局组件
├── package.json                     ← 项目依赖
├── scripts/fetch-commits.js         ← 获取commit数据脚本
├── copy_content.sh                  ← 内容复制脚本
└── trigger-update.sh                ← 触发更新脚本

工作区根目录工具脚本:
├── push-to-github.py               ← ★GitHub API推送（含token）
├── batch-replace.py                ← 批量URL替换
├── parse-docx.py                   ← Word文档解析
├── cleanup-remaining.py            ← 残留清理
└── 网盘转存名单.docx/md             ← 链接映射数据
```

---

## ⚡ 常用操作速查

| 操作 | 命令 |
|------|------|
| 启动开发服务器 | `pnpm dev` (或 `npm run dev`) |
| 构建生产版本 | `npm run build` |
| 推送到GitHub | `python push-to-github.py` |
| 批量替换链接 | `python batch-replace.py` |
| 清理残留引用 | `python cleanup-remaining.py` |
| 解析Word转存单 | `python parse-docx.py` |

---

## ⚠️ 注意事项

1. **Token 安全**：PAT token 已保存在 push-to-github.py 中，不要将此文件上传到公开位置
2. **路径硬编码**：所有 Python 脚本中的 Windows 绝对路径需要根据新电脑调整
3. **Python 版本**：本机使用 managed Python 3.13.12 (`C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe`)
4. **PowerShell 中文编码问题**：含中文路径时建议用 Python 脚本而非 PowerShell 原生命令
5. **Fine-grained Token 要求 Bearer 格式**：headers 中用 `Bearer {token}` 不是 `token {token}`

---

*保持此文档随项目一起迁移，它是你恢复开发环境的唯一手册。*
