# WebTools 前端应用

基于 Vue 3 + Vite 构建的现代化工具箱前端应用，提供直观的用户界面和丰富的功能体验。

## 项目概述

WebTools 前端是一个多功能的应用平台，集成了多种实用工具，包括数据分析、价格监控等功能，具有以下特性：

- 🎨 **现代化界面**：基于 Vue 3 Composition API，响应式设计
- 📊 **丰富的图表**：集成 Chart.js，提供多种数据可视化方式
- 🔄 **实时更新**：自动刷新黄金价格数据，支持 WebSocket 实时推送
- 🌐 **国际化支持**：中英文双语界面
- 📱 **移动端适配**：完美支持各种设备和屏幕尺寸
- 🎯 **用户体验**：流畅的动画效果和交互反馈
- 🔧 **组件化开发**：高度可复用的组件架构

## 技术栈

- **框架**: Vue 3.4+
- **构建工具**: Vite 5.0+
- **类型检查**: TypeScript
- **UI 组件**: Element Plus / 自定义组件
- **图表库**: Chart.js + vue-chartjs
- **HTTP 客户端**: Axios
- **状态管理**: Pinia (Vue Store)
- **路由管理**: Vue Router 4
- **样式方案**: SCSS + CSS Modules
- **代码规范**: ESLint + Prettier
- **测试框架**: Vitest + Vue Test Utils

## 项目结构

```
frontend/
├── public/                     # 静态资源
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── main.js                 # 应用入口文件
│   ├── App.vue                 # 根组件
│   ├── assets/                 # 静态资源
│   │   ├── images/             # 图片资源
│   │   ├── icons/              # 图标文件
│   │   └── styles/             # 全局样式
│   │       ├── main.scss       # 主样式文件
│   │       ├── variables.scss  # SCSS 变量
│   │       └── mixins.scss     # SCSS 混入
│   ├── components/             # 可复用组件
│   │   ├── common/             # 通用组件
│   │   │   ├── Header.vue      # 页面头部
│   │   │   ├── Footer.vue      # 页面底部
│   │   │   ├── Loading.vue     # 加载组件
│   │   │   └── Pagination.vue  # 分页组件
│   │   ├── charts/             # 图表组件
│   │   │   ├── GoldPriceChart.vue      # 黄金价格图表
│   │   │   ├── TrendChart.vue         # 趋势分析图表
│   │   │   ├── ComparisonChart.vue     # 对比图表
│   │   │   └── CandlestickChart.vue    # K线图表
│   │   ├── forms/              # 表单组件
│   │   │   ├── DateRangePicker.vue    # 日期范围选择器
│   │   │   ├── MarketSelector.vue     # 市场选择器
│   │   │   └── SearchInput.vue        # 搜索输入框
│   │   └── layout/             # 布局组件
│   │       ├── Sidebar.vue           # 侧边栏
│   │       ├── Breadcrumb.vue         # 面包屑导航
│   │       └── Container.vue          # 容器组件
│   ├── views/                  # 页面组件
│   │   ├── Home.vue            # 首页
│   │   ├── Dashboard.vue       # 仪表盘
│   │   ├── GoldPrice.vue       # 黄金价格页面
│   │   ├── Analysis.vue        # 数据分析页面
│   │   ├── Compare.vue         # 市场对比页面
│   │   ├── Settings.vue        # 设置页面
│   │   ├── Login.vue           # 登录页面
│   │   └── NotFound.vue        # 404 页面
│   ├── router/                 # 路由配置
│   │   └── index.js            # 路由定义
│   ├── api/                    # API 接口
│   │   ├── index.js            # API 客户端配置
│   │   ├── auth.js             # 认证相关接口
│   │   ├── gold.js             # 黄金价格接口
│   │   └── stats.js            # 统计数据接口
│   ├── stores/                 # 状态管理
│   │   ├── index.js            # Store 入口
│   │   ├── auth.js             # 用户认证状态
│   │   ├── gold.js             # 黄金数据状态
│   │   └── settings.js         # 应用设置状态
│   ├── utils/                  # 工具函数
│   │   ├── constants.js        # 常量定义
│   │   ├── formatters.js       # 数据格式化
│   │   ├── validators.js       # 数据验证
│   │   └── helpers.js          # 辅助函数
│   └── composables/            # Composition API
│       ├── useApi.js           # API 调用组合函数
│       ├── useAuth.js          # 认证组合函数
│       ├── useChart.js         # 图表组合函数
│       └── useLocalStorage.js  # 本地存储组合函数
├── tests/                      # 测试文件
│   ├── unit/                   # 单元测试
│   ├── integration/            # 集成测试
│   └── e2e/                    # 端到端测试
├── package.json                # 项目依赖
├── vite.config.js              # Vite 配置
├── jsconfig.json               # JavaScript 配置
├── .env.example                # 环境变量示例
├── .env.development            # 开发环境变量
├── .env.production             # 生产环境变量
├── .eslintrc.js                # ESLint 配置
├── .prettierrc                 # Prettier 配置
├── vitest.config.js            # Vitest 配置
└── README.md                   # 项目文档
```

## 快速开始

### 环境要求

- Node.js 18.0+
- npm 9.0+ 或 yarn 1.22+
- 现代浏览器（Chrome 88+, Firefox 85+, Safari 14+, Edge 88+）

### 1. 克隆项目并进入前端目录

```bash
cd frontend
```

### 2. 安装依赖

```bash
# 使用 npm
npm install

# 或使用 yarn
yarn install

# 或使用 pnpm
pnpm install
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env.development

# 编辑环境变量文件，配置 API 地址等
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=WebTools - 黄金价格分析
VITE_APP_VERSION=1.0.0
```

### 4. 启动开发服务器

```bash
# 启动开发服务器（默认端口 5173）
npm run dev

# 或指定端口
npm run dev -- --port 3000

# 或使用 yarn
yarn dev
```

### 5. 构建生产版本

```bash
# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

### 6. 访问应用

启动成功后，在浏览器中访问：

- **开发环境**: http://localhost:5173
- **生产预览**: http://localhost:4173

## 开发指南

### 推荐开发环境

#### IDE 设置

推荐使用 [VS Code](https://code.visualstudio.com/) 并安装以下插件：

- **[Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar)** - Vue 3 语言支持
- **[Vue VSCode Snippets](https://marketplace.visualstudio.com/items?itemName=sdras.vue-vscode-snippets)** - Vue 代码片段
- **[ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)** - 代码规范检查
- **[Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)** - 代码格式化
- **[Auto Rename Tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag)** - 标签自动重命名
- **[Path Intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense)** - 路径智能提示

#### 浏览器开发工具

- **Chrome/Edge**: 安装 [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
- **Firefox**: 安装 [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)

### 项目配置说明

#### Vite 配置 (vite.config.js)

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@views': resolve(__dirname, 'src/views'),
      '@api': resolve(__dirname, 'src/api'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@stores': resolve(__dirname, 'src/stores'),
    }
  },
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          chart: ['chart.js', 'vue-chartjs'],
          utils: ['axios', 'dayjs']
        }
      }
    }
  }
})
```

#### 环境变量

```bash
# .env.development (开发环境)
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=WebTools - 黄金价格分析
VITE_APP_VERSION=1.0.0
VITE_MOCK_DATA=true
VITE_DEBUG=true

# .env.production (生产环境)
VITE_API_BASE_URL=https://api.webtools.com/api/v1
VITE_APP_TITLE=WebTools
VITE_APP_VERSION=1.0.0
VITE_MOCK_DATA=false
VITE_DEBUG=false
```

### 开发最佳实践

#### 1. 组件开发规范

```vue
<template>
  <div class="component-name">
    <!-- 模板内容 -->
  </div>
</template>

<script setup>
// 导入依赖
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 定义 props 和 emits
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  data: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update', 'change'])

// 响应式数据
const isLoading = ref(false)
const errorMessage = ref('')

// 计算属性
const computedValue = computed(() => {
  return props.data.length > 0
})

// 方法
const handleAction = () => {
  emit('update', newValue)
}

// 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style lang="scss" scoped>
.component-name {
  // 组件样式
}
</style>
```

#### 2. API 接口封装

```javascript
// src/api/gold.js
import request from './index'

export const goldApi = {
  // 获取最新黄金价格
  getLatest: () => {
    return request.get('/gold/latest')
  },

  // 获取历史价格
  getHistory: (params) => {
    return request.get('/gold/history', { params })
  },

  // 获取市场对比数据
  getComparison: (params) => {
    return request.get('/gold/compare', { params })
  }
}
```

#### 3. 状态管理 (Pinia)

```javascript
// src/stores/gold.js
import { defineStore } from 'pinia'
import { goldApi } from '@/api/gold'

export const useGoldStore = defineStore('gold', {
  state: () => ({
    prices: [],
    currentPrice: null,
    loading: false,
    error: null
  }),

  getters: {
    latestPrice: (state) => state.prices[0],
    priceChange: (state) => {
      if (!state.currentPrice) return 0
      return state.currentPrice.change
    }
  },

  actions: {
    async fetchLatestPrice() {
      this.loading = true
      try {
        const response = await goldApi.getLatest()
        this.currentPrice = response.data
        this.error = null
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchHistory(params) {
      // 获取历史数据逻辑
    }
  }
})
```

#### 4. 组合函数 (Composables)

```javascript
// src/composables/useChart.js
import { ref, onMounted, onUnmounted } from 'vue'
import Chart from 'chart.js/auto'

export function useChart(canvasRef, options) {
  const chart = ref(null)

  const initChart = () => {
    if (canvasRef.value) {
      chart.value = new Chart(canvasRef.value, options)
    }
  }

  const updateChart = (newData) => {
    if (chart.value) {
      chart.value.data = newData
      chart.value.update()
    }
  }

  const destroyChart = () => {
    if (chart.value) {
      chart.value.destroy()
      chart.value = null
    }
  }

  onMounted(() => {
    initChart()
  })

  onUnmounted(() => {
    destroyChart()
  })

  return {
    chart,
    updateChart,
    destroyChart
  }
}
```

## 可用脚本

```bash
# 开发
npm run dev          # 启动开发服务器
npm run preview      # 预览生产构建

# 构建
npm run build        # 构建生产版本
npm run build:report # 构建并生成分析报告

# 测试
npm run test         # 运行单元测试
npm run test:e2e     # 运行端到端测试
npm run test:coverage # 运行测试并生成覆盖率报告

# 代码质量
npm run lint         # 运行 ESLint 检查
npm run lint:fix     # 自动修复 ESLint 错误
npm run format       # 格式化代码
npm run type-check   # TypeScript 类型检查
```

## 测试

### 单元测试

使用 Vitest 进行单元测试：

```javascript
// tests/unit/components/GoldPriceChart.spec.js
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import GoldPriceChart from '@/components/charts/GoldPriceChart.vue'

describe('GoldPriceChart', () => {
  it('renders correctly', () => {
    const wrapper = mount(GoldPriceChart, {
      props: {
        data: [1, 2, 3]
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('updates chart when data changes', async () => {
    const wrapper = mount(GoldPriceChart, {
      props: {
        data: [1, 2, 3]
      }
    })

    await wrapper.setProps({ data: [4, 5, 6] })
    expect(wrapper.vm.chartData).toEqual([4, 5, 6])
  })
})
```

### 端到端测试

使用 Playwright 进行 E2E 测试：

```javascript
// tests/e2e/dashboard.spec.js
import { test, expect } from '@playwright/test'

test('dashboard displays gold prices', async ({ page }) => {
  await page.goto('/dashboard')

  // 检查页面标题
  await expect(page.locator('h1')).toContainText('黄金价格分析')

  // 检查图表是否渲染
  await expect(page.locator('.chart-container')).toBeVisible()

  // 检查数据表格
  await expect(page.locator('.price-table')).toBeVisible()
})
```

## 部署

### 构建生产版本

```bash
# 构建生产版本
npm run build

# 构建结果将输出到 dist/ 目录
```

### 部署到 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### CI/CD 配置

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm run test

    - name: Build
      run: npm run build

    - name: Deploy
      run: |
        # 部署脚本
        echo "Deploying to production..."
```

## 常见问题

### Q: 如何添加新的图表类型？

1. 在 `src/components/charts/` 中创建新的图表组件
2. 在 `src/composables/useChart.js` 中添加图表配置
3. 在需要使用的页面中导入并使用新组件

### Q: 如何处理大文件上传？

使用分片上传和进度显示：

```javascript
const uploadFile = async (file) => {
  const chunkSize = 1024 * 1024 // 1MB
  const chunks = Math.ceil(file.size / chunkSize)

  for (let i = 0; i < chunks; i++) {
    const start = i * chunkSize
    const end = Math.min(file.size, start + chunkSize)
    const chunk = file.slice(start, end)

    await uploadChunk(chunk, i, chunks)
  }
}
```

### Q: 如何优化应用性能？

- 使用路由懒加载
- 组件异步加载
- 图片懒加载
- 合理使用缓存策略
- 开启 gzip 压缩

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
