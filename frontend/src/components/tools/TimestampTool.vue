<template>
  <div class="timestamp-tool">
    <div class="tool-section">
      <!-- 时间戳转日期 -->
      <div class="converter-section">
        <h3 class="section-title">时间戳转日期</h3>

        <div class="input-group">
          <label>Unix 时间戳 (秒)</label>
          <input
            v-model="timestampSeconds"
            type="number"
            placeholder="输入时间戳..."
            class="timestamp-input"
            @input="convertTimestampToDate"
          />
        </div>

        <div class="input-group">
          <label>日期时间</label>
          <input
            v-model="dateString"
            type="text"
            class="result-input"
            readonly
            placeholder="转换结果将显示在这里..."
          />
          <button class="control-btn" @click="copyDateString" :disabled="!dateString">
            复制
          </button>
        </div>

        <div class="quick-buttons">
          <button class="quick-btn" @click="setCurrentTimestamp">
            当前时间戳
          </button>
          <button class="quick-btn" @click="setZeroTimestamp">
            1970-01-01
          </button>
        </div>
      </div>

      <div class="divider"></div>

      <!-- 日期转时间戳 -->
      <div class="converter-section">
        <h3 class="section-title">日期转时间戳</h3>

        <div class="input-group">
          <label>选择日期时间</label>
          <input
            v-model="selectedDateTime"
            type="datetime-local"
            class="datetime-input"
            @change="convertDateToTimestamp"
          />
        </div>

        <div class="input-group">
          <label>Unix 时间戳 (秒)</label>
          <input
            v-model="outputTimestamp"
            type="text"
            class="result-input"
            readonly
            placeholder="转换结果将显示在这里..."
          />
          <button class="control-btn" @click="copyOutputTimestamp" :disabled="!outputTimestamp">
            复制
          </button>
        </div>

        <div class="quick-buttons">
          <button class="quick-btn" @click="setCurrentDateTime">
            当前时间
          </button>
        </div>
      </div>

      <div class="divider"></div>

      <!-- 常用时间戳 -->
      <div class="converter-section">
        <h3 class="section-title">常用时间戳</h3>
        <div class="timestamps-grid">
          <div class="timestamp-item">
            <span class="timestamp-label">当前时间戳：</span>
            <span class="timestamp-value">{{ currentTimestamp }}</span>
            <button class="small-btn" @click="copyValue(currentTimestamp)">复制</button>
          </div>
          <div class="timestamp-item">
            <span class="timestamp-label">今天开始：</span>
            <span class="timestamp-value">{{ todayStart }}</span>
            <button class="small-btn" @click="copyValue(todayStart)">复制</button>
          </div>
          <div class="timestamp-item">
            <span class="timestamp-label">本周开始：</span>
            <span class="timestamp-value">{{ weekStart }}</span>
            <button class="small-btn" @click="copyValue(weekStart)">复制</button>
          </div>
          <div class="timestamp-item">
            <span class="timestamp-label">本月开始：</span>
            <span class="timestamp-value">{{ monthStart }}</span>
            <button class="small-btn" @click="copyValue(monthStart)">复制</button>
          </div>
          <div class="timestamp-item">
            <span class="timestamp-label">今年开始：</span>
            <span class="timestamp-value">{{ yearStart }}</span>
            <button class="small-btn" @click="copyValue(yearStart)">复制</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';

export default {
  name: 'TimestampTool',
  setup() {
    const timestampSeconds = ref('');
    const dateString = ref('');
    const selectedDateTime = ref('');
    const outputTimestamp = ref('');
    const currentTimestamp = ref(0);

    const currentTime = computed(() => new Date());

    const todayStart = computed(() => {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return Math.floor(today.getTime() / 1000);
    });

    const weekStart = computed(() => {
      const now = new Date();
      const day = now.getDay();
      const diff = now.getDate() - day + (day === 0 ? -6 : 1);
      const monday = new Date(now.setDate(diff));
      monday.setHours(0, 0, 0, 0);
      return Math.floor(monday.getTime() / 1000);
    });

    const monthStart = computed(() => {
      const now = new Date();
      const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
      firstDay.setHours(0, 0, 0, 0);
      return Math.floor(firstDay.getTime() / 1000);
    });

    const yearStart = computed(() => {
      const now = new Date();
      const firstDay = new Date(now.getFullYear(), 0, 1);
      firstDay.setHours(0, 0, 0, 0);
      return Math.floor(firstDay.getTime() / 1000);
    });

    let timer = null;

    onMounted(() => {
      updateCurrentTimestamp();
      timer = setInterval(updateCurrentTimestamp, 1000);
    });

    onUnmounted(() => {
      if (timer) {
        clearInterval(timer);
      }
    });

    const updateCurrentTimestamp = () => {
      currentTimestamp.value = Math.floor(Date.now() / 1000);
    };

    const convertTimestampToDate = () => {
      if (!timestampSeconds.value) {
        dateString.value = '';
        return;
      }
      try {
        const timestamp = parseInt(timestampSeconds.value);
        const date = new Date(timestamp * 1000);
        dateString.value = date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false
        });
      } catch (e) {
        dateString.value = '转换失败';
      }
    };

    const convertDateToTimestamp = () => {
      if (!selectedDateTime.value) {
        outputTimestamp.value = '';
        return;
      }
      try {
        const date = new Date(selectedDateTime.value);
        outputTimestamp.value = Math.floor(date.getTime() / 1000).toString();
      } catch (e) {
        outputTimestamp.value = '转换失败';
      }
    };

    const setCurrentTimestamp = () => {
      timestampSeconds.value = currentTimestamp.value.toString();
      convertTimestampToDate();
    };

    const setZeroTimestamp = () => {
      timestampSeconds.value = '0';
      convertTimestampToDate();
    };

    const setCurrentDateTime = () => {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      const hour = String(now.getHours()).padStart(2, '0');
      const minute = String(now.getMinutes()).padStart(2, '0');
      const second = String(now.getSeconds()).padStart(2, '0');
      selectedDateTime.value = `${year}-${month}-${day}T${hour}:${minute}:${second}`;
      convertDateToTimestamp();
    };

    const copyDateString = async () => {
      if (dateString.value) {
        await navigator.clipboard.writeText(dateString.value);
        alert('已复制到剪贴板！');
      }
    };

    const copyOutputTimestamp = async () => {
      if (outputTimestamp.value) {
        await navigator.clipboard.writeText(outputTimestamp.value);
        alert('已复制到剪贴板！');
      }
    };

    const copyValue = async (value) => {
      await navigator.clipboard.writeText(value.toString());
      alert('已复制到剪贴板！');
    };

    return {
      timestampSeconds,
      dateString,
      selectedDateTime,
      outputTimestamp,
      currentTimestamp,
      todayStart,
      weekStart,
      monthStart,
      yearStart,
      convertTimestampToDate,
      convertDateToTimestamp,
      setCurrentTimestamp,
      setZeroTimestamp,
      setCurrentDateTime,
      copyDateString,
      copyOutputTimestamp,
      copyValue
    };
  }
};
</script>

<style scoped>
.timestamp-tool {
  width: 100%;
}

.tool-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.converter-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  font-size: 20px;
  color: #333;
  font-weight: 600;
  margin: 0;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group label {
  font-weight: 600;
  color: #333;
  font-size: 15px;
}

.timestamp-input,
.result-input,
.datetime-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 15px;
  font-family: 'Courier New', monospace;
  transition: border-color 0.3s ease;
}

.timestamp-input:focus,
.datetime-input:focus {
  outline: none;
  border-color: #4dabf7;
}

.result-input {
  background-color: #f8f9fa;
  color: #495057;
  display: flex;
  align-items: center;
}

.timestamp-input[readonly] {
  background-color: #f8f9fa;
}

.control-btn {
  padding: 10px 20px;
  margin-left: 10px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #4dabf7;
  color: white;
  white-space: nowrap;
}

.control-btn:hover:not(:disabled) {
  background: #339af0;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quick-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.quick-btn {
  padding: 8px 16px;
  border: 2px solid #4dabf7;
  border-radius: 6px;
  background: white;
  color: #4dabf7;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quick-btn:hover {
  background: #4dabf7;
  color: white;
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, #dee2e6, transparent);
}

.timestamps-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.timestamp-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  flex-wrap: wrap;
}

.timestamp-label {
  font-weight: 600;
  color: #495057;
  min-width: 120px;
}

.timestamp-value {
  font-family: 'Courier New', monospace;
  color: #333;
  flex: 1;
  word-break: break-all;
}

.small-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  background: #4dabf7;
  color: white;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.small-btn:hover {
  background: #339af0;
}

@media (max-width: 768px) {
  .timestamp-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .small-btn {
    width: 100%;
  }

  .control-btn {
    width: 100%;
    margin-left: 0;
    margin-top: 10px;
  }
}
</style>
