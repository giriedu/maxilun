# Maxilun Network: Baseline RouterOS v7 Enterprise Hardening
# Invariants: Default-Drop, Interface-List Isolation, Stateful FastTrack, Raw SYN-Flood Defense
# Safe for RouterOS v7.12+

/interface list
add name=WAN comment="Public Internet Uplinks"
add name=LAN comment="Internal Trusted Networks"

/interface list member
add interface=ether1 list=WAN
add interface=bridge list=LAN

# ----------------------------------------------------
# 1. IP Service Hardening (Disable Insecure Protocols)
# ----------------------------------------------------
/ip service
set telnet disabled=yes
set ftp disabled=yes
set www disabled=yes
set api disabled=yes
set api-ssl disabled=yes
set winbox address=192.168.88.0/24
set ssh port=2222 address=192.168.88.0/24

# ----------------------------------------------------
# 2. RAW Table: Anti-DDoS & SYN-Flood Mitigation
# ----------------------------------------------------
/ip firewall raw
add action=drop chain=prerouting in-interface-list=WAN protocol=tcp tcp-flags=fin,syn,rst,psh,ack,urg comment="Drop TCP Xmas Scan"
add action=drop chain=prerouting in-interface-list=WAN protocol=tcp tcp-flags=!fin,!syn,!rst,!psh,!ack,!urg comment="Drop TCP Null Scan"
add action=drop chain=prerouting in-interface-list=WAN protocol=tcp tcp-flags=fin,syn comment="Drop TCP SYN/FIN Scan"
add action=drop chain=prerouting in-interface-list=WAN dst-address-type=broadcast comment="Drop directed broadcast"

# ----------------------------------------------------
# 3. Filter Rules: Stateful Default-Drop Firewall
# ----------------------------------------------------
/ip firewall filter
# Input Chain (Router Self-Protection)
add action=accept chain=input connection-state=established,related,untracked comment="Accept Established, Related, Untracked"
add action=drop chain=input connection-state=invalid comment="Drop Invalid Connections"
add action=accept chain=input protocol=icmp limit=5,10:packet comment="Accept ICMP with strict rate limit"
add action=accept chain=input in-interface-list=LAN comment="Accept all from LAN interface list"
add action=drop chain=input comment="Default Drop: Everything else to router"

# Forward Chain (Transit Traffic Protection)
add action=fasttrack-connection chain=forward connection-state=established,related hw-offload=yes comment="FastTrack Established & Related"
add action=accept chain=forward connection-state=established,related,untracked comment="Accept Established, Related, Untracked"
add action=drop chain=forward connection-state=invalid comment="Drop Invalid Forwarded Traffic"
add action=accept chain=forward in-interface-list=LAN out-interface-list=WAN comment="LAN to Internet"
add action=accept chain=forward connection-nat-state=dstnat in-interface-list=WAN comment="Accept Port Forwards via DST-NAT"
add action=drop chain=forward comment="Default Drop: Everything else forward"

# ----------------------------------------------------
# 4. NAT Configuration
# ----------------------------------------------------
/ip firewall nat
add action=masquerade chain=srcnat out-interface-list=WAN comment="Default Outbound Masquerade"

# ----------------------------------------------------
# 5. WireGuard Site-to-Site / RoadWarrior Scaffold
# ----------------------------------------------------
/interface wireguard
add listen-port=51820 mtu=1420 name=wg0 comment="Maxilun Secure VPN Endpoint"

/ip address
add address=10.10.0.1/24 interface=wg0 network=10.10.0.0
