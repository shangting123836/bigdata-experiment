# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

font_path = 'C:/Windows/Fonts/msyh.ttc'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'Microsoft YaHei'
else:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

COLORS = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47',
          '#264478', '#9B59B6', '#E74C3C', '#1ABC9C']


def chart1_dynamic_bar():
    """1 动态柱形图 - 各区域月度销售额"""
    months = ['1月', '2月', '3月', '4月', '5月', '6月']
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    data = [
        [259, 247, 705, 513, 463, 384],
        [235, 266, 529, 324, 579, 282],
        [330, 342, 705, 540, 492, 308],
        [282, 342, 599, 270, 492, 384],
        [282, 323, 705, 486, 405, 308],
        [965, 380, 282, 567, 463, 897],
    ]

    selected = 4  # 5月 (index 4)
    values = data[selected]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(regions, values, color=COLORS[:6], width=0.6, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
                str(val), ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_title(f'各区域{months[selected]}销售额', fontsize=16, fontweight='bold', pad=15)
    ax.set_ylabel('销售额', fontsize=12)
    ax.set_ylim(0, max(values) * 1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart1_动态柱形图.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('  chart1 done')


def chart2_dynamic_stacked_bar():
    """2 动态跑道图 - 各部门人数月度堆积条形图"""
    depts = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
    months = ['1月', '2月', '3月', '4月']
    data = {
        '1月': [451, 326, 293, 238, 226, 130],
        '2月': [456, 349, 305, 228, 206, 138],
        '3月': [406, 316, 314, 255, 217, 130],
        '4月': [433, 359, 264, 226, 226, 129],
    }
    totals = {m: sum(v) for m, v in data.items()}

    selected_month = '4月'
    values = data[selected_month]
    total = totals[selected_month]

    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = np.arange(len(depts))
    bars = ax.barh(y_pos, values, color=COLORS[:6], height=0.6, edgecolor='white')

    for bar, val, dept in zip(bars, values, depts):
        ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
                str(val), ha='left', va='center', fontsize=11, fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(depts, fontsize=11)
    ax.set_title(f'{selected_month}各部门人数分布（公司总人数: {total}）',
                 fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel('人数', fontsize=12)
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart2_动态跑道图.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('  chart2 done')


def chart3_nightingale_rose():
    """3 动态南丁格尔圆环图 - 流量来源占比"""
    categories = ['首页推荐', '关注页面', '搜索', '个人主页', '其他来源']
    data_7d = [0.44, 0.17, 0.15, 0.08, 0.16]
    data_30d = [0.38, 0.21, 0.15, 0.09, 0.17]

    selected = 0  # 0=近7天, 1=近30天
    labels = ['近7天', '近30天']
    values = data_7d if selected == 0 else data_30d

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

    N = len(categories)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    bar_width = 2 * np.pi / N * 0.75

    colors_pie = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5']

    bars = ax.bar(theta, values, width=bar_width, bottom=0.1,
                  color=colors_pie, alpha=0.8, edgecolor='white', linewidth=1.5)

    for i, (t, val) in enumerate(zip(theta, values)):
        r = 0.1 + val + 0.06
        ax.text(t, r, f'{categories[i]}\n{val:.0%}', ha='center', va='center',
                fontsize=10, fontweight='bold', color=colors_pie[i])

    ax.set_ylim(0, max(values) * 1.4)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(f'流量来源占比（{labels[selected]}）', fontsize=15, fontweight='bold', pad=25)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart3_动态南丁格尔圆环图.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('  chart3 done')


def chart4_combo():
    """4 动态组合图 - 化妆品销售额(柱) + 利润(柱) + 利润率(折线)"""
    categories = ['口红', '面膜', '隔离', '粉底液']
    sales = [2800, 2564, 2282, 2353]
    profit = [1896, 1563, 986, 1324]
    profit_rate = [0.6771, 0.6096, 0.4321, 0.5627]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(10, 6))

    bars1 = ax1.bar(x - width/2, sales, width, label='销售额', color='#4472C4', edgecolor='white')
    bars2 = ax1.bar(x + width/2, profit, width, label='利润', color='#ED7D31', edgecolor='white')

    for bar, val in zip(bars1, sales):
        ax1.text(bar.get_x(), bar.get_height() + 40, str(val),
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='#4472C4')
    for bar, val in zip(bars2, profit):
        ax1.text(bar.get_x(), bar.get_height() + 40, str(val),
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='#ED7D31')

    ax1.set_ylabel('金额', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=12)
    ax1.set_ylim(0, max(sales) * 1.25)
    ax1.spines['top'].set_visible(False)
    ax1.grid(axis='y', alpha=0.2, linestyle='--')

    ax2 = ax1.twinx()
    line = ax2.plot(x, [r * 100 for r in profit_rate], 'o-', color='#70AD47',
                    linewidth=2.5, markersize=8, label='利润率', zorder=5)
    for i, (xi, r) in enumerate(zip(x, profit_rate)):
        ax2.text(xi, r * 100 + 1.5, f'{r:.1%}', ha='center', va='bottom',
                 fontsize=10, fontweight='bold', color='#70AD47')
    ax2.set_ylabel('利润率 (%)', fontsize=12, color='#70AD47')
    ax2.set_ylim(0, 100)
    ax2.spines['top'].set_visible(False)
    ax2.tick_params(axis='y', colors='#70AD47')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)

    ax1.set_title('化妆品销售额与利润率', fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart4_动态组合图.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('  chart4 done')


def chart5_pivot_salary():
    """5 透视表切片器 - 各学历平均月收入"""
    edu_labels = ['专科', '本科', '硕士', '博士', '高中']
    avg_salary = [6908.04, 6138.32, 6739.01, 7187.00, 5853.63]
    total_avg = 6446.50

    fig, ax = plt.subplots(figsize=(10, 6))
    colors_bar = ['#4472C4', '#5B9BD5', '#70AD47', '#ED7D31', '#A5A5A5']

    bars = ax.bar(edu_labels, avg_salary, color=colors_bar, width=0.6, edgecolor='white')

    ax.axhline(y=total_avg, color='#E74C3C', linestyle='--', linewidth=1.5, label=f'总平均: {total_avg:.0f}')

    for bar, val in zip(bars, avg_salary):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 80,
                f'{val:.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_title('各学历平均月收入', fontsize=16, fontweight='bold', pad=15)
    ax.set_ylabel('平均月收入', fontsize=12)
    ax.set_ylim(0, max(avg_salary) * 1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.legend(fontsize=10)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart5_透视表切片器.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('  chart5 done')


def chart6_jade_ring():
    """6 VBA动态玉图 - 流量来源占比(玉玦图/玫瑰图变体)"""
    categories = ['首页推荐', '关注页面', '搜索', '个人主页']
    data_7d = [0.36, 0.32, 0.19, 0.13]
    data_30d = [0.38, 0.29, 0.24, 0.09]

    selected = 1  # 0=近7天, 1=近30天
    labels = ['近7天', '近30天']
    values = data_7d if selected == 0 else data_30d

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

    colors_jade = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000']
    N = len(categories)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    bar_width = 2 * np.pi / N * 0.7

    bars = ax.bar(theta, values, width=bar_width, bottom=0.2,
                  color=colors_jade, alpha=0.85, edgecolor='white', linewidth=1.5)

    for i, (t, val, cat) in enumerate(zip(theta, values, categories)):
        r = 0.2 + val + 0.08
        ax.text(t, r, f'{cat}\n{val:.0%}', ha='center', va='center',
                fontsize=11, fontweight='bold', color=colors_jade[i])

    ax.set_ylim(0, max(values) * 1.5)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(f'流量来源占比（{labels[selected]}）', fontsize=15, fontweight='bold', pad=25)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart6_VBA动态玉玦图.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('  chart6 done')


def chart7_sliding_bead():
    """7 动态滑珠图 - 各区域月度完成率"""
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    months = ['1月', '2月', '3月', '4月', '5月', '6月']
    data = [
        [0.32, 0.45, 0.66, 0.52, 0.69, 0.771],
        [0.49, 0.36, 0.54, 0.39, 0.415, 0.403],
        [0.65, 0.53, 0.58, 0.48, 0.445, 0.399],
        [0.73, 0.63, 0.61, 0.53, 0.47, 0.408],
        [0.536, 0.498, 0.527, 0.708, 0.7035, 0.758],
        [0.32, 0.49, 0.65, 0.73, 0.536, 0.7468],
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()

    for m_idx, month in enumerate(months):
        ax = axes[m_idx]
        values = [data[r][m_idx] for r in range(len(regions))]

        y_pos = np.arange(len(regions))
        ax.barh(y_pos, [1] * len(regions), color='#E8E8E8', height=0.5)
        bars = ax.barh(y_pos, values, color=[COLORS[i] for i in range(len(regions))],
                       height=0.5, edgecolor='white')

        for bar, val in zip(bars, values):
            ax.plot(bar.get_width(), bar.get_y() + bar.get_height()/2,
                    'o', color='white', markersize=6, markeredgecolor='white', markeredgewidth=1.5)
            ax.text(min(bar.get_width() + 0.03, 0.95), bar.get_y() + bar.get_height()/2,
                    f'{val:.1%}', ha='left', va='center', fontsize=8, fontweight='bold')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(regions, fontsize=9)
        ax.set_xlim(0, 1.15)
        ax.set_title(month, fontsize=12, fontweight='bold')
        ax.invert_yaxis()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xticks([])

    fig.suptitle('各区域月度完成率', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'chart7_动态滑珠图.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('  chart7 done')


if __name__ == '__main__':
    print('开始复现图表...')
    chart1_dynamic_bar()
    chart2_dynamic_stacked_bar()
    chart3_nightingale_rose()
    chart4_combo()
    chart5_pivot_salary()
    chart6_jade_ring()
    chart7_sliding_bead()
    print(f'\n全部完成! 图片保存在: {OUTPUT_DIR}')
