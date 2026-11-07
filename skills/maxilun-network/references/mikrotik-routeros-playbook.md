# MikroTik RouterOS Engineering Playbook (RouterOS v6 & v7)

Panduan konfigurasi, otomatisasi skrip, manajemen firewall, QoS/PCQ, dan routing tingkat produksi untuk MikroTik RouterOS.

## 1. Arsitektur Firewall Stateful Standar Produksi

### 1.1 Aturan Filter Input & Forward
Terapkan prinsip *default-drop* dengan inspeksi state koneksi:
```routeros
# Filter Input (Melindungi Router Sendiri)
/ip firewall filter
add chain=input action=accept connection-state=established,related,untracked comment="Terima koneksi established/related"
add chain=input action=drop connection-state=invalid comment="Buang paket invalid"
add chain=input action=accept protocol=icmp comment="Izinkan ICMP terukur"
add chain=input action=accept in-interface-list=LAN comment="Izinkan akses administrasi hanya dari LAN"
add chain=input action=drop comment="Default drop seluruh akses input luar"

# Filter Forward (Melindungi Trafik Antar-Subnet & Internet)
add chain=forward action=fasttrack-connection connection-state=established,related comment="FastTrack untuk efisiensi CPU"
add chain=forward action=accept connection-state=established,related,untracked comment="Terima koneksi established/related"
add chain=forward action=drop connection-state=invalid comment="Buang paket invalid"
add chain=forward action=accept in-interface-list=LAN out-interface-list=WAN comment="Izinkan trafik LAN menuju WAN"
add chain=forward action=accept connection-nat-state=dstnat in-interface-list=WAN comment="Izinkan port forwarding resmi"
add chain=forward action=drop comment="Default drop seluruh trafik forward tak dikenal"
```

### 1.2 Aturan NAT & Hairpin NAT
- **Masquerade**: Selalu tentukan `out-interface-list=WAN` atau `out-interface=ether1`. Dilarang membuat rule masquerade tanpa batasan antarmuka keluar karena dapat memicu kebocoran IP dan loop routing internal.
- **Hairpin NAT**: Wajib saat server lokal diakses oleh klien LAN menggunakan IP publik atau nama domain:
  ```routeros
  /ip firewall nat
  add chain=srcnat action=masquerade src-address=192.168.88.0/24 dst-address=192.168.88.10 protocol=tcp dst-port=443 comment="Hairpin NAT HTTPS"
  ```

---

## 2. Manajemen Bandwidth (QoS & PCQ)

### 2.1 Mangle & Packet Marking
- Saat menandai paket di `/ip firewall mangle`:
  1. Tandai koneksi terlebih dahulu (`action=mark-connection`, `passthrough=yes`).
  2. Tandai paket berdasarkan tanda koneksi (`action=mark-packet`, `passthrough=no`).
- Nonaktifkan `FastTrack` pada antarmuka atau subnet yang wajib melalui antrean Queue Tree, karena FastTrack memotong jalur pemrosesan paket (*bypass*) sebelum mencapai layer antrean.

### 2.2 Per Connection Queue (PCQ) untuk Pembagian Rata
Gunakan tipe antrean PCQ untuk mendistribusikan bandwidth secara adil tanpa mengalokasikan limit tetap per pengguna:
```routeros
/queue type
add name="PCQ-Download" kind=pcq pcq-classifier=dst-address pcq-rate=0 pcq-total-limit=2000KiB
add name="PCQ-Upload" kind=pcq pcq-classifier=src-address pcq-rate=0 pcq-total-limit=2000KiB

/queue simple
add name="Total-LAN" target=192.168.88.0/24 max-limit=100M/100M queue=PCQ-Upload/PCQ-Download
```

---

## 3. Bridge VLAN Filtering & WireGuard (RouterOS v7)

### 3.1 Bridge VLAN Filtering
Gunakan satu bridge perangkat keras dengan `vlan-filtering=yes`:
```routeros
/interface bridge
add name=bridge1 vlan-filtering=yes

/interface bridge port
add bridge=bridge1 interface=ether2 pvid=10 comment="Access Port VLAN 10"
add bridge=bridge1 interface=ether3 pvid=20 comment="Access Port VLAN 20"
add bridge=bridge1 interface=ether24 comment="Trunk Port Switch Core"

/interface bridge vlan
add bridge=bridge1 tagged=bridge1,ether24 untagged=ether2 vlan-ids=10
add bridge=bridge1 tagged=bridge1,ether24 untagged=ether3 vlan-ids=20
```

### 3.2 WireGuard di RouterOS v7
```routeros
/interface wireguard
add name=wg0 listen-port=13231 private-key="<SERVER_PRIVATE_KEY>"

/ip address
add address=10.10.0.1/24 interface=wg0

/interface wireguard peers
add interface=wg0 public-key="<CLIENT_PUBLIC_KEY>" allowed-address=10.10.0.2/32
```
