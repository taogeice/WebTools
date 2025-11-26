/**
 * 黄金价格API
 */
import axios from 'axios';

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log('发送请求:', config);
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('收到响应:', response.data);
    return response.data;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

export default {
  /**
   * 获取黄金价格数据
   * @param {string} marketType - 市场类型 (domestic/international)
   * @param {string} startDate - 开始日期 (YYYY-MM-DD)
   * @param {string} endDate - 结束日期 (YYYY-MM-DD)
   */
  getGoldPriceData(marketType, startDate, endDate) {
    return api.get(`/gold/data/${marketType}`, {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    });
  },

  /**
   * 同步黄金价格数据
   * @param {string} startDate - 开始日期
   * @param {string} endDate - 结束日期
   */
  syncGoldPriceData(startDate, endDate) {
    return api.post('/gold/sync', {
      start_date: startDate,
      end_date: endDate
    });
  },

  /**
   * 获取市场汇总信息
   * @param {string} marketType - 市场类型
   */
  getMarketSummary(marketType) {
    return api.get(`/gold/summary/${marketType}`);
  },

  /**
   * 比较国内外市场
   * @param {string} startDate - 开始日期
   * @param {string} endDate - 结束日期
   */
  compareMarkets(startDate, endDate) {
    return api.get('/gold/comparison', {
      params: {
        start_date: startDate,
        end_date: endDate
      }
    });
  },

  /**
   * 获取最新价格
   */
  getLatestPrices() {
    return api.get('/gold/latest');
  },

  /**
   * 获取元数据
   */
  getMetadata() {
    return api.get('/gold/metadata');
  }
};
