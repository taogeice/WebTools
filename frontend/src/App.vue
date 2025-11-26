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
          {{ tab.label }}
          <span class="btn-glow"></span>
        </button>
      </div>
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

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #0a0e27;
  min-height: 100vh;
  overflow-x: hidden;
}

/* 科技风网格背景 */
.bg-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(0, 242, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 242, 255, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
  z-index: 0;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(50px, 50px);
  }
}

/* 发光背景 */
.bg-glow {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(0, 242, 255, 0.15) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 0;
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.5;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.8;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

#app {
  max-width: 1600px;
  margin: 0 auto;
  padding: 40px 20px;
  position: relative;
  z-index: 1;
}

/* 科技风头部 */
.app-header {
  text-align: center;
  padding: 50px 30px;
  margin-bottom: 40px;
  position: relative;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.header-line {
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #00f2ff, transparent);
  box-shadow: 0 0 10px #00f2ff;
  animation: lineGlow 2s ease-in-out infinite;
}

@keyframes lineGlow {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

.app-header h1 {
  font-size: 42px;
  color: #fff;
  margin: 0;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
  background: linear-gradient(135deg, #00f2ff 0%, #0084ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 18px;
  color: #8899aa;
  font-weight: 400;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.subtitle-icon {
  font-size: 20px;
  animation: iconFloat 2s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

/* 科技风导航 */
.app-nav {
  margin-bottom: 40px;
}

.nav-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  padding: 10px;
}

.nav-btn {
  position: relative;
  padding: 15px 35px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  color: #8899aa;
  cursor: pointer;
  transition: all 0.4s ease;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  gap: 10px;
  overflow: hidden;
}

.btn-icon {
  font-size: 18px;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 242, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.nav-btn:hover .btn-glow {
  left: 100%;
}

.nav-btn:hover {
  border-color: #00f2ff;
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
  transform: translateY(-2px);
  color: #00f2ff;
}

.nav-btn.active {
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.2) 0%, rgba(0, 132, 255, 0.2) 100%);
  border-color: #00f2ff;
  color: #fff;
  box-shadow: 0 0 30px rgba(0, 242, 255, 0.5);
}

.nav-btn.active::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(135deg, #00f2ff, #0084ff, #00f2ff);
  border-radius: 12px;
  z-index: -1;
  animation: borderRotate 3s linear infinite;
  opacity: 0.5;
}

@keyframes borderRotate {
  0% {
    filter: hue-rotate(0deg);
  }
  100% {
    filter: hue-rotate(360deg);
  }
}

.app-main {
  min-height: 600px;
}

.tab-content {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 科技风底部 */
.app-footer {
  margin-top: 60px;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 30px;
}

.footer-line {
  width: 100px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(0, 242, 255, 0.3), transparent);
}

.app-footer p {
  color: #556677;
  font-size: 14px;
  white-space: nowrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  #app {
    padding: 15px;
  }

  .app-header h1 {
    font-size: 32px;
  }

  .header-content {
    flex-direction: column;
    gap: 15px;
  }

  .header-line {
    width: 100px;
  }

  .subtitle {
    font-size: 16px;
    flex-wrap: wrap;
  }

  .nav-btn {
    padding: 12px 25px;
    font-size: 14px;
  }

  .footer-content {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
