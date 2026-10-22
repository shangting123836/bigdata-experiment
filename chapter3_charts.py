# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

print("脚本开始运行！")

# 字体兼容修复：同时判断ttc/ttf
font_path = 'C:/Windows/Fonts/msyh.ttc'
font_path2 = 'C:/Windows/Fonts/msyh.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'Microsoft YaHei'
elif os.path.exists(font_path2):
    fm.fontManager.addfont(font_path2)
    plt.rcParams['font.family'] = 'Microsoft YaHei'
else:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 指定输出目录
OUTPUT_DIR = r'C:\study\大数据可视化分析\第二章Python图表输出\chapter3-images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLORS = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47',
          '#264478', '#9B59B6', '#E74C3C', '#1ABC9C']

def chart1_dynamic_bar(selected_idx, save_name):
    """1 动态柱形图 - 各区域月度销售额
    :param selected_idx: 月份索引 0~5
    :param save_name: 输出文件名
    """
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
    values = data[selected_idx]
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(regions, values, color=COLORS[:6], width=0.6, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
                str(val), ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_title(f'各区域{months[selected_idx]}销售额', fontsize=16, fontweight='bold', pad=15)
    ax.set_ylabel('销售额', fontsize=12)
    ax.set_ylim(0, max(values) * 1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, save_name), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  {save_name} done')

def chart2_dynamic_horizontal_bar(selected_month, save_name):
    """2 动态跑道图 - 各部门人数横向条形图
    :param selected_month: '1月','2月','3月','4月'
    :param save_name: 输出文件名
    """
    depts = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
    months = ['1月', '2月', '3月', '4月']
    data = {
        '1月': [451, 326, 293, 238, 226, 130],
        '2月': [456, 349, 305, 228, 206, 138],
        '3月': [406, 316, 314, 255, 217, 130],
        '4月': [433, 359, 264, 226, 226, 129],
    }
    totals = {m: sum(v) for m, v in data.items()}
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
    fig.savefig(os.path.join(OUTPUT_DIR, save_name), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  {save_name} done')

def chart3_nightingale_rose(selected_idx, save_name):
    """3 动态南丁格尔圆环图 - 流量来源占比
    :param selected_idx: 0=近7天,1=近30天
    :param save_name: 输出文件名
    """
    categories = ['首页推荐', '关注页面', '搜索', '个人主页', '其他来源']
    data_7d = [0.44, 0.17, 0.15, 0.08, 0.16]
    data_30d = [0.38, 0.21, 0.15, 0.09, 0.17]
    labels = ['近7天', '近30天']
    values = [data_7d, data_30d][selected_idx]
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
    ax.set_title(f'流量来源占比（{labels[selected_idx]}）', fontsize=15, fontweight='bold', pad=25)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, save_name), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  {save_name} done')

def chart4_combo(save_name):
    """4 动态组合图 - 化妆品销售额(柱) + 利润(柱) + 利润率(折线)，本组无切片，仅1张"""
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
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height() + 40, str(val),
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='#4472C4')
    for bar, val in zip(bars2, profit):
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height() + 40, str(val),
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
    fig.savefig(os.path.join(OUTPUT_DIR, save_name), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  {save_name} done')

def chart5_pivot_salary(save_name):
    """5 透视表切片器 - 各学历平均月收入，本组无切片，仅1张"""
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
    fig.savefig(os.path.join(OUTPUT_DIR, save_name), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  {save_name} done')

def chart6_jade_ring(selected_idx, save_name):
    """6 VBA动态玉玦图 - 流量来源占比
    :param selected_idx:0=近7天,1=近30天
    :param save_name:输出文件名
    """
    categories = ['首页推荐', '关注页面', '搜索', '个人主页']
    data_7d = [0.36, 0.32, 0.19, 0.13]
    data_30d = [0.38, 0.29, 0.24, 0.09]
    labels = ['近7天', '近30天']
    values = [data_7d, data_30d][selected_idx]
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
    ax.set_title(f'流量来源占比（{labels[selected_idx]}）', fontsize=15, fontweight='bold', pad=25)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, save_name), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  {save_name} done')

def chart7_sliding_bead(save_name):
    """7 动态滑珠图，本身已经是6个子图在一张画布，无需切片，仅1张"""
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
            # 修复滑珠圆点：白色填充 + 深色描边
            ax.plot(bar.get_width(), bar.get_y() + bar.get_height()/2,
                    'o', color='white', markersize=6, markeredgecolor='#333333', markeredgewidth=1.5)
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
    fig.savefig(os.path.join(OUTPUT_DIR, save_name), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  {save_name} done')


if __name__ == '__main__':
    print('===== 开始批量生成全部切片图表 =====')

    # chart1：6个月
    for idx, m in enumerate(['1月','2月','3月','4月','5月','6月']):
        chart1_dynamic_bar(idx, f'chart1_动态柱形图_{m}.png')

    # chart2：4个月
    for m in ['1月','2月','3月','4月']:
        chart2_dynamic_horizontal_bar(m, f'chart2_动态跑道图_{m}.png')

    # chart3：2个周期
    for idx, t in enumerate(['近7天','近30天']):
        chart3_nightingale_rose(idx, f'chart3_南丁格尔玫瑰_{t}.png')

    # chart4 无切片，单张
    chart4_combo('chart4_动态组合图.png')

    # chart5 无切片，单张
    chart5_pivot_salary('chart5_透视表切片器.png')

    # chart6：2个周期
    for idx, t in enumerate(['近7天','近30天']):
        chart6_jade_ring(idx, f'chart6_VBA玉玦图_{t}.png')

    # chart7 无切片，单张
    chart7_sliding_bead('chart7_动态滑珠图.png')

    print(f'\n✅ 全部切片图生成完毕！目录：{OUTPUT_DIR}')
