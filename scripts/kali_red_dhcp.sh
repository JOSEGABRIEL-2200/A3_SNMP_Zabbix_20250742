#!/usr/bin/env bash
# =====================================================================
# kali_red_dhcp.sh - Asignacion 3: el servidor Zabbix (Kali eth1) como cliente DHCP
# Jose Gabriel Feliz Maria - 2025-0742
# eth1 (VMnet2 -> nube NET-ZABBIX -> SW1 e0/1, VLAN 10) pide IP por DHCP al R1.
# - dhcp-client-id mac: manda 01+MAC para que R1 le de la reserva 10.7.42.10
# - never-default: la salida a Internet sigue por eth0 (bridged)
# - ruta a la VLAN 99 (gestion del SW1) por el R1
# - autoconnect no: no interfiere con los perfiles de las practicas anteriores
# =====================================================================
set -euo pipefail

if ! nmcli -t -f NAME con show | grep -x 'a3-zabbix' >/dev/null; then
  sudo nmcli con add type ethernet ifname eth1 con-name a3-zabbix autoconnect no \
    ipv4.method auto ipv4.dhcp-client-id mac ipv4.never-default yes \
    ipv4.routes "10.7.42.136/29 10.7.42.1" ipv6.method disabled
fi
sudo nmcli con up a3-zabbix

ip -br a show eth1
ip route
