import numpy as np
import matplotlib.pyplot as plt

# 1. Define the exact values based on your formulas
lan_val = 0
wan_min, wan_max = np.exp(-6), 3.333 * np.exp(-6)
global_min, global_max = np.exp(-2), 2 * np.exp(-2)

# Midpoints for summary comparison
mediums = ['LAN', 'WAN', 'Global']
mid_values = [lan_val, (wan_min + wan_max) / 2, (global_min + global_max) / 2]

# 2. Simulate distribution datasets for the Histogram
np.random.seed(42)
lan_sim = np.zeros(1000)
wan_sim = np.random.uniform(wan_min, wan_max, 1000)
global_sim = np.random.uniform(global_min, global_max, 1000)

# Create the figure and subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# --- PLOT 1: Histogram of Simulated Packet Loss ---
ax1 = axes[0]
# Use log spacing for bins to capture all ranges accurately
bins = np.logspace(-7, 0, 50)
bins = np.insert(bins, 0, 0) # Include exact 0 for LAN

ax1.hist(lan_sim, bins=bins, alpha=0.7, label='LAN (0%)', color='g', edgecolor='black')
ax1.hist(wan_sim, bins=bins, alpha=0.7, label='WAN (e^-6 to 3.33e^-6)', color='b', edgecolor='black')
ax1.hist(global_sim, bins=bins, alpha=0.7, label='Global (e^-2 to 2e^-2)', color='r', edgecolor='black')

ax1.set_xscale('log')
ax1.set_title('Histogram of Simulated Packet Loss (Log X-Axis)')
ax1.set_xlabel('Packet Loss Ratio (Log Scale)')
ax1.set_ylabel('Frequency Count')
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend()

# --- PLOT 2: Bar Chart with Log Scale to Explain Scale Differences ---
ax2 = axes[1]
bars = ax2.bar(mediums, [v + 1e-7 for v in mid_values], color=['green', 'blue', 'red'], alpha=0.8, edgecolor='black')

ax2.set_yscale('log')
ax2.set_title('Average Value Comparison (Log Y-Axis)')
ax2.set_ylabel('Loss Ratio (Log Scale)')
ax2.set_xlabel('Medium')
ax2.grid(True, which="both", ls="--", alpha=0.5)

# Add exact percentage labels above bars
labels = ['0%', f'{mid_values[1]*100:.3f}%', f'{mid_values[2]*100:.1f}%']
for bar, label in zip(bars, labels):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height * 1.2, label,
             ha='center', va='bottom', fontsize=10, weight='bold')

plt.tight_layout()
plt.show()
