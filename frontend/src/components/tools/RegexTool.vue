<template>
  <div class="regex-tool">
    <div class="tool-section">
      <div class="input-group">
        <label>正则表达式</label>
        <input
          v-model="pattern"
          type="text"
          class="pattern-input"
          placeholder="输入正则表达式，例如：\\d+"
        />
      </div>

      <div class="flags-group">
        <label class="flags-label">标志：</label>
        <label class="flag-label">
          <input type="checkbox" v-model="flags.g" value="g" @change="testRegex" />
          g (全局)
        </label>
        <label class="flag-label">
          <input type="checkbox" v-model="flags.i" value="i" @change="testRegex" />
          i (忽略大小写)
        </label>
        <label class="flag-label">
          <input type="checkbox" v-model="flags.m" value="m" @change="testRegex" />
          m (多行)
        </label>
        <label class="flag-label">
          <input type="checkbox" v-model="flags.s" value="s" @change="testRegex" />
          s (dotall)
        </label>
        <label class="flag-label">
          <input type="checkbox" v-model="flags.u" value="u" @change="testRegex" />
          u (unicode)
        </label>
        <label class="flag-label">
          <input type="checkbox" v-model="flags.y" value="y" @change="testRegex" />
          y (粘性)
        </label>
      </div>

      <div class="input-group">
        <label>测试文本</label>
        <textarea
          v-model="testText"
          @input="testRegex"
          placeholder="在此输入要测试的文本..."
          class="test-textarea"
          rows="8"
        ></textarea>
      </div>

      <div v-if="regexError" class="error-message">
        <strong>正则表达式错误：</strong>{{ regexError }}
      </div>

      <div class="divider"></div>

      <div class="results-section">
        <h3 class="section-title">匹配结果</h3>

        <div class="stats">
          <div class="stat-item">
            <span class="stat-label">匹配次数：</span>
            <span class="stat-value">{{ matchCount }}</span>
          </div>
          <div class="stat-item" v-if="matchCount > 0">
            <span class="stat-label">匹配内容：</span>
            <span class="stat-value">{{ matchCount }} 个匹配</span>
          </div>
        </div>

        <div v-if="matches.length > 0" class="matches-list">
          <h4 class="matches-title">匹配详情：</h4>
          <div v-for="(match, index) in matches" :key="index" class="match-item">
            <div class="match-header">
              <span class="match-index">匹配 #{{ index + 1 }}</span>
              <span class="match-position">位置: {{ match.index }}</span>
            </div>
            <div class="match-content">
              <span class="match-text">匹配文本: "{{ match.value }}"</span>
              <div v-if="match.groups && Object.keys(match.groups).length > 0" class="match-groups">
                <strong>捕获组：</strong>
                <div class="groups-list">
                  <div v-for="(value, key) in match.groups" :key="key" class="group-item">
                    <span class="group-name">{{ key }}:</span>
                    <span class="group-value">{{ value }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="pattern && testText && !regexError" class="no-matches">
          <p>未找到匹配项</p>
        </div>
      </div>

      <div class="divider"></div>

      <div class="presets-section">
        <h3 class="section-title">常用正则表达式</h3>
        <div class="presets-grid">
          <div
            v-for="preset in regexPresets"
            :key="preset.name"
            class="preset-item"
            @click="loadPreset(preset)"
          >
            <div class="preset-name">{{ preset.name }}</div>
            <div class="preset-pattern">{{ preset.pattern }}</div>
            <div class="preset-desc">{{ preset.description }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  name: 'RegexTool',
  setup() {
    const pattern = ref('');
    const testText = ref('');
    const flags = ref({
      g: true,
      i: false,
      m: false,
      s: false,
      u: false,
      y: false
    });
    const matches = ref([]);
    const regexError = ref('');

    const matchCount = computed(() => matches.value.length);

    const testRegex = () => {
      matches.value = [];
      regexError.value = '';

      if (!pattern.value) {
        return;
      }

      if (!testText.value) {
        return;
      }

      try {
        const flagsString = Object.keys(flags.value)
          .filter(key => flags.value[key])
          .join('');

        const regex = new RegExp(pattern.value, flagsString);
        const foundMatches = testText.value.match(regex);

        if (foundMatches) {
          const regexForExec = new RegExp(pattern.value, flagsString + (flagsString.includes('g') ? '' : 'g'));
          let match;
          while ((match = regexForExec.exec(testText.value)) !== null) {
            const matchObj = {
              value: match[0],
              index: match.index,
              groups: match.groups || {}
            };
            matches.value.push(matchObj);

            if (match[0] === '' && regexForExec.lastIndex === match.index) {
              regexForExec.lastIndex++;
            }
          }
        }
      } catch (e) {
        regexError.value = e.message;
      }
    };

    const loadPreset = (preset) => {
      pattern.value = preset.pattern;
      testText.value = preset.example;
      flags.value = preset.flags;
      testRegex();
    };

    const regexPresets = [
      {
        name: '邮箱验证',
        pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
        description: '验证邮箱地址格式',
        example: 'user@example.com\ninvalid-email\ntest.user@domain.co.uk',
        flags: { g: true, i: true, m: false, s: false, u: false, y: false }
      },
      {
        name: '手机号验证',
        pattern: '^1[3-9]\\d{9}$',
        description: '验证中国大陆手机号',
        example: '13812345678\n12345678901\n13900111000',
        flags: { g: true, i: false, m: false, s: false, u: false, y: false }
      },
      {
        name: 'URL 验证',
        pattern: 'https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)',
        description: '验证 HTTP/HTTPS URL',
        example: 'https://www.example.com\nhttp://example.com/path\nftp://example.com',
        flags: { g: true, i: true, m: false, s: false, u: false, y: false }
      },
      {
        name: '身份证号',
        pattern: '^[1-9]\\d{5}(18|19|20)\\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$',
        description: '验证18位身份证号码',
        example: '110101199003071234\n123456789012345678',
        flags: { g: true, i: false, m: false, s: false, u: false, y: false }
      },
      {
        name: 'IPv4 地址',
        pattern: '((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
        description: '验证 IPv4 地址',
        example: '192.168.1.1\n255.255.255.255\n0.0.0.0\n999.999.999.999',
        flags: { g: true, i: false, m: false, s: false, u: false, y: false }
      },
      {
        name: '提取数字',
        pattern: '\\d+',
        description: '提取所有数字',
        example: 'abc123def456ghi789',
        flags: { g: true, i: false, m: false, s: false, u: false, y: false }
      }
    ];

    return {
      pattern,
      testText,
      flags,
      matches,
      regexError,
      matchCount,
      regexPresets,
      testRegex,
      loadPreset
    };
  }
};
</script>

<style scoped>
.regex-tool {
  width: 100%;
}

.tool-section {
  display: flex;
  flex-direction: column;
  gap: 25px;
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

.pattern-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 15px;
  transition: border-color 0.3s ease;
}

.pattern-input:focus {
  outline: none;
  border-color: #4dabf7;
}

.flags-group {
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.flags-label {
  font-weight: 600;
  color: #495057;
  margin-right: 10px;
}

.flag-label {
  display: flex;
  gap: 6px;
  align-items: center;
  cursor: pointer;
  color: #495057;
  font-size: 14px;
}

.flag-label input[type="checkbox"] {
  cursor: pointer;
}

.test-textarea {
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

.test-textarea:focus {
  outline: none;
  border-color: #4dabf7;
}

.error-message {
  padding: 15px;
  background: #fff5f5;
  border: 2px solid #ff6b6b;
  border-radius: 8px;
  color: #c92a2a;
  font-size: 14px;
}

.results-section {
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

.matches-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.matches-title {
  font-size: 16px;
  color: #495057;
  font-weight: 600;
  margin: 0 0 10px 0;
}

.match-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #4dabf7;
}

.match-header {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 14px;
}

.match-index {
  font-weight: 700;
  color: #4dabf7;
}

.match-position {
  color: #666;
}

.match-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.match-text {
  font-family: 'Courier New', monospace;
  color: #333;
  font-weight: 600;
}

.match-groups {
  padding: 10px;
  background: white;
  border-radius: 6px;
  font-size: 14px;
}

.groups-list {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding-left: 10px;
}

.group-item {
  display: flex;
  gap: 8px;
  font-family: 'Courier New', monospace;
}

.group-name {
  color: #4dabf7;
  font-weight: 600;
}

.group-value {
  color: #333;
}

.no-matches {
  padding: 20px;
  text-align: center;
  color: #868e96;
  font-size: 16px;
}

.presets-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.presets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.preset-item {
  padding: 15px;
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.preset-item:hover {
  border-color: #4dabf7;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(77, 171, 247, 0.2);
}

.preset-name {
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
  font-size: 15px;
}

.preset-pattern {
  font-family: 'Courier New', monospace;
  color: #4dabf7;
  font-size: 13px;
  margin-bottom: 8px;
  word-break: break-all;
}

.preset-desc {
  color: #666;
  font-size: 13px;
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, #dee2e6, transparent);
}

@media (max-width: 768px) {
  .flags-group {
    flex-direction: column;
    align-items: flex-start;
  }

  .presets-grid {
    grid-template-columns: 1fr;
  }

  .stats {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
