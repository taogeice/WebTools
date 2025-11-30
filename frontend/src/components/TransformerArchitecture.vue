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
          <div class="process-visualization">
            <div class="data-flow">
              <div class="data-step">1. <strong>数据输入</strong>: 大规模文本数据</div>
              <div class="data-step">2. <strong>Token化</strong>: 文本转为数字序列</div>
              <div class="data-step">3. <strong>位置编码</strong>: 添加位置信息</div>
              <div class="data-step">4. <strong>模型处理</strong>: 编码器-解码器处理</div>
              <div class="data-step">5. <strong>损失计算</strong>: 预测与实际比较</div>
              <div class="data-step">6. <strong>参数更新</strong>: 反向传播优化</div>
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
          <div class="process-steps">
            <div class="step">
              <div class="step-icon">📥</div>
              <h4>输入编码</h4>
              <p>输入序列通过编码器编码为表示向量</p>
            </div>
            <div class="step">
              <div class="step-icon">🔄</div>
              <h4>自回归生成</h4>
              <p>解码器逐步生成输出，每步预测下一个token</p>
            </div>
            <div class="step">
              <div class="step-icon">📊</div>
              <h4>概率计算</h4>
              <p>计算词汇表中每个token的概率分布</p>
            </div>
            <div class="step">
              <div class="step-icon">🎯</div>
              <h4>采样策略</h4>
              <p>使用贪婪搜索、束搜索或随机采样选择输出token</p>
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
export default {
  name: 'TransformerArchitecture',
  data() {
    return {
      // 组件数据
    };
  },
  methods: {
    // 组件方法
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

.encoder-decoder {
  display: flex;
  gap: 20px;
  min-width: 800px;
}

.encoder, .decoder {
  flex: 1;
  padding: 15px;
  border: 1px solid rgba(0, 242, 255, 0.3);
  border-radius: 8px;
  background: rgba(0, 30, 60, 0.4);
}

.encoder h5, .decoder h5 {
  text-align: center;
  color: #51cf66;
  margin-bottom: 15px;
  font-size: 20px;
}

.blocks {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.block {
  padding: 12px;
  border: 1px solid rgba(100, 200, 255, 0.3);
  border-radius: 6px;
  background: rgba(0, 40, 80, 0.4);
}

.block-label {
  display: block;
  text-align: center;
  font-weight: bold;
  color: #ffd43b;
  margin-bottom: 8px;
}

.sublayers {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.sublayer {
  padding: 6px;
  background: rgba(100, 150, 255, 0.2);
  border: 1px solid rgba(100, 150, 255, 0.4);
  border-radius: 4px;
  text-align: center;
  font-size: 14px;
}

.process-steps, .inference-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.step {
  padding: 20px;
  background: rgba(0, 40, 80, 0.3);
  border: 1px solid rgba(0, 150, 200, 0.3);
  border-radius: 8px;
}

.step h4 {
  color: #4dabf7;
  margin-bottom: 10px;
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

.code-blocks {
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

@media (max-width: 768px) {
  .transformer-container {
    padding: 15px;
  }
  
  .transformer-title {
    font-size: 28px;
  }
  
  .encoder-decoder {
    flex-direction: column;
    min-width: auto;
  }
  
  .process-steps, .inference-steps, .component-grid {
    grid-template-columns: 1fr;
  }
}
</style>