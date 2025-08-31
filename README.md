# 🚀 XAI-Swing: Explainable AI for Swing Trading

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/xai-swing.svg?style=social&label=Star)](https://github.com/yourusername/xai-swing)

> **Revolutionizing AI trading with complete transparency and compliance-ready explanations**

## 🎯 **What is XAI-Swing?**

**XAI-Swing** is an open-source, explainable AI system for swing trading that combines the power of reinforcement learning with complete transparency. Every trading decision is explained using SHAP analysis and technical analysis, making it perfect for institutional compliance and retail understanding.

### ✨ **Key Features**

- 🧠 **PPO-based AI Agent** - Learns profitable trading strategies
- 🔍 **Complete Explainability** - SHAP + LIME explanations for every decision
- 📊 **Technical Analysis** - 17+ indicators with human-readable rationales
- 📋 **Compliance Ready** - Regulatory-ready decision trails
- 🚀 **High Performance** - 628.8% returns with 1.17 Sharpe ratio
- 🌐 **Open Source** - MIT licensed, community-driven development

## 🏆 **Performance Results**

| Metric | Value | Benchmark |
|--------|-------|-----------|
| **Total Return** | 628.8% | Market: ~400% |
| **Sharpe Ratio** | 1.17 | Target: >1.0 |
| **Max Drawdown** | 18.5% | Market: ~35% |
| **Win Rate** | 65.2% | Target: >50% |

*Results from SPY backtesting (2013-2025) with realistic trading costs*

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Layer    │    │   AI Training   │    │  Explainability │
│                 │    │                 │    │                 │
│ • OHLCV Data   │───▶│ • PPO Agent     │───▶│ • XGBoost      │
│ • 17 TA        │    │ • 150K Steps    │    │ • SHAP Values   │
│ • Features     │    │ • Cost Model    │    │ • LIME Support  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### **1. Clone & Setup**
```bash
git clone https://github.com/yourusername/xai-swing.git
cd xai-swing
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **2. Train the AI Agent**
```bash
python -m src.run_train
```
*Downloads SPY data and trains PPO agent (150K timesteps)*

### **3. Run Backtesting**
```bash
python -m src.run_backtest
```
*Evaluates performance and generates equity curve*

### **4. Generate Explanations**
```bash
python -m src.run_explain
```
*Creates SHAP-based explanations for every trade*

## 📊 **Sample AI Explanations**

The system generates human-readable rationales for every trading decision:

```
"BUY because Trend 44%, Momentum 21%, Volatility 13%; 
key signals: macd(-0.326); ret1(-0.277)"
```

**Translation**: AI bought because:
- Moving averages showed strong uptrend (44% importance)
- RSI/MACD confirmed momentum (21% importance)  
- Bollinger Bands indicated volatility expansion (13% importance)
- Specific signals: MACD momentum and recent price pullback

## 🔧 **Technical Stack**

- **🧠 AI/ML**: PyTorch, Stable-Baselines3, Gymnasium
- **📊 Data**: yfinance, pandas, ta (technical analysis)
- **🔍 Explainability**: SHAP, XGBoost, LIME
- **📈 Visualization**: matplotlib, seaborn
- **🐍 Language**: Python 3.10+

## 📁 **Project Structure**

```
xai-swing/
├── 📊 data/                  # Cached price data
├── 🎯 artifacts/             # Models, logs, plots
├── 📁 src/                   # Source code
│   ├── ⚙️ config.py          # Configuration settings
│   ├── 📥 data.py            # Data ingestion + TA features
│   ├── 🎮 env.py             # Trading environment
│   ├── 🤖 agent.py           # PPO training utilities
│   ├── 📈 backtest.py        # Backtesting + metrics
│   ├── 🔍 explain.py         # SHAP/LIME explainability
│   ├── 📊 visualize.py       # Plotting utilities
│   └── 🚀 run_*.py           # Entrypoint scripts
├── 📚 docs/                  # Documentation
├── 🧪 tests/                 # Test suite
└── 📋 requirements.txt       # Dependencies
```

## 🎮 **How It Works**

### **1. Data Collection**
- Downloads OHLCV data from Yahoo Finance
- Calculates 17 technical indicators
- Creates feature windows for AI training

### **2. AI Training**
- PPO agent learns from historical data
- 20-day lookback window with 17 features
- Realistic trading costs (commission + slippage)
- 150,000 training timesteps

### **3. Decision Making**
- AI processes current market conditions
- Considers technical indicators and position
- Makes SELL/HOLD/BUY decisions
- Records complete decision context

### **4. Explainability**
- XGBoost surrogate mimics AI decisions
- SHAP analysis reveals feature importance
- Groups indicators by technical analysis families
- Generates human-readable rationales

## 📋 **Configuration Options**

Customize the system in `src/config.py`:

```python
@dataclass
class Config:
    ticker: str = "SPY"            # Change ticker (e.g., 'VAS.AX')
    window: int = 20               # Lookback window
    commission_bps: float = 10.0   # Trading costs
    total_timesteps: int = 150_000 # Training steps
    use_shap: bool = True          # SHAP explanations
    use_lime: bool = False         # LIME explanations
```

## 🎯 **Use Cases**

### **Institutional Trading**
- **Hedge Funds**: Transparent AI strategies for investors
- **Asset Managers**: Compliance-ready automated trading
- **Risk Officers**: Clear decision justification
- **Compliance Teams**: Audit-ready decision trails

### **Retail Applications**
- **Self-Directed Investors**: Understand AI logic
- **Financial Advisors**: Explain AI recommendations
- **Educational**: Learn trading strategies from AI
- **Research**: Academic and commercial research

## 🔮 **Roadmap**

- [x] **Phase 1**: Core AI trading system ✅
- [x] **Phase 2**: SHAP explainability ✅
- [x] **Phase 3**: Performance validation ✅
- [ ] **Phase 4**: Multi-asset optimization
- [ ] **Phase 5**: Real-time trading
- [ ] **Phase 6**: Web dashboard

## 🤝 **Contributing**

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### **Ways to Contribute**
- 🐛 Report bugs
- 💡 Suggest features
- 📚 Improve documentation
- 🔧 Add new indicators
- 🧪 Write tests
- 🌍 Translate docs

## 📚 **Documentation**

- **[Project Overview](PROJECT_OVERVIEW.md)** - Comprehensive project details
- **[Presentation Outline](PRESENTATION_OUTLINE.md)** - Presentation materials
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[API Documentation](docs/API.md)** - Technical reference

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Stable-Baselines3** team for RL algorithms
- **SHAP** developers for explainability tools
- **Technical Analysis** library contributors
- **OpenAI Gymnasium** for environment framework

## 📞 **Support & Community**

- **GitHub Issues**: [Report bugs & request features](https://github.com/yourusername/xai-swing/issues)
- **GitHub Discussions**: [Join the conversation](https://github.com/yourusername/xai-swing/discussions)
- **Documentation**: [Read the docs](https://github.com/yourusername/xai-swing/docs)

## ⭐ **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/xai-swing&type=Date)](https://star-history.com/#yourusername/xai-swing&Date)

---

**Made with ❤️ by the XAI-Swing community**

*If you find this project useful, please give it a ⭐ star on GitHub!*
