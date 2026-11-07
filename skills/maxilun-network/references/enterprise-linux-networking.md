# Enterprise Linux Networking & Infrastructure Playbook

Panduan rekayasa jaringan server Linux tingkat produksi, firewall nftables, routing kebijakan, dan analisis paket.

## 1. Linux Network Stack & Policy Routing (`iproute2`)

### 1.1 Multi-WAN & Routing Berbasis Kebijakan (`ip rule`)
Saat server memiliki 2 gateway uplink (misalnya ISP-A di `eth0` dan ISP-B di `eth1`):
1. Definisikan tabel routing terpisah di `/etc/iproute2/rt_tables`:
   ```
   100   T1_ISP_A
   200   T2_ISP_B
   ```
2. Buat rute default terpisah per tabel:
   ```bash
   ip route add 192.168.1.0/24 dev eth0 src 192.168.1.10 table T1_ISP_A
   ip route add default via 192.168.1.1 dev eth0 table T1_ISP_A

   ip route add 192.168.2.0/24 dev eth1 src 192.168.2.10 table T2_ISP_B
   ip route add default via 192.168.2.1 dev eth1 table T2_ISP_B
   ```
3. Arahkan trafik kembali ke gateway yang sama dengan IP sumbernya:
   ```bash
   ip rule add from 192.168.1.10 table T1_ISP_A
   ip rule add from 192.168.2.10 table T2_ISP_B
   ```

---

## 2. Firewall Modern Berbasis `nftables`

Gunakan `nftables` alih-alih `iptables` untuk performa tinggi dan atomisitas pembaruan:
```nftables
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Terima loopback dan koneksi established
        iifname "lo" accept
        ct state established,related accept
        ct state invalid drop

        # ICMP dan akses SSH terisolasi
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

## 3. Diagnostik Jaringan & Analisis Paket

- **Pemeriksaan Port & Socket (`ss`)**:
  Periksa proses yang mendengarkan port tanpa resolusi DNS lambat:
  ```bash
  ss -tulpn
  ```
- **Inspeksi Paket Terfokus (`tcpdump`)**:
  Tangkap payload DNS atau SYN handshake spesifik:
  ```bash
  tcpdump -nn -i eth0 'tcp[tcpflags] & (tcp-syn) != 0 and not src and dst net 10.0.0.0/8' -c 100
  ```
- **MTU Clamping untuk Terowongan VPN**:
  Cegah fragmentasi paket pada WireGuard atau GRE tunnel dengan menyetel MSS clamping di firewall:
  ```bash
  iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
  ```
