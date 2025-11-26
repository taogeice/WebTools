<template>
  <div class="base64-tool">
    <div class="tool-section">
      <div class="input-group">
        <label>文本输入</label>
        <textarea
          v-model="inputText"
          placeholder="在此输入要编码的文本..."
          class="text-textarea"
          rows="6"
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn primary" @click="encodeText" :disabled="!inputText">
          编码为 Base64
        </button>
        <button class="control-btn" @click="clearInput">
          清空输入
        </button>
      </div>

      <div class="input-group">
        <label>Base64 输出</label>
        <textarea
          v-model="encodedText"
          placeholder="Base64 编码结果将显示在这里..."
          class="text-textarea"
          rows="6"
          readonly
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn" @click="copyEncoded" :disabled="!encodedText">
          复制编码结果
        </button>
      </div>

      <div class="divider"></div>

      <div class="input-group">
        <label>Base64 输入</label>
        <textarea
          v-model="inputBase64"
          placeholder="在此输入要解码的 Base64 字符串..."
          class="text-textarea"
          rows="6"
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn primary" @click="decodeText" :disabled="!inputBase64">
          解码为文本
        </button>
        <button class="control-btn" @click="clearDecodeInput">
          清空输入
        </button>
      </div>

      <div v-if="decodeError" class="error-message">
        <strong>解码错误：</strong>{{ decodeError }}
      </div>

      <div class="input-group">
        <label>解码结果</label>
        <textarea
          v-model="decodedText"
          placeholder="Base64 解码结果将显示在这里..."
          class="text-textarea"
          rows="6"
          readonly
        ></textarea>
      </div>

      <div class="controls">
        <button class="control-btn" @click="copyDecoded" :disabled="!decodedText">
          复制解码结果
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'Base64Tool',
  setup() {
    const inputText = ref('');
    const encodedText = ref('');
    const inputBase64 = ref('');
    const decodedText = ref('');
    const decodeError = ref('');

    const encodeText = () => {
      try {
        encodedText.value = btoa(inputText.value);
      } catch (e) {
        console.error('编码错误:', e);
        encodedText.value = '编码失败';
      }
    };

    const decodeText = () => {
      decodeError.value = '';
      try {
        decodedText.value = atob(inputBase64.value);
      } catch (e) {
        decodeError.value = e.message;
        decodedText.value = '';
      }
    };

    const clearInput = () => {
      inputText.value = '';
      encodedText.value = '';
    };

    const clearDecodeInput = () => {
      inputBase64.value = '';
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
      inputBase64,
      decodedText,
      decodeError,
      encodeText,
      decodeText,
      clearInput,
      clearDecodeInput,
      copyEncoded,
      copyDecoded
    };
  }
};
</script>

<style scoped>
.base64-tool {
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
