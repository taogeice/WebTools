<template>
  <div class="echarts-chart-container">
    <div class="chart-header">
      <h2>{{ chartTitle }}</h2>
      <div class="market-selector">
        <label>市场选择：</label>
        <select v-model="selectedMarket" @change="loadData">
          <option v-for="market in markets" :key="market.value" :value="market.value">
            {{ market.label }}
          </option>
        </select>
      </div>
      <div class="date-range">
        <label>开始日期：</label>
        <input type="date" v-model="startDate" @change="loadData" />
        <label>结束日期：</label>
        <input type="date" v-model="endDate" @change="loadData" />
        <button @click="syncData" :disabled="loading" class="sync-btn">
          {{ loading ? '同步中...' : '同步数据' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="error = null" class="close-error">×</button>
    </div>

    <div class="chart-wrapper">
      <div v-if="loading" class="loading">
        <p>加载数据中...</p>
      </div>
      <div v-else-if="!chartData.length" class="no-data">
        <p>暂无数据</p>
      </div>
      <div v-else id="echartsContainer" class="chart-container"></div>
    </div>

    <div v-if="chartData.length" class="chart-summary">
      <h3>数据统计</h3>
      <div class="summary-grid">
        <div class="summary-item">
          <span class="label">最高价：</span>
          <span class="value">¥{{ maxPrice.toFixed(2) }}</span>
        </div>
        <div class="summary-item">
          <span class="label">最低价：</span>
          <span class="value">¥{{ minPrice.toFixed(2) }}</span>
        </div>
        <div class="summary-item">
          <span class="label">平均价：</span>
          <span class="value">¥{{ avgPrice.toFixed(2) }}</span>
        </div>
        <div class="summary-item">
          <span class="label">最新价：</span>
          <span class="value">¥{{ latestPrice.toFixed(2) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import goldAPI from '../api/gold.js'

export default {
  name: 'GoldPriceChartECharts',
  setup() {
    const echartsContainerRef = ref(null)
    const chart = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const selectedMarket = ref('domestic')
    const startDate = ref('')
    const endDate = ref('')
    const chartData = ref([])

    const markets = [
      { value: 'domestic', label: '国内黄金' },
      { value: 'international', label: '国际黄金' }
    ]

    // 计算统计信息
    const maxPrice = computed(() => {
      if (!chartData.value.length) return 0
      return Math.max(...chartData.value.map(item => item.close_price || 0))
    })

    const minPrice = computed(() => {
      if (!chartData.value.length) return 0
      return Math.min(...chartData.value.map(item => item.close_price || 0))
    })

    const avgPrice = computed(() => {
      if (!chartData.value.length) return 0
      const sum = chartData.value.reduce((acc, item) => acc + (item.close_price || 0), 0)
      return sum / chartData.value.length
    })

    const latestPrice = computed(() => {
      if (!chartData.value.length) return 0
      return chartData.value[chartData.value.length - 1]?.close_price || 0
    })

    const chartTitle = computed(() => {
      const market = markets.find(m => m.value === selectedMarket.value)
      return `${market?.label || ''}价格走势`
    })

    // 初始化日期范围（默认30天）
    const initDateRange = () => {
      const today = new Date()
      const thirtyDaysAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)

      startDate.value = thirtyDaysAgo.toISOString().split('T')[0]
      endDate.value = today.toISOString().split('T')[0]
    }

    // 加载数据
    const loadData = async () => {
      if (!startDate.value || !endDate.value) {
        console.warn('请选择日期范围')
        return
      }

      loading.value = true
      error.value = null

      try {
        console.log('开始获取数据，参数:', {
          market: selectedMarket.value,
          startDate: startDate.value,
          endDate: endDate.value
        })

        const response = await goldAPI.getGoldPriceData(
          selectedMarket.value,
          startDate.value,
          endDate.value
        )

        console.log('API响应:', response)

        if (response && response.data) {
          chartData.value = response.data || []
          console.log('设置图表数据，条数:', chartData.value.length)
          await nextTick()
          updateChart()
        } else {
          throw new Error('API返回数据格式错误')
        }
      } catch (err) {
        console.error('获取数据失败:', err)
        error.value = err.message || '获取数据失败'
      } finally {
        loading.value = false
      }
    }

    // 同步数据
    const syncData = async () => {
      if (!startDate.value || !endDate.value) {
        console.warn('请选择日期范围')
        return
      }

      loading.value = true
      error.value = null

      try {
        console.log('开始同步数据，参数:', {
          start_date: startDate.value,
          end_date: endDate.value
        })

        const response = await goldAPI.syncGoldPriceData(startDate.value, endDate.value)
        console.log('同步响应:', response)

        if (response && response.data) {
          alert('数据同步成功！')
          // 同步后重新加载数据
          await loadData()
        } else {
          throw new Error('同步响应格式错误')
        }
      } catch (err) {
        console.error('同步数据失败:', err)
        error.value = err.message || '同步数据失败'
      } finally {
        loading.value = false
      }
    }

    // 更新图表
    const updateChart = () => {
      if (!echartsContainer.value || !chart.value) {
        console.warn('图表容器未初始化')
        return
      }

      console.log('更新图表，数据条数:', chartData.value.length)

      if (chartData.value.length === 0) {
        chart.value.clear()
        return
      }

      // 准备数据
      const dates = chartData.value.map(item =>
        new Date(item.date).toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        })
      )

      const prices = chartData.value.map(item => item.close_price || 0)

      // 配置选项
      const option = {
        title: {
          text: chartTitle.value,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        tooltip: {
          trigger: 'axis',
          formatter: function (params) {
            const date = params[0].axisValue
            const price = params[0].value
            return `${date}<br/>价格: ¥${price.toFixed(2)}`
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: dates,
          axisLabel: {
            rotate: 45,
            fontSize: 10
          }
        },
        yAxis: {
          type: 'value',
          name: '价格 (¥)',
          axisLabel: {
            formatter: function (value) {
              return '¥' + value.toFixed(0)
            }
          }
        },
        series: [{
          name: '收盘价',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          data: prices,
          itemStyle: {
            color: '#ff6b6b'
          },
          lineStyle: {
            color: '#ff6b6b',
            width: 3
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(255, 107, 107, 0.3)' },
              { offset: 1, color: 'rgba(255, 107, 107, 0.1)' }
            ])
          }
        }]
      }

      // 设置选项
      chart.value.setOption(option, true)
    }

    // 监听数据变化
    watch(chartData, () => {
      if (chartData.value.length > 0) {
        nextTick(() => {
          updateChart()
        })
      }
    }, { deep: true })

    // 监听市场变化
    watch(selectedMarket, () => {
      loadData()
    })

    // 组件挂载
    onMounted(() => {
      console.log('ECharts图表组件挂载')

      // 初始化日期
      initDateRange()

      // 使用setTimeout确保DOM完全渲染后再初始化图表
      setTimeout(() => {
        initChart()
      }, 1000) // 延迟100ms确保DOM元素可用

      // 确保DOM完全渲染后再初始化图表
      // 使用多个nextTick确保元素可用
      nextTick()
        .then(() => {
          return nextTick()
        })
        .then(() => {
          return nextTick()
        })
        .then(() => {
          if (echartsContainer.value) {
            console.log('初始化ECharts实例, 容器:', echartsContainer.value)
            chart.value = echarts.init(echartsContainer.value)

            // 设置响应式
            const resizeHandler = () => {
              if (chart.value) {
                chart.value.resize()
              }
            }

            // 添加事件监听
            window.addEventListener('resize', resizeHandler)

            // 初始加载数据
            loadData()
          } else {
            console.error('找不到图表容器')
          }
        })
        .catch(err => {
          console.error('初始化图表时出错:', err)
        })
    })

    // 组件卸载
    onUnmounted(() => {
      console.log('ECharts图表组件卸载')

      // 清理事件监听
      window.removeEventListener('resize', () => {})

      // 销毁图表实例
      if (chart.value) {
        chart.value.dispose()
        chart.value = null
      }
    })

    return {
      chartData,
      loading,
      error,
      selectedMarket,
      markets,
      startDate,
      endDate,
      chartTitle,
      maxPrice,
      minPrice,
      avgPrice,
      latestPrice
    }
  }
}
</script>

<style scoped>
.echarts-chart-container {
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.chart-header h2 {
  margin: 0;
  color: #333;
}

.market-selector select {
  padding: 8px 12px;
  border: 2px solid #e1e5e7;
  border-radius: 6px;
  background: white;
  font-size: 14px;
}

.date-range {
  display: flex;
  gap: 10px;
  align-items: center;
}

.date-range label {
  font-size: 14px;
  color: #666;
}

.date-range input {
  padding: 8px 12px;
  border: 2px solid #e1e5e7;
  border-radius: 6px;
  font-size: 14px;
}

.sync-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #ff6b6b, #ff9f40);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.sync-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff9f40, #ffc947);
  transform: translateY(-1px);
}

.sync-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c53030;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-error {
  background: none;
  border: none;
  color: #c53030;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
}

.chart-wrapper {
  position: relative;
}

.chart-container {
  width: 100%;
  height: 400px;
  min-height: 300px;
}

.loading, .no-data {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  font-size: 16px;
  color: #666;
}

.chart-summary {
  margin-top: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.summary-item .label {
  font-weight: 500;
  color: #666;
}

.summary-item .value {
  font-weight: bold;
  color: #ff6b6b;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .date-range {
    flex-wrap: wrap;
  }

  .summary-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }

  .chart-container {
    height: 300px;
  }
}
</style>