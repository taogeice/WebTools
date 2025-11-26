<template>
  <div class="url-tool">
    <div class="tool-section">
      <div class="input-group">
        <label>URL 编码</label>
        <textarea
          v-model="inputText"
          placeholder="在此输入要编码的 URL..."
          class="text-textarea"
          rows="6"
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn primary" @click="encodeUrl" :disabled="!inputText">
          编码
        </button>
        <button class="control-btn" @click="clearEncode">
          清空
        </button>
      </div>

      <div class="input-group">
        <label>编码结果</label>
        <textarea
          v-model="encodedText"
          placeholder="URL 编码结果将显示在这里..."
          class="text-textarea"
          rows="6"
          readonly
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn" @click="copyEncoded" :disabled="!encodedText">
          复制
        </button>
      </div>

      <div class="divider"></div>

      <div class="input-group">
        <label>URL 解码</label>
        <textarea
          v-model="inputEncoded"
          placeholder="在此输入要解码的 URL 编码字符串..."
          class="text-textarea"
          rows="6"
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn primary" @click="decodeUrl" :disabled="!inputEncoded">
          解码
        </button>
        <button class="control-btn" @click="clearDecode">
          清空
        </button>
      </div>

      <div v-if="decodeError" class="error-message">
        <strong>解码错误：</strong>{{ decodeError }}
      </div>

      <div class="input-group">
        <label>解码结果</label>
        <textarea
          v-model="decodedText"
          placeholder="URL 解码结果将显示在这里..."
          class="text-textarea"
          rows="6"
          readonly
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn" @click="copyDecoded" :disabled="!decodedText">
          复制
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'UrlTool',
  setup() {
    const inputText = ref('');
    const encodedText = ref('');
    const inputEncoded = ref('');
    const decodedText = ref('');
    const decodeError = ref('');

    const encodeUrl = () => {
      try {
        encodedText.value = encodeURIComponent(inputText.value);
      } catch (e) {
        encodedText.value = '编码失败';
      }
    };

    const decodeUrl = () => {
      decodeError.value = '';
      try {
        decodedText.value = decodeURIComponent(inputEncoded.value);
      } catch (e) {
        decodeError.value = e.message;
        decodedText.value = '';
      }
    };

    const clearEncode = () => {
      inputText.value = '';
      encodedText.value = '';
    };

    const clearDecode = () => {
      inputEncoded.value = '';
      decodedText.value = '';
      decodeError.value = '';
    };

    const copyEncoded = async () => {
      try {
        await navigator.clipboard.writeText(encodedText.value);
        alert('已复制到剪贴板！');
      } catch (e) {
        console.error('复制失败:', e);
      }
    };

    const copyDecoded = async () => {
      try {
        await navigator.clipboard.writeText(decodedText.value);
        alert('已复制到剪贴板！');
      } catch (e) {
        console.error('复制失败:', e);
      }
    };

    return {
      inputText,
      encodedText,
      inputEncoded,
      decodedText,
      decodeError,
      encodeUrl,
      decodeUrl,
      clearEncode,
      clearDecode,
      copyEncoded,
      copyDecoded
    };
  }
};
</script>

<style scoped>
.url-tool {
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

.text-textarea {
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

.text-textarea:focus {
  outline: none;
  border-color: #4dabf7;
}

.text-textarea[readonly] {
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

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, #dee2e6, transparent);
  margin: 10px 0;
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
