# MikroTik RouterOS Engineering Playbook (RouterOS v6 & v7)

Production guide for MikroTik RouterOS configuration, script automation, firewall management, QoS/PCQ, and routing.

## 1. Production Stateful Firewall Architecture

### 1.1 Input & Forward Filter Rules
Apply the default-drop principle with connection state inspection:
```routeros
# Input filter (protects the router itself)
/ip firewall filter
add chain=input action=accept connection-state=established,related,untracked comment="Accept established/related connections"
add chain=input action=drop connection-state=invalid comment="Drop invalid packets"
add chain=input action=accept protocol=icmp comment="Allow limited ICMP"
add chain=input action=accept in-interface-list=LAN comment="Allow administrative access from LAN only"
add chain=input action=drop comment="Default drop all outside input access"

# Forward filter (protects inter-subnet and internet traffic)
add chain=forward action=fasttrack-connection connection-state=established,related comment="FastTrack for CPU efficiency"
add chain=forward action=accept connection-state=established,related,untracked comment="Accept established/related connections"
add chain=forward action=drop connection-state=invalid comment="Drop invalid packets"
add chain=forward action=accept in-interface-list=LAN out-interface-list=WAN comment="Allow LAN traffic to WAN"
add chain=forward action=accept connection-nat-state=dstnat in-interface-list=WAN comment="Allow authorized port forwarding"
add chain=forward action=drop comment="Default drop all unknown forward traffic"
```

### 1.2 NAT & Hairpin NAT Rules
- **Masquerade**: Always set `out-interface-list=WAN` or `out-interface=ether1`. Never create a masquerade rule without an outgoing interface restriction, because it can cause IP leaks and internal routing loops.
- **Hairpin NAT**: Required when LAN clients reach a local server through its public IP or domain name:
  ```routeros
  /ip firewall nat
  add chain=srcnat action=masquerade src-address=192.168.88.0/24 dst-address=192.168.88.10 protocol=tcp dst-port=443 comment="Hairpin NAT HTTPS"
  ```

---

## 2. Bandwidth Management (QoS & PCQ)

### 2.1 Mangle & Packet Marking
- When marking packets in `/ip firewall mangle`:
  1. Mark the connection first (`action=mark-connection`, `passthrough=yes`).
  2. Mark packets based on the connection mark (`action=mark-packet`, `passthrough=no`).
- Disable `FastTrack` on any interface or subnet that must pass through a Queue Tree, because FastTrack bypasses packet processing before the queue layer.

### 2.2 Per Connection Queue (PCQ) for Even Sharing
Use the PCQ queue type to distribute bandwidth fairly without allocating a fixed limit per user:
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
Use one hardware bridge with `vlan-filtering=yes`:
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

### 3.2 WireGuard on RouterOS v7
```routeros
/interface wireguard
add name=wg0 listen-port=13231 private-key="<SERVER_PRIVATE_KEY>"

/ip address
add address=10.10.0.1/24 interface=wg0

/interface wireguard peers
add interface=wg0 public-key="<CLIENT_PUBLIC_KEY>" allowed-address=10.10.0.2/32
```
