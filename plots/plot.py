import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

# Set random seed for reproducibility
np.random.seed(42)

# =====================================================================
# DATA GENERATION
# =====================================================================

# 1. Packet Loss Parameters (Derived from your mathematical bounds)
# LAN: 0
# WAN: e^-6 to 3.333*e^-6 (~0.0025 to ~0.0083) -> Midpoint ~ 0.0054
# Global: e^-2 to 2*e^-2 (~0.1353 to ~0.2707) -> Midpoint ~ 0.2030
wan_mid = (np.exp(-6) + 3.333 * np.exp(-6)) / 2
global_mid = (np.exp(-2) + 2 * np.exp(-2)) / 2

# Generate continuous range for smooth PDF plotting
x_wan = np.linspace(0.0001, 0.02, 1000)
x_global = np.linspace(0.05, 0.45, 1000)

# 2. 3D Scatter Plot Data Synthesis (100 sample points per medium)
n_samples = 100

# LAN Data Profile
lan_dist = np.random.uniform(0.01, 0.1, n_samples)
lan_bw = np.random.uniform(100, 1000, n_samples)
lan_loss = np.zeros(n_samples)

# WAN Data Profile
wan_dist = np.random.uniform(100, 800, n_samples)
wan_bw = np.random.uniform(50, 100, n_samples)
# Log-normal distribution centered around the calculated WAN loss
wan_loss = np.random.lognormal(mean=np.log(wan_mid), sigma=0.2, size=n_samples)

# Global Data Profile
global_dist = np.random.uniform(5000, 20000, n_samples)
global_bw = np.random.uniform(10, 30, n_samples)
# Log-normal distribution centered around the calculated Global loss
global_loss = np.random.lognormal(mean=np.log(global_mid), sigma=0.15, size=n_samples)

# =====================================================================
# PLOTTING
# =====================================================================

fig = plt.figure(figsize=(16, 7))

# --- PLOT 1: Smooth Probability Density Functions (PDF) ---
ax1 = fig.add_subplot(1, 2, 1)

# LAN is represented as a Delta function (spike at 0)
ax1.axvline(x=0, color='green', linestyle='-', linewidth=3, label='LAN PDF (Spike at 0%)')

# Fit and plot WAN log-normal PDF
shape_w, loc_w, scale_w = lognorm.fit(wan_loss, floc=0)
ax1.plot(x_wan, lognorm.pdf(x_wan, shape_w, loc_w, scale_w), 
         color='blue', linewidth=2.5, label='WAN PDF (e^-6 Base)')
ax1.fill_between(x_wan, lognorm.pdf(x_wan, shape_w, loc_w, scale_w), color='blue', alpha=0.15)

# Fit and plot Global log-normal PDF
shape_g, loc_g, scale_g = lognorm.fit(global_loss, floc=0)
ax1.plot(x_global, lognorm.pdf(x_global, shape_g, loc_g, scale_g), 
         color='red', linewidth=2.5, label='Global PDF (e^-2 Base)')
ax1.fill_between(x_global, lognorm.pdf(x_global, shape_g, loc_g, scale_g), color='red', alpha=0.15)

ax1.set_xscale('symlog', linthresh=0.001)  # Symlog handles exact 0 alongside log distributions
ax1.set_title('Packet Loss Probability Density Functions (PDF)', fontsize=13, pad=10)
ax1.set_xlabel('Packet Loss Ratio (Symmetric Log Scale)')
ax1.set_ylabel('Probability Density')
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend(fontsize=10)

# --- PLOT 2: Multi-Variable 3D Scatter Plot ---
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

# Scatter plots for each medium profile
ax2.scatter(lan_dist, lan_bw, lan_loss * 100, c='green', marker='o', s=35, alpha=0.7, label='LAN')
ax2.scatter(wan_dist, wan_bw, wan_loss * 100, c='blue', marker='^', s=35, alpha=0.7, label='WAN')
ax2.scatter(global_dist, global_bw, global_loss * 100, c='red', marker='s', s=35, alpha=0.7, label='Global')

ax2.set_title('Multi-Variable Profile: Distance vs. Bandwidth vs. Loss', fontsize=13, pad=15)
ax2.set_xlabel('Distance (km)', labelpad=10)
ax2.set_ylabel('Bandwidth (Mbps)', labelpad=10)
ax2.set_zlabel('Packet Loss (%)', labelpad=5)

# Adjust viewing perspective to balance all 3 axes cleanly
ax2.view_init(elev=20, azim=-45)
ax2.legend(fontsize=10, loc='upper left')

plt.tight_layout()
plt.show()
