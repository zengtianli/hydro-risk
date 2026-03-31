# hydro-risk — GeoJSON 水文数据 → Excel 风险评估工作簿 ETL 流水线

## Quick Reference

| 项目 | 路径/值 |
|------|---------|
| 入口 | `app.py` (Streamlit UI) |
| 数据库阶段 | `1.1_` ~ `1.4_database_*.py` |
| 预测阶段 | `2.1_forecast_*.py` |
| 风险分析 | `3.01_` ~ `3.09_risk_*.py` |
| 公共库 | `lib/` (excel_ops / file_ops / display) |
| 输出目录 | `output/` |

## 三阶段 Pipeline

| Phase | 脚本前缀 | 功能 |
|-------|----------|------|
| 1 — 数据库构建 | `1.x_database_*.py` | GeoJSON → 标准化底表 |
| 2 — 预测 | `2.x_forecast_*.py` | 水力模型 → 预测数据 |
| 3 — 风险分析 | `3.xx_risk_*.py` | 风险评分 → 18+ sheet 工作簿 |

## 常用命令

```bash
cd /Users/tianli/Dev/hydro-risk

# 启动 Streamlit UI（全流程入口）
streamlit run app.py

# 单独运行某一阶段脚本
python3 1.1_database_protection_area.py
python3 2.1_forecast_cross_section.py
python3 3.01_risk_protection_info.py

# 快速检查输出
python3 quick_check.py
python3 check_excel_headers.py
```

## 项目结构

```
hydro-risk/
├── app.py                    # Streamlit UI，流水线总控入口
├── 1.x_database_*.py         # Phase 1：底表构建（4 个脚本）
├── 2.x_forecast_*.py         # Phase 2：预测计算（1 个脚本）
├── 3.xx_risk_*.py            # Phase 3：风险评估（9 个脚本）
├── lib/
│   ├── excel_ops.py          # Excel 读写工具
│   ├── file_ops.py           # 文件路径操作
│   ├── display.py            # Streamlit 显示组件
│   └── hydraulic/            # 水力学计算模块
├── src/
│   ├── common/               # 公共逻辑
│   └── risk/                 # 风险模型
└── output/                   # 生成的 Excel 工作簿
```

## 开发约定

- 每个脚本可独立运行，也可由 `app.py` 统一调度
- 新增 Phase 脚本按命名规则 `{phase}.{seq}_{phase_name}_{topic}.py`
- 公共 Excel 操作统一走 `lib/excel_ops.py`，不要重复造轮子
- 输入 GeoJSON 放项目根目录或 `output/`，脚本内路径用 `Path(__file__).parent` 相对定位
