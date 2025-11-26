<template>
  <div class="latest-prices">
    <h2>最新黄金价格</h2>

    <div class="refresh-section">
      <button class="refresh-btn" @click="loadData" :disabled="loading">
        {{ loading ? '刷新中...' : '刷新数据' }}
      </button>
    </div>

    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-else class="prices-container">
      <div class="price-card domestic">
        <div class="card-header">
          <h3>国内黄金</h3>
          <span class="badge">人民币</span>
        </div>
        <div class="price-value">
          {{ domesticPrice ? formatPrice(domesticPrice) : '暂无数据' }}
        </div>
        <div class="price-unit">元/克</div>
        <div v-if="domesticPrice" class="price-date">
          更新时间：{{ formatDate(domesticDate) }}
        </div>
      </div>

      <div class="price-card international">
        <div class="card-header">
          <h3>国际黄金</h3>
          <span class="badge">美元</span>
        </div>
        <div class="price-value">
          {{ internationalPrice ? formatPrice(internationalPrice) : '暂无数据' }}
        </div>
        <div class="price-unit">美元/盎司</div>
        <div v-if="internationalPrice" class="price-date">
          更新时间：{{ formatDate(internationalDate) }}
        </div>
      </div>
    </div>

    <div v-if="domesticPrice && internationalPrice" class="comparison-section">
      <h3>价格对比</h3>
      <div class="comparison-stats">
        <div class="stat-item">
          <span class="label">价差</span>
          <span class="value">{{ priceDiff.toFixed(2) }}</span>
        </div>
        <div class="stat-item">
          <span class="label">比率</span>
          <span class="value">{{ priceRatio.toFixed(4) }}</span>
        </div>
      </div>
    </div>

    <div v-if="!loading && !error" class="metadata">
      <h4>数据来源</h4>
      <ul>
        <li>国内数据：AKShare（黄金现货价格）</li>
        <li>国际数据：Yahoo Finance（GLD ETF）</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { format } from 'date-fns';
import goldAPI from '../api/gold.js';

export default {
  name: 'LatestPrices',
  setup() {
    const loading = ref(false);
    const error = ref(null);
    const data = ref({});

    const domesticPrice = computed(() => data.value.domestic?.price);
    const internationalPrice = computed(() => data.value.international?.price);
    const domesticDate = computed(() => data.value.domestic?.date);
    const internationalDate = computed(() => data.value.international?.date);

    const priceDiff = computed(() => {
      if (!domesticPrice.value || !internationalPrice.value) return 0;
      // 注意：这里需要考虑汇率转换，这里仅作简单对比
      return domesticPrice.value - (internationalPrice.value / 10);
    });

    const priceRatio = computed(() => {
      if (!domesticPrice.value || !internationalPrice.value) return 0;
      return domesticPrice.value / (internationalPrice.value / 10);
    });

    const loadData = async () => {
      loading.value = true;
      error.value = null;

      try {
        const response = await goldAPI.getLatestPrices();
        data.value = response.data || {};
      } catch (err) {
        error.value = err.message || '加载数据失败';
        console.error('加载数据失败:', err);
      } finally {
        loading.value = false;
      }
    };

    const formatPrice = (price) => {
      return Number(price).toFixed(2);
    };

    const formatDate = (date) => {
      if (!date) return '';
      return format(new Date(date), 'yyyy-MM-dd HH:mm:ss');
    };

    // 自动刷新（每5分钟）
    let timer;
    onMounted(() => {
      loadData();
      timer = setInterval(loadData, 5 * 60 * 1000);
    });

    onUnmounted(() => {
      if (timer) {
        clearInterval(timer);
      }
    });

    return {
      loading,
      error,
      domesticPrice,
      internationalPrice,
      domesticDate,
      internationalDate,
      priceDiff,
      priceRatio,
      loadData,
      formatPrice,
      formatDate
    };
  }
};
</script>

<style scoped>
.latest-prices {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin: 0 0 20px 0;
  font-size: 24px;
  color: #333;
  text-align: center;
}

h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #666;
}

.refresh-section {
  text-align: center;
  margin-bottom: 30px;
}

.refresh-btn {
  padding: 10px 30px;
  background: #4dabf7;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background: #339af0;
}

.refresh-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 16px;
}

.error {
  color: #ff6b6b;
}

.prices-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 40px;
}

.price-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  color: white;
  transition: transform 0.3s;
}

.price-card:hover {
  transform: translateY(-5px);
}

.price-card.domestic {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
}

.price-card.international {
  background: linear-gradient(135deg, #4dabf7 0%, #339af0 100%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
}

.price-value {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.price-unit {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 15px;
}

.price-date {
  font-size: 14px;
  opacity: 0.8;
}

.comparison-section {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.comparison-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 15px;
}

.stat-item {
  text-align: center;
}

.stat-item .label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.stat-item .value {
  display: block;
  font-size: 28px;
  font-weight: bold;
  color: #4dabf7;
}

.metadata {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.metadata ul {
  list-style: none;
  padding: 0;
}

.metadata li {
  padding: 8px 0;
  color: #666;
  font-size: 14px;
}

.metadata li:before {
  content: "• ";
  color: #4dabf7;
  font-weight: bold;
}

@media (max-width: 768px) {
  .prices-container {
    grid-template-columns: 1fr;
  }

  .price-value {
    font-size: 36px;
  }

  .comparison-stats {
    grid-template-columns: 1fr;
  }
}
</style>
