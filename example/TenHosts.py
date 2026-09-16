import time
import random

class GlobalNetworkSimulation:
    def __init__(self, total_users=10, base_bitrate_per_user=1.1, link_capacity_mbps=30.0):
        self.users = total_users
        self.base_bitrate = base_bitrate_per_user  # 1.1 Mbps (Upstream + Downstream average per node)
        self.capacity = link_capacity_mbps         # 30 Mbps Global Link constraint
        
    def _calculate_router_packet_loss(self, current_load_mbps):
        """
        Simulates an Active Queue Management (AQM) / Tail-Drop router behavior.
        Loss triggers exponentially once link capacity utilization crosses a critical threshold.
        """
        utilization = current_load_mbps / self.capacity
        
        if utilization <= 0.25:
            return 0.005  # Base background public transit jitter/loss (0.5%)
        elif utilization <= 0.35:
            # Linear queue pressure buildup
            return 0.005 + (utilization - 0.25) * 0.2
        else:
            # Catastrophic congestion cliff / queue buffer saturation
            return 0.025 + ((utilization - 0.35) ** 1.8) * 2.5

    def run_simulation(self):
        print("=" * 65)
        print(f" SIMULATING WEBRTC FEC PARADOX ({self.users} Users on {self.capacity} Mbps Global Link)")
        print("=" * 65)
        
        # --- PHASE 1: Baseline Load Without FEC ---
        no_fec_load = self.users * self.base_bitrate
        no_fec_loss_rate = min(self._calculate_router_packet_loss(no_fec_load), 1.0)
        
        print(f"Phase 1: No FEC Enabled")
        print(f"  - Total Aggregate Network Load : {no_fec_load:.2f} Mbps")
        print(f"  - Link Capacity Utilization    : {(no_fec_load / self.capacity) * 100:.1f}%")
        print(f"  - Router Drop Rate (Raw Loss)  : {no_fec_loss_rate * 100:.2f}%")
        print(f"  - Effective Media Loss Rate    : {no_fec_loss_rate * 100:.2f}%")
        print("-" * 65)
        
        # --- PHASE 2: Turning on FEC to Combat Loss ---
        # WebRTC dynamically injects extra FEC overhead to attempt recovery from the Phase 1 loss.
        # To recover from e.g. 5% loss, Redundancy algorithms typically add 1.5x - 2x that loss in overhead.
        fec_overhead_multiplier = min(no_fec_loss_rate * 2.2, 0.75) # Cap overhead at 75% max
        
        fec_bitrate_per_user = self.base_bitrate * (1 + fec_overhead_multiplier)
        fec_total_load = self.users * fec_bitrate_per_user
        
        # New network drop rate calculated using the heavier aggregate load
        fec_router_loss_rate = min(self._calculate_router_packet_loss(fec_total_load), 1.0)
        
        # Effective Loss Calculation: 
        # Realized loss minus the maximum repair capabilities of the injected FEC packets.
        effective_loss_after_fec = max(0.0, fec_router_loss_rate - fec_overhead_multiplier)
        
        print(f"Phase 2: FEC Aggressively Engaged")
        print(f"  - Injected FEC Redundancy      : +{fec_overhead_multiplier * 100:.1f}% overhead per user")
        print(f"  - New Heavy Network Load       : {fec_total_load:.2f} Mbps")
        print(f"  - Elevated Link Utilization    : {(fec_total_load / self.capacity) * 100:.1f}%")
        print(f"  - New Router Drop Rate         : {fec_router_loss_rate * 100:.2f}%  <-- (Router dropped more!)")
        print(f"  - Effective Media Loss Rate    : {effective_loss_after_fec * 100:.2f}%")
        print("=" * 65)
        
        # --- Conclusion Verdict ---
        print("VERDICT:")
        if effective_loss_after_fec > no_fec_loss_rate:
            print(f" [!] PARADOX CONFIRMED: Enabling FEC increased effective stream corruption\n"
                  f"     from {no_fec_loss_rate*100:.2f}% to {effective_loss_after_fec*100:.2f}% due to induced link collapse.")
        else:
            print(" [✓] The link had enough structural cushion to handle the FEC overhead recovery packet bursts.")
        print("=" * 65)

if __name__ == "__main__":
    # Test a heavily crowded link (Base per-user media bitrates elevated to highlight congestion thresholds)
    sim = GlobalNetworkSimulation(total_users=10, base_bitrate_per_user=1.12, link_capacity_mbps=30.0)
    sim.run_simulation()
