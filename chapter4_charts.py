import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # 无界面后端，直接保存图片
import matplotlib.pyplot as plt
# ---------------- 路径与全局样式 ----------------
XLSX_PATH = r"C:\study\大数据可视化分析\《Excel数据可视化——从图表到数据大屏》\第四章 人力资源可视化看板.xlsx"
OUT_DIR = r"C:\study\大数据可视化分析\第二章Python图表输出\chapter4-images"
os.makedirs(OUT_DIR, exist_ok=True)
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
# Excel 2016 默认主题色（环形图多系列/条形图单系列均取自主题色板）
EXCEL_COLORS = ["#4472C4", "#ED7D31", "#A5A5A5", "#FFC000", "#5B9BD5", "#70AD47"]
SERIES_BLUE = EXCEL_COLORS[0]  # 条形图/柱形图默认使用主题色 Accent1（蓝）
# ---------------- 1. 读取数据 ----------------
def load_data():
    """读取员工明细，并按工作簿中的辅助统计表口径汇总各维度。"""
    df = pd.read_excel(XLSX_PATH, sheet_name="202203人员基础信息",
                       usecols=["员工编号", "年龄", "性别", "学历", "婚姻状况",
                                "部门", "本月入转调", "年龄段"])
    df = df.dropna(subset=["员工编号"])
    # 年龄段分组（与工作簿 H 列口径一致：18-24 / 25-29 / 30-34 / 35-39 / 40=<）
    bins = [17, 24, 29, 34, 39, 200]
    labels = ["18-24", "25-29", "30-34", "35-39", "40=<"]
    df["年龄段"] = pd.cut(df["年龄"], bins=bins, labels=labels)
    return df
def aggregate(df):
    """各维度人数统计（对应工作簿 J:K 与 M:N 辅助区）。"""
    age = df["年龄段"].value_counts().reindex(
        ["18-24", "25-29", "30-34", "35-39", "40=<"])
    gender = df["性别"].value_counts().reindex(["男", "女"])
    edu = df["学历"].value_counts().reindex(
        ["专科以下", "专科", "本科", "硕士研究生", "博士研究生"])
    marriage = df["婚姻状况"].value_counts().reindex(["单身", "已婚", "离异"])
    dept = df["部门"].value_counts().reindex(
        ["销售部", "研发部", "信息技术部", "行政部", "人力资源部", "财务部"])
    turnover = df["本月入转调"].dropna().value_counts().reindex(["入职", "转入", "转出"])
    return age, gender, edu, marriage, dept, turnover
# ---------------- 2. 各图绘制函数 ----------------
def draw_doughnut(ax, series, title, show_pct_outside=False):
    """环形图：复现工作簿中 holeSize=75% 的 DoughnutChart，图例在右侧。
    show_pct_outside=True 时，在环形外侧绘制百分比标签
    """
    colors = [EXCEL_COLORS[i % len(EXCEL_COLORS)] for i in range(len(series))]
    wedges, texts = ax.pie(
        series.values, colors=colors, startangle=90, counterclock=False,
        wedgeprops=dict(width=0.75, edgecolor="white", linewidth=2))  # 环宽 25%
    total_val = series.sum()
    if show_pct_outside:
        for w, v in zip(wedges, series.values):
            ang = (w.theta2 + w.theta1) / 2
            r = 1.15  # 百分比标签放在环外面，半径1.15
            x, y = r * np.cos(np.deg2rad(ang)), r * np.sin(np.deg2rad(ang))
            pct = v / total_val * 100
            ax.text(x, y, f"{pct:.0f}%", ha="center", va="center", fontsize=10)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)
    ax.legend(wedges, series.index, loc="center left",
              bbox_to_anchor=(0.98, 0.5), frameon=False, fontsize=10)
    ax.set(aspect="equal")

def draw_barh(ax, series, title, show_value=True):
    """条形图（barDir=bar，横向）：单系列，主题蓝，数据标签显示数值。"""
    y = range(len(series))[::-1]  # 让第一项显示在最上方（与 Excel 条形图一致）
    ax.barh(list(y), series.values, color=SERIES_BLUE, height=0.6)
    ax.set_yticks(list(y))
    ax.set_yticklabels(series.index, fontsize=11)
    ax.invert_yaxis()  # 第一项在最上
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)
    if show_value:
        for yi, v in zip(y, series.values):
            ax.text(v + max(series.values) * 0.01, yi, f"{int(v)}",
                    va="center", fontsize=10, color="#333333")
    ax.spines[["top", "right"]].set_visible(False)
def draw_bar(ax, series, title, show_value=True):
    """柱形图（barDir=col，纵向）：单系列，主题蓝，数据标签显示数值。"""
    x = range(len(series))
    ax.bar(x, series.values, color=SERIES_BLUE, width=0.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels(series.index, fontsize=11)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)
    if show_value:
        for xi, v in zip(x, series.values):
            ax.text(xi, v + max(series.values) * 0.02, f"{int(v)}",
                    ha="center", fontsize=10, color="#333333")
    ax.set_ylim(0, max(series.values) * 1.15)
    ax.spines[["top", "right"]].set_visible(False)
# ---------------- 3. 主流程：单图 + 组合看板 ----------------
def main():
    df = load_data()
    age, gender, edu, marriage, dept, turnover = aggregate(df)
    total = len(df)
    print(f"总人数：{total}")
    for name, s in [("年龄", age), ("性别", gender), ("学历", edu),
                    ("婚姻状况", marriage), ("部门", dept), ("入转调", turnover)]:
        print(f"\n{name}：\n{s}")
    # --- 单图输出（与工作簿 6 张图一一对应） ---
    singles = [
        ("01_年龄_环形图",    lambda ax: draw_doughnut(ax, age, "年龄", show_pct_outside=True)),
        ("02_性别_环形图",    lambda ax: draw_doughnut(ax, gender, "性别", show_pct_outside=True)),
        ("03_婚姻状况_环形图", lambda ax: draw_doughnut(ax, marriage, "婚姻状况", show_pct_outside=True)),
        ("04_学历_条形图",    lambda ax: draw_barh(ax, edu, "学历")),
        ("05_入转调_柱形图",  lambda ax: draw_bar(ax, turnover, "入转调")),
        ("06_部门_条形图",    lambda ax: draw_barh(ax, dept, "部门")),
    ]
    for fname, draw in singles:
        fig, ax = plt.subplots(figsize=(7, 5), dpi=120)
        draw(ax)
        fig.tight_layout()
        fig.savefig(os.path.join(OUT_DIR, fname + ".png"), bbox_inches="tight")
        plt.close(fig)
        print(f"已生成：{fname}.png")
    # --- 组合看板（2行 × 3列，布局与工作簿一致） ---
    fig, axes = plt.subplots(2, 3, figsize=(19, 10), dpi=120)
    draw_doughnut(axes[0][0], age, "年龄", show_pct_outside=True)
    draw_doughnut(axes[0][1], gender, "性别", show_pct_outside=True)
    draw_doughnut(axes[0][2], marriage, "婚姻状况", show_pct_outside=True)
    draw_barh(axes[1][0], edu, "学历", True)
    draw_bar(axes[1][1], turnover, "入转调", True)
    draw_barh(axes[1][2], dept, "部门", True)
    fig.suptitle("公司人员结构看板", fontsize=18, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    dash = os.path.join(OUT_DIR, "公司人员结构看板.png")
    fig.savefig(dash, bbox_inches="tight")
    plt.close(fig)
    print(f"已生成：公司人员结构看板.png\n全部输出目录：{OUT_DIR}")
if __name__ == "__main__":
    main()
