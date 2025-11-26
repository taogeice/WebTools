<template>
  <div class="gold-price-chart">
    <div class="chart-header">
      <h2>{{ chartTitle }}</h2>
      <div class="market-toggle">
        <button
          v-for="market in markets"
          :key="market.value"
          :class="['market-btn', { active: selectedMarket === market.value }]"
          @click="selectMarket(market.value)"
        >
          {{ market.label }}
        </button>
      </div>
    </div>

    <div class="chart-controls">
      <div class="date-range">
        <label>
          开始日期：
          <input type="date" v-model="startDate" @change="loadData" />
        </label>
        <label>
          结束日期：
          <input type="date" v-model="endDate" @change="loadData" />
        </label>
      </div>

      <div class="chart-type">
        <label>
          图表类型：
          <select v-model="chartType" @change="updateChart">
            <option value="line">折线图</option>
            <option value="bar">柱状图</option>
            <option value="candlestick">K线图</option>
          </select>
        </label>
      </div>

      <button class="sync-btn" @click="syncData" :disabled="loading">
        {{ loading ? '同步中...' : '同步数据' }}
      </button>
    </div>

    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-else class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>

    <div v-if="chartData.length > 0" class="chart-summary">
      <div class="summary-item">
        <span class="label">最高价：</span>
        <span class="value">{{ maxPrice.toFixed(2) }}</span>
      </div>
      <div class="summary-item">
        <span class="label">最低价：</span>
        <span class="value">{{ minPrice.toFixed(2) }}</span>
      </div>
      <div class="summary-item">
        <span class="label">平均价：</span>
        <span class="value">{{ avgPrice.toFixed(2) }}</span>
      </div>
      <div class="summary-item">
        <span class="label">最新价：</span>
        <span class="value">{{ latestPrice.toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import { format, subDays } from 'date-fns';
import goldAPI from '../api/gold.js';

Chart.register(...registerables);

export default {
  name: 'GoldPriceChart',
  setup() {
    const chartCanvas = ref(null);
    const chart = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const selectedMarket = ref('domestic');
    const chartType = ref('line');
    const chartData = ref([]);

    const markets = [
      { value: 'domestic', label: '国内黄金' },
      { value: 'international', label: '国际黄金' }
    ];

    // 日期范围（默认30天）
    const today = new Date();
    const thirtyDaysAgo = subDays(today, 30);
    const startDate = ref(format(thirtyDaysAgo, 'yyyy-MM-dd'));
    const endDate = ref(format(today, 'yyyy-MM-dd'));

    const chartTitle = computed(() => {
      const market = markets.find(m => m.value === selectedMarket.value);
      return `${market?.label || ''}价格走势`;
    });

    const maxPrice = computed(() => {
      if (!chartData.value.length) return 0;
      return Math.max(...chartData.value.map(d => d.close_price));
    });

    const minPrice = computed(() => {
      if (!chartData.value.length) return 0;
      return Math.min(...chartData.value.map(d => d.close_price));
    });

    const avgPrice = computed(() => {
      if (!chartData.value.length) return 0;
      const sum = chartData.value.reduce((acc, d) => acc + d.close_price, 0);
      return sum / chartData.value.length;
    });

    const latestPrice = computed(() => {
      if (!chartData.value.length) return 0;
      return chartData.value[chartData.value.length - 1].close_price;
    });

    const selectMarket = (market) => {
      selectedMarket.value = market;
      loadData();
    };

    const loadData = async () => {
      loading.value = true;
      error.value = null;

      try {
        const response = await goldAPI.getGoldPriceData(
          selectedMarket.value,
          startDate.value,
          endDate.value
        );

        chartData.value = response.data || [];
        await nextTick();
        updateChart();
      } catch (err) {
        error.value = err.message || '加载数据失败';
        console.error('加载数据失败:', err);
      } finally {
        loading.value = false;
      }
    };

    const syncData = async () => {
      loading.value = true;
      error.value = null;

      try {
        await goldAPI.syncGoldPriceData(startDate.value, endDate.value);
        await loadData();
        alert('数据同步成功！');
      } catch (err) {
        error.value = err.message || '同步数据失败';
        console.error('同步数据失败:', err);
      } finally {
        loading.value = false;
      }
    };

    const updateChart = async () => {
      if (!chartCanvas.value || !chartData.value.length) return;

      // 销毁旧图表
      if (chart.value) {
        chart.value.destroy();
      }

      const ctx = chartCanvas.value.getContext('2d');

      // 准备数据
      const labels = chartData.value.map(d => format(new Date(d.date), 'MM/dd'));
      const prices = chartData.value.map(d => d.close_price);

      // 配置图表
      const config = {
        type: chartType.value === 'candlestick' ? 'line' : chartType.value,
        data: {
          labels: labels,
          datasets: [
            {
              label: '收盘价',
              data: prices,
              borderColor: selectedMarket.value === 'domestic' ? '#ff6b6b' : '#4dabf7',
              backgroundColor: selectedMarket.value === 'domestic'
                ? 'rgba(255, 107, 107, 0.1)'
                : 'rgba(77, 171, 247, 0.1)',
              tension: 0.4,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            },
            title: {
              display: true,
              text: chartTitle.value
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              callbacks: {
                label: (context) => {
                  return `${context.dataset.label}: ${context.parsed.y.toFixed(2)}`;
                }
              }
            }
          },
          scales: {
            x: {
              display: true,
              title: {
                display: true,
                text: '日期'
              }
            },
            y: {
              display: true,
              title: {
                display: true,
                text: '价格'
              },
              ticks: {
                callback: (value) => {
                  return value.toFixed(2);
                }
              }
            }
          }
        }
      };

      chart.value = new Chart(ctx, config);
    };

    onMounted(() => {
      loadData();
    });

    return {
      chartCanvas,
      loading,
      error,
      selectedMarket,
      chartType,
      chartData,
      markets,
      startDate,
      endDate,
      chartTitle,
      maxPrice,
      minPrice,
      avgPrice,
      latestPrice,
      selectMarket,
      loadData,
      syncData,
      updateChart
    };
  }
};
</script>

<style scoped>
.gold-price-chart {
  padding: 30px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.chart-header h2 {
  margin: 0;
  font-size: 28px;
  color: #00f2ff;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
}

.market-toggle {
  display: flex;
  gap: 12px;
}

.market-btn {
  padding: 10px 20px;
  border: 1px solid rgba(0, 242, 255, 0.3);
  background: rgba(0, 242, 255, 0.05);
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  color: #8899aa;
  transition: all 0.3s ease;
}

.market-btn:hover {
  border-color: #00f2ff;
  background: rgba(0, 242, 255, 0.1);
  color: #00f2ff;
  box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
}

.market-btn.active {
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.2) 0%, rgba(0, 132, 255, 0.2) 100%);
  border-color: #00f2ff;
  color: #fff;
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
}

.chart-controls {
  display: flex;
  gap: 20px;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(0, 242, 255, 0.1);
}

.date-range,
.chart-type {
  display: flex;
  gap: 12px;
  align-items: center;
}

.date-range label,
.chart-type label {
  font-size: 14px;
  color: #8899aa;
  font-weight: 500;
}

.date-range input,
.chart-type select {
  padding: 8px 12px;
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 6px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  outline: none;
  transition: all 0.3s;
}

.date-range input:focus,
.chart-type select:focus {
  border-color: #00f2ff;
  box-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
}

.sync-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.2) 0%, rgba(0, 132, 255, 0.2) 100%);
  color: #00f2ff;
  border: 1px solid #00f2ff;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.sync-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.3) 0%, rgba(0, 132, 255, 0.3) 100%);
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
  transform: translateY(-2px);
}

.sync-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading,
.error {
  text-align: center;
  padding: 60px 40px;
  font-size: 18px;
  color: #8899aa;
}

.error {
  color: #ff6b6b;
}

.chart-container {
  width: 100%;
  height: 500px;
  margin: 30px 0;
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(0, 242, 255, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-container canvas {
  max-width: 100%;
  height: auto !important;
}

.chart-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 25px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  margin-top: 30px;
  border: 1px solid rgba(0, 242, 255, 0.1);
}

.summary-item {
  text-align: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(0, 242, 255, 0.1);
  transition: all 0.3s;
}

.summary-item:hover {
  border-color: #00f2ff;
  box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
  transform: translateY(-2px);
}

.summary-item .label {
  display: block;
  font-size: 14px;
  color: #8899aa;
  margin-bottom: 8px;
  font-weight: 500;
}

.summary-item .value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #00f2ff;
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }

  .chart-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .date-range,
  .chart-type {
    flex-direction: column;
    align-items: stretch;
  }

  .chart-summary {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}
</style>
