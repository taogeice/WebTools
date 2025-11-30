<template>
  <div class="attention-visualization-chart" ref="chartRef" :style="{ height: height, width: width }"></div>
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
      default: '400px'
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
  mounted() {
    this.$nextTick(() => {
      this.initChart();
    });
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
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

      const option = {
        title: {
          text: '注意力权重热力图',
          left: 'center',
          textStyle: {
            color: '#00f2ff'
          }
        },
        tooltip: {
          position: 'top',
          formatter: (params) => {
            return `${this.targetTokens[params.data[1]]} → ${this.sourceTokens[params.data[0]]}<br/>权重: ${(params.data[2]).toFixed(3)}`;
          }
        },
        grid: {
          height: '50%',
          top: '15%'
        },
        xAxis: {
          type: 'category',
          data: this.sourceTokens,
          splitArea: {
            show: true
          },
          axisLabel: {
            color: '#e0e0e0'
          }
        },
        yAxis: {
          type: 'category',
          data: this.targetTokens,
          splitArea: {
            show: true
          },
          axisLabel: {
            color: '#e0e0e0'
          }
        },
        visualMap: {
          min: 0,
          max: 1,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '15%',
          inRange: {
            color: ['#003', '#00f', '#0ff', '#fff']
          }
        },
        series: [{
          name: '注意力权重',
          type: 'heatmap',
          data: weights,
          label: {
            show: true,
            formatter: (params) => {
              return params.data[2] > 0.3 ? params.data[2].toFixed(2) : '';
            },
            color: '#fff',
            fontSize: 10
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      };

      this.chart.setOption(option);
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
.attention-visualization-chart {
  margin-top: 20px;
}
</style>