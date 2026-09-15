#Scenario2: WebRTC
import random

def simulate_webrtc_vs_tcp(distance_km, bandwidth_mbps, video_bitrate_mbps, 
                           packet_loss_rate=0.01, jitter_max_ms=5, mt_size_bytes=1500):
    """
    Simulates video chunk transfer for WebRTC (SRTP/UDP with NACK/FEC) vs TCP.
    """
    # 1. Propagation Delay (One-way)
    speed_of_light_fiber = 200000.0  # km/s
    prop_delay_ms = (distance_km / speed_of_light_fiber) * 1000
    rtt_ms = (2 * prop_delay_ms) + 10  # Round Trip Time with light hardware processing overhead
    
    # 2. Protocol Header Overheads (Bytes per packet)
    # Ethernet (18B) + IPv4 (20B) = 38B Base
    # TCP: Base + TCP (20B) = 58B
    # WebRTC: Base + UDP (8B) + DTLS/SRTP Crypto & RTP Headers (~40B) = 86B
    
    tcp_overhead = 18 + 20 + 20
    webrtc_overhead = 18 + 20 + 8 + 40
    
    tcp_payload = mt_size_bytes - tcp_overhead
    webrtc_payload = mt_size_bytes - webrtc_overhead
    
    video_size_bytes = (video_bitrate_mbps * 1_000_000 * 1.0) / 8
    
    # WebRTC includes Forward Error Correction (FEC) overhead to proactively protect against loss
    # Typically, WebRTC dynamically injects ~15% redundant FEC data under medium/high loss conditions
    fec_overhead_factor = 1.15 if packet_loss_rate > 0.005 else 1.05
    webrtc_video_bytes = video_size_bytes * fec_overhead_factor
    
    tcp_packets = int(video_size_bytes / tcp_payload) + 1
    webrtc_packets = int(webrtc_video_bytes / webrtc_payload) + 1
    
    # 3. Transmission Delay (Data Size / Bandwidth)
    tcp_trans_ms = ((tcp_packets * mt_size_bytes * 8) / 1_000_000 / bandwidth_mbps) * 1000
    webrtc_trans_ms = ((webrtc_packets * mt_size_bytes * 8) / 1_000_000 / bandwidth_mbps) * 1000
    
    # 4. Jitter (Randomized variance)
    random.seed(42)
    jitter_ms = random.uniform(0, jitter_max_ms)
    
    # 5. Loss Penalty Engine
    tcp_loss_penalty = 0
    webrtc_loss_penalty = 0
    
    if packet_loss_rate > 0:
        lost_tcp_pkts = tcp_packets * packet_loss_rate
        # TCP stops stream (Head-of-Line Blocking) - combination of Fast Retransmit and heavy Timeout penalties
        tcp_avg_penalty = (0.8 * rtt_ms) + (0.2 * max(200, rtt_ms * 2))
        tcp_loss_penalty = lost_tcp_pkts * tcp_avg_penalty
        
        # WebRTC handles loss intelligently:
        # - FEC catches a portion of the losses instantly (0ms penalty)
        # - Remaining losses trigger a NACK (Negative Acknowledgment), resulting in an immediate retransmission
        # Unlike TCP, WebRTC does NOT freeze the queue; it plays out audio/video concurrently while NACK processes.
        effective_unrecovered_loss_rate = max(0, packet_loss_rate - 0.02) # assume FEC covers up to 2% loss
        lost_webrtc_pkts = webrtc_packets * effective_unrecovered_loss_rate
        
        # WebRTC NACK recovery takes exactly 1 RTT (No exponential backoff timeouts)
        webrtc_loss_penalty = lost_webrtc_pkts * rtt_ms

    # Total Latency Calculations
    tcp_total = prop_delay_ms + tcp_trans_ms + jitter_ms + tcp_loss_penalty
    webrtc_total = prop_delay_ms + webrtc_trans_ms + jitter_ms + webrtc_loss_penalty
    
    return {
        "TCP": {
            "Packets": tcp_packets,
            "Trans (ms)": round(tcp_trans_ms, 2),
            "Loss Penalty (ms)": round(tcp_loss_penalty, 2),
            "Total (ms)": round(tcp_total, 2)
        },
        "WebRTC": {
            "Packets": webrtc_packets,
            "Trans (ms)": round(webrtc_trans_ms, 2),
            "Loss Penalty (ms)": round(webrtc_loss_penalty, 2),
            "Total (ms)": round(webrtc_total, 2)
        },
        "Prop (ms)": round(prop_delay_ms, 2),
        "Jitter (ms)": round(jitter_ms, 2)
    }

# Rerun the exact network scenarios
scenarios = {
    "1. LAN (0.1 km, 1 Gbps, 0.01% loss)": {"dist": 0.1, "bw": 1000, "loss": 0.0001, "jitter": 1},
    "2. WAN (500 km, 100 Mbps, 0.5% loss)": {"dist": 500, "bw": 100, "loss": 0.005, "jitter": 5},
    "3. Global (15,000 km, 30 Mbps, 2% loss)": {"dist": 15000, "bw": 30, "loss": 0.02, "jitter": 20}
}

VIDEO_BITRATE = 10.0

print(f"=== Alice to Bob: WebRTC vs TCP Real-World Performance ===")
for name, spec in scenarios.items():
    res = simulate_webrtc_vs_tcp(spec["dist"], spec["bw"], VIDEO_BITRATE, spec["loss"], spec["jitter"])
    print(f"\n[ {name} ]")
    print(f"  Physical Prop Delay: {res['Prop (ms)']}ms | Environment Jitter: {res['Jitter (ms)']}ms")
    print(f"  --> TCP    | Packets: {res['TCP']['Packets']:4d} | Base Trans: {res['TCP']['Trans (ms)']:6.2f}ms | Loss Penalty: {res['TCP']['Loss Penalty (ms)']:7.2f}ms | TOTAL: {res['TCP']['Total (ms)']:7.2f}ms")
    print(f"  --> WebRTC | Packets: {res['WebRTC']['Packets']:4d} | Base Trans: {res['WebRTC']['Trans (ms)']:6.2f}ms | Loss Penalty: {res['WebRTC']['Loss Penalty (ms)']:7.2f}ms | TOTAL: {res['WebRTC']['Total (ms)']:7.2f}ms")
