import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D

# 1. Define Mesh Grid Dimensions (Bandwidth vs. Packet Loss)
# X: Available Bandwidth (0 to 100 Mbps)
# Y: Packet Loss (0% to 30% to encompass LAN, WAN, and Global ranges)
bw = np.linspace(0.5, 100, 100)
loss = np.linspace(0, 30, 100)
BW, LOSS = np.meshgrid(bw, loss)

# 2. Calculate Theoretical WebRTC Call Quality Score (MOS: 1.0 to 4.5)
# Base score starts high if bandwidth is sufficient. Drops sharply as loss climbs.
# Below 2 Mbps, bandwidth starvation also degrades the stream.
base_r = 94.0  # Maximum standard E-model rating
R_loss = LOSS * 2.5  # Degradation multiplier from packet drop
R_bw = 20.0 * np.exp(-BW / 1.5)  # Starvation factor for very low bandwidth

R_factor = base_r - R_loss - R_bw
R_factor = np.clip(R_factor, 0, 100)

# Convert R-factor to standard Mean Opinion Score (MOS)
MOS = 1 + 0.035 * R_factor + R_factor * (R_factor - 60) * (100 - R_factor) * 0.000007
MOS = np.clip(MOS, 1.0, 4.5)

# 3. Create Custom WebRTC Quality Colormap (Green -> Yellow -> Red)
colors = [(0.8, 0.1, 0.1), (0.9, 0.8, 0.1), (0.1, 0.6, 0.2)]  # Red, Yellow, Green
webrtc_cmap = LinearSegmentedColormap.from_list("webrtc_quality", colors, N=256)

# 4. Generate Interactive Matplotlib Canvas
%matplotlib notebook  # Enables active 3D rotation dragging in Jupyter/IPython notebooks
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1, 1, 1, projection='3d')

# Plot the continuous 3D Surface
surf = ax.plot_surface(BW, LOSS, MOS, cmap=webrtc_cmap, edgecolor='none', alpha=0.85)

# 5. Highlight Exact Transition Threshold Contours (Choppy Boundary)
# Standard WebRTC streams become visibly 'choppy' when MOS drops below 3.6
ax.contour(BW, LOSS, MOS, levels=[3.6], colors=['black'], linewidths=[3], linestyles=['--'])

# Decorate and position the axis labels
ax.set_title("WebRTC Quality Topology Map\n(Black Dashed Line = Threshold to Choppy Call Quality)", fontsize=13, pad=20)
ax.set_xlabel("Available Bandwidth (Mbps)", labelpad=12)
ax.set_ylabel("Packet Loss (%)", labelpad=12)
ax.set_zlabel("Call Quality Score (MOS)", labelpad=10)

# Set initial visual angle for best topology interpretation
ax.view_init(elev=30, azim=-130)

# Add a visual color legend scale
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
cbar.set_label('Mean Opinion Score (MOS)', rotation=270, labelpad=15)
cbar.set_ticks([1.0, 2.5, 3.6, 4.5])
cbar.set_ticklabels(['1.0 (Dropped)', '2.5 (Poor/Choppy)', '3.6 (Good Threshold)', '4.5 (Excellent)'])

plt.tight_layout()
plt.show()
