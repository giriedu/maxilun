# VPN Architecture, Dynamic Routing & Gateway Redundancy

Engineering standards for WireGuard tunnels, OSPF/BGP dynamic routing, recursive route failover, and VRRP high availability on MikroTik RouterOS and Linux.

---

## 1. WireGuard Site-to-Site & Mesh Architecture

WireGuard provides kernel-level cryptographic tunneling with low overhead:

1. **RouterOS v7 WireGuard Setup**:
   ```routeros
   /interface wireguard
   add listen-port=51820 mtu=1420 name=wg-backbone private-key="..."

   /interface wireguard peers
   add allowed-address=10.200.0.0/24 endpoint-address=vpn.datacenter.net \
       endpoint-port=51820 interface=wg-backbone persistent-keepalive=25s \
       public-key="..."
   ```
2. **Persistent Keepalive Invariant**:
   - Peers behind NAT must set `persistent-keepalive=25s` to keep stateful firewall connection mappings open.
3. **MSS Clamping**:
   - Encapsulation overhead reduces standard 1500 MTU to 1420 (IPv4) or 1400 (IPv6). Clamp MSS to avoid silent packet drops:
   ```routeros
   /ip firewall mangle
   add action=change-mss chain=forward new-mss=clamp-to-pmtu passthrough=yes \
       protocol=tcp tcp-flags=syn
   ```

---

## 2. Multi-WAN Recursive Route Failover

Do not rely solely on interface link state for WAN failover. If an ISP cable modem remains linked but upstream internet routing fails, standard routes never fail over.

### Recursive Routing via External DNS Checks (RouterOS)
```routeros
# Step 1: Host routes to trustworthy DNS checkers via specific ISP gateways
/ip route
add check-gateway=ping dst-address=1.1.1.1/32 gateway=192.168.1.1 scope=10
add check-gateway=ping dst-address=8.8.8.8/32 gateway=192.168.2.1 scope=10

# Step 2: Default internet routes target the DNS checkers with target-scope
add distance=1 dst-address=0.0.0.0/0 gateway=1.1.1.1 target-scope=11
add distance=2 dst-address=0.0.0.0/0 gateway=8.8.8.8 target-scope=11
```
- **Invariant**: Primary route distance is `1`, secondary backup is `2`. When `1.1.1.1` ceases answering pings, the primary default route drops automatically within 10 seconds.

---

## 3. Dynamic Routing: OSPFv3 & BGP Peering

1. **OSPF Single-Area & Multi-Area Design**:
   - Use Area 0 (`backbone`) for router interconnections. Configure point-to-point network type on tunnel interfaces to skip Designated Router (DR) election delays.
2. **BGP Multi-Homed Routing**:
   - Enforce route filters on all external eBGP sessions: reject private ASNs (`64512–65534`) and bogon IP prefixes (`RFC 1918`, `RFC 6598`) on incoming announcements.

---

## 4. VRRP Gateway High Availability

For dual-router redundancy on high-traffic LAN segments:

```routeros
/interface vrrp
add interface=bridge-lan name=vrrp-lan priority=150 vrid=10
/ip address
add address=192.168.10.1/24 interface=vrrp-lan
```
- Master router runs `priority=150`, standby backup runs `priority=100`.
- Clients configure `192.168.10.1` as their default gateway. On master failure, standby assumes virtual MAC within 3 seconds with zero IP conflict.
