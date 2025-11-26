<template>
  <div class="json-formatter">
    <div class="tool-section">
      <div class="input-group">
        <label>JSON 输入</label>
        <textarea
          v-model="inputJson"
          placeholder="在此粘贴您的 JSON 数据..."
          class="json-textarea"
          rows="12"
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn primary" @click="formatJson" :disabled="!inputJson">
          格式化
        </button>
        <button class="control-btn" @click="minifyJson" :disabled="!inputJson">
          压缩
        </button>
        <button class="control-btn" @click="clearAll">
          清空
        </button>
        <button class="control-btn" @click="copyToClipboard" :disabled="!outputJson">
          复制结果
        </button>
      </div>

      <div v-if="error" class="error-message">
        <strong>错误：</strong>{{ error }}
      </div>

      <div class="input-group">
        <label>格式化结果</label>
        <textarea
          v-model="outputJson"
          placeholder="格式化后的 JSON 将显示在这里..."
          class="json-textarea"
          rows="12"
          readonly
        ></textarea>
      </div>

      <div class="stats" v-if="outputJson">
        <div class="stat-item">
          <span class="stat-label">字符数：</span>
          <span class="stat-value">{{ outputJson.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">行数：</span>
          <span class="stat-value">{{ outputJson.split('\n').length }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'JsonFormatter',
  setup() {
    const inputJson = ref('');
    const outputJson = ref('');
    const error = ref('');

    const formatJson = () => {
      error.value = '';
      try {
        const parsed = JSON.parse(inputJson.value);
        outputJson.value = JSON.stringify(parsed, null, 2);
      } catch (e) {
        error.value = e.message;
        outputJson.value = '';
      }
    };

    const minifyJson = () => {
      error.value = '';
      try {
        const parsed = JSON.parse(inputJson.value);
        outputJson.value = JSON.stringify(parsed);
      } catch (e) {
        error.value = e.message;
        outputJson.value = '';
      }
    };

    const clearAll = () => {
      inputJson.value = '';
      outputJson.value = '';
      error.value = '';
    };

    const copyToClipboard = async () => {
      try {
        await navigator.clipboard.writeText(outputJson.value);
        alert('已复制到剪贴板！');
      } catch (e) {
        console.error('复制失败:', e);
      }
    };

    return {
      inputJson,
      outputJson,
      error,
      formatJson,
      minifyJson,
      clearAll,
      copyToClipboard
    };
  }
};
</script>

<style scoped>
.json-formatter {
  width: 100%;
}

.tool-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group label {
  font-weight: 600;
  color: #333;
  font-size: 16px;
}

.json-textarea {
  width: 100%;
  padding: 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.json-textarea:focus {
  outline: none;
  border-color: #4dabf7;
}

.json-textarea[readonly] {
  background-color: #f8f9fa;
  color: #495057;
}

.controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.control-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  color: #333;
  border: 2px solid #dee2e6;
}

.control-btn:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #adb5bd;
}

.control-btn:active:not(:disabled) {
  transform: translateY(1px);
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.control-btn.primary {
  background: #4dabf7;
  color: white;
  border-color: #4dabf7;
}

.control-btn.primary:hover:not(:disabled) {
  background: #339af0;
  border-color: #339af0;
}

.error-message {
  padding: 15px;
  background: #fff5f5;
  border: 2px solid #ff6b6b;
  border-radius: 8px;
  color: #c92a2a;
  font-size: 14px;
}

.stats {
  display: flex;
  gap: 30px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  gap: 8px;
}

.stat-label {
  color: #666;
  font-weight: 500;
}

.stat-value {
  color: #333;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

@media (max-width: 768px) {
  .controls {
    flex-direction: column;
  }

  .control-btn {
    width: 100%;
  }
}
</style>
