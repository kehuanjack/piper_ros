import numpy as np
import matplotlib.pyplot as plt

# 打印说明信息
print("="*80)
print("SEQUENCE ANALYSIS SYSTEM")
print("="*80)
print("SEQ DEFINITIONS:")
print("- seq_start: 下发159控制指令时的seq数")
print("- seq_end:   接收到seq3 != 0时的seq数")
print("- seq1:      主控接收到控制指令的seq数")
print("- seq2:      运动完成的seq数")
print("- seq3:      接收到上位机101反馈指令的seq数")
print("\nMOTION COMPLETION CRITERIA:")
print("- M1: 主控判断运动完成 (seq2 != 0)")
print("- M2: 上位机判断运动完成 (gripper_angle <= 0)")
print("\nTIME DIFFERENCE DEFINITIONS:")
print("- T0: seq1 - seq_start (指令传输时间)")
print("- T1: seq2 - seq1 (运动执行时间)")
print("- T2: seq3 - seq2 (反馈传输时间)")
print("="*80)

# 加载和处理M1序列数据
seq_M1 = np.loadtxt("seq200hzM1.csv", delimiter=',', dtype=int)
# 计算时间差
T0_M1 = (seq_M1[:, 2] - seq_M1[:, 0])  # seq1 - seq_start
T1_M1 = (seq_M1[:, 3] - seq_M1[:, 2])  # seq2 - seq1
T2_M1 = (seq_M1[:, 4] - seq_M1[:, 3])  # seq3 - seq2
index_M1 = np.arange(len(T0_M1))
M1_len = len(T0_M1)

# 加载和处理M2序列数据
seq_M2 = np.loadtxt("seq200hzM2.csv", delimiter=',', dtype=int)
T0_M2 = (seq_M2[:, 2] - seq_M2[:, 0])  # seq1 - seq_start
T1_M2 = (seq_M2[:, 3] - seq_M2[:, 2])  # seq2 - seq1
T2_M2 = (seq_M2[:, 4] - seq_M2[:, 3])  # seq3 - seq2
index_M2 = np.arange(len(T0_M2))
M2_len = len(T0_M2)

# 打印数据长度
print("\n" + "="*50)
print(f"M1 SEQUENCE DATA POINTS: {M1_len} (主控判断运动完成，200Hz)")
print(f"M2 SEQUENCE DATA POINTS: {M2_len} (上位机判断运动完成，200Hz)")
print("="*50)

# 计算统计指标
def calculate_stats(data):
    return {
        'min': np.min(data),
        'max': np.max(data),
        'mean': np.mean(data),
        'std': np.std(data),
        'data': data
    }

stats_M1 = {
    'T0': calculate_stats(T0_M1),
    'T1': calculate_stats(T1_M1),
    'T2': calculate_stats(T2_M1)
}

stats_M2 = {
    'T0': calculate_stats(T0_M2),
    'T1': calculate_stats(T1_M2),
    'T2': calculate_stats(T2_M2)
}

# 打印统计信息
print("\n" + "="*50)
print("M1 SEQUENCE STATISTICS (ms) - 主控判断运动完成:")
for t in ['T0', 'T1', 'T2']:
    s = stats_M1[t]
    print(f"{t}: min={s['min']:.2f}, max={s['max']:.2f}, mean={s['mean']:.2f}, std={s['std']:.2f}")

print("\n" + "="*50)
print("M2 SEQUENCE STATISTICS (ms) - 上位机判断运动完成:")
for t in ['T0', 'T1', 'T2']:
    s = stats_M2[t]
    print(f"{t}: min={s['min']:.2f}, max={s['max']:.2f}, mean={s['mean']:.2f}, std={s['std']:.2f}")
print("="*50)

# 创建可视化图表
time_diffs = ['T0', 'T1', 'T2']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 优化颜色方案

# M1序列分析图表
plt.figure(figsize=(14, 10))
plt.suptitle('M1 Sequence: Motion Completed by Controller (ms)', fontsize=16, fontweight='bold')

for i, t in enumerate(time_diffs):
    # 时间序列图
    ax1 = plt.subplot(3, 2, 2*i+1)
    ax1.plot(index_M1, stats_M1[t]['data'], color=colors[i], 
             label=f'M1 {t} (mean: {stats_M1[t]["mean"]:.2f} ms)', linewidth=1)
    ax1.axhline(stats_M1[t]['mean'], color=colors[i], linestyle='-', alpha=0.5)
    ax1.axhline(stats_M1[t]['min'], color=colors[i], linestyle=':', alpha=0.7)
    ax1.axhline(stats_M1[t]['max'], color=colors[i], linestyle=':', alpha=0.7)
    
    # 添加统计信息文本
    stats_text = (f"min: {stats_M1[t]['min']:.2f} ms\n"
                  f"max: {stats_M1[t]['max']:.2f} ms\n"
                  f"mean: {stats_M1[t]['mean']:.2f} ms\n"
                  f"std: {stats_M1[t]['std']:.2f} ms")
    ax1.text(0.02, 0.95, stats_text, transform=ax1.transAxes, 
             color=colors[i], fontsize=9, verticalalignment='top', 
             bbox=dict(boxstyle='round,pad=0.3', alpha=0.1, color=colors[i]))
    
    ax1.set_xlabel('Data Point Index')
    ax1.set_ylabel('Time Difference (ms)')
    ax1.set_title(f'M1 {t} Time Series ({M1_len} data points)')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 分布直方图
    ax2 = plt.subplot(3, 2, 2*i+2)
    ax2.hist(stats_M1[t]['data'], bins=20, color=colors[i], alpha=0.7)
    ax2.axvline(stats_M1[t]['min'], color=colors[i], linestyle=':', linewidth=2)
    ax2.axvline(stats_M1[t]['max'], color=colors[i], linestyle=':', linewidth=2)
    ax2.axvline(stats_M1[t]['mean'], color=colors[i], linestyle='-', linewidth=2)
    
    # 添加统计信息文本
    ax2.text(0.02, 0.95, stats_text, transform=ax2.transAxes, 
             color=colors[i], fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.3', alpha=0.1, color=colors[i]))
    
    ax2.set_xlabel('Time Difference (ms)')
    ax2.set_ylabel('Frequency')
    ax2.set_title(f'M1 {t} Distribution')
    ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout(rect=[0, 0, 1, 0.96])
# plt.savefig('M1_sequence_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# M2序列分析图表
plt.figure(figsize=(14, 10))
plt.suptitle('M2 Sequence: Motion Completed by Host PC (ms)', fontsize=16, fontweight='bold')

for i, t in enumerate(time_diffs):
    # 时间序列图
    ax1 = plt.subplot(3, 2, 2*i+1)
    ax1.plot(index_M2, stats_M2[t]['data'], color=colors[i], 
             label=f'M2 {t} (mean: {stats_M2[t]["mean"]:.2f} ms)', linewidth=1)
    ax1.axhline(stats_M2[t]['mean'], color=colors[i], linestyle='-', alpha=0.5)
    ax1.axhline(stats_M2[t]['min'], color=colors[i], linestyle=':', alpha=0.7)
    ax1.axhline(stats_M2[t]['max'], color=colors[i], linestyle=':', alpha=0.7)
    
    # 添加统计信息文本
    stats_text = (f"min: {stats_M2[t]['min']:.2f} ms\n"
                  f"max: {stats_M2[t]['max']:.2f} ms\n"
                  f"mean: {stats_M2[t]['mean']:.2f} ms\n"
                  f"std: {stats_M2[t]['std']:.2f} ms")
    ax1.text(0.02, 0.95, stats_text, transform=ax1.transAxes, 
             color=colors[i], fontsize=9, verticalalignment='top', 
             bbox=dict(boxstyle='round,pad=0.3', alpha=0.1, color=colors[i]))
    
    ax1.set_xlabel('Data Point Index')
    ax1.set_ylabel('Time Difference (ms)')
    ax1.set_title(f'M2 {t} Time Series ({M2_len} data points)')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 分布直方图
    ax2 = plt.subplot(3, 2, 2*i+2)
    ax2.hist(stats_M2[t]['data'], bins=20, color=colors[i], alpha=0.7)
    ax2.axvline(stats_M2[t]['min'], color=colors[i], linestyle=':', linewidth=2)
    ax2.axvline(stats_M2[t]['max'], color=colors[i], linestyle=':', linewidth=2)
    ax2.axvline(stats_M2[t]['mean'], color=colors[i], linestyle='-', linewidth=2)
    
    # 添加统计信息文本
    ax2.text(0.02, 0.95, stats_text, transform=ax2.transAxes, 
             color=colors[i], fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.3', alpha=0.1, color=colors[i]))
    
    ax2.set_xlabel('Time Difference (ms)')
    ax2.set_ylabel('Frequency')
    ax2.set_title(f'M2 {t} Distribution')
    ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout(rect=[0, 0, 1, 0.96])
# plt.savefig('M2_sequence_analysis.png', dpi=300, bbox_inches='tight')
plt.show()