# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, Wedge, Circle, PathPatch
from matplotlib.path import Path
from matplotlib.path import Path as MPath
import matplotlib.patheffects as pe
from matplotlib.collections import PatchCollection
import numpy as np
import os

# ==================== 全局配置 ====================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'STSong']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.15

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# 统一配色
COLORS = {
    'blue': '#4472C4',
    'orange': '#ED7D31',
    'green': '#70AD47',
    'red': '#C00000',
    'purple': '#7030A0',
    'teal': '#00B0F0',
    'pink': '#FF6699',
    'gold': '#FFC000',
    'dark_blue': '#2F5597',
    'light_blue': '#5B9BD5',
    'light_gray': '#D9D9D9',
    'gray': '#A5A5A5',
    'dark_gray': '#595959',
    'bg': '#FAFAFA',
}

BAR_GRADIENT_COLORS = ['#4472C4', '#5B9BD5']


def save_fig(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, facecolor='white', bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)
    print(f'  [OK] {name}')


def make_gradient_bar(ax, x, y, width=0.6, color_low='#5B9BD5', color_high='#2F5597'):
    """绘制渐变柱形"""
    for i, (xi, yi) in enumerate(zip(x, y)):
        grad = np.linspace(0, 1, 256).reshape(-1, 1)
        grad_img = np.hstack([
            np.ones((256, 1)) * np.array(
                [int(color_low[j*2+1:j*2+3], 16) * (1-g) + int(color_high[j*2+1:j*2+3], 16) * g
                 for g in np.linspace(0, 1, 256)]
            )[:, None] for j in range(3)
        ]) / 255.0
        from matplotlib.image import AxesImage
        import matplotlib.transforms as mtransforms
        rect = mtransforms.Bbox([[xi - width/2, 0], [xi + width/2, yi]])
        im = ax.imshow(
            grad_img, aspect='auto', origin='lower',
            extent=[xi - width/2, xi + width/2, 0, yi],
            zorder=2, clip_on=True
        )
    return im


# ==================== 图表1: 渐变柱形图 ====================
def chart_01():
    fig, ax = plt.subplots(figsize=(8, 5))
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    values = [2354, 1902, 3524, 2698, 2896, 2563]

    x = np.arange(len(regions))
    c_low = np.array([0x5B/255, 0x9B/255, 0xD5/255])
    c_high = np.array([0x2F/255, 0x55/255, 0x97/255])
    for i, (xi, yi) in enumerate(zip(x, values)):
        grad = np.zeros((256, 1, 3))
        for c_idx in range(3):
            grad[:, 0, c_idx] = np.linspace(c_low[c_idx], c_high[c_idx], 256)
        ax.imshow(grad, aspect='auto', origin='lower',
                  extent=[xi - 0.35, xi + 0.35, 0, yi], zorder=2)

    ax.set_xticks(x)
    ax.set_xticklabels(regions, fontsize=11)
    ax.set_ylabel('销售量', fontsize=12)
    ax.set_xlim(-0.6, len(regions) - 0.4)
    ax.set_ylim(0, max(values) * 1.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(colors='#666666')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    for xi, yi in zip(x, values):
        ax.text(xi, yi + 50, str(yi), ha='center', va='bottom', fontsize=10, color='#333333')

    save_fig(fig, '01_渐变柱形图.png')


# ==================== 图表2: 带均值柱形图 ====================
def chart_02():
    fig, ax = plt.subplots(figsize=(8, 5))
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    values = [2354, 1902, 3524, 2698, 2896, 2563]
    mean_val = np.mean(values)

    x = np.arange(len(regions))
    colors = ['#4472C4' if v >= mean_val else '#5B9BD5' for v in values]
    bars = ax.bar(x, values, 0.55, color=colors, zorder=2, edgecolor='white', linewidth=0.5)

    ax.axhline(y=mean_val, color='#ED7D31', linewidth=1.5, linestyle='--', zorder=3)
    ax.text(len(regions) - 0.5, mean_val + 60, f'均值: {mean_val:.0f}',
            ha='right', va='bottom', fontsize=10, color='#ED7D31', fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(regions, fontsize=11)
    ax.set_ylabel('销售量', fontsize=12)
    ax.set_xlim(-0.6, len(regions) - 0.4)
    ax.set_ylim(0, max(values) * 1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    for xi, yi in zip(x, values):
        ax.text(xi, yi + 50, str(yi), ha='center', va='bottom', fontsize=10, color='#333333')

    save_fig(fig, '02_带均值柱形图.png')


# ==================== 图表3: 渐变圆角柱形图 ====================
def chart_03():
    fig, ax = plt.subplots(figsize=(8, 5))
    products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
    values = [653, 523, 648, 856, 714, 785]

    y = np.arange(len(products))
    max_val = max(values) * 1.2

    for i, (yi, vi) in enumerate(zip(y, values)):
        color = plt.cm.Blues(0.4 + 0.5 * vi / max(values))
        bbox = FancyBboxPatch((0, yi - 0.35), vi, 0.7,
                               boxstyle="round,pad=0,rounding_size=0.15",
                               facecolor=color, edgecolor='white', linewidth=0.5, zorder=2)
        ax.add_patch(bbox)
        ax.text(vi + 15, yi, str(vi), ha='left', va='center', fontsize=10, color='#333333')

    ax.set_yticks(y)
    ax.set_yticklabels(products, fontsize=11)
    ax.set_xlabel('销量', fontsize=12)
    ax.set_xlim(0, max_val)
    ax.set_ylim(-0.5, len(products) - 0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.invert_yaxis()
    ax.xaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    save_fig(fig, '03_渐变圆角柱形图.png')


# ==================== 图表4: 标注柱形图 ====================
def chart_04():
    fig, ax = plt.subplots(figsize=(8, 5))
    products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜', '眼影', '气垫']
    values = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]
    max_v = max(values)

    x = np.arange(len(products))
    colors = ['#ED7D31' if v == max_v else '#4472C4' for v in values]
    ax.bar(x, values, 0.55, color=colors, zorder=2, edgecolor='white', linewidth=0.5)

    for xi, yi in zip(x, values):
        color = '#ED7D31' if yi == max_v else '#333333'
        fw = 'bold' if yi == max_v else 'normal'
        ax.text(xi, yi + 150, str(yi), ha='center', va='bottom',
                fontsize=9, color=color, fontweight=fw)

    ax.set_xticks(x)
    ax.set_xticklabels(products, fontsize=10)
    ax.set_ylabel('销量', fontsize=12)
    ax.set_xlim(-0.6, len(products) - 0.4)
    ax.set_ylim(0, max_v * 1.18)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    ax.annotate('最大值', xy=(0, 9221), xytext=(0.8, 9600),
                fontsize=10, color='#ED7D31', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#ED7D31', lw=1.5),
                ha='center')

    save_fig(fig, '04_标注柱形图.png')


# ==================== 图表5: 层叠柱形图 ====================
def chart_05():
    fig, ax = plt.subplots(figsize=(8, 5))
    quarters = ['2021Q1', 'Q2', 'Q3', 'Q4', '2022Q1', 'Q2']
    sales = [3121, 4086, 4321, 4601, 4936, 4231]
    profit = [1020, 1421, 1502, 1623, 1781, 1432]

    x = np.arange(len(quarters))
    width = 0.5

    ax.bar(x, sales, width, color='#4472C4', zorder=2, label='销售额', alpha=0.85)
    ax.bar(x, profit, width * 0.5, color='#ED7D31', zorder=3, label='利润额', alpha=0.9)

    for xi, (si, pi) in enumerate(zip(sales, profit)):
        ax.text(xi, si + 80, str(si), ha='center', va='bottom', fontsize=9, color='#4472C4')
        ax.text(xi, pi + 80, str(pi), ha='center', va='bottom', fontsize=8, color='#ED7D31')

    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=10)
    ax.set_ylabel('金额', fontsize=12)
    ax.set_xlim(-0.6, len(quarters) - 0.4)
    ax.set_ylim(0, max(sales) * 1.18)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc='upper left', fontsize=10, frameon=False)

    save_fig(fig, '05_层叠柱形图.png')


# ==================== 图表6: 蝴蝶图 ====================
def chart_06():
    fig, ax = plt.subplots(figsize=(9, 5))
    regions = ['华东', '西北', '东北', '华北', '华南']
    val_2022 = [1215, 1321, 1426, 1531, 2238]
    val_2021 = [1003, 1265, 1531, 1436, 2066]

    y = np.arange(len(regions))
    max_val = max(max(val_2022), max(val_2021))

    ax.barh(y, [-v for v in val_2021], 0.45, color='#5B9BD5', zorder=2, label='2021年销量')
    ax.barh(y, val_2022, 0.45, color='#ED7D31', zorder=2, label='2022年销量')

    for yi, (v22, v21) in enumerate(zip(val_2022, val_2021)):
        ax.text(v22 + 40, yi, str(v22), ha='left', va='center', fontsize=9, color='#ED7D31')
        ax.text(-v21 - 40, yi, str(v21), ha='right', va='center', fontsize=9, color='#5B9BD5')

    ax.set_yticks(y)
    ax.set_yticklabels(regions, fontsize=11)
    ax.set_xlim(-max_val * 1.35, max_val * 1.35)
    ax.set_ylim(-0.6, len(regions) - 0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.axvline(x=0, color='#999999', linewidth=0.8)
    ax.set_xticks([])
    ax.legend(loc='lower right', fontsize=10, frameon=False)

    ax.text(-max_val * 1.1, -0.9, '2021年', ha='center', fontsize=10, color='#5B9BD5', fontweight='bold')
    ax.text(max_val * 1.1, -0.9, '2022年', ha='center', fontsize=10, color='#ED7D31', fontweight='bold')

    save_fig(fig, '06_蝴蝶图.png')


# ==================== 图表7: 蝴蝶图(百分比) ====================
def chart_07():
    fig, ax = plt.subplots(figsize=(9, 5))
    regions = ['华东', '西北', '东北', '华北', '华南']
    pct_2022 = [0.36, 0.31, 0.18, 0.13, 0.09]
    pct_2021 = [0.42, 0.26, 0.19, 0.12, 0.05]

    y = np.arange(len(regions))
    max_pct = max(max(pct_2022), max(pct_2021))

    ax.barh(y, [-v for v in pct_2021], 0.45, color='#5B9BD5', zorder=2, label='2021年')
    ax.barh(y, pct_2022, 0.45, color='#ED7D31', zorder=2, label='2022年')

    for yi, (v22, v21) in enumerate(zip(pct_2022, pct_2021)):
        ax.text(v22 + 0.01, yi, f'{v22:.0%}', ha='left', va='center', fontsize=9, color='#ED7D31')
        ax.text(-v21 - 0.01, yi, f'{v21:.0%}', ha='right', va='center', fontsize=9, color='#5B9BD5')

    ax.set_yticks(y)
    ax.set_yticklabels(regions, fontsize=11)
    ax.set_xlim(-max_pct * 1.5, max_pct * 1.5)
    ax.set_ylim(-0.6, len(regions) - 0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.axvline(x=0, color='#999999', linewidth=0.8)
    ax.set_xticks([])
    ax.legend(loc='lower right', fontsize=10, frameon=False)

    save_fig(fig, '07_蝴蝶图_百分比.png')


# ==================== 图表8: 数值百分比 ====================
def chart_08():
    fig, ax = plt.subplots(figsize=(9, 5))
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    values = [4321, 1946, 1536, 1872, 1369, 2109]
    yoy = [-0.136, -0.208, -0.093, -0.159, -0.179, -0.058]
    max_val = max(values)

    y = np.arange(len(regions))
    bar_width = 0.45
    unit = max_val / 4

    ax.barh(y, values, bar_width, color='#4472C4', zorder=2)

    for yi, (vi, yi_pct) in enumerate(zip(values, yoy)):
        ax.text(vi + 60, yi, f'{vi}  {yi_pct:.1%}', ha='left', va='center',
                fontsize=9, color='#333333')

    marker_x = unit
    for yi in y:
        ax.plot(marker_x, yi, marker='D', color='#ED7D31', markersize=7, zorder=3)

    ax.set_yticks(y)
    ax.set_yticklabels(regions, fontsize=11)
    ax.set_xlim(0, max_val * 1.45)
    ax.set_ylim(-0.5, len(regions) - 0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.invert_yaxis()
    ax.set_xticks([])

    ax.axvline(x=marker_x, color='#ED7D31', linewidth=1, linestyle=':', zorder=1, alpha=0.5)
    ax.text(marker_x, -0.7, '均值', ha='center', fontsize=9, color='#ED7D31')

    save_fig(fig, '08_数值百分比.png')


# ==================== 图表9: 对比柱形图 ====================
def chart_09():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    products = ['口红', '面膜', '隔离', '防晒', '精华']
    val_2021 = [3568, 4135, 4436, 4106, 4936]
    val_2022 = [2569, 3241, 2965, 3209, 3541]
    diff = [a - b for a, b in zip(val_2021, val_2022)]

    x = np.arange(len(products))
    width = 0.32
    ax.bar(x - width/2, val_2021, width, color='#4472C4', zorder=2, label='2021销量')
    ax.bar(x + width/2, val_2022, width, color='#ED7D31', zorder=2, label='2022销量')

    for xi, d in zip(x, diff):
        ax.plot([xi, xi], [max(val_2021[xi], val_2022[xi]) + 80,
                           max(val_2021[xi], val_2022[xi]) + 250],
                color='#595959', linewidth=1.5, zorder=3)
        ax.plot(xi, max(val_2021[xi], val_2022[xi]) + 280,
                marker='D', color='#595959', markersize=6, zorder=3)
        ax.text(xi, max(val_2021[xi], val_2022[xi]) + 320,
                str(d), ha='center', va='bottom', fontsize=9, color='#595959')

    ax.set_xticks(x)
    ax.set_xticklabels(products, fontsize=11)
    ax.set_ylabel('销量', fontsize=12)
    ax.set_xlim(-0.5, len(products) - 0.5)
    ax.set_ylim(0, max(max(val_2021), max(val_2022)) * 1.25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=10, frameon=False)

    save_fig(fig, '09_对比柱形图.png')


# ==================== 图表10: 甘特图 ====================
def chart_10():
    fig, ax = plt.subplots(figsize=(10, 5))
    tasks = ['制定计划', '方案设计', '资源调配', '第一阶段', '第二阶段', '第三阶段', '项目总结']
    start_dates = ['2022-03-01', '2022-03-13', '2022-03-22', '2022-04-02',
                   '2022-04-16', '2022-05-11', '2022-05-26']
    durations = [11, 8, 10, 13, 24, 14, 7]
    progress = [0.51, 0.32, 0.21, 0.85, 0.36, 0.68, 0.68]

    from datetime import datetime
    starts = [datetime.strptime(d, '%Y-%m-%d') for d in start_dates]
    start_nums = [(s - starts[0]).days for s in starts]

    y = np.arange(len(tasks))

    for i in range(len(tasks)):
        ax.barh(i, durations[i], left=start_nums[i], height=0.45,
                color='#D9D9D9', zorder=2, edgecolor='#BBBBBB', linewidth=0.5)
        ax.barh(i, durations[i] * progress[i], left=start_nums[i], height=0.45,
                color='#4472C4', zorder=3, alpha=0.85)
        ax.text(start_nums[i] + durations[i] / 2, i,
                f'{progress[i]:.0%}', ha='center', va='center',
                fontsize=9, color='white', fontweight='bold', zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels(tasks, fontsize=10)
    ax.set_xlabel('天数', fontsize=12)
    ax.set_xlim(-2, max(s + d for s, d in zip(start_nums, durations)) + 5)
    ax.set_ylim(-0.6, len(tasks) - 0.4)
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.xaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    save_fig(fig, '10_甘特图.png')


# ==================== 图表11: 平滑折线图 ====================
def chart_11():
    fig, ax = plt.subplots(figsize=(9, 5))
    labels = ['5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月', '2月', '3月']
    values = [146, 198, 296, 412, 506, 615, 789, 1021, 3782, 3215, 2936]

    x = np.arange(len(labels))
    ax.plot(x, values, color='#4472C4', linewidth=2, zorder=3)
    ax.plot(x, values, marker='o', color='#4472C4', markersize=5,
            markerfacecolor='white', markeredgewidth=2, markeredgecolor='#4472C4', zorder=4)

    ax.fill_between(x, values, alpha=0.08, color='#4472C4', zorder=2)

    max_idx = np.argmax(values)
    ax.annotate(f'峰值: {values[max_idx]}', xy=(max_idx, values[max_idx]),
                xytext=(max_idx - 1.5, values[max_idx] + 400),
                fontsize=10, color='#C00000', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#C00000', lw=1.5))

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('销量', fontsize=12)
    ax.set_xlim(-0.3, len(labels) - 0.7)
    ax.set_ylim(0, max(values) * 1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    ax.axvline(x=7.5, color='#DDDDDD', linewidth=1, linestyle='--', zorder=1)
    ax.text(3.5, max(values) * 1.12, '2021年', ha='center', fontsize=10, color='#999999')
    ax.text(9, max(values) * 1.12, '2022年', ha='center', fontsize=10, color='#999999')

    save_fig(fig, '11_平滑折线图.png')


# ==================== 图表12: 菱形走势图 ====================
def chart_12():
    fig, ax = plt.subplots(figsize=(8, 5))
    months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月']
    rates = [0.536, 0.498, 0.527, 0.708, 0.609, 0.496, 0.586, 0.704]

    x = np.arange(len(months))
    ax.plot(x, rates, color='#4472C4', linewidth=2, zorder=3)

    for xi, ri in zip(x, rates):
        ax.plot(xi, ri, marker='D', color='#4472C4', markersize=8,
                markerfacecolor='#5B9BD5', markeredgecolor='#2F5597',
                markeredgewidth=1.5, zorder=4)
        ax.text(xi, ri + 0.025, f'{ri:.1%}', ha='center', va='bottom',
                fontsize=8, color='#333333')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=10)
    ax.set_ylabel('完成率', fontsize=12)
    ax.set_xlim(-0.3, len(months) - 0.7)
    ax.set_ylim(0.3, 0.85)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    save_fig(fig, '12_菱形走势图.png')


# ==================== 图表13: 对比折线图 ====================
def chart_13():
    fig, ax = plt.subplots(figsize=(8, 5))
    months = ['1月', '2月', '3月', '4月', '5月', '6月']
    val_2021 = [1686, 1345, 1934, 1658, 1865, 1936]
    val_2022 = [1385, 1846, 1654, 1936, 2564, 2236]

    x = np.arange(len(months))
    ax.plot(x, val_2021, color='#5B9BD5', linewidth=2, marker='o', markersize=6,
            markerfacecolor='white', markeredgewidth=2, markeredgecolor='#5B9BD5',
            zorder=3, label='2021年')
    ax.plot(x, val_2022, color='#ED7D31', linewidth=2, marker='o', markersize=6,
            markerfacecolor='white', markeredgewidth=2, markeredgecolor='#ED7D31',
            zorder=3, label='2022年')

    for xi, (v1, v2) in enumerate(zip(val_2021, val_2022)):
        ax.text(xi, v1 - 80, str(v1), ha='center', va='top', fontsize=8, color='#5B9BD5')
        ax.text(xi, v2 + 60, str(v2), ha='center', va='bottom', fontsize=8, color='#ED7D31')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=10)
    ax.set_ylabel('销量', fontsize=12)
    ax.set_xlim(-0.3, len(months) - 0.7)
    ax.set_ylim(min(min(val_2021), min(val_2022)) * 0.7, max(max(val_2021), max(val_2022)) * 1.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc='upper left', fontsize=10, frameon=False)

    save_fig(fig, '13_对比折线图.png')


# ==================== 图表14: 单值圆环图 ====================
def chart_14():
    fig, ax = plt.subplots(figsize=(6, 6))
    rate = 0.85
    sizes = [rate, 1 - rate]
    colors_pie = ['#4472C4', '#E8E8E8']
    explode = (0, 0)

    wedges, _ = ax.pie(sizes, colors=colors_pie, startangle=90,
                        wedgeprops=dict(width=0.25, edgecolor='white', linewidth=2))

    ax.text(0, 0, f'{rate:.0%}', ha='center', va='center',
            fontsize=28, fontweight='bold', color='#4472C4')
    ax.text(0, -0.15, '完成率', ha='center', va='center',
            fontsize=12, color='#999999')

    save_fig(fig, '14_单值圆环图.png')


# ==================== 图表15: 水球图 ====================
def chart_15():
    fig, ax = plt.subplots(figsize=(6, 6))
    rate = 0.65

    theta_full = np.linspace(0, 2 * np.pi, 300)
    cx = 0.5 * np.ones_like(theta_full)
    cy = 0.5 * np.ones_like(theta_full)
    r = 0.4

    circle_x = cx + r * np.cos(theta_full)
    circle_y = cy + r * np.sin(theta_full)

    water_level = 0.5 - r + rate * 2 * r

    wave1_y = water_level + 0.015 * np.sin(10 * theta_full)
    wave2_y = water_level + 0.012 * np.sin(12 * theta_full + 2) + 0.008

    for wave_y, color, alpha, zorder in [
        (wave1_y, '#4472C4', 0.25, 2),
        (wave2_y, '#5B9BD5', 0.45, 3),
    ]:
        verts_x = np.concatenate([circle_x, circle_x[::-1]])
        verts_y = np.concatenate([wave_y, np.full_like(circle_y, circle_y.min() - 0.1)])
        from matplotlib.patches import Polygon
        poly = Polygon(np.column_stack([verts_x, verts_y]),
                       closed=True, facecolor=color, alpha=alpha, edgecolor='none', zorder=zorder)
        poly.set_clip_path(plt.Circle((0.5, 0.5), r, transform=ax.transAxes))
        ax.add_patch(poly)

    circle = plt.Circle((0.5, 0.5), r, transform=ax.transAxes,
                         facecolor='none', edgecolor='#4472C4', linewidth=2.5, zorder=5)
    ax.add_patch(circle)

    ax.text(0.5, 0.5, f'{rate:.0%}', ha='center', va='center',
            fontsize=28, fontweight='bold', color='#2F5597', zorder=6,
            transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    save_fig(fig, '15_水球图.png')


# ==================== 图表16: 波浪水球图 ====================
def chart_16():
    fig, ax = plt.subplots(figsize=(6, 6))
    rate = 0.65
    r = 0.4

    theta_full = np.linspace(0, 2 * np.pi, 300)
    circle_x = 0.5 + r * np.cos(theta_full)
    circle_y = 0.5 + r * np.sin(theta_full)

    water_level = 0.5 - r + rate * 2 * r

    from matplotlib.patches import Polygon

    for amp, freq, phase, color, alpha, zorder in [
        (0.018, 8, 0, '#4472C4', 0.2, 2),
        (0.014, 11, 1.5, '#5B9BD5', 0.35, 3),
        (0.010, 14, 3.0, '#2F5597', 0.3, 4),
    ]:
        wave_y = water_level + amp * np.sin(freq * theta_full + phase)
        verts_x = np.concatenate([circle_x, circle_x[::-1]])
        verts_y = np.concatenate([wave_y, np.full_like(circle_y, circle_y.min() - 0.1)])
        poly = Polygon(np.column_stack([verts_x, verts_y]),
                       closed=True, facecolor=color, alpha=alpha, edgecolor='none', zorder=zorder)
        poly.set_clip_path(plt.Circle((0.5, 0.5), r, transform=ax.transAxes))
        ax.add_patch(poly)

    circle = plt.Circle((0.5, 0.5), r, transform=ax.transAxes,
                         facecolor='none', edgecolor='#4472C4', linewidth=2.5, zorder=5)
    ax.add_patch(circle)

    ax.text(0.5, 0.5, f'{rate:.0%}', ha='center', va='center',
            fontsize=28, fontweight='bold', color='white', zorder=6,
            transform=ax.transAxes,
            path_effects=[pe.withStroke(linewidth=2, foreground='#2F5597')])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    save_fig(fig, '16_波浪水球图.png')


# ==================== 图表17: 玉玦图 ====================
def chart_17():
    fig, ax = plt.subplots(figsize=(7, 7))
    labels = ['>=50', '[40,50)', '[30,40)', '[20,30)']
    values = [0.125, 0.208, 0.292, 0.375]
    colors_pie = ['#2F5597', '#4472C4', '#5B9BD5', '#ED7D31']

    gap_angle = 3
    total = sum(values)
    start_angle = 90

    for i, (val, color, label) in enumerate(zip(values, colors_pie, labels)):
        angle = val / total * 360 - gap_angle
        wedge = Wedge((0, 0), 1.0, start_angle, start_angle + angle,
                       width=0.3, facecolor=color, edgecolor='white', linewidth=1, alpha=0.85)
        ax.add_patch(wedge)

        mid_angle = np.radians(start_angle + angle / 2)
        ax.text(1.2 * np.cos(mid_angle), 1.2 * np.sin(mid_angle),
                f'{label}\n{val:.1%}', ha='center', va='center',
                fontsize=9, color='#333333')

        start_angle += val / total * 360

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')

    save_fig(fig, '17_玉玦图.png')


# ==================== 图表18: 跑道图 ====================
def chart_18():
    fig, ax = plt.subplots(figsize=(7, 7))
    depts = ['人力部', '行政部', '财务部', '工程部', '采购部', '销售部']
    values = [130, 226, 238, 293, 326, 451]
    total = sum(values)
    colors_pie = plt.cm.Set3(np.linspace(0, 1, len(depts)))

    gap_angle = 2
    start_angle = 90

    for i, (val, color, dept) in enumerate(zip(values, colors_pie, depts)):
        angle = val / total * 360 - gap_angle
        radius = 1.0 - i * 0.12
        wedge = Wedge((0, 0), radius, start_angle, start_angle + angle,
                       width=0.1, facecolor=color, edgecolor='white', linewidth=0.5, alpha=0.85)
        ax.add_patch(wedge)

        mid_angle = np.radians(start_angle + angle / 2)
        label_r = radius + 0.08
        ax.text(label_r * np.cos(mid_angle), label_r * np.sin(mid_angle),
                f'{dept}', ha='center', va='center', fontsize=7, color='#333333', rotation=0)

        start_angle += val / total * 360

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    save_fig(fig, '18_跑道图.png')


# ==================== 图表19: 南丁格尔圆饼图 ====================
def chart_19():
    fig, ax = plt.subplots(figsize=(7, 7))
    depts = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
    pcts = [0.292, 0.227, 0.175, 0.136, 0.103, 0.067]
    colors_pie = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47']

    n = len(depts)
    angle_per_sector = 360 / n
    gap = 1

    for i, (dept, pct, color) in enumerate(zip(depts, pcts, colors_pie)):
        start = i * angle_per_sector + gap / 2
        end = (i + 1) * angle_per_sector - gap / 2
        radius = pct / max(pcts) * 1.0
        wedge = Wedge((0, 0), radius, start, end,
                       facecolor=color, edgecolor='white', linewidth=1, alpha=0.85)
        ax.add_patch(wedge)

        mid_angle = np.radians((start + end) / 2)
        label_r = radius + 0.15
        ax.text(label_r * np.cos(mid_angle), label_r * np.sin(mid_angle),
                f'{dept}\n{pct:.1%}', ha='center', va='center',
                fontsize=8, color='#333333')

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    save_fig(fig, '19_南丁格尔圆饼图.png')


# ==================== 图表20: 南丁格尔圆环图 ====================
def chart_20():
    fig, ax = plt.subplots(figsize=(7, 7))
    labels = ['[20,30)', '[30,40)', '[40,50)', '>=50']
    pcts = [0.375, 0.292, 0.208, 0.125]
    colors_pie = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000']

    n = len(labels)
    angle_per_sector = 360 / n
    gap = 2

    for i, (label, pct, color) in enumerate(zip(labels, pcts, colors_pie)):
        start = i * angle_per_sector + gap / 2
        end = (i + 1) * angle_per_sector - gap / 2
        radius = pct / max(pcts) * 1.0
        wedge = Wedge((0, 0), radius, start, end,
                       width=0.35, facecolor=color, edgecolor='white', linewidth=1, alpha=0.85)
        ax.add_patch(wedge)

        mid_angle = np.radians((start + end) / 2)
        label_r = radius + 0.18
        ax.text(label_r * np.cos(mid_angle), label_r * np.sin(mid_angle),
                f'{label}\n{pct:.1%}', ha='center', va='center',
                fontsize=9, color='#333333')

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    save_fig(fig, '20_南丁格尔圆环图.png')


# ==================== 图表22: 仪表盘图 ====================
def chart_22():
    fig, ax = plt.subplots(figsize=(7, 5))
    pointer_val = 76
    min_val, max_val = 50, 150

    scale_colors = ['#C00000', '#FFC000', '#70AD47']
    ranges = [(50, 83), (83, 117), (117, 150)]

    for (lo, hi), color in zip(ranges, scale_colors):
        theta_lo = np.pi - (lo - min_val) / (max_val - min_val) * np.pi
        theta_hi = np.pi - (hi - min_val) / (max_val - min_val) * np.pi
        theta = np.linspace(theta_hi, theta_lo, 50)
        x_outer = 1.0 * np.cos(theta)
        y_outer = 1.0 * np.sin(theta)
        x_inner = 0.75 * np.cos(theta)
        y_inner = 0.75 * np.sin(theta)

        verts = np.column_stack([
            np.concatenate([x_outer, x_inner[::-1]]),
            np.concatenate([y_outer, y_inner[::-1]])
        ])
        codes = [MPath.MOVETO] + [MPath.LINETO] * (len(verts) - 1)
        path = MPath(verts, codes)
        patch = PathPatch(path, facecolor=color, edgecolor='white', linewidth=1, alpha=0.7)
        ax.add_patch(patch)

    for v in range(50, 151, 10):
        theta = np.pi - (v - min_val) / (max_val - min_val) * np.pi
        x1, y1 = 1.0 * np.cos(theta), 1.0 * np.sin(theta)
        x2, y2 = 1.08 * np.cos(theta), 1.08 * np.sin(theta)
        ax.plot([x1, x2], [y1, y2], color='#333333', linewidth=1)
        xt, yt = 1.2 * np.cos(theta), 1.2 * np.sin(theta)
        ax.text(xt, yt, str(v), ha='center', va='center', fontsize=8, color='#666666')

    pointer_theta = np.pi - (pointer_val - min_val) / (max_val - min_val) * np.pi
    ax.annotate('', xy=(0.65 * np.cos(pointer_theta), 0.65 * np.sin(pointer_theta)),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=2.5))
    ax.plot(0, 0, 'o', color='#333333', markersize=6, zorder=5)

    ax.text(0, -0.3, str(pointer_val), ha='center', va='center',
            fontsize=22, fontweight='bold', color='#333333')

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.6, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    save_fig(fig, '22_仪表盘图.png')


# ==================== 图表23: 柱形折线图 ====================
def chart_23():
    fig, ax1 = plt.subplots(figsize=(8, 5))
    years = ['2017', '2018', '2019', '2020', '2021', '2022']
    sales = [1603, 2106, 2406, 3265, 3721, 3921]
    yoy = [0.27, 0.314, 0.142, 0.357, 0.140, 0.054]

    x = np.arange(len(years))
    bars = ax1.bar(x, sales, 0.5, color='#4472C4', zorder=2, alpha=0.8)

    for xi, yi in zip(x, sales):
        ax1.text(xi, yi + 60, str(yi), ha='center', va='bottom', fontsize=9, color='#333333')

    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=10)
    ax1.set_ylabel('销售量', fontsize=12, color='#4472C4')
    ax1.set_ylim(0, max(sales) * 1.2)
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_color('#4472C4')
    ax1.spines['bottom'].set_color('#CCCCCC')
    ax1.spines['right'].set_visible(False)
    ax1.tick_params(axis='y', colors='#4472C4')
    ax1.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax1.set_axisbelow(True)

    ax2 = ax1.twinx()
    ax2.plot(x, yoy, color='#ED7D31', linewidth=2, marker='o', markersize=6,
             markerfacecolor='white', markeredgewidth=2, markeredgecolor='#ED7D31', zorder=3)
    for xi, yi in zip(x, yoy):
        ax2.text(xi, yi + 0.02, f'{yi:.1%}', ha='center', va='bottom',
                fontsize=9, color='#ED7D31')

    ax2.set_ylabel('同比增长率', fontsize=12, color='#ED7D31')
    ax2.set_ylim(0, max(yoy) * 1.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_color('#ED7D31')
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_color('#CCCCCC')
    ax2.tick_params(axis='y', colors='#ED7D31')

    save_fig(fig, '23_柱形折线图.png')


# ==================== 图表24: 目标柱形图 ====================
def chart_24():
    fig, ax = plt.subplots(figsize=(8, 5))
    products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
    actual = [653, 523, 648, 856, 714, 785]
    target = [700, 500, 600, 900, 600, 600]

    x = np.arange(len(products))
    width = 0.35

    ax.bar(x - width/2, actual, width, color='#4472C4', zorder=2, label='实际销量')
    ax.bar(x + width/2, target, width, color='#D9D9D9', zorder=2, label='目标销量',
           edgecolor='#999999', linewidth=0.5)

    for xi, (a, t) in enumerate(zip(actual, target)):
        color = '#70AD47' if a >= t else '#C00000'
        ax.plot(xi + width/2, t, marker='_', color=color, markersize=15,
                markeredgewidth=2.5, zorder=3)
        ax.text(xi - width/2, a + 15, str(a), ha='center', va='bottom', fontsize=8, color='#4472C4')

    ax.set_xticks(x)
    ax.set_xticklabels(products, fontsize=10)
    ax.set_ylabel('销量', fontsize=12)
    ax.set_xlim(-0.5, len(products) - 0.5)
    ax.set_ylim(0, max(max(actual), max(target)) * 1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=10, frameon=False)

    save_fig(fig, '24_目标柱形图.png')


# ==================== 图表25: 子弹图 ====================
def chart_25():
    fig, ax = plt.subplots(figsize=(9, 5))
    products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
    actual = [653, 523, 648, 856, 714, 785]
    target = [700, 500, 600, 900, 600, 600]
    pass_level = [600, 600, 600, 600, 600, 600]
    good_extra = [200, 200, 200, 200, 200, 200]
    excellent_extra = [200, 200, 200, 200, 200, 200]

    y = np.arange(len(products))
    max_val = 1000

    for i in range(len(products)):
        base = 0
        for val, color in [(pass_level[i] + good_extra[i] + excellent_extra[i], '#E8E8E8'),
                           (pass_level[i] + good_extra[i], '#D0D0D0'),
                           (pass_level[i], '#B8B8B8')]:
            ax.barh(i, val, left=base, height=0.5, color=color, zorder=1, edgecolor='white', linewidth=0.3)

    for i in range(len(products)):
        ax.barh(i, actual[i], height=0.25, color='#4472C4', zorder=3, alpha=0.85)

    for i in range(len(products)):
        ax.plot(target[i], i, marker='|', color='#C00000', markersize=18,
                markeredgewidth=2.5, zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels(products, fontsize=11)
    ax.set_xlabel('销量', fontsize=12)
    ax.set_xlim(0, max_val)
    ax.set_ylim(-0.5, len(products) - 0.5)
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.xaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    from matplotlib.lines import Line2D
    legend_elements = [
        mpatches.Patch(facecolor='#4472C4', label='实际'),
        Line2D([0], [0], color='#C00000', marker='|', linestyle='None',
               markersize=12, markeredgewidth=2.5, label='目标'),
        mpatches.Patch(facecolor='#B8B8B8', label='及格'),
        mpatches.Patch(facecolor='#D0D0D0', label='良好'),
        mpatches.Patch(facecolor='#E8E8E8', label='优秀'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9, frameon=False)

    save_fig(fig, '25_子弹图.png')


# ==================== 图表26: 柱形圆 ====================
def chart_26():
    fig, axes = plt.subplots(1, 6, figsize=(14, 4))
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    values = [2354, 1902, 3524, 2698, 2896, 2563]
    placeholders = [4500] * 6
    yoy = [0.12, 0.25, 0.16, 0.21, 0.18, 0.25]

    for idx, (region, val, ph, yoy_val) in enumerate(zip(regions, values, placeholders, yoy)):
        ax = axes[idx]
        rate = val / ph

        circle_bg = plt.Circle((0.5, 0.5), 0.4, facecolor='#E8E8E8', edgecolor='none',
                                transform=ax.transAxes, zorder=1)
        ax.add_patch(circle_bg)

        theta = np.linspace(np.pi/2, np.pi/2 - rate * 2 * np.pi, 100)
        x_arc = 0.5 + 0.4 * np.cos(theta)
        y_arc = 0.5 + 0.4 * np.sin(theta)
        x_inner = 0.5 + 0.3 * np.cos(theta[::-1])
        y_inner = 0.5 + 0.3 * np.sin(theta[::-1])

        verts = np.column_stack([
            np.concatenate([x_arc, x_inner]),
            np.concatenate([y_arc, y_inner])
        ])
        codes = [MPath.MOVETO] + [MPath.LINETO] * (len(verts) - 1)
        path = MPath(verts, codes)
        patch = PathPatch(path, facecolor='#4472C4', edgecolor='none', alpha=0.8, zorder=2)
        ax.add_patch(patch)

        ax.text(0.5, 0.55, str(val), ha='center', va='center',
                fontsize=11, fontweight='bold', color='#333333', transform=ax.transAxes, zorder=3)
        ax.text(0.5, 0.35, f'同比 +{yoy_val:.0%}', ha='center', va='center',
                fontsize=8, color='#70AD47', transform=ax.transAxes, zorder=3)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(region, fontsize=11, color='#333333', pad=5)

    plt.tight_layout()
    save_fig(fig, '26_柱形圆.png')


# ==================== 图表27: 簇状柱形折线图 ====================
def chart_27():
    fig, ax1 = plt.subplots(figsize=(9, 5))
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    val_2022 = [2354, 1902, 3524, 2698, 2896, 2563]
    val_2021 = [2021, 1563, 3213, 2531, 2631, 2361]
    yoy = [0.16, 0.22, 0.10, 0.07, 0.10, 0.09]

    x = np.arange(len(regions))
    width = 0.3
    ax1.bar(x - width/2, val_2022, width, color='#4472C4', zorder=2, label='2022销量')
    ax1.bar(x + width/2, val_2021, width, color='#5B9BD5', zorder=2, label='2021销量')

    ax1.set_xticks(x)
    ax1.set_xticklabels(regions, fontsize=10)
    ax1.set_ylabel('销量', fontsize=12, color='#4472C4')
    ax1.set_ylim(0, max(max(val_2022), max(val_2021)) * 1.2)
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_color('#4472C4')
    ax1.spines['bottom'].set_color('#CCCCCC')
    ax1.spines['right'].set_visible(False)
    ax1.tick_params(axis='y', colors='#4472C4')
    ax1.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax1.set_axisbelow(True)
    ax1.legend(loc='upper left', fontsize=9, frameon=False)

    ax2 = ax1.twinx()
    ax2.plot(x, yoy, color='#ED7D31', linewidth=2, marker='o', markersize=6,
             markerfacecolor='white', markeredgewidth=2, markeredgecolor='#ED7D31', zorder=3)
    for xi, yi in zip(x, yoy):
        ax2.text(xi, yi + 0.01, f'{yi:.0%}', ha='center', va='bottom',
                fontsize=9, color='#ED7D31')

    ax2.set_ylabel('同比增长率', fontsize=12, color='#ED7D31')
    ax2.set_ylim(0, max(yoy) * 1.6)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_color('#ED7D31')
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_color('#CCCCCC')
    ax2.tick_params(axis='y', colors='#ED7D31')

    save_fig(fig, '27_簇状柱形折线图.png')


# ==================== 图表28: 复合柱形图 ====================
def chart_28():
    fig, ax = plt.subplots(figsize=(10, 5))
    months = ['1月', '2月', '3月', '4月', '5月', '6月',
              '7月', '8月', '9月', '10月', '11月', '12月']
    monthly = [2354, 1902, 3524, 2698, 2896, 2563,
               3156, 2896, 3621, 2635, 2963, 2789]
    quarterly = [sum(monthly[0:3]), sum(monthly[3:6]), sum(monthly[6:9]), sum(monthly[9:12])]

    x = np.arange(len(months))
    quarter_labels = ['Q1', 'Q2', 'Q3', 'Q4']
    quarter_colors = ['#4472C4', '#5B9BD5', '#ED7D31', '#FFC000']

    for q in range(4):
        start = q * 3
        end = start + 3
        q_val = quarterly[q] / 3
        for m in range(start, end):
            ax.bar(x[m], q_val, 0.55, color=quarter_colors[q], zorder=2, alpha=0.35,
                   edgecolor=quarter_colors[q], linewidth=0.5)

    for m, v in zip(x, monthly):
        ax.bar(m, v, 0.25, color='#4472C4', zorder=3, alpha=0.85)

    for q in range(4):
        center_x = q * 3 + 1
        ax.text(center_x, quarterly[q] / 3 + 100, f'Q{q+1}: {quarterly[q]}',
                ha='center', va='bottom', fontsize=9, color='#333333', fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=9)
    ax.set_ylabel('销量', fontsize=12)
    ax.set_xlim(-0.6, len(months) - 0.4)
    ax.set_ylim(0, max(max(monthly), max(quarterly)/3) * 1.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.yaxis.grid(True, color='#EEEEEE', zorder=0)
    ax.set_axisbelow(True)

    save_fig(fig, '28_复合柱形图.png')


# ==================== 图表29: 滑珠图 ====================
def chart_29():
    fig, ax = plt.subplots(figsize=(9, 5))
    regions = ['华东', '西北', '东北', '华北', '华南']
    rates = [0.35, 0.51, 0.62, 0.74, 0.86]
    positions = [1, 3, 5, 7, 9]

    for yi, (region, rate, pos) in enumerate(zip(regions, rates, positions)):
        ax.barh(pos, 1.0, height=0.2, color='#E0E0E0', zorder=1, edgecolor='none')
        ax.barh(pos, rate, height=0.2, color='#4472C4', zorder=2, alpha=0.6)
        ax.plot(rate, pos, marker='o', color='#2F5597', markersize=14,
                markerfacecolor='#4472C4', markeredgecolor='white',
                markeredgewidth=2, zorder=3)
        ax.text(-0.06, pos, region, ha='right', va='center', fontsize=10, color='#333333')
        ax.text(rate + 0.03, pos, f'{rate:.0%}', ha='left', va='center',
                fontsize=10, color='#2F5597', fontweight='bold')

    ax.set_xlim(-0.35, 1.2)
    ax.set_ylim(0, 10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    save_fig(fig, '29_滑珠图.png')


# ==================== 图表30: 对比滑珠图 ====================
def chart_30():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    regions = ['华东', '西北', '东北', '华北', '华南']
    rate_2022 = [0.35, 0.51, 0.62, 0.74, 0.86]
    rate_2021 = [0.45, 0.39, 0.53, 0.69, 0.92]
    positions = [1, 3, 5, 7, 9]

    for yi, (region, r22, r21, pos) in enumerate(zip(regions, rate_2022, rate_2021, positions)):
        ax.barh(pos, 1.0, height=0.15, color='#E0E0E0', zorder=1, edgecolor='none')

        ax.barh(pos + 0.12, r21, height=0.12, color='#5B9BD5', zorder=2, alpha=0.5)
        ax.plot(r21, pos + 0.12, marker='o', color='#5B9BD5', markersize=10,
                markeredgecolor='white', markeredgewidth=1.5, zorder=3)

        ax.barh(pos - 0.12, r22, height=0.12, color='#ED7D31', zorder=2, alpha=0.5)
        ax.plot(r22, pos - 0.12, marker='o', color='#ED7D31', markersize=10,
                markeredgecolor='white', markeredgewidth=1.5, zorder=3)

        ax.text(-0.06, pos, region, ha='right', va='center', fontsize=10, color='#333333')
        ax.text(max(r22, r21) + 0.04, pos + 0.12, f'{r21:.0%}', ha='left', va='center',
                fontsize=8, color='#5B9BD5')
        ax.text(max(r22, r21) + 0.04, pos - 0.12, f'{r22:.0%}', ha='left', va='center',
                fontsize=8, color='#ED7D31')

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#ED7D31',
               markersize=8, label='2022完成率'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#5B9BD5',
               markersize=8, label='2021完成率'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9, frameon=False)

    ax.set_xlim(-0.35, 1.25)
    ax.set_ylim(0, 10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    save_fig(fig, '30_对比滑珠图.png')


# ==================== 主函数 ====================
if __name__ == '__main__':
    from matplotlib.path import Path as MPath

    print('=' * 50)
    print('开始生成30个可视化图表...')
    print(f'输出目录: {OUTPUT_DIR}')
    print('=' * 50)

    charts = [
        ('图表1: 渐变柱形图', chart_01),
        ('图表2: 带均值柱形图', chart_02),
        ('图表3: 渐变圆角柱形图', chart_03),
        ('图表4: 标注柱形图', chart_04),
        ('图表5: 层叠柱形图', chart_05),
        ('图表6: 蝴蝶图', chart_06),
        ('图表7: 蝴蝶图(百分比)', chart_07),
        ('图表8: 数值百分比', chart_08),
        ('图表9: 对比柱形图', chart_09),
        ('图表10: 甘特图', chart_10),
        ('图表11: 平滑折线图', chart_11),
        ('图表12: 菱形走势图', chart_12),
        ('图表13: 对比折线图', chart_13),
        ('图表14: 单值圆环图', chart_14),
        ('图表15: 水球图', chart_15),
        ('图表16: 波浪水球图', chart_16),
        ('图表17: 玉玦图', chart_17),
        ('图表18: 跑道图', chart_18),
        ('图表19: 南丁格尔圆饼图', chart_19),
        ('图表20: 南丁格尔圆环图', chart_20),
        ('图表22: 仪表盘图', chart_22),
        ('图表23: 柱形折线图', chart_23),
        ('图表24: 目标柱形图', chart_24),
        ('图表25: 子弹图', chart_25),
        ('图表26: 柱形圆', chart_26),
        ('图表27: 簇状柱形折线图', chart_27),
        ('图表28: 复合柱形图', chart_28),
        ('图表29: 滑珠图', chart_29),
        ('图表30: 对比滑珠图', chart_30),
    ]

    success = 0
    failed = 0
    for name, func in charts:
        try:
            print(f'\n正在绘制: {name}')
            func()
            success += 1
        except Exception as e:
            print(f'  [FAIL] {name}: {e}')
            import traceback
            traceback.print_exc()
            failed += 1

    print('\n' + '=' * 50)
    print(f'完成! 成功: {success}, 失败: {failed}, 总计: {len(charts)}')
    print(f'输出目录: {OUTPUT_DIR}')
    print('=' * 50)
