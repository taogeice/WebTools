<template>
  <div class="color-tool">
    <div class="tool-section">
      <div class="color-picker-section">
        <div class="color-preview" :style="{ backgroundColor: selectedColor }"></div>
        <input
          type="color"
          v-model="selectedColor"
          class="color-input"
        />
      </div>

      <div class="color-formats">
        <h3 class="section-title">颜色格式</h3>

        <div class="format-group">
          <label>十六进制</label>
          <div class="format-input-group">
            <input
              v-model="hexColor"
              @input="updateFromHex"
              type="text"
              class="format-input"
              placeholder="#000000"
            />
            <button class="copy-btn" @click="copyToClipboard(hexColor)">复制</button>
          </div>
        </div>

        <div class="format-group">
          <label>RGB</label>
          <div class="format-input-group">
            <input
              :value="rgbColor"
              type="text"
              class="format-input"
              placeholder="rgb(0, 0, 0)"
              readonly
            />
            <button class="copy-btn" @click="copyToClipboard(rgbColor)">复制</button>
          </div>
        </div>

        <div class="format-group">
          <label>RGBA</label>
          <div class="format-input-group">
            <input
              :value="rgbaColor"
              type="text"
              class="format-input"
              placeholder="rgba(0, 0, 0, 1)"
              readonly
            />
            <button class="copy-btn" @click="copyToClipboard(rgbaColor)">复制</button>
          </div>
        </div>

        <div class="format-group">
          <label>HSL</label>
          <div class="format-input-group">
            <input
              :value="hslColor"
              type="text"
              class="format-input"
              placeholder="hsl(0, 0%, 0%)"
              readonly
            />
            <button class="copy-btn" @click="copyToClipboard(hslColor)">复制</button>
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="rgba-inputs">
        <h3 class="section-title">手动调整 RGBA</h3>
        <div class="rgba-sliders">
          <div class="slider-group">
            <label>红色 (R): {{ r }}</label>
            <input
              type="range"
              v-model.number="r"
              min="0"
              max="255"
              class="slider"
              @input="updateFromRGBA"
            />
          </div>
          <div class="slider-group">
            <label>绿色 (G): {{ g }}</label>
            <input
              type="range"
              v-model.number="g"
              min="0"
              max="255"
              class="slider"
              @input="updateFromRGBA"
            />
          </div>
          <div class="slider-group">
            <label>蓝色 (B): {{ b }}</label>
            <input
              type="range"
              v-model.number="b"
              min="0"
              max="255"
              class="slider"
              @input="updateFromRGBA"
            />
          </div>
          <div class="slider-group">
            <label>透明度 (A): {{ alpha.toFixed(2) }}</label>
            <input
              type="range"
              v-model.number="alpha"
              min="0"
              max="1"
              step="0.01"
              class="slider"
              @input="updateFromRGBA"
            />
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="preset-colors">
        <h3 class="section-title">预设颜色</h3>
        <div class="preset-grid">
          <div
            v-for="color in presetColors"
            :key="color"
            class="preset-color"
            :style="{ backgroundColor: color }"
            @click="selectedColor = color; updateFromHex()"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  name: 'ColorTool',
  setup() {
    const selectedColor = ref('#000000');
    const r = ref(0);
    const g = ref(0);
    const b = ref(0);
    const alpha = ref(1);

    const hexColor = computed({
      get: () => selectedColor.value,
      set: (value) => {
        selectedColor.value = value;
        updateFromHex();
      }
    });

    const rgbColor = computed(() => `rgb(${r.value}, ${g.value}, ${b.value})`);

    const rgbaColor = computed(() => `rgba(${r.value}, ${g.value}, ${b.value}, ${alpha.value})`);

    const hslColor = computed(() => {
      const [h, s, l] = rgbToHsl(r.value, g.value, b.value);
      return `hsl(${Math.round(h)}, ${Math.round(s)}%, ${Math.round(l)}%)`;
    });

    const presetColors = [
      '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
      '#FFA500', '#800080', '#FFC0CB', '#A52A2A', '#808080', '#000000',
      '#FFFFFF', '#FFD700', '#C0C0C0', '#FF69B4', '#40E0D0', '#8B4513'
    ];

    const updateFromHex = () => {
      const hex = selectedColor.value.replace('#', '');
      if (hex.length === 6) {
        r.value = parseInt(hex.substr(0, 2), 16);
        g.value = parseInt(hex.substr(2, 2), 16);
        b.value = parseInt(hex.substr(4, 2), 16);
      }
    };

    const updateFromRGBA = () => {
      const hex = `#${toHex(r.value)}${toHex(g.value)}${toHex(b.value)}`;
      selectedColor.value = hex;
    };

    const toHex = (value) => {
      return value.toString(16).padStart(2, '0');
    };

    const rgbToHsl = (r, g, b) => {
      r /= 255;
      g /= 255;
      b /= 255;
      const max = Math.max(r, g, b);
      const min = Math.min(r, g, b);
      let h, s, l = (max + min) / 2;

      if (max === min) {
        h = s = 0;
      } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
          case r: h = (g - b) / d + (g < b ? 6 : 0); break;
          case g: h = (b - r) / d + 2; break;
          case b: h = (r - g) / d + 4; break;
        }
        h *= 60;
      }

      return [h, s * 100, l * 100];
    };

    const copyToClipboard = async (text) => {
      try {
        await navigator.clipboard.writeText(text);
        alert('已复制到剪贴板！');
      } catch (e) {
        console.error('复制失败:', e);
      }
    };

    return {
      selectedColor,
      r,
      g,
      b,
      alpha,
      hexColor,
      rgbColor,
      rgbaColor,
      hslColor,
      presetColors,
      updateFromHex,
      updateFromRGBA,
      copyToClipboard
    };
  }
};
</script>

<style scoped>
.color-tool {
  width: 100%;
}

.tool-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.color-picker-section {
  display: flex;
  gap: 20px;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

.color-preview {
  width: 150px;
  height: 150px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 3px solid white;
}

.color-input {
  width: 80px;
  height: 80px;
  border: none;
  cursor: pointer;
}

.color-formats,
.rgba-inputs,
.preset-colors {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.section-title {
  font-size: 20px;
  color: #333;
  font-weight: 600;
  margin: 0;
}

.format-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.format-group label {
  font-weight: 600;
  color: #495057;
  font-size: 14px;
}

.format-input-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.format-input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.format-input:focus {
  outline: none;
  border-color: #4dabf7;
}

.copy-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  background: #4dabf7;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.copy-btn:hover {
  background: #339af0;
}

.rgba-sliders {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.slider-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.slider-group label {
  font-weight: 600;
  color: #495057;
  font-size: 14px;
}

.slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: #e9ecef;
  outline: none;
  cursor: pointer;
  -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4dabf7;
  cursor: pointer;
  transition: all 0.3s ease;
}

.slider::-webkit-slider-thumb:hover {
  background: #339af0;
  transform: scale(1.1);
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4dabf7;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
}

.slider::-moz-range-thumb:hover {
  background: #339af0;
  transform: scale(1.1);
}

.preset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  gap: 15px;
}

.preset-color {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.preset-color:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, #dee2e6, transparent);
}

@media (max-width: 768px) {
  .color-picker-section {
    flex-direction: column;
    align-items: center;
  }

  .color-preview {
    width: 200px;
    height: 200px;
  }

  .format-input-group {
    flex-direction: column;
  }

  .copy-btn {
    width: 100%;
  }
}
</style>
