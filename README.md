# Latency Breakdown 


by MediumSpeed of light in fiber optic cable: 
≈ 200,000 km/sPropagation delay formula: \(\text{Distance (km)} / 200,000 \times 1,000 \times 2 \text{ (Round Trip)}\)
Transmission delay formula for a typical 9,600-bit WebRTC packet (1,200 bytes)


ratio analysis 

1. LAN (Local Area Network)Distance: 0.1 km; Bandwidth: 1,000 Mbps (1 Gbps)Propagation Delay (RTT): 0.001 ms; Transmission Delay: 0.0096 msTotal Network RTT: 0.01 msEstimated End-to-End Media Latency (including 60 ms codec processing): `60.01` ms
2. WAN (Wide Area Network)Distance: 500 km; Bandwidth: 100 Mbps; Propagation Delay (RTT): 5.0 ms; Transmission Delay: 0.096 ms
   Total Network RTT: 5.1 ms;Estimated End-to-End Media Latency (including 60 ms codec processing): 62.55 ms (One-way net delay is 2.55 ms)
3. Arbitrary Network (Global): Distance: 15,000 km Bandwidth: 30 Mbps; Propagation Delay (RTT): 150.0 ms; Transmission Delay: 0.32 ms; Total Network RTT: 150.32 ms Estimated End-to-End Media Latency (including 60 ms codec processing): `135.16` ms (One-way net delay is `75.16` ms)

### Ratio analysis 
#### Transmission Delay 
1. LAN : R1 = delay / distance =  0.0096 / 0.1 km = 0.096
2. WAN: R2 delay : Trans.delay 0.096 ms /500 km  = 0.000192
3. Arbitrary Network (Global): R3 =  0.32 ms / 15000 = 2.133333333333333e-5
The larger the network, the more efficient Transmission becomes

#### Propogation Delay 
1. LAN : R1 = delay / distance =    0.001 ms / 0.1 km =  0.01
2. WAN: R2 delay : Trans.delay  5.0 ms /500 km  = 0.01 
3. Arbitrary Network (Global): R3 =  150.0 ms / 15000 =  0.01
   Thus propagation Deley is fixed and is medium invariant

### Broader Transmission Meaning 

**1. LAN (R1) — High Ratio ( (0.096 { ms/km}))In a Local Area Network:**
The physical distance is microscopic ( (0.1 { km})). 
However, the data packet still must go through fixed network overhead—such as processing time at the network interface card (NIC), 
serialization delay, and software stack handling. 
Because the distance is so short,  these fixed overhead costs dominate the ratio, making the delay "per kilometer" appear exceptionally high.

**2. WAN (R2) — Medium Ratio ( (0.000192 { ms/km})):**
As you scale out to a Wide Area Network ((500text{ km})), 
the data travels over high-speed backbone infrastructure (like fiber-optic cables). While the total delay increases slightly,
 the distance increases by a factor of 5,000. The fixed processing overhead becomes a negligible fraction of the trip, meaning the network is orders of magnitude more efficient per unit of distance.

**3. Arbitrary/Global Network (R3) — Lowest Ratio ( (0.0000213 { ms/km}))At a global scale ((15,000 { km})):**
the transmission delay is almost entirely dictated by the physical speed of light in fiber ((approx 5 { ms}) per (1,000 { km})). 
The fixed equipment delays at the endpoints are completely diluted by the massive distance. This ratio approaches the absolute theoretical physical limit of how fast data can travel through a medium over earth-sized distances.

## potential Issues with WebRTC
1. Packet Loss Impacts (The Multiplier Effect)WebRTC uses two main strategies to fix dropped packets, both of which add massive delays:NACK (Negative Acknowledgment): The receiver realizes a packet is missing and asks the sender to retransmit it.
Latency Cost: Adds exactly 1 extra Network RTT to the delayed packet.FEC (Forward Error Correction): The sender injects extra recovery data into future packets.Latency Cost: Minimal network delay, but requires extra bandwidth (up to 50%+ more), which can worsen congestion on low-bandwidth links like your Global Network.
2. Jitter Buffer Configuration (The Safety Cushion)A jitter buffer holds incoming packets in a queue to smooth out irregular arrival times before playing them.Adaptive Buffering (Default): WebRTC dynamically grows the buffer when network conditions degrade. Under load, a standard jitter buffer frequently adds 20 ms to 100+ ms of artificial delay.Fixed Buffering

If configured with a fixed size to prioritize low latency, packet arrival spikes will exceed the buffer, resulting in choppy audio and frozen video.
