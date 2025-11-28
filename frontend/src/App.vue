<template>
  <div id="app">
    <!-- 科技风格背景网格 -->
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>

    <header class="app-header">
      <div class="header-content">
        <div class="header-line"></div>
        <h1>黄金价格分析系统</h1>
        <div class="header-line"></div>
      </div>
      <p class="subtitle">
        <span class="subtitle-icon">⚡</span>
        实时追踪国内外黄金价格走势
        <span class="subtitle-icon">⚡</span>
      </p>
    </header>

    <nav class="app-nav">
      <div class="nav-container">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['nav-btn', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          <span class="btn-icon">{{ getTabIcon(tab.id) }}</span>
          {{ tab.label }} (ECharts)
          <span class="btn-glow"></span>
        </button>
      </div>
    </nav>

    <main class="app-main">
      <div v-if="activeTab === 'chart'" class="tab-content">
        <GoldPriceChartECharts />
      </div>

      <div v-else-if="activeTab === 'comparison'" class="tab-content">
        <GoldPriceComparison />
      </div>

      <div v-else-if="activeTab === 'latest'" class="tab-content">
        <LatestPrices />
      </div>

      <div v-else-if="activeTab === 'devtools'" class="tab-content">
        <DevTools />
      </div>
    </main>

    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-line"></div>
        <p>&copy; 2024 黄金价格分析系统 | 基于 FastAPI + Vue 3 构建</p>
        <div class="footer-line"></div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue';
import GoldPriceChartECharts from './components/GoldPriceChartECharts.vue';
import GoldPriceComparison from './components/GoldPriceComparison.vue';
import LatestPrices from './components/LatestPrices.vue';
import DevTools from './components/DevTools.vue';

export default {
  name: 'App',
  components: {
    GoldPriceChartECharts,
    GoldPriceComparison,
    LatestPrices,
    DevTools
  },
  setup() {
    const activeTab = ref('chart');

    const tabs = [
      { id: 'chart', label: '价格走势 (ECharts)' },
      { id: 'comparison', label: '市场对比' },
      { id: 'latest', label: '最新价格' },
      { id: 'devtools', label: '开发工具' }
    ];

    const getTabIcon = (tabId) => {
      const icons = {
        chart: '📊',
        comparison: '📈',
        latest: '⚡',
        devtools: '🔧'
      };
      return icons[tabId] || '•';
    };

    return {
      activeTab,
      tabs,
      getTabIcon
    };
  }
};
</script>

<style scoped>
/* App组件特定的样式，大部分样式已经移到CSS模块中 */

/* 标签页内容动画 */
.tab-content {
  animation: fadeInUp var(--duration-normal) var(--ease-in-out);
}
</style>
