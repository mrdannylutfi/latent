import time

def evaluate_video_latency(distance_km, bandwidth_mbps, video_bitrate_mbps):
    """
    Calculates the theoretical one-way latency for transferring a video segment.
    """
    # 1. Propagation Delay (Speed of light in glass/fiber is ~200,000 km/s)
    speed_of_light_fiber = 200000.0  # km/s
    prop_delay_sec = distance_km / speed_of_light_fiber
    
    # 2. Transmission Delay (Data Size in Mb / Bandwidth in Mbps)
    # Assuming we transmit a 1-second segment of video data
    video_size_mb = video_bitrate_mbps * 1.0  
    trans_delay_sec = video_size_mb / bandwidth_mbps
    
    # Total Latency
    total_latency_ms = (prop_delay_sec + trans_delay_sec) * 1000
    
    return {
        "Propagation Delay (ms)": round(prop_delay_sec * 1000, 4),
        "Transmission Delay (ms)": round(trans_delay_sec * 1000, 4),
        "Total Latency (ms)": round(total_latency_ms, 2)
    }

# Video Profile: 1080p @ 60fps streaming chunk (approx. 10 Mbps)
VIDEO_BITRATE = 10.0 

# Define network profiles
scenarios = {
    "1. LAN (Local Area Network)": {
        "distance_km": 0.1,       # Local building / switch distance
        "bandwidth_mbps": 1000.0  # 1 Gbps Ethernet
    },
    "2. WAN (Wide Area Network)": {
        "distance_km": 500.0,     # Regional or multi-city network
        "bandwidth_mbps": 100.0   # Standard enterprise lease line/broadband
    },
    "3. Arbitrary Network (Global)": {
        "distance_km": 15000.0,   # Cross-continental (e.g., US to Asia)
        "bandwidth_mbps": 30.0    # Typical public international transit link
    }
}

# Run evaluation
print(f"--- Video Transfer Latency Evaluation ({VIDEO_BITRATE} Mbps stream) ---")
for network, specs in scenarios.items():
    metrics = evaluate_video_latency(
        specs["distance_km"], 
        specs["bandwidth_mbps"], 
        VIDEO_BITRATE
    )
    print(f"\n[ {network} ]")
    print(f"  Distance: {specs['distance_km']} km | Bandwidth: {specs['bandwidth_mbps']} Mbps")
    for key, val in metrics.items():
        print(f"  {key}: {val}")
