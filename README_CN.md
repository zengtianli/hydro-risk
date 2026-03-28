# ⚠️ 风险图数据处理

[English](README.md) | **中文**

[![GitHub stars](https://img.shields.io/github/stars/zengtianli/hydro-risk)](https://github.com/zengtianli/hydro-risk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B.svg)](https://streamlit.io)
[![在线演示](https://img.shields.io/badge/%E5%9C%A8%E7%BA%BF%E6%BC%94%E7%A4%BA-hydro--risk.tianlizeng.cloud-brightgreen)](https://hydro-risk.tianlizeng.cloud)

风险图数据表自动填充 ETL 管线 -- GeoJSON 到 Excel，三阶段处理。

![screenshot](docs/screenshot.png)

## 功能特点

- **三阶段 ETL 管线** -- 数据库建设→预报断面→风险分析
- **14 个处理脚本** -- 每个处理一张特定数据表
- **GeoJSON→Excel** -- 自动提取空间数据填充表格
- **编码规范化** -- 自动大写、河流/流域编码生成
- **Web + CLI** -- Streamlit 交互界面 + 命令行脚本执行
- **处理报告** -- 详细日志含统计和验证结果

## 快速开始

```bash
git clone https://github.com/zengtianli/hydro-risk.git
cd hydro-risk
pip install -r requirements.txt
streamlit run app.py
```

## 处理管线

| 阶段 | 脚本 | 输入 | 输出 |
|------|------|------|------|
| 数据库建设 | 1.1-1.4 | GeoJSON（保护片、堤防、河流）+ CSV 映射表 | database_sx.xlsx |
| 预报断面 | 2.1 | GeoJSON（断面里程） | forecast_sx.xlsx |
| 风险分析 | 3.01-3.09 | GeoJSON + CSV + database_sx.xlsx | risk_sx.xlsx（18+ sheets） |

## 命令行用法

```bash
# 阶段一：建库
python 1.1_database_protection_area.py
python 1.2_database_dike_section.py
python 1.3_database_dike.py
python 1.4_database_river_centerline.py

# 阶段二：预报
python 2.1_forecast_cross_section.py

# 阶段三：风险分析（带参数）
python 3.01_risk_protection_info.py -g input/env.geojson -e output/risk_sx.xlsx
```

## 部署（VPS）

```bash
git clone https://github.com/zengtianli/hydro-risk.git
cd hydro-risk
pip install -r requirements.txt
nohup streamlit run app.py --server.port 8519 --server.headless true &
```

## Hydro Toolkit 插件

本项目是 [Hydro Toolkit](https://github.com/zengtianli/hydro-toolkit) 的插件，也可独立运行。在 Toolkit 的插件管理页面粘贴本仓库 URL 即可安装。也可以直接**[在线体验](https://hydro-risk.tianlizeng.cloud)**，无需安装。

## 许可证

MIT
