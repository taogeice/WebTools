<template>
  <div class="dev-tools-container">
    <h2 class="tools-title">开发者工具箱</h2>
    <p class="tools-subtitle">常用的开发工具集合</p>

    <div class="tools-grid">
      <!-- JSON 格式化工具 -->
      <div class="tool-card">
        <div class="tool-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#4dabf7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
        </div>
        <h3>JSON 格式化</h3>
        <p>格式化、验证和压缩 JSON 数据</p>
        <button class="tool-btn" @click="activeTool = 'json'">使用工具</button>
      </div>

      <!-- Base64 编解码 -->
      <div class="tool-card">
        <div class="tool-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ff6b6b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="20" rx="2" ry="2"/>
            <path d="M7 7h10v10H7z"/>
          </svg>
        </div>
        <h3>Base64 编解码</h3>
        <p>文本与 Base64 格式互转</p>
        <button class="tool-btn" @click="activeTool = 'base64'">使用工具</button>
      </div>

      <!-- URL 编解码 -->
      <div class="tool-card">
        <div class="tool-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#51cf66" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
          </svg>
        </div>
        <h3>URL 编解码</h3>
        <p>URL 编码和解码工具</p>
        <button class="tool-btn" @click="activeTool = 'url'">使用工具</button>
      </div>

      <!-- 时间戳转换 -->
      <div class="tool-card">
        <div class="tool-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ffd43b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <h3>时间戳转换</h3>
        <p>Unix 时间戳与日期互转</p>
        <button class="tool-btn" @click="activeTool = 'timestamp'">使用工具</button>
      </div>

      <!-- 颜色选择器 -->
      <div class="tool-card">
        <div class="tool-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#9775fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 2a15.3 15.3 0 0 1 0 20"/>
            <path d="M12 2a15.3 15.3 0 0 0 0 20"/>
          </svg>
        </div>
        <h3>颜色选择器</h3>
        <p>选择颜色并获取各种格式</p>
        <button class="tool-btn" @click="activeTool = 'color'">使用工具</button>
      </div>

      <!-- 正则表达式测试 -->
      <div class="tool-card">
        <div class="tool-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ff8787" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </div>
        <h3>正则测试</h3>
        <p>测试正则表达式匹配</p>
        <button class="tool-btn" @click="activeTool = 'regex'">使用工具</button>
      </div>
    </div>

    <!-- 工具面板 -->
    <div v-if="activeTool" class="tool-panel-overlay" @click.self="activeTool = ''">
      <div class="tool-panel">
        <div class="panel-header">
          <h3>{{ getToolTitle(activeTool) }}</h3>
          <button class="close-btn" @click="activeTool = ''">×</button>
        </div>
        <div class="panel-content">
          <JsonFormatter v-if="activeTool === 'json'" />
          <Base64Tool v-if="activeTool === 'base64'" />
          <UrlTool v-if="activeTool === 'url'" />
          <TimestampTool v-if="activeTool === 'timestamp'" />
          <ColorTool v-if="activeTool === 'color'" />
          <RegexTool v-if="activeTool === 'regex'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import JsonFormatter from './tools/JsonFormatter.vue';
import Base64Tool from './tools/Base64Tool.vue';
import UrlTool from './tools/UrlTool.vue';
import TimestampTool from './tools/TimestampTool.vue';
import ColorTool from './tools/ColorTool.vue';
import RegexTool from './tools/RegexTool.vue';

export default {
  name: 'DevTools',
  components: {
    JsonFormatter,
    Base64Tool,
    UrlTool,
    TimestampTool,
    ColorTool,
    RegexTool
  },
  setup() {
    const activeTool = ref('');

    const getToolTitle = (tool) => {
      const titles = {
        json: 'JSON 格式化工具',
        base64: 'Base64 编解码',
        url: 'URL 编解码',
        timestamp: '时间戳转换',
        color: '颜色选择器',
        regex: '正则表达式测试'
      };
      return titles[tool] || '';
    };

    return {
      activeTool,
      getToolTitle
    };
  }
};
</script>

<style scoped>
.dev-tools-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 30px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.tools-title {
  text-align: center;
  font-size: 38px;
  color: #00f2ff;
  margin-bottom: 15px;
  font-weight: 700;
  text-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
}

.tools-subtitle {
  text-align: center;
  font-size: 16px;
  color: #8899aa;
  margin-bottom: 40px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.tool-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(0, 242, 255, 0.1);
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;
}

.tool-card:hover {
  transform: translateY(-8px);
  border-color: #00f2ff;
  box-shadow: 0 8px 30px rgba(0, 242, 255, 0.3);
}

.tool-icon {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
}

.tool-card h3 {
  font-size: 22px;
  color: #00f2ff;
  margin-bottom: 12px;
  font-weight: 600;
}

.tool-card p {
  color: #8899aa;
  font-size: 14px;
  margin-bottom: 20px;
  line-height: 1.6;
}

.tool-btn {
  width: 100%;
  padding: 12px 24px;
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.2) 0%, rgba(0, 132, 255, 0.2) 100%);
  color: #00f2ff;
  border: 1px solid #00f2ff;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tool-btn:hover {
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.3) 0%, rgba(0, 132, 255, 0.3) 100%);
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
  transform: translateY(-2px);
}

.tool-panel-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  backdrop-filter: blur(5px);
}

.tool-panel {
  background: rgba(10, 14, 39, 0.95);
  border: 1px solid rgba(0, 242, 255, 0.3);
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
}

.panel-header {
  padding: 25px 30px;
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.2) 0%, rgba(0, 132, 255, 0.2) 100%);
  color: #00f2ff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 242, 255, 0.2);
}

.panel-header h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
}

.close-btn {
  background: rgba(0, 242, 255, 0.1);
  border: 1px solid rgba(0, 242, 255, 0.3);
  color: #00f2ff;
  font-size: 32px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(0, 242, 255, 0.3);
  box-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
  transform: rotate(90deg);
}

.panel-content {
  padding: 30px;
  overflow-y: auto;
  flex: 1;
  color: #ccc;
}

@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }

  .tool-panel {
    max-height: 95vh;
  }

  .panel-content {
    padding: 20px;
  }
}
</style>
