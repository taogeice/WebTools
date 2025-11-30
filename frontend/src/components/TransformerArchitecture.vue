<template>
  <div class="transformer-container">
    <h2 class="transformer-title">Transformer 架构详解</h2>
    <p class="transformer-subtitle">深度学习模型的革命性架构 - 从训练到推理的完整解析</p>

    <!-- 概述部分 -->
    <section class="section overview">
      <h3>什么是Transformer？</h3>
      <div class="content">
        <p>
          Transformer是一种深度学习模型架构，首次在论文《Attention is All You Need》中提出。
          它完全基于注意力机制，摒弃了传统的循环和卷积结构，成为现代大语言模型的基础架构。
        </p>
        <div class="architecture-diagram">
          <h4>Transformer整体架构</h4>
          <div class="diagram-container">
            <div class="transformer-flow">
              <div class="input-section">
                <div class="input-tokens">
                  <span class="token">The</span>
                  <span class="token">Transformer</span>
                  <span class="token">model</span>
                  <span class="token">is</span>
                  <span class="token">powerful</span>
                </div>
                <div class="input-label">输入序列</div>
              </div>
              
              <div class="encoder-stack">
                <div class="encoder-header">编码器堆叠 (N=6)</div>
                <div class="encoder-blocks">
                  <div class="encoder-block" v-for="i in 6" :key="'enc-' + i">
                    <div class="block-title">编码器块 {{i}}</div>
                    <div class="attention-layer">
                      <div class="layer-name">多头自注意力</div>
                      <div class="attention-connections">
                        <div class="conn-row" v-for="j in 5" :key="'conn-' + j">
                          <div class="conn-cell" v-for="k in 5" :key="'cell-' + k" 
                               :class="{ 'active': j === k || i % 2 === 0 }">
                            <div class="conn-dot"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="ffn-layer">
                      <div class="layer-name">前馈网络</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="decoder-stack">
                <div class="decoder-header">解码器堆叠 (N=6)</div>
                <div class="decoder-blocks">
                  <div class="decoder-block" v-for="i in 6" :key="'dec-' + i">
                    <div class="block-title">解码器块 {{i}}</div>
                    <div class="masked-attention-layer">
                      <div class="layer-name">掩码多头自注意力</div>
                    </div>
                    <div class="cross-attention-layer">
                      <div class="layer-name">编码器-解码器注意力</div>
                    </div>
                    <div class="ffn-layer">
                      <div class="layer-name">前馈网络</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="output-section">
                <div class="output-label">输出序列</div>
                <div class="output-tokens">
                  <span class="token">Le</span>
                  <span class="token">modèle</span>
                  <span class="token">Transformer</span>
                  <span class="token">est</span>
                  <span class="token">puissant</span>
                </div>
              </div>
            </div>

            <!-- 注意力机制可视化 -->
            <div class="attention-chart">
              <AttentionVisualization :attention-weights="attentionWeights" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 训练过程 -->
    <section class="section training">
      <h3>训练过程</h3>
      <div class="content">
        <p>
          Transformer的训练过程包括预训练和微调两个阶段。在预训练阶段，模型在大量文本数据上学习语言表示。
          在微调阶段，模型在特定任务上进行进一步训练。
        </p>
        <div class="training-process">
          <div class="timeline-header">
            <h4>训练流程</h4>
            <div class="timeline-controls">
              <button class="control-btn" @click="startTrainingAnimation">
                <span v-if="!isTrainingActive">▶ 播放动画</span>
                <span v-else>⏸ 暂停</span>
              </button>
            </div>
          </div>
          <div class="timeline-container training-timeline">
            <div class="timeline-line">
              <div class="timeline-progress"
                   :style="{ width: trainingProgress + '%' }"></div>
            </div>
            <div class="timeline-steps">
              <div class="timeline-step"
                   v-for="(step, index) in trainingSteps"
                   :key="index"
                   :class="{
                     'active': index <= currentTrainingStep && isTrainingActive,
                     'completed': index < currentTrainingStep
                   }"
                   @click="selectTrainingStep(index)">
                <div class="step-number">{{ index + 1 }}</div>
                <div class="step-content">
                  <h4>{{ step.title }}</h4>
                  <p>{{ step.desc }}</p>
                </div>
                <div class="step-connector">
                  <div class="connector-line"></div>
                  <div class="connector-arrow">➜</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="training-details">
          <h4>训练细节</h4>
          <ul>
            <li><strong>损失函数</strong>: 通常使用交叉熵损失</li>
            <li><strong>优化器</strong>: Adam优化器，带学习率预热</li>
            <li><strong>并行处理</strong>: 批量处理序列中的所有token</li>
            <li><strong>预训练任务</strong>: 掩码语言建模或下一句预测</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 推理过程 -->
    <section class="section inference">
      <h3>推理过程</h3>
      <div class="content">
        <p>
          在推理阶段，Transformer模型接收输入序列并生成输出序列。对于自回归生成（如文本生成），
          模型会逐步生成输出token，每次生成一个token并将其作为下一步的输入。
        </p>
        <div class="inference-process">
          <div class="timeline-header">
            <h4>推理流程</h4>
            <div class="timeline-controls">
              <button class="control-btn" @click="startInferenceAnimation">
                <span v-if="!isInferenceActive">▶ 播放动画</span>
                <span v-else>⏸ 暂停</span>
              </button>
            </div>
          </div>
          <div class="timeline-container inference-timeline">
            <div class="timeline-line">
              <div class="timeline-progress"
                   :style="{ width: inferenceProgress + '%' }"></div>
            </div>
            <div class="timeline-steps">
              <div class="timeline-step"
                   v-for="(step, index) in inferenceSteps"
                   :key="index"
                   :class="{
                     'active': index <= currentInferenceStep && isInferenceActive,
                     'completed': index < currentInferenceStep
                   }"
                   @click="selectInferenceStep(index)">
                <div class="step-icon">{{ step.icon }}</div>
                <div class="step-content">
                  <h4>{{ step.title }}</h4>
                  <p>{{ step.desc }}</p>
                </div>
                <div class="step-connector">
                  <div class="connector-line"></div>
                  <div class="connector-arrow">➜</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="inference-details">
          <h4>推理策略</h4>
          <ul>
            <li><strong>贪婪搜索</strong>: 每步选择概率最高的token</li>
            <li><strong>束搜索</strong>: 保留多个候选序列，选择整体最优</li>
            <li><strong>随机采样</strong>: 根据概率分布随机选择token</li>
            <li><strong>Top-k/Top-p采样</strong>: 限制采样范围以平衡创造性与质量</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 核心组件 -->
    <section class="section components">
      <h3>核心组件详解</h3>
      <div class="content">
        <div class="component-grid">
          <div class="component">
            <h4>多头自注意力机制</h4>
            <p>
              通过线性变换生成Q、K、V矩阵，计算注意力权重，实现对输入序列中不同位置的关联。
              公式：Attention(Q, K, V) = softmax(QK^T / √d_k)V
            </p>
          </div>
          <div class="component">
            <h4>位置编码</h4>
            <p>
              由于Transformer没有循环结构，需要添加位置编码来保留序列顺序信息。
              通常使用正弦/余弦函数或学习的位置嵌入。
            </p>
          </div>
          <div class="component">
            <h4>前馈网络</h4>
            <p>
              两个线性变换和一个激活函数组成的全连接网络，应用于每个位置的表示。
              通常使用ReLU或GELU激活函数。
            </p>
          </div>
          <div class="component">
            <h4>残差连接与层归一化</h4>
            <p>
              在每个子层后添加残差连接和层归一化，有助于梯度传播和训练稳定性。
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 代码示例 -->
    <section class="section code">
      <h3>核心代码示例</h3>
      <div class="content">
        <div class="code-container">
          <div class="code-block">
            <h4>多头注意力实现</h4>
            <pre><code>class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        matmul_qk = torch.matmul(Q, K.transpose(-2, -1))
        dk = K.size()[-1]
        scaled_attention_logits = matmul_qk / math.sqrt(dk)
        
        if mask is not None:
            scaled_attention_logits += (mask * -1e9)
            
        attention_weights = F.softmax(scaled_attention_logits, dim=-1)
        output = torch.matmul(attention_weights, V)
        return output
        
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        Q = self.W_q(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        scaled_attention = self.scaled_dot_product_attention(Q, K, V, mask)
        concat_attention = scaled_attention.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        
        output = self.W_o(concat_attention)
        return output</code></pre>
          </div>
          
          <div class="code-block">
            <h4>位置编码实现</h4>
            <pre><code>class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                            -(math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        self.register_buffer('pe', pe.unsqueeze(0))
        
    def forward(self, x):
        return x + self.pe[:, :x.size(1)]</code></pre>
          </div>
          
          <div class="code-block">
            <h4>完整Transformer实现</h4>
            <pre><code>class Transformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model, num_heads, num_layers, d_ff, max_len, dropout):
        super(Transformer, self).__init__()
        self.d_model = d_model
        self.num_layers = num_layers
        
        # 词嵌入层
        self.src_embedding = nn.Embedding(src_vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model)
        
        # 位置编码
        self.positional_encoding = PositionalEncoding(d_model, max_len)
        
        # 编码器和解码器层
        self.encoder_layers = nn.ModuleList([
            EncoderLayer(d_model, num_heads, d_ff, dropout) for _ in range(num_layers)
        ])
        self.decoder_layers = nn.ModuleList([
            DecoderLayer(d_model, num_heads, d_ff, dropout) for _ in range(num_layers)
        ])
        
        # 输出层
        self.dropout = nn.Dropout(dropout)
        self.fc_out = nn.Linear(d_model, tgt_vocab_size)
        
    def forward(self, src, tgt, src_mask, tgt_mask):
        # 源序列嵌入和位置编码
        src_embedding = self.dropout(self.positional_encoding(self.src_embedding(src) * math.sqrt(self.d_model)))
        
        # 目标序列嵌入和位置编码
        tgt_embedding = self.dropout(self.positional_encoding(self.tgt_embedding(tgt) * math.sqrt(self.d_model)))
        
        # 编码器处理
        enc_output = src_embedding
        for enc_layer in self.encoder_layers:
            enc_output = enc_layer(enc_output, src_mask)
        
        # 解码器处理
        dec_output = tgt_embedding
        for dec_layer in self.decoder_layers:
            dec_output = dec_layer(dec_output, enc_output, src_mask, tgt_mask)
        
        # 输出层
        output = self.fc_out(dec_output)
        return output</code></pre>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import AttentionVisualization from './AttentionVisualization.vue';

export default {
  name: 'TransformerArchitecture',
  components: {
    AttentionVisualization
  },
  data() {
    return {
      // 预定义的注意力权重用于ECharts可视化
      attentionWeights: [],
      // 训练流程数据
      trainingSteps: [
        { id: 1, title: '数据输入', desc: '大规模文本数据' },
        { id: 2, title: 'Token化', desc: '文本转为数字序列' },
        { id: 3, title: '位置编码', desc: '添加位置信息' },
        { id: 4, title: '模型处理', desc: '编码器-解码器处理' },
        { id: 5, title: '损失计算', desc: '预测与实际比较' },
        { id: 6, title: '参数更新', desc: '反向传播优化' }
      ],
      // 推理流程数据
      inferenceSteps: [
        { icon: '📥', title: '输入编码', desc: '输入序列通过编码器编码为表示向量' },
        { icon: '🔄', title: '自回归生成', desc: '解码器逐步生成输出，每步预测下一个token' },
        { icon: '📊', title: '概率计算', desc: '计算词汇表中每个token的概率分布' },
        { icon: '🎯', title: '采样策略', desc: '使用贪婪搜索、束搜索或随机采样选择输出token' }
      ],
      // 当前训练步骤
      currentTrainingStep: -1,
      // 当前推理步骤
      currentInferenceStep: -1,
      // 训练进度百分比
      trainingProgress: 0,
      // 推理进度百分比
      inferenceProgress: 0,
      // 动画状态
      isTrainingActive: false,
      isInferenceActive: false,
      // 定时器引用
      trainingTimer: null,
      inferenceTimer: null
    };
  },
  mounted() {
    // 生成模拟的注意力权重数据
    this.generateAttentionWeights();
  },
  beforeUnmount() {
    // 清理定时器
    if (this.trainingTimer) {
      clearInterval(this.trainingTimer);
    }
    if (this.inferenceTimer) {
      clearInterval(this.inferenceTimer);
    }
  },
  methods: {
    // 生成ECharts需要的注意力权重数据
    generateAttentionWeights() {
      const weights = [];
      const sourceTokens = ['The', 'Transformer', 'model', 'is', 'powerful'];
      const targetTokens = ['Le', 'modèle', 'Transformer', 'est', 'puissant'];

      for (let i = 0; i < sourceTokens.length; i++) {
        for (let j = 0; j < targetTokens.length; j++) {
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
      this.attentionWeights = weights;
    },

    // 开始训练动画
    startTrainingAnimation() {
      if (this.isTrainingActive) {
        this.pauseTrainingAnimation();
        return;
      }

      this.isTrainingActive = true;
      this.currentTrainingStep = 0;
      this.trainingProgress = 0;

      // 清除之前的定时器
      if (this.trainingTimer) {
        clearInterval(this.trainingTimer);
      }

      this.trainingTimer = setInterval(() => {
        if (this.currentTrainingStep < this.trainingSteps.length - 1) {
          this.currentTrainingStep++;
          this.trainingProgress = ((this.currentTrainingStep + 1) / this.trainingSteps.length) * 100;
        } else {
          // 动画完成
          this.pauseTrainingAnimation();
        }
      }, 1500);
    },

    // 暂停训练动画
    pauseTrainingAnimation() {
      this.isTrainingActive = false;
      if (this.trainingTimer) {
        clearInterval(this.trainingTimer);
        this.trainingTimer = null;
      }
    },

    // 开始推理动画
    startInferenceAnimation() {
      if (this.isInferenceActive) {
        this.pauseInferenceAnimation();
        return;
      }

      this.isInferenceActive = true;
      this.currentInferenceStep = 0;
      this.inferenceProgress = 0;

      // 清除之前的定时器
      if (this.inferenceTimer) {
        clearInterval(this.inferenceTimer);
      }

      this.inferenceTimer = setInterval(() => {
        if (this.currentInferenceStep < this.inferenceSteps.length - 1) {
          this.currentInferenceStep++;
          this.inferenceProgress = ((this.currentInferenceStep + 1) / this.inferenceSteps.length) * 100;
        } else {
          // 动画完成
          this.pauseInferenceAnimation();
        }
      }, 1500);
    },

    // 暂停推理动画
    pauseInferenceAnimation() {
      this.isInferenceActive = false;
      if (this.inferenceTimer) {
        clearInterval(this.inferenceTimer);
        this.inferenceTimer = null;
      }
    },

    // 选择训练步骤
    selectTrainingStep(index) {
      this.currentTrainingStep = index;
      this.trainingProgress = ((index + 1) / this.trainingSteps.length) * 100;
    },

    // 选择推理步骤
    selectInferenceStep(index) {
      this.currentInferenceStep = index;
      this.inferenceProgress = ((index + 1) / this.inferenceSteps.length) * 100;
    }
  }
};
</script>

<style scoped>
.transformer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
  color: #e0e0e0;
  background: rgba(10, 14, 39, 0.8);
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.transformer-title {
  text-align: center;
  font-size: 38px;
  color: #00f2ff;
  margin-bottom: 15px;
  font-weight: 700;
  text-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
}

.transformer-subtitle {
  text-align: center;
  font-size: 18px;
  color: #8899aa;
  margin-bottom: 40px;
}

.section {
  margin-bottom: 40px;
  padding: 25px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(0, 242, 255, 0.1);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.section h3 {
  font-size: 26px;
  color: #00f2ff;
  margin-bottom: 20px;
  font-weight: 600;
}

.content {
  line-height: 1.8;
}

.content p {
  margin-bottom: 20px;
  font-size: 16px;
}

.architecture-diagram {
  margin-top: 20px;
}

.diagram-container {
  background: rgba(0, 0, 0, 0.3);
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
}

.transformer-flow {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  min-width: 1000px;
}

.input-section, .output-section {
  text-align: center;
  padding: 15px;
  background: rgba(0, 60, 120, 0.4);
  border: 1px solid rgba(0, 150, 255, 0.4);
  border-radius: 8px;
  min-width: 150px;
}

.input-tokens, .output-tokens {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 10px;
}

.token {
  padding: 8px;
  background: rgba(100, 150, 255, 0.3);
  border: 1px solid rgba(100, 150, 255, 0.5);
  border-radius: 4px;
  font-weight: bold;
}

.input-label, .output-label {
  font-size: 14px;
  color: #4dabf7;
}

.encoder-stack, .decoder-stack {
  flex: 1;
  min-width: 200px;
}

.encoder-header, .decoder-header {
  text-align: center;
  color: #51cf66;
  margin-bottom: 15px;
  font-size: 18px;
  font-weight: bold;
}

.encoder-blocks, .decoder-blocks {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.encoder-block, .decoder-block {
  padding: 15px;
  background: rgba(0, 40, 80, 0.4);
  border: 1px solid rgba(0, 120, 200, 0.4);
  border-radius: 8px;
}

.block-title {
  text-align: center;
  color: #ffd43b;
  margin-bottom: 10px;
  font-weight: bold;
}

.layer-name {
  text-align: center;
  font-size: 14px;
  color: #ff6b6b;
  margin-bottom: 8px;
}

.attention-layer,
.masked-attention-layer,
.cross-attention-layer,
.ffn-layer {
  margin-bottom: 10px;
  padding: 8px;
  background: rgba(80, 0, 120, 0.3);
  border: 1px solid rgba(120, 0, 200, 0.4);
  border-radius: 4px;
}

.attention-connections {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(5, 1fr);
  gap: 2px;
  width: 100px;
  height: 100px;
  margin: 0 auto;
}

.conn-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(100, 100, 100, 0.3);
  border: 1px solid rgba(150, 150, 150, 0.3);
  transition: all 0.3s ease;
}

.conn-cell.active {
  background: rgba(50, 200, 100, 0.5);
  box-shadow: 0 0 5px rgba(50, 200, 100, 0.7);
}

.conn-dot {
  width: 6px;
  height: 6px;
  background: #00f2ff;
  border-radius: 50%;
}

.attention-chart {
  margin-top: 30px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(0, 242, 255, 0.2);
  border-radius: 12px;
}

.training-process, .inference-process {
  margin: 20px 0;
  padding: 15px;
  background: rgba(0, 30, 60, 0.3);
  border-radius: 8px;
}

.process-visualization {
  padding: 15px;
  background: rgba(0, 40, 80, 0.4);
  border-radius: 8px;
  margin-bottom: 15px;
}

.data-flow {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.data-step {
  padding: 10px;
  background: rgba(100, 150, 255, 0.2);
  border: 1px solid rgba(100, 150, 255, 0.3);
  border-radius: 4px;
  text-align: left;
}

.training-details, .inference-details {
  margin-top: 15px;
}

.training-details ul, .inference-details ul {
  padding-left: 20px;
}

.training-details li, .inference-details li {
  margin-bottom: 10px;
}

/* 时间线样式 */
.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(0, 242, 255, 0.2);
}

.timeline-header h4 {
  color: #00f2ff;
  font-size: 20px;
  margin: 0;
}

.timeline-controls {
  display: flex;
  gap: 10px;
}

.control-btn {
  padding: 8px 16px;
  background: rgba(0, 150, 255, 0.3);
  border: 1px solid rgba(0, 150, 255, 0.5);
  border-radius: 6px;
  color: #00f2ff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-btn:hover {
  background: rgba(0, 150, 255, 0.5);
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.6);
  transform: translateY(-2px);
}

.timeline-container {
  position: relative;
  padding: 40px 0;
  margin: 20px 0;
  overflow-x: auto;
}

.timeline-line {
  position: absolute;
  top: 50%;
  left: 5%;
  right: 5%;
  height: 4px;
  background: linear-gradient(90deg, rgba(0, 242, 255, 0.3), rgba(0, 242, 255, 0.6));
  border-radius: 2px;
  z-index: 1;
}

.timeline-progress {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, #00f2ff, #00ff88);
  border-radius: 2px;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 10px rgba(0, 242, 255, 0.8);
}

.timeline-steps {
  display: flex;
  justify-content: space-between;
  position: relative;
  z-index: 2;
  padding: 0 5%;
}

.timeline-step {
  flex: 1;
  position: relative;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  max-width: 180px;
}

.timeline-step:hover {
  transform: translateY(-5px);
}

.timeline-step.active .step-number {
  background: linear-gradient(135deg, #00f2ff, #00ff88);
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.8);
  animation: stepPulse 2s infinite;
}

.timeline-step.completed .step-number {
  background: linear-gradient(135deg, #00ff88, #00cc66);
}

.timeline-step.completed .step-content h4 {
  color: #00ff88;
}

.step-number {
  width: 50px;
  height: 50px;
  margin: 0 auto 15px;
  background: rgba(0, 100, 150, 0.4);
  border: 2px solid rgba(0, 150, 255, 0.6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  color: #00f2ff;
  transition: all 0.3s ease;
}

.step-icon {
  width: 50px;
  height: 50px;
  margin: 0 auto 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  transition: all 0.3s ease;
}

.timeline-step.active .step-icon {
  animation: stepPulse 2s infinite;
}

.step-content {
  background: rgba(0, 30, 60, 0.5);
  border: 1px solid rgba(0, 150, 255, 0.3);
  border-radius: 8px;
  padding: 15px 10px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.timeline-step:hover .step-content {
  border-color: rgba(0, 242, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.4);
}

.step-content h4 {
  color: #4dabf7;
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
}

.step-content p {
  margin: 0;
  font-size: 13px;
  color: #b0c4de;
  line-height: 1.5;
}

.step-connector {
  position: absolute;
  top: 25px;
  left: 100%;
  width: 100%;
  height: 4px;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.connector-line {
  flex: 1;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 242, 255, 0.8), transparent);
  animation: dataFlow 2s infinite;
}

.connector-arrow {
  color: #00f2ff;
  font-size: 20px;
  margin-left: 5px;
  animation: arrowMove 1s infinite;
}

.timeline-step:last-child .step-connector {
  display: none;
}

/* 动画效果 */
@keyframes dataFlow {
  0% {
    transform: translateX(-100%);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateX(100%);
    opacity: 0;
  }
}

@keyframes stepPulse {
  0%, 100% {
    box-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
  }
  50% {
    box-shadow: 0 0 25px rgba(0, 242, 255, 0.9);
  }
}

@keyframes arrowMove {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(5px);
  }
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin: 20px 0;
}

.step {
  padding: 15px;
  background: rgba(0, 40, 80, 0.3);
  border: 1px solid rgba(0, 150, 200, 0.3);
  border-radius: 8px;
  text-align: center;
}

.step-icon {
  font-size: 24px;
  margin-bottom: 10px;
}

.step h4 {
  color: #4dabf7;
  margin: 10px 0 5px 0;
  font-size: 18px;
}

.component-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.component {
  padding: 20px;
  background: rgba(60, 0, 80, 0.2);
  border: 1px solid rgba(150, 100, 255, 0.3);
  border-radius: 8px;
}

.component h4 {
  color: #9775fa;
  margin-bottom: 10px;
  font-size: 18px;
}

.code-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.code-block {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(100, 200, 255, 0.3);
  border-radius: 8px;
  overflow: hidden;
}

.code-block h4 {
  padding: 12px 20px;
  background: rgba(0, 30, 60, 0.6);
  color: #ff6b6b;
  margin: 0;
  font-size: 18px;
}

pre {
  margin: 0;
  padding: 20px;
  overflow-x: auto;
  background: rgba(0, 0, 0, 0.5);
  color: #f8f8f2;
  font-size: 14px;
  line-height: 1.5;
}

@media (max-width: 1100px) {
  .transformer-flow {
    flex-direction: column;
    min-width: auto;
    gap: 30px;
  }

  .transformer-container {
    padding: 15px;
  }

  .transformer-title {
    font-size: 28px;
  }

  .process-steps, .inference-steps, .component-grid {
    grid-template-columns: 1fr;
  }

  .attention-grid {
    max-width: 100%;
    overflow-x: auto;
  }

  .timeline-steps {
    overflow-x: auto;
    padding-bottom: 20px;
  }

  .timeline-step {
    min-width: 150px;
  }
}

@media (max-width: 768px) {
  .timeline-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .timeline-container {
    padding: 30px 0;
  }

  .timeline-line {
    left: 10%;
    right: 10%;
  }

  .timeline-steps {
    padding: 0 10%;
  }

  .timeline-step {
    min-width: 130px;
  }

  .step-number {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }

  .step-icon {
    width: 40px;
    height: 40px;
    font-size: 24px;
  }

  .step-content {
    padding: 12px 8px;
  }

  .step-content h4 {
    font-size: 14px;
  }

  .step-content p {
    font-size: 12px;
  }
}
</style>