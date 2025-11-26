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
  margin: 0;
  font-size: 20px;
  color: #fff;
  font-weight: 600;
}

h4 {
  margin: 0 0 15px 0;
  font-size: 18px;
  color: #00f2ff;
  font-weight: 600;
}

.refresh-section {
  text-align: center;
  margin-bottom: 30px;
}

.refresh-btn {
  padding: 12px 35px;
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.2) 0%, rgba(0, 132, 255, 0.2) 100%);
  color: #00f2ff;
  border: 1px solid #00f2ff;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.3) 0%, rgba(0, 132, 255, 0.3) 100%);
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
  transform: translateY(-2px);
}

.refresh-btn:disabled {
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

.prices-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 40px;
}

.price-card {
  padding: 40px 30px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  text-align: center;
  color: white;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.price-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
}

.price-card.domestic {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(238, 90, 111, 0.2) 100%);
  border-color: rgba(255, 107, 107, 0.3);
}

.price-card.international {
  background: linear-gradient(135deg, rgba(0, 242, 255, 0.2) 0%, rgba(0, 132, 255, 0.2) 100%);
  border-color: rgba(0, 242, 255, 0.3);
}

.price-card.domestic:hover {
  border-color: #ff6b6b;
  box-shadow: 0 0 30px rgba(255, 107, 107, 0.4);
}

.price-card.international:hover {
  border-color: #00f2ff;
  box-shadow: 0 0 30px rgba(0, 242, 255, 0.4);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.badge {
  background: rgba(255, 255, 255, 0.15);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.price-value {
  font-size: 52px;
  font-weight: bold;
  margin-bottom: 12px;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
  font-family: 'SF Mono', monospace;
}

.price-unit {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 18px;
  font-weight: 500;
}

.price-date {
  font-size: 14px;
  opacity: 0.75;
  font-style: italic;
}

.comparison-section {
  background: rgba(0, 0, 0, 0.2);
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 30px;
  border: 1px solid rgba(0, 242, 255, 0.1);
}

.comparison-section h3 {
  text-align: center;
  margin-bottom: 20px;
}

.comparison-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  margin-top: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid rgba(0, 242, 255, 0.1);
  transition: all 0.3s;
}

.stat-item:hover {
  border-color: #00f2ff;
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
  transform: translateY(-2px);
}

.stat-item .label {
  display: block;
  font-size: 14px;
  color: #8899aa;
  margin-bottom: 10px;
  font-weight: 500;
}

.stat-item .value {
  display: block;
  font-size: 32px;
  font-weight: bold;
  color: #00f2ff;
  text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
  font-family: 'SF Mono', monospace;
}

.metadata {
  padding: 25px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  border: 1px solid rgba(0, 242, 255, 0.1);
}

.metadata h4 {
  margin-bottom: 15px;
}

.metadata ul {
  list-style: none;
  padding: 0;
}

.metadata li {
  padding: 10px 0;
  color: #8899aa;
  font-size: 14px;
  transition: all 0.3s;
}

.metadata li:hover {
  color: #00f2ff;
  padding-left: 10px;
}

.metadata li:before {
  content: "▹ ";
  color: #00f2ff;
  font-weight: bold;
  margin-right: 8px;
}

@media (max-width: 768px) {
  .prices-container {
    grid-template-columns: 1fr;
  }

  .price-value {
    font-size: 40px;
  }

  .comparison-stats {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
