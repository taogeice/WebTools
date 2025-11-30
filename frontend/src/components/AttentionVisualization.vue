<template>
  <div class="attention-container">
    <div class="attention-header">
      <h3>
        <span class="header-icon">🧠</span>
        注意力机制可视化
      </h3>
      <div class="attention-controls">
        <button class="control-btn" @click="regenerateData" title="重新生成数据">
          <span>🔄</span> 刷新
        </button>
        <button class="control-btn" @click="toggleAnimation" :class="{ active: isAnimating }" title="切换动画">
          <span v-if="!isAnimating">▶</span>
          <span v-else>⏸</span>
          {{ isAnimating ? '暂停' : '动画' }}
        </button>
      </div>
    </div>
    <div class="attention-visualization-chart" ref="chartRef" :style="{ height: height, width: width }"></div>
    <div class="attention-info">
      <div class="info-item">
        <span class="info-label">高注意力:</span>
        <span class="info-value" :style="{ color: '#00ff88' }">对角线区域</span>
      </div>
      <div class="info-item">
        <span class="info-label">中注意力:</span>
        <span class="info-value" style="color: #ffd43b;">邻近位置</span>
      </div>
      <div class="info-item">
        <span class="info-label">低注意力:</span>
        <span class="info-value" style="color: #339af0;">其他区域</span>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'AttentionVisualization',
  props: {
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '450px'
    },
    attentionWeights: {
      type: Array,
      default: () => []
    },
    sourceTokens: {
      type: Array,
      default: () => ['The', 'Transformer', 'model', 'is', 'powerful']
    },
    targetTokens: {
      type: Array,
      default: () => ['Le', 'modèle', 'Transformer', 'est', 'puissant']
    }
  },
  data() {
    return {
      chart: null,
      isAnimating: false,
      animationTimer: null,
      colorSchemes: [
        ['#001f3f', '#0074D9', '#00f2ff', '#ffffff'],
        ['#3d0000', '#ff0000', '#ff7f7f', '#ffffff'],
        ['#1a0033', '#4d0099', '#b366ff', '#ffffff'],
        ['#003300', '#00cc44', '#99ff99', '#ffffff']
      ],
      currentColorIndex: 0
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
    });
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
    if (this.animationTimer) {
      clearInterval(this.animationTimer);
    }
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.chartRef);
      this.setOptions();
    },
    setOptions() {
      // 如果没有提供注意力权重，则生成模拟数据
      const weights = this.attentionWeights.length > 0
        ? this.attentionWeights
        : this.generateMockAttention();

      const currentColors = this.colorSchemes[this.currentColorIndex];

      const option = {
        title: {
          text: '',
          left: 'center',
          top: 10
        },
        tooltip: {
          position: 'top',
          backgroundColor: 'rgba(0, 20, 40, 0.95)',
          borderColor: '#00f2ff',
          borderWidth: 1,
          textStyle: {
            color: '#e0e0e0'
          },
          formatter: (params) => {
            return `<div style="padding: 8px;">
              <div style="font-weight: bold; margin-bottom: 5px; color: #00f2ff;">
                ${this.targetTokens[params.data[1]]} → ${this.sourceTokens[params.data[0]]}
              </div>
              <div>权重: <span style="color: #00ff88;">${(params.data[2] * 100).toFixed(1)}%</span></div>
            </div>`;
          }
        },
        grid: {
          height: '60%',
          top: '15%',
          left: '10%',
          right: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.sourceTokens,
          splitArea: {
            show: true,
            areaStyle: {
              color: ['rgba(0, 50, 100, 0.3)', 'rgba(0, 30, 60, 0.3)']
            }
          },
          axisLine: {
            lineStyle: {
              color: '#00f2ff'
            }
          },
          axisLabel: {
            color: '#b0c4de',
            fontSize: 13,
            fontWeight: 'bold'
          },
          axisTick: {
            show: false
          }
        },
        yAxis: {
          type: 'category',
          data: this.targetTokens,
          splitArea: {
            show: true,
            areaStyle: {
              color: ['rgba(0, 50, 100, 0.3)', 'rgba(0, 30, 60, 0.3)']
            }
          },
          axisLine: {
            lineStyle: {
              color: '#00f2ff'
            }
          },
          axisLabel: {
            color: '#b0c4de',
            fontSize: 13,
            fontWeight: 'bold'
          },
          axisTick: {
            show: false
          }
        },
        visualMap: {
          min: 0,
          max: 1,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '5%',
          inRange: {
            color: currentColors
          },
          textStyle: {
            color: '#e0e0e0',
            fontSize: 12
          },
          itemWidth: 12,
          itemHeight: 80
        },
        series: [{
          name: '注意力权重',
          type: 'heatmap',
          data: weights,
          label: {
            show: true,
            formatter: (params) => {
              return params.data[2] > 0.3 ? `${(params.data[2] * 100).toFixed(0)}%` : '';
            },
            color: '#fff',
            fontSize: 11,
            fontWeight: 'bold'
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 15,
              shadowColor: 'rgba(0, 242, 255, 0.8)',
              borderWidth: 2,
              borderColor: '#00f2ff'
            }
          },
          itemStyle: {
            borderColor: 'rgba(0, 0, 0, 0.3)',
            borderWidth: 1
          },
          animation: true,
          animationDuration: 800,
          animationEasing: 'cubicOut'
        }]
      };

      this.chart.setOption(option, true);
    },
    generateMockAttention() {
      const weights = [];
      for (let i = 0; i < this.sourceTokens.length; i++) {
        for (let j = 0; j < this.targetTokens.length; j++) {
          // 生成模拟的注意力权重
          let weight;
          if (i === j) {
            weight = 0.7 + Math.random() * 0.3; // 对角线位置权重较高
          } else if (Math.abs(i - j) === 1) {
            weight = 0.3 + Math.random() * 0.4; // 邻近位置权重中等
          } else {
            weight = Math.random() * 0.3; // 其他位置权重较低
          }
          weights.push([i, j, parseFloat(weight.toFixed(3))]);
        }
      }
      return weights;
    },
    regenerateData() {
      // 重新生成模拟数据
      const weights = this.generateMockAttention();
      this.chart.setOption({
        series: [{
          data: weights
        }]
      });

      // 添加闪烁效果提示用户
      const container = this.$el.querySelector('.attention-container');
      container.style.animation = 'flashEffect 0.5s ease';
      setTimeout(() => {
        container.style.animation = '';
      }, 500);
    },
    toggleAnimation() {
      this.isAnimating = !this.isAnimating;

      if (this.isAnimating) {
        // 开始动画：自动切换颜色主题
        this.animationTimer = setInterval(() => {
          this.currentColorIndex = (this.currentColorIndex + 1) % this.colorSchemes.length;
          this.setOptions();
        }, 3000);
      } else {
        // 停止动画
        if (this.animationTimer) {
          clearInterval(this.animationTimer);
          this.animationTimer = null;
        }
      }
    }
  },
  watch: {
    attentionWeights: {
      handler() {
        if (this.chart) {
          this.setOptions();
        }
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.attention-container {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.attention-container:hover {
  border-color: rgba(0, 242, 255, 0.4);
  box-shadow: 0 8px 24px rgba(0, 150, 255, 0.3);
}

.attention-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(0, 242, 255, 0.2);
}

.attention-header h3 {
  margin: 0;
  color: #00f2ff;
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  font-size: 24px;
  animation: iconPulse 2s infinite;
}

.attention-controls {
  display: flex;
  gap: 10px;
}

.control-btn {
  padding: 6px 14px;
  background: rgba(0, 100, 150, 0.3);
  border: 1px solid rgba(0, 150, 255, 0.5);
  border-radius: 6px;
  color: #00f2ff;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.control-btn:hover {
  background: rgba(0, 150, 255, 0.5);
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.6);
  transform: translateY(-2px);
}

.control-btn.active {
  background: rgba(0, 255, 136, 0.3);
  border-color: rgba(0, 255, 136, 0.6);
  color: #00ff88;
}

.attention-visualization-chart {
  margin: 10px 0;
}

.attention-info {
  display: flex;
  justify-content: center;
  gap: 25px;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(0, 242, 255, 0.1);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.info-label {
  color: #8899aa;
}

.info-value {
  font-weight: bold;
  padding: 4px 10px;
  background: rgba(0, 50, 100, 0.3);
  border-radius: 4px;
  border: 1px solid rgba(0, 150, 255, 0.3);
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

@keyframes flashEffect {
  0% {
    box-shadow: 0 0 0 rgba(0, 242, 255, 0);
  }
  50% {
    box-shadow: 0 0 30px rgba(0, 242, 255, 0.8);
  }
  100% {
    box-shadow: 0 0 0 rgba(0, 242, 255, 0);
  }
}

@media (max-width: 768px) {
  .attention-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .attention-info {
    flex-wrap: wrap;
    gap: 15px;
  }

  .attention-header h3 {
    font-size: 18px;
  }
}
</style>