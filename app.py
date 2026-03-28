#!/usr/bin/env python3
"""风险图数据表填充 -- Streamlit Web 界面"""

import sys
import shutil
import tempfile
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.common.st_utils import page_config, footer
from src.risk.runner import run_script, PHASE_1, PHASE_2, PHASE_3, REPO_DIR

page_config("风险图数据 - Hydro Toolkit", "⚠️")

st.title("⚠️ 风险图数据表填充")
st.caption("GeoJSON → Excel 三阶段 ETL 管线（数据库建设 → 预报断面 → 风险分析）")

# ── Sidebar ──
with st.sidebar:
    st.header("使用说明")
    st.markdown("""
    **三阶段流程：**
    1. **数据库建设**（1.1-1.4）：从 GeoJSON 构建基础数据库
    2. **预报断面**（2.1）：处理断面里程数据
    3. **风险分析**（3.01-3.09）：生成风险图数据表

    每个阶段可独立运行，阶段三依赖阶段一的输出。
    """)
    st.markdown("---")
    st.markdown("**输入格式**")
    st.markdown("- GeoJSON: 保护片、堤段、堤防、断面等空间数据")
    st.markdown("- CSV: 行政区映射、GDP 数据等")
    st.markdown("- Excel: 目标输出工作簿（可选，自动创建）")

# ── Tabs ──
tab1, tab2, tab3 = st.tabs(["📦 阶段一：数据库建设", "📐 阶段二：预报断面", "⚠️ 阶段三：风险分析"])

def _run_phase(scripts, args_fn, tab_key):
    """Generic phase runner UI."""
    # Script selection
    selected = []
    cols = st.columns(min(len(scripts), 4))
    for i, (num, fname, label) in enumerate(scripts):
        with cols[i % len(cols)]:
            if st.checkbox(f"{num} {label}", value=True, key=f"{tab_key}_{num}"):
                selected.append((num, fname, label))

    if st.button("🚀 开始运行", key=f"run_{tab_key}", type="primary", use_container_width=True):
        if not selected:
            st.error("请至少选择一个脚本")
            return

        progress = st.progress(0, text="准备中...")
        results = []

        for i, (num, fname, label) in enumerate(selected):
            progress.progress(i / len(selected), text=f"正在运行: {num} {label}...")
            args = args_fn(num, fname)
            success, stdout, stderr = run_script(fname, args)
            results.append((num, label, success, stdout, stderr))

        progress.progress(1.0, text="运行完成！")

        # Show results
        for num, label, success, stdout, stderr in results:
            icon = "✅" if success else "❌"
            with st.expander(f"{icon} {num} {label}", expanded=not success):
                if stdout.strip():
                    st.text(stdout[-2000:])  # Last 2000 chars
                if stderr.strip():
                    st.code(stderr[-1000:], language="text")

# ── Tab 1: Phase 1 ──
with tab1:
    st.subheader("数据库建设（1.1-1.4）")
    st.markdown("从 GeoJSON 空间数据构建 `database_sx.xlsx` 基础数据库。")

    st.markdown("**上传文件**")
    p1_col1, p1_col2 = st.columns(2)
    with p1_col1:
        p1_geojson_bh = st.file_uploader("保护片 GeoJSON (1.1)", type=["geojson", "json"], key="p1_bh")
        p1_geojson_dd = st.file_uploader("堤段 GeoJSON (1.2)", type=["geojson", "json"], key="p1_dd")
    with p1_col2:
        p1_geojson_df = st.file_uploader("堤防 GeoJSON (1.3)", type=["geojson", "json"], key="p1_df")
        p1_geojson_rc = st.file_uploader("河流中心线 GeoJSON (1.4)", type=["geojson", "json"], key="p1_rc")

    p1_csv_region = st.file_uploader("行政区映射 CSV", type=["csv"], key="p1_region")
    p1_csv_city = st.file_uploader("城市-县-镇 CSV", type=["csv"], key="p1_city")

    # Prepare work directory
    if "p1_workdir" not in st.session_state:
        st.session_state["p1_workdir"] = tempfile.mkdtemp(prefix="hydro_risk_p1_")
    work_dir = Path(st.session_state["p1_workdir"])
    input_dir = work_dir / "input"
    output_dir = work_dir / "output"
    input_dir.mkdir(parents=True, exist_ok=True)
    (input_dir / "保护片").mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # Save uploaded files
    file_map = {
        "p1_bh": (input_dir / "保护片" / "env.geojson", p1_geojson_bh),
        "p1_dd": (input_dir / "geojson" / "dd.geojson", p1_geojson_dd),
        "p1_df": (input_dir / "df.geojson", p1_geojson_df),
        "p1_rc": (input_dir / "river_center_points.geojson", p1_geojson_rc),
    }
    for key, (path, fobj) in file_map.items():
        if fobj:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(fobj.getvalue())
    if p1_csv_region:
        (input_dir / "region_name_code.csv").write_bytes(p1_csv_region.getvalue())
    if p1_csv_city:
        (input_dir / "city_county_town.csv").write_bytes(p1_csv_city.getvalue())

    def p1_args(num, fname):
        """Build args for Phase 1 scripts -- they use hardcoded paths relative to cwd."""
        return None  # Phase 1 scripts don't accept argparse, they use hardcoded paths

    _run_phase(PHASE_1, p1_args, "p1")

    # Download output
    db_file = output_dir / "datebase_sx.xlsx"
    if not db_file.exists():
        db_file = REPO_DIR / "output" / "datebase_sx.xlsx"
    if db_file.exists():
        st.download_button(
            "📥 下载 database_sx.xlsx",
            db_file.read_bytes(),
            file_name="database_sx.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_db",
        )

# ── Tab 2: Phase 2 ──
with tab2:
    st.subheader("预报断面（2.1）")
    st.markdown("处理断面里程数据，生成 `forecast_sx.xlsx`。")

    p2_geojson = st.file_uploader("断面里程 GeoJSON", type=["geojson", "json"], key="p2_dm")

    def p2_args(num, fname):
        return None

    _run_phase(PHASE_2, p2_args, "p2")

    fc_file = REPO_DIR / "output" / "forecast_sx.xlsx"
    if fc_file.exists():
        st.download_button(
            "📥 下载 forecast_sx.xlsx",
            fc_file.read_bytes(),
            file_name="forecast_sx.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_fc",
        )

# ── Tab 3: Phase 3 ──
with tab3:
    st.subheader("风险分析（3.01-3.09）")
    st.markdown("从 GeoJSON + 基础数据库生成 `risk_sx.xlsx` 风险图数据表。")

    st.markdown("**上传文件**")
    p3_col1, p3_col2 = st.columns(2)
    with p3_col1:
        p3_geojson = st.file_uploader("保护片 GeoJSON", type=["geojson", "json"], key="p3_bh")
        p3_geojson_dd = st.file_uploader("堤段 GeoJSON (dd_fix)", type=["geojson", "json"], key="p3_dd")
        p3_geojson_dm = st.file_uploader("断面里程 GeoJSON", type=["geojson", "json"], key="p3_dm")
    with p3_col2:
        p3_geojson_df = st.file_uploader("堤防 GeoJSON", type=["geojson", "json"], key="p3_df")
        p3_geojson_fac = st.file_uploader("设施 GeoJSON (3.09)", type=["geojson", "json"], key="p3_fac")

    p3_csv_gdp = st.file_uploader("GDP 数据 CSV", type=["csv"], key="p3_gdp")
    p3_csv_region = st.file_uploader("行政区映射 CSV", type=["csv"], key="p3_region")
    p3_excel = st.file_uploader("目标 risk_sx.xlsx（已有则上传）", type=["xlsx"], key="p3_excel")

    # Save uploaded files to repo's input/output dirs for script access
    if p3_excel:
        (REPO_DIR / "output").mkdir(exist_ok=True)
        (REPO_DIR / "output" / "risk_sx.xlsx").write_bytes(p3_excel.getvalue())

    def p3_args(num, fname):
        """Build argparse args for Phase 3 scripts."""
        args = {}
        # Most 3.x scripts accept -g (geojson) and -e (excel output)
        risk_xlsx = REPO_DIR / "output" / "risk_sx.xlsx"
        if risk_xlsx.exists():
            args["-e"] = str(risk_xlsx)
        return args if args else None

    _run_phase(PHASE_3, p3_args, "p3")

    risk_file = REPO_DIR / "output" / "risk_sx.xlsx"
    if risk_file.exists():
        st.download_button(
            "📥 下载 risk_sx.xlsx",
            risk_file.read_bytes(),
            file_name="risk_sx.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_risk",
        )

# ── Footer ──
footer("风险图数据", repo_url="https://github.com/zengtianli/hydro-risk")
