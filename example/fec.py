import random

def simulate_fec_paradox(users=10, base_bitrate_per_user=1.1, capacity=30.0, recovery_target=0.35):
    """
    Simulates the WebRTC FEC paradox on a constrained link.
    - users: number of parallel users on the link
    - base_bitrate_per_user: total up/down bitrate in Mbps per user
    - capacity: total link capacity in Mbps
    """
    results = {}
    
    # Base configuration without FEC
    total_base_load = users * base_bitrate_per_user
    base_utilization = total_base_load / capacity
    
    # Model packet loss rate (PLR) based on utilization
    # Using a standard non-linear queue overflow model (e.g., M/M/1 queue drop simulation approximation)
    def calculate_plr(utilization):
        if utilization <= 0.2:
            return 0.005 # nominal public internet loss
        elif utilization <= 0.4:
            # Linear rise as queues fill
            return 0.005 + (utilization - 0.2) * 0.1
        else:
            # Sharp non-linear tail-drop explosion
            return 0.025 + (utilization - 0.4) ** 1.5 * 1.5

    base_plr = min(calculate_plr(base_utilization), 1.0)
    results['no_fec'] = {
        'load_mbps': total_base_load,
        'utilization': base_utilization,
        'plr_percent': base_plr * 100
    }
    
    # With FEC enabled to recover from base_plr
    # To recover from e.g., 5% loss, we need roughly 2x that in FEC overhead
    fec_overhead_factor = base_plr * 2.0
    # Cap overhead factor for realistic WebRTC limits (max ~80%)
    fec_overhead_factor = min(fec_overhead_factor, 0.8)
    
    fec_load_per_user = base_bitrate_per_user * (1 + fec_overhead_factor)
    total_fec_load = users * fec_load_per_user
    fec_utilization = total_fec_load / capacity
    
    fec_plr = min(calculate_plr(fec_utilization), 1.0)
    
    # Net effective loss after FEC recovery attempt
    # Simplified Reed-Solomon / XOR recovery capacity model: 
    # If raw loss exceeds the overhead recovery capacity, recovery fails catastrophically
    recovered_loss = max(0, fec_plr - fec_overhead_factor)
    
    results['with_fec'] = {
        'overhead_percent': fec_overhead_factor * 100,
        'load_mbps': total_fec_load,
        'utilization': fec_utilization,
        'raw_plr_percent': fec_plr * 100,
        'effective_loss_percent': recovered_loss * 100
    }
    
    return results

res = simulate_fec_paradox()
print(res)
