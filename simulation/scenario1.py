import random

def simulate_alice_to_bob(distance_km, bandwidth_mbps, video_bitrate_mbps, 
                            protocol="UDP", packet_loss_rate=0.01, 
                            jitter_max_ms=5, mt_size_bytes=1500):
    """
    Simulates video chunk transfer accounting for headers, jitter, and loss penalties.
    """
    # 1. Propagation Delay
    speed_of_light_fiber = 200000.0  # km/s
    prop_delay_ms = (distance_km / speed_of_light_fiber) * 1000
    
    # 2. Protocol Overhead Allocation
    # Ethernet (18B) + IPv4 (20B) = 38B base. Add L4 Protocol headers.
    if protocol == "TCP":
        payload_per_packet = mt_size_bytes - 20 - 20 - 18 # 1442 bytes payload
    else: # UDP
        payload_per_packet = mt_size_bytes - 8 - 20 - 18  # 1454 bytes payload
        
    video_size_bytes = (video_bitrate_mbps * 1_000_000 * 1.0) / 8
    num_packets = int(video_size_bytes / payload_per_packet) + 1
    
    # Total wire size including protocol headers
    total_data_mb = (num_packets * mt_size_bytes * 8) / 1_000_000
    
    # 3. Transmission Delay
    trans_delay_ms = (total_data_mb / bandwidth_mbps) * 1000
    
    # 4. Jitter (Randomized variance)
    random.seed(42)  # For consistency across runs
    jitter_ms = random.uniform(0, jitter_max_ms)
    
    # 5. Packet Loss Penalty
    loss_penalty_ms = 0
    if protocol == "TCP" and packet_loss_rate > 0:
        # Approximate Round Trip Time (RTT)
        rtt_ms = (2 * prop_delay_ms) + 10 
        
        # Expected penalty: 80% Fast Retransmit (1 RTT delay), 20% Timeout (min 200ms)
        avg_retransmit_penalty = (0.8 * rtt_ms) + (0.2 * max(200, rtt_ms * 2))
        lost_packets = num_packets * packet_loss_rate
        loss_penalty_ms = lost_packets * avg_retransmit_penalty
    
    total_latency_ms = prop_delay_ms + trans_delay_ms + jitter_ms + loss_penalty_ms
    
    return {
        "Packets": num_packets,
        "Prop (ms)": round(prop_delay_ms, 2),
        "Trans+Overhead (ms)": round(trans_delay_ms, 2),
        "Jitter (ms)": round(jitter_ms, 2),
        "Loss Penalty (ms)": round(loss_penalty_ms, 2),
        "Total Latency (ms)": round(total_latency_ms, 2)
    }

# Scenarios configurations
scenarios = {
    "1. LAN (0.1 km, 1 Gbps, 0.01% loss)": {"dist": 0.1, "bw": 1000, "loss": 0.0001, "jitter": 1},
    "2. WAN (500 km, 100 Mbps, 0.5% loss)": {"dist": 500, "bw": 100, "loss": 0.005, "jitter": 5},
    "3. Global (15,000 km, 30 Mbps, 2% loss)": {"dist": 15000, "bw": 30, "loss": 0.02, "jitter": 20}
}

VIDEO_BITRATE = 10.0 # 10 Mbps stream

print(f"=== Alice to Bob Video Latency ({VIDEO_BITRATE} Mbps stream) ===")
for name, spec in scenarios.items():
    print(f"\n[ {name} ]")
    for proto in ["UDP", "TCP"]:
        res = simulate_alice_to_bob(spec["dist"], spec["bw"], VIDEO_BITRATE, protocol=proto, packet_loss_rate=spec["loss"], jitter_max_ms=spec["jitter"])
        print(f"  {proto:3} -> Total: {res['Total Latency (ms)']:7.2f}ms | Base Trans: {res['Trans+Overhead (ms)']:6.2f}ms | Jitter: {res['Jitter (ms)']:4.2f}ms | Loss Penalty: {res['Loss Penalty (ms)']:7.2f}ms ({res['Packets']} pkts)")
