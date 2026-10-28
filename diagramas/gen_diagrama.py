import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(17, 12), dpi=150)
ax.set_xlim(0, 170); ax.set_ylim(0, 120); ax.axis("off")
fig.patch.set_facecolor("white")

INK = "#1f2937"; MUTED = "#6b7280"
C_R = "#0f766e"; C_ZBX = "#dc2626"; C_SNMP = "#2563eb"; C_DHCP = "#7c3aed"; C_MG = "#9ca3af"


def box(x, y, w, h, title, lines, color, fs=9.0, tfs=12, face="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.8",
                                linewidth=2, edgecolor=color, facecolor=face, zorder=3))
    ax.text(x + w/2, y + h - 3.0, title, ha="center", va="center", fontsize=tfs, fontweight="bold", color=color, zorder=4)
    for i, t in enumerate(lines):
        ax.text(x + w/2, y + h - 6.8 - i*3.1, t, ha="center", va="center", fontsize=fs,
                color=INK, family="DejaVu Sans Mono", zorder=4)


def link(p1, p2, label=None, color=INK, lw=2.2, off=(0, 1.8), fs=8.3):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, zorder=2, solid_capstyle="round")
    if label:
        ax.text((p1[0]+p2[0])/2 + off[0], (p1[1]+p2[1])/2 + off[1], label, ha="center", va="center",
                fontsize=fs, color=MUTED, zorder=5, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))


def flow(p1, p2, color, rad=0.0, lw=2.4):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=16, color=color, lw=lw,
                                 ls=(0, (5, 3)), connectionstyle=f"arc3,rad={rad}", zorder=2))


ax.text(85, 117, "Asignación 3 — Monitoreo SNMP de solo lectura con Zabbix",
        ha="center", fontsize=17, fontweight="bold", color=INK)
ax.text(85, 113.2, "Jose Gabriel Feliz Maria · Matrícula 2025-0742 · Seguridad de Redes (ITLA)",
        ha="center", fontsize=10.5, color=MUTED)

box(57, 84, 56, 25, "R1 (Cisco IOL 15.7)", [
    "e0/0.10  10.7.42.1/25    VLAN 10 LAN",
    "e0/0.99  10.7.42.137/29  VLAN 99 GESTION",
    "Servidor DHCP de la LAN",
    "reserva 10.7.42.10 -> Zabbix",
    "SNMP v2c RO + ACL-SNMP-ZABBIX"], C_R, tfs=11.5)

box(57, 52, 56, 20.5, "SW1 (Cisco IOL L2 15.2)", [
    "e0/0 trunk 10,99 · nativa 999",
    "e0/1 VLAN 10 · port-security",
    "Vlan99  10.7.42.138/29",
    "SNMP v2c RO + ACL-SNMP-ZABBIX"], C_R, tfs=11.5)

box(52, 12, 66, 26, "SERVIDOR ZABBIX (Kali + Docker)", [
    "eth1  10.7.42.10/25  cliente DHCP",
    "Zabbix 7.0 LTS + PostgreSQL 16",
    "web solo en 127.0.0.1:8080",
    "plantilla: Cisco IOS by SNMP",
    "comunidad en macro secreta",
    "NET-ZABBIX = Cloud1 (VMnet2)"], C_ZBX, fs=8.8, tfs=11.5)

link((85, 83.5), (85, 73), "e0/0 ↔ e0/0 (trunk)", off=(12, 0))
link((85, 51.5), (85, 38.5), "e0/1 ↔ NET-ZABBIX", off=(11, 0))

flow((51.5, 30), (56.5, 96), C_SNMP, rad=-0.35)
flow((51.5, 24), (56.5, 60), C_SNMP, rad=-0.3, lw=2.0)
ax.text(17, 66, "SNMP (UDP 161)\nGET / GETBULK cada minuto\ninterfaces · CPU · memoria\nuptime · hardware",
        ha="center", fontsize=9.2, color=C_SNMP, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_SNMP, lw=1), zorder=5)

flow((113.5, 92), (118.5, 30), C_DHCP, rad=-0.35)
ax.text(152, 66, "DHCP\nR1 entrega 10.7.42.10\n(reserva por client-id\n01 + MAC del Kali)",
        ha="center", fontsize=9.2, color=C_DHCP, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_DHCP, lw=1), zorder=5)

ax.add_patch(FancyBboxPatch((2, 0.3), 166, 7.2, boxstyle="round,pad=0.4,rounding_size=1.5",
                            linewidth=1.2, edgecolor=C_MG, facecolor="#f9fafb", zorder=1))
ax.text(4.5, 5.2, "Seguridad SNMP:", fontsize=9.6, fontweight="bold", color=C_ZBX, va="center")
ax.text(32, 5.2, "comunidad propia (no 'public') · solo lectura (RO) · ACL: solo 10.7.42.10 consulta, el resto se descarta y se registra",
        fontsize=9.0, color=INK, va="center")
ax.text(32, 2.4, "sin HTTP ni VTY en los equipos · la comunidad no aparece en Zabbix (Secret text) ni en el repositorio",
        fontsize=9.0, color=INK, va="center")

plt.savefig("topologia_a3_snmp_zabbix.png", bbox_inches="tight", facecolor="white")
print("ok")
