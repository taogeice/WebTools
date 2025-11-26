<template>
  <div id="app">
    <header class="app-header">
      <h1>黄金价格分析系统</h1>
      <p class="subtitle">实时追踪国内外黄金价格走势</p>
    </header>

    <nav class="app-nav">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="['nav-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </nav>

    <main class="app-main">
      <div v-if="activeTab === 'chart'" class="tab-content">
        <GoldPriceChart />
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
      <p>&copy; 2024 黄金价格分析系统 | 基于 FastAPI + Vue 3 构建</p>
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue';
import GoldPriceChart from './components/GoldPriceChart.vue';
import GoldPriceComparison from './components/GoldPriceComparison.vue';
import LatestPrices from './components/LatestPrices.vue';
import DevTools from './components/DevTools.vue';

export default {
  name: 'App',
  components: {
    GoldPriceChart,
    GoldPriceComparison,
    LatestPrices,
    DevTools
  },
  setup() {
    const activeTab = ref('chart');

    const tabs = [
      { id: 'chart', label: '价格走势' },
      { id: 'comparison', label: '市场对比' },
      { id: 'latest', label: '最新价格' },
      { id: 'devtools', label: '开发工具' }
    ];

    return {
      activeTab,
      tabs
    };
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

#app {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.app-header h1 {
  font-size: 36px;
  color: #333;
  margin-bottom: 10px;
  font-weight: 700;
}

.subtitle {
  font-size: 16px;
  color: #666;
  font-weight: 400;
}

.app-nav {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.nav-btn {
  padding: 12px 30px;
  background: white;
  border: 2px solid transparent;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.nav-btn.active {
  background: #4dabf7;
  color: white;
  border-color: #4dabf7;
}

.app-main {
  min-height: 500px;
}

.tab-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.app-footer {
  text-align: center;
  padding: 30px 20px;
  margin-top: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.app-footer p {
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  #app {
    padding: 10px;
  }

  .app-header h1 {
    font-size: 28px;
  }

  .nav-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
}
</style>
