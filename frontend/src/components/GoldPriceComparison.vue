<template>
  <div class="gold-price-comparison">
    <h2>国内外黄金价格对比</h2>

    <div class="comparison-controls">
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

    <div v-else class="comparison-container">
      <div class="charts-row">
        <div class="chart-box">
          <h3>国内黄金</h3>
          <canvas ref="domesticChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>国际黄金</h3>
          <canvas ref="internationalChart"></canvas>
        </div>
      </div>

      <div class="comparison-chart">
        <h3>对比图</h3>
        <canvas ref="comparisonChart"></canvas>
      </div>

      <div class="summary-table">
        <h3>价格对比表</h3>
        <table>
          <thead>
            <tr>
              <th>市场</th>
              <th>平均价格</th>
              <th>最高价</th>
              <th>最低价</th>
              <th>最新价格</th>
              <th>波动率</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>国内黄金</td>
              <td>{{ domesticStats.avg.toFixed(2) }}</td>
              <td>{{ domesticStats.max.toFixed(2) }}</td>
              <td>{{ domesticStats.min.toFixed(2) }}</td>
              <td>{{ domesticStats.latest.toFixed(2) }}</td>
              <td>{{ domesticStats.volatility.toFixed(2) }}%</td>
            </tr>
            <tr>
              <td>国际黄金</td>
              <td>{{ internationalStats.avg.toFixed(2) }}</td>
              <td>{{ internationalStats.max.toFixed(2) }}</td>
              <td>{{ internationalStats.min.toFixed(2) }}</td>
              <td>{{ internationalStats.latest.toFixed(2) }}</td>
              <td>{{ internationalStats.volatility.toFixed(2) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="correlation">
        <h3>相关性分析</h3>
        <p>两市场价格相关系数：<strong>{{ correlation.toFixed(4) }}</strong></p>
        <p class="correlation-note">
          {{ getCorrelationNote(correlation) }}
        </p>
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
  name: 'GoldPriceComparison',
  setup() {
    const domesticChart = ref(null);
    const internationalChart = ref(null);
    const comparisonChart = ref(null);
    const chart = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const domesticData = ref([]);
    const internationalData = ref([]);

    // 日期范围
    const today = new Date();
    const sevenDaysAgo = subDays(today, 7);
    const startDate = ref(format(sevenDaysAgo, 'yyyy-MM-dd'));
    const endDate = ref(format(today, 'yyyy-MM-dd'));

    const loadData = async () => {
      loading.value = true;
      error.value = null;

      try {
        const response = await goldAPI.compareMarkets(
          startDate.value,
          endDate.value
        );

        domesticData.value = response.domestic?.data || [];
        internationalData.value = response.international?.data || [];

        await nextTick();
        renderCharts();
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

    const renderCharts = () => {
      renderIndividualChart(domesticChart.value, domesticData.value, '#ff6b6b', '国内黄金');
      renderIndividualChart(internationalChart.value, internationalData.value, '#4dabf7', '国际黄金');
      renderComparisonChart();
    };

    const renderIndividualChart = (canvas, data, color, label) => {
      if (!canvas || !data.length) return;

      const ctx = canvas.getContext('2d');
      const labels = data.map(d => format(new Date(d.date), 'MM/dd'));
      const prices = data.map(d => d.close_price);

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: label,
              data: prices,
              borderColor: color,
              backgroundColor: color.replace(')', ', 0.1)').replace('rgb', 'rgba'),
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
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: (value) => value.toFixed(2)
              }
            }
          }
        }
      });
    };

    const renderComparisonChart = () => {
      if (!comparisonChart.value || !domesticData.value.length || !internationalData.value.length) return;

      const ctx = comparisonChart.value.getContext('2d');

      // 对齐数据
      const domesticMap = new Map(domesticData.value.map(d => [format(new Date(d.date), 'MM/dd'), d.close_price]));
      const internationalMap = new Map(internationalData.value.map(d => [format(new Date(d.date), 'MM/dd'), d.close_price]));

      const allDates = Array.from(new Set([
        ...Array.from(domesticMap.keys()),
        ...Array.from(internationalMap.keys())
      ])).sort();

      const domesticPrices = allDates.map(date => domesticMap.get(date) || null);
      const internationalPrices = allDates.map(date => internationalMap.get(date) || null);

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: allDates,
          datasets: [
            {
              label: '国内黄金',
              data: domesticPrices,
              borderColor: '#ff6b6b',
              backgroundColor: 'rgba(255, 107, 107, 0.1)',
              tension: 0.4,
              fill: false
            },
            {
              label: '国际黄金',
              data: internationalPrices,
              borderColor: '#4dabf7',
              backgroundColor: 'rgba(77, 171, 247, 0.1)',
              tension: 0.4,
              fill: false
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
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: (value) => value.toFixed(2)
              }
            }
          }
        }
      });
    };

    // 计算统计数据
    const domesticStats = computed(() => {
      if (!domesticData.value.length) return { avg: 0, max: 0, min: 0, latest: 0, volatility: 0 };
      const prices = domesticData.value.map(d => d.close_price);
      return {
        avg: prices.reduce((a, b) => a + b, 0) / prices.length,
        max: Math.max(...prices),
        min: Math.min(...prices),
        latest: prices[prices.length - 1],
        volatility: ((Math.max(...prices) - Math.min(...prices)) / Math.min(...prices)) * 100
      };
    });

    const internationalStats = computed(() => {
      if (!internationalData.value.length) return { avg: 0, max: 0, min: 0, latest: 0, volatility: 0 };
      const prices = internationalData.value.map(d => d.close_price);
      return {
        avg: prices.reduce((a, b) => a + b, 0) / prices.length,
        max: Math.max(...prices),
        min: Math.min(...prices),
        latest: prices[prices.length - 1],
        volatility: ((Math.max(...prices) - Math.min(...prices)) / Math.min(...prices)) * 100
      };
    });

    // 计算相关系数
    const correlation = computed(() => {
      if (!domesticData.value.length || !internationalData.value.length) return 0;

      // 对齐数据
      const domesticMap = new Map(domesticData.value.map(d => [new Date(d.date).getTime(), d.close_price]));
      const internationalMap = new Map(internationalData.value.map(d => [new Date(d.date).getTime(), d.close_price]));

      const commonDates = Array.from(domesticMap.keys()).filter(date => internationalMap.has(date));

      if (commonDates.length < 2) return 0;

      const domesticPrices = commonDates.map(date => domesticMap.get(date));
      const internationalPrices = commonDates.map(date => internationalMap.get(date));

      // 计算相关系数
      const n = domesticPrices.length;
      const sumX = domesticPrices.reduce((a, b) => a + b, 0);
      const sumY = internationalPrices.reduce((a, b) => a + b, 0);
      const sumXY = domesticPrices.reduce((acc, x, i) => acc + x * internationalPrices[i], 0);
      const sumX2 = domesticPrices.reduce((acc, x) => acc + x * x, 0);
      const sumY2 = internationalPrices.reduce((acc, y) => acc + y * y, 0);

      const numerator = n * sumXY - sumX * sumY;
      const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));

      return denominator === 0 ? 0 : numerator / denominator;
    });

    const getCorrelationNote = (corr) => {
      if (corr > 0.8) return '两市场高度正相关，趋势非常一致';
      if (corr > 0.5) return '两市场正相关，趋势较为一致';
      if (corr > 0.2) return '两市场弱正相关，存在一定关联性';
      if (corr > -0.2) return '两市场相关性较弱';
      if (corr > -0.5) return '两市场负相关，趋势相反';
      return '两市场高度负相关，趋势完全相反';
    };

    onMounted(() => {
      loadData();
    });

    return {
      domesticChart,
      internationalChart,
      comparisonChart,
      loading,
      error,
      startDate,
      endDate,
      domesticStats,
      internationalStats,
      correlation,
      getCorrelationNote,
      loadData,
      syncData
    };
  }
};
</script>

<style scoped>
.gold-price-comparison {
  padding: 30px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

h2 {
  margin: 0 0 30px 0;
  font-size: 32px;
  color: #00f2ff;
  font-weight: 700;
  text-align: center;
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
}

h3 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #00f2ff;
  font-weight: 600;
}

.comparison-controls {
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

.date-range {
  display: flex;
  gap: 15px;
  align-items: center;
}

.date-range label {
  font-size: 14px;
  color: #8899aa;
  font-weight: 500;
}

.date-range input {
  padding: 8px 12px;
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 6px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  outline: none;
  transition: all 0.3s;
}

.date-range input:focus {
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

.comparison-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
}

.chart-box {
  background: rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(0, 242, 255, 0.1);
  transition: all 0.3s;
}

.chart-box:hover {
  border-color: #00f2ff;
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
}

.chart-box h3 {
  text-align: center;
  margin-bottom: 15px;
}

.chart-box canvas {
  width: 100% !important;
  height: 350px !important;
}

.comparison-chart {
  background: rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(0, 242, 255, 0.1);
}

.comparison-chart h3 {
  text-align: center;
  margin-bottom: 15px;
}

.comparison-chart canvas {
  width: 100% !important;
  height: 450px !important;
}

.summary-table {
  overflow-x: auto;
  background: rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(0, 242, 255, 0.1);
}

.summary-table table {
  width: 100%;
  border-collapse: collapse;
}

.summary-table th,
.summary-table td {
  padding: 15px;
  text-align: center;
  border: 1px solid rgba(0, 242, 255, 0.2);
}

.summary-table th {
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.3) 0%, rgba(0, 132, 255, 0.3) 100%);
  color: #fff;
  font-weight: 600;
  font-size: 15px;
}

.summary-table td {
  color: #ccc;
  font-size: 14px;
}

.summary-table tr {
  background: rgba(255, 255, 255, 0.02);
  transition: all 0.3s;
}

.summary-table tr:hover {
  background: rgba(0, 242, 255, 0.05);
}

.correlation {
  padding: 30px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  text-align: center;
  border: 1px solid rgba(0, 242, 255, 0.1);
}

.correlation strong {
  color: #00f2ff;
  font-size: 28px;
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
}

.correlation-note {
  margin-top: 15px;
  color: #8899aa;
  font-style: italic;
  font-size: 15px;
}

@media (max-width: 768px) {
  .charts-row {
    grid-template-columns: 1fr;
  }

  .comparison-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .date-range {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
