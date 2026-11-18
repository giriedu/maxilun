# Enterprise Linux Networking & Infrastructure Playbook

Engineering guide for production Linux server networking, nftables firewalls, policy routing, and packet analysis.

## 1. Linux Network Stack & Policy Routing (`iproute2`)

### 1.1 Multi-WAN & Policy-Based Routing (`ip rule`)
When a server has 2 uplink gateways (for example ISP-A on `eth0` and ISP-B on `eth1`):
1. Define separate routing tables in `/etc/iproute2/rt_tables`:
   ```
   100   T1_ISP_A
   200   T2_ISP_B
   ```
2. Create a separate default route per table:
   ```bash
   ip route add 192.168.1.0/24 dev eth0 src 192.168.1.10 table T1_ISP_A
   ip route add default via 192.168.1.1 dev eth0 table T1_ISP_A

   ip route add 192.168.2.0/24 dev eth1 src 192.168.2.10 table T2_ISP_B
   ip route add default via 192.168.2.1 dev eth1 table T2_ISP_B
   ```
3. Send return traffic out through the gateway that matches its source IP:
   ```bash
   ip rule add from 192.168.1.10 table T1_ISP_A
   ip rule add from 192.168.2.10 table T2_ISP_B
   ```

---

## 2. Modern Firewall with `nftables`

Use `nftables` instead of `iptables` for high performance and atomic updates:
```nftables
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Accept loopback and established connections
        iifname "lo" accept
        ct state established,related accept
        ct state invalid drop

        # ICMP and restricted SSH access
        ip protocol icmp accept
        ip6 nexthdr ipv6-icmp accept
        tcp dport 22 ip saddr 10.0.0.0/8 accept
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
        ct state established,related accept
        iifname "wg0" oifname "eth0" accept
    }
}
```

---

## 3. Network Diagnostics & Packet Analysis

- **Port & socket inspection (`ss`)**:
  List the processes listening on ports without slow DNS resolution:
  ```bash
  ss -tulpn
  ```
- **Focused packet inspection (`tcpdump`)**:
  Capture a specific DNS payload or SYN handshake:
  ```bash
  tcpdump -nn -i eth0 'tcp[tcpflags] & (tcp-syn) != 0 and not src and dst net 10.0.0.0/8' -c 100
  ```
- **MTU clamping for VPN tunnels**:
  Prevent packet fragmentation on a WireGuard or GRE tunnel by setting MSS clamping in the firewall:
  ```bash
  iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
  ```
