# Erzeugt topologyData aus der (aus den GNS3-Screenshots abgelesenen) Topologie.
# Koordinaten im System von Screenshot 1; Screenshot 2 wird über Offset (-270, +1128) eingepasst.
import json, sys

S = 1.8  # Skalierung auf Kartenkoordinaten
SITE1_DY = -330
SITE2_DY = 40

def img2(x, y, dy=0):
    return (x - 270, y + 1128 + dy)

nodes = []  # (label, x, y, area, kind, role)
def N(label, xy, area, kind, role):
    nodes.append(dict(label=label, x=xy[0], y=xy[1], area=area, kind=kind, role=role))

# ---------- Standort 1 ----------
s1 = lambda x, y: (x, y + SITE1_DY)
N('LEAF-MGMT', s1(148, 96), 'site1', 'switch', 'Leaf-Switch (Management)')
N('LEAF-INT', s1(399, 96), 'site1', 'switch', 'Leaf-Switch (Intern)')
N('LEAF-DMZ', s1(634, 96), 'site1', 'switch', 'Leaf-Switch (DMZ)')
N('SPINE-1', s1(300, 247), 'site1', 'switch', 'Spine-Switch')
N('SPINE-2', s1(512, 247), 'site1', 'switch', 'Spine-Switch')
N('BORDER-1', s1(300, 416), 'site1', 'switch', 'Border-Switch')
N('BORDER-2', s1(512, 416), 'site1', 'switch', 'Border-Switch')
N('FortiGate STD-1', s1(406, 500), 'site1', 'firewall', 'FortiGate Firewall')
# Services Standort 1 (Rocky Linux, auf ESXi) – oberhalb der Leafs
site1_services = {
 'LEAF-MGMT': [('Syslog-Server', 'rsyslog'), ('SNMP-Manager', 'Net-SNMP')],
 'LEAF-INT': [('NTP-Server', 'chrony'), ('DHCP-Server', 'ISC dhcpd'), ('DNS-Server', 'BIND9'), ('File-Server', 'Samba')],
 'LEAF-DMZ': [('Web-Server', 'nginx')],
}
leaf_pos1 = {'LEAF-MGMT': 148, 'LEAF-INT': 399, 'LEAF-DMZ': 634}
for leaf, svcs in site1_services.items():
    for k, (lab, sw) in enumerate(svcs):
        N(lab, s1(leaf_pos1[leaf] + (k - (len(svcs) - 1) / 2) * 85, 96 - 120), 'site1', 'server', lab)
        nodes[-1].update(env='ESXi', os='Rocky Linux', sw=sw)

# ---------- ISP1 ----------
isp1 = {
 'PE-CUST01-ISP1': (409, 522, 'PE-Router (Kundenanbindung)'),
 'P12-ISP1': (602, 628, 'P-Router'), 'RR-01-ISP1': (912, 592, 'Route Reflector'),
 'P8-ISP1': (778, 660, 'P-Router'), 'P14-ISP1': (454, 658, 'P-Router'),
 'P9-ISP1': (544, 704, 'P-Router'), 'P5-ISP1': (636, 760, 'P-Router'),
 'P4-ISP1': (888, 756, 'P-Router'), 'PE-IAS1-ISP1': (1125, 707, 'PE-Router (ISP-Interconnect)'),
 'P1-ISP1': (975, 802, 'P-Router'), 'P3-ISP1': (814, 838, 'P-Router'),
 'P15-ISP1': (454, 838, 'P-Router'), 'P2-ISP1': (976, 866, 'P-Router'),
 'P6-ISP1': (630, 896, 'P-Router'), 'P7-ISP1': (892, 912, 'P-Router'),
 'PE-IAS2-ISP1': (1125, 980, 'PE-Router (ISP-Interconnect)'),
 'P10-ISP1': (544, 974, 'P-Router'), 'P11-ISP1': (784, 998, 'P-Router'),
 'P16-ISP1': (454, 1018, 'P-Router'), 'P13-ISP1': (598, 1040, 'P-Router'),
 'RR-02-ISP1': (902, 1072, 'Route Reflector'),
 'PE-CUST02-ISP1': (378, 1163, 'PE-Router (Kundenanbindung)'),
}
isp2 = {
 'PE-IAS1-ISP2': (1308, 710, 'PE-Router (ISP-Interconnect)'),
 'PE-IAS2-ISP2': (1312, 982, 'PE-Router (ISP-Interconnect)'),
 'RR-01-ISP2': (1570, 590, 'Route Reflector'), 'P12-ISP2': (1826, 656, 'P-Router'),
 'P8-ISP2': (1684, 673, 'P-Router'), 'PE-CUST01-ISP2': (2026, 512, 'PE-Router (Kundenanbindung)'),
 'Breakout': (2187, 373, 'Internet-Breakout'), 'P14-ISP2': (1982, 688, 'P-Router'),
 'P4-ISP2': (1488, 755, 'P-Router'), 'P9-ISP2': (1896, 733, 'P-Router'),
 'P5-ISP2': (1806, 775, 'P-Router'), 'P1-ISP2': (1431, 817, 'P-Router'),
 'P3-ISP2': (1640, 842, 'P-Router'), 'P15-ISP2': (1982, 856, 'P-Router'),
 'P2-ISP2': (1418, 898, 'P-Router'), 'P7-ISP2': (1494, 920, 'P-Router'),
 'P6-ISP2': (1800, 926, 'P-Router'), 'P10-ISP2': (1892, 980, 'P-Router'),
 'P11-ISP2': (1664, 996, 'P-Router'), 'P16-ISP2': (1978, 997, 'P-Router'),
 'P13-ISP2': (1810, 1047, 'P-Router'), 'RR-02-ISP2': (1560, 1078, 'Route Reflector'),
 'PE-CUST02-ISP2': (2026, 1160, 'PE-Router (Kundenanbindung)'),
}
for name, (x, y, role) in isp1.items(): N(name, (x, y), 'isp', 'router', role)
for name, (x, y, role) in isp2.items(): N(name, (x, y), 'isp', 'router', role)

# ---------- Standort 2 ----------
s2 = lambda x, y: img2(x, y, SITE2_DY)
# Services pro Leaf (max. 2); Leaf-7 trägt die CML-Umgebung (Cloud) mit den SD-WAN-Komponenten
services = {
 1: [('Licensing Manager', 'server', 'Licensing Manager', 'ESXi'), ('Cluster Manager', 'server', 'Splunk Cluster Manager', 'ESXi')],
 2: [('Indexer-1', 'server', 'Splunk Indexer', 'ESXi'), ('Indexer-2', 'server', 'Splunk Indexer', 'ESXi')],
 3: [('Search Head-1', 'server', 'Splunk Search Head', 'ESXi'), ('Search Head-2', 'server', 'Splunk Search Head', 'ESXi')],
 4: [('Search Head-3', 'server', 'Splunk Search Head', 'ESXi')],
 5: [('TACACS+', 'server', 'TACACS+-Server', 'ESXi')],
 6: [('Ansible Control Node', 'server', 'Ansible Control Node', 'ESXi')],
 7: [('CML-Umgebung', 'cloud', 'CML-Umgebung (Cloud)', 'CML')],
}
cml_children = [('vBond', 'SD-WAN-Komponente'), ('vManage', 'SD-WAN-Komponente'), ('vSync', 'SD-WAN-Komponente')]
SP, GAP, X0 = 95, 30, 20
y_leaf = s2(0, 643)[1]; y_srv = s2(0, 772)[1]; y_cml = y_srv + 100
x = X0; leaf_x = {}; srv_pos = []
for i in range(1, 8):
    xs = []
    for svc in services[i]:
        xs.append(x); srv_pos.append((i, svc, x)); x += SP
    leaf_x[i] = sum(xs) / len(xs); x += GAP
old_center = sum(p[0] for p in [(334,0),(461,0),(601,0),(711,0),(829,0),(926,0),(1030,0)]) / 7 - 270
dx = sum(leaf_x.values()) / 7 - old_center
s2u = lambda px, py: (s2(px, py)[0] + dx, s2(px, py)[1])
N('FortiGate STD-2', s2u(720, 140), 'site2', 'firewall', 'FortiGate Firewall')
N('Border-Leaf-1', s2u(683, 232), 'site2', 'switch', 'Border-Leaf')
N('Border-Leaf-2', s2u(756, 232), 'site2', 'switch', 'Border-Leaf')
N('Spine-1', s2u(605, 382), 'site2', 'switch', 'Spine-Switch')
N('Spine-2', s2u(713, 380), 'site2', 'switch', 'Spine-Switch')
N('Spine-3', s2u(825, 377), 'site2', 'switch', 'Spine-Switch')
for i in range(1, 8): N(f'Leaf-{i}', (leaf_x[i], y_leaf), 'site2', 'switch', 'Leaf-Switch')
for i, (lab, kind, role, env), px in srv_pos:
    N(lab, (px, y_srv), 'site2', kind, role); nodes[-1]['env'] = env
cml_x = [p for p in srv_pos if p[1][0] == 'CML-Umgebung'][0][2]
for k, (lab, role) in enumerate(cml_children):
    N(lab, (cml_x + (k - 1) * SP, y_cml), 'site2', 'server', role); nodes[-1]['env'] = 'CML'

# ---------- Standort 3 ----------
s3 = lambda x, y: img2(x, y)
N('FortiGate STD-3', s3(1990, 210), 'site3', 'firewall', 'FortiGate Firewall')
N('EDGE1', s3(1869, 355), 'site3', 'router', 'Edge-Router')
N('EDGE2', s3(2110, 355), 'site3', 'router', 'Edge-Router')
N('DIST1', s3(1876, 502), 'site3', 'switch', 'Distribution-Switch')
N('DIST2', s3(2092, 502), 'site3', 'switch', 'Distribution-Switch')
for lab, x3 in [('SW-P1', 1714), ('SW-P2', 1894), ('SW-Q1', 2074), ('SW-Q2', 2254)]:
    N(lab, s3(x3, 657), 'site3', 'switch', 'Access-Switch')
N('ESXi-Host', s3(1989, 770), 'site3', 'server', 'ESXi-Host (Clients & Services)'); nodes[-1]['env'] = 'ESXi'
for k, (lab, kind, role) in enumerate([('Linux-Client-1', 'desktop', 'Linux-Client'), ('Linux-Client-2', 'desktop', 'Linux-Client'),
                                       ('Windows-Client', 'desktop', 'Windows-Client'), ('Linux-Server', 'server', 'Linux-Server')]):
    N(lab, s3(1989 + (k - 1.5) * 95, 872), 'site3', kind, role); nodes[-1]['env'] = 'ESXi'

# ---------- Links: (A, ifA, B, ifB) ----------
L = []
def l(a, ia, b, ib): L.append((a, ia, b, ib))

# Standort 1
for leaf, sp1, sp2 in [('LEAF-MGMT', 'Gi1/1', 'Gi1/1'), ('LEAF-INT', 'Gi1/2', 'Gi1/2'), ('LEAF-DMZ', 'Gi1/3', 'Gi1/3')]:
    l(leaf, 'Gi0/0', 'SPINE-1', sp1); l(leaf, 'Gi0/1', 'SPINE-2', sp2)
l('SPINE-1', 'Port-Channel', 'SPINE-2', 'Port-Channel')
l('SPINE-1', 'Gi0/1', 'BORDER-1', 'Gi0/1'); l('SPINE-1', 'Gi0/2', 'BORDER-2', 'Gi0/2')
l('SPINE-2', 'Gi0/2', 'BORDER-1', 'Gi0/2'); l('SPINE-2', 'Gi0/1', 'BORDER-2', 'Gi0/1')
l('BORDER-1', 'Port-Channel', 'BORDER-2', 'Port-Channel')
for leaf, svcs in site1_services.items():
    for lab, _ in svcs: l(leaf, '', lab, '')
l('BORDER-1', '', 'FortiGate STD-1', ''); l('BORDER-2', '', 'FortiGate STD-1', '')
l('FortiGate STD-1', '', 'PE-CUST01-ISP1', '')

# ISP1 (bei ISP2 identisch bis auf die Unterschiede unten)
core = [
 ('PE-CUST01', 'Gi1', 'P12', 'Gi1'), ('PE-CUST01', 'Gi2', 'P14', 'Gi1'),
 ('P12', 'Gi3', 'RR-01', 'Gi3'), ('P12', 'Gi2', 'P8', 'Gi3'), ('P12', 'Gi4', 'P5', 'Gi4'),
 ('RR-01', 'Gi1', 'P8', 'Gi1'), ('RR-01', 'Gi2', 'P4', 'Gi2'),
 ('P8', 'Gi4', 'P9', 'Gi4'), ('P8', 'Gi2', 'P4', 'Gi4'),
 ('P14', 'Gi2', 'P15', 'Gi3'), ('P9', 'Gi3', 'P15', 'Gi2'), ('P9', 'Gi1', 'P10', 'Gi1'),
 ('P9', 'Gi2', 'P6', 'Gi2'), ('P5', 'Gi2', 'P10', 'Gi2'), ('P15', 'Gi1', 'P10', 'Gi3'),
 ('P15', 'Gi4', 'P16', 'Gi2'), ('P16', 'Gi1', 'PE-CUST02', 'Gi1'),
 ('P5', 'Gi3', 'P4', 'Gi3'), ('P5', 'Gi1', 'P3', 'Gi3'),
 ('P4', 'Gi1', 'PE-IAS1', 'Gi3'), ('P1', 'Gi1', 'PE-IAS1', 'Gi4'),
 ('P1', 'Gi2', 'P3', 'Gi2'), ('P3', 'Gi1', 'P2', 'Gi2'), ('P3', 'Gi4', 'P6', 'Gi1'),
 ('P2', 'Gi1', 'PE-IAS2', 'Gi3'), ('P6', 'Gi3', 'P7', 'Gi3'),
 ('P7', 'Gi1', 'PE-IAS2', 'Gi4'), ('P7', 'Gi4', 'P11', 'Gi2'), ('P7', 'Gi2', 'RR-02', 'Gi2'),
 ('P11', 'Gi3', 'P13', 'Gi2'), ('P11', 'Gi1', 'RR-02', 'Gi1'), ('P13', 'Gi3', 'RR-02', 'Gi3'),
 ('P13', 'Gi1', 'PE-CUST02', 'Gi2'), ('P10', 'Gi4', 'P11', 'Gi4'),
]
for isp in ('ISP1', 'ISP2'):
    for a, ia, b, ib in core: l(f'{a}-{isp}', ia, f'{b}-{isp}', ib)
l('P6-ISP1', 'Gi4', 'P13-ISP1', 'Gi4')
l('PE-CUST01-ISP2', 'Gi3', 'Breakout', 'Gi0/0')
l('PE-IAS1-ISP1', 'Gi1', 'PE-IAS1-ISP2', 'Gi1')
l('PE-IAS2-ISP1', 'Gi1', 'PE-IAS2-ISP2', 'Gi1')

# Standort 2
l('PE-CUST02-ISP1', '', 'FortiGate STD-2', '')
l('FortiGate STD-2', '', 'Border-Leaf-1', ''); l('FortiGate STD-2', '', 'Border-Leaf-2', '')
for s in (1, 2, 3):
    l('Border-Leaf-1', f'Gi0/{s-1}', f'Spine-{s}', 'Gi3/3')
    l('Border-Leaf-2', f'Gi0/{s-1}', f'Spine-{s}', 'Gi3/2')
sp_ports = ['Gi0/0', 'Gi0/1', 'Gi0/2', 'Gi0/3', 'Gi1/0', 'Gi1/1', 'Gi1/2']
for s in (1, 2, 3):
    for i in range(1, 8):
        l(f'Spine-{s}', sp_ports[i-1], f'Leaf-{i}', f'Gi3/{s}')
for i in range(1, 8):
    for k, svc in enumerate(services[i]):
        l(f'Leaf-{i}', 'Gi0/0' if k == 0 else '', svc[0], '')
for lab, _ in cml_children: l('CML-Umgebung', '', lab, '')

# Standort 3
l('PE-CUST02-ISP2', '2/0', 'FortiGate STD-3', '')
l('FortiGate STD-3', '', 'EDGE1', '0/0'); l('FortiGate STD-3', '', 'EDGE2', '0/0')
l('EDGE1', '2/0', 'DIST1', '0/0'); l('EDGE1', '3/0', 'DIST2', '0/0')
l('EDGE2', '2/0', 'DIST1', '1/0'); l('EDGE2', '3/0', 'DIST2', '1/0')
l('DIST1', 'Port-Channel', 'DIST2', 'Port-Channel')
for k, sw in enumerate(['SW-P1', 'SW-P2', 'SW-Q1', 'SW-Q2']):
    l('DIST1', f'{4+k}/0', sw, '0/0'); l('DIST2', f'{4+k}/0', sw, '1/0')
    l(sw, '2/0', 'ESXi-Host', f'0/{k+1}')
for lab in ('Linux-Client-1', 'Linux-Client-2', 'Windows-Client', 'Linux-Server'): l('ESXi-Host', '', lab, '')

# ---------- Aufbereitung ----------
lab2id = {}
out_nodes = []
for i, n in enumerate(nodes):
    nid = f'n{i}'; lab2id[n['label']] = nid
    out_nodes.append(dict(id=nid, label=n['label'], x=round(n['x'] * S), y=round(n['y'] * S),
                          area=n['area'], kind=n['kind'], role=n['role'], **({'os': n['os'], 'sw': n['sw']} if n.get('os') else {}), env=n.get('env') or ('FortiGate (extern)' if n['kind'] == 'firewall' else 'GNS3')))
out_links = []
for a, ia, b, ib in L:
    assert a in lab2id and b in lab2id, (a, b)
    out_links.append(dict(s=lab2id[a], t=lab2id[b], si=ia, ti=ib))

# Doppelte Interfaces pro Gerät prüfen
seen = {}
for a, ia, b, ib in L:
    for dev, itf in ((a, ia), (b, ib)):
        if itf and itf != 'Port-Channel':
            k = (dev, itf); assert k not in seen, f'Interface doppelt: {k}'; seen[k] = 1

def bounds(area, pad=120, extra_bottom=60):
    xs = [n['x'] for n in out_nodes if n['area'] == area]
    ys = [n['y'] for n in out_nodes if n['area'] == area]
    x0, y0 = min(xs) - pad, min(ys) - pad
    return dict(x=x0, y=y0, w=max(xs) + pad - x0, h=max(ys) + pad + extra_bottom - y0)

B = {k: bounds(k) for k in ('site1', 'site2', 'site3', 'isp')}
allx = [n['x'] for n in out_nodes]; ally = [n['y'] for n in out_nodes]
M = 260
canvas = dict(minX=min(allx) - M, minY=min(ally) - M,
              width=max(allx) - min(allx) + 2 * M, height=max(ally) - min(ally) + 2 * M)

def sub(area, pred, pad=95):
    xs = [n['x'] for n in out_nodes if n['area'] == area and pred(n)]
    ys = [n['y'] for n in out_nodes if n['area'] == area and pred(n)]
    return dict(x=min(xs) - pad, y=min(ys) - pad, w=max(xs) - min(xs) + 2 * pad, h=max(ys) - min(ys) + 2 * pad + 40)

r1 = sub('isp', lambda n: n['label'].endswith('ISP1'))
r2 = sub('isp', lambda n: n['label'].endswith('ISP2') or n['label'] == 'Breakout')
ann = [
    dict(type='rect', x=r1['x'], y=r1['y'], w=r1['w'], h=r1['h'], color='#0297DE'),
    dict(type='rect', x=r2['x'], y=r2['y'], w=r2['w'], h=r2['h'], color='#FC734D'),
    dict(type='text', x=r1['x'] - 330, y=r1['y'] + r1['h'] // 2, text='ISP1', size=50),
    dict(type='text', x=r2['x'] + r2['w'] - 330, y=r2['y'] + r2['h'] - 60, text='ISP2', size=50),
    dict(type='text', x=B['site1']['x'] + B['site1']['w'] + 40, y=B['site1']['y'] + 130, text='Standort 1', size=50),
    dict(type='text', x=B['site2']['x'] + 50, y=B['site2']['y'] + 150, text='Standort 2', size=50),
    dict(type='text', x=B['site3']['x'] + B['site3']['w'] + 50, y=B['site3']['y'] + 150, text='Standort 3', size=50),
]

cnt = lambda a: sum(1 for n in out_nodes if n['area'] == a)
areas = {
 'all': dict(title='Gesamtansicht', count=len(out_nodes),
   text='Die vollständige GNS3-Gesamttopologie mit allen Geräten und Verbindungen. Die drei Standorte sind jeweils über eine FortiGate an die Provider-Netze ISP1 und ISP2 angebunden. Wähle einen Bereich oder klicke direkt auf ein Gerät.'),
 'site1': dict(title='Standort 1', count=cnt('site1'),
   text='Spine-Leaf-Struktur mit Leafs für Management, internes Netz und DMZ, zwei Spines und zwei Border-Switches; geroutet wird mit OSPFv2. An den Leafs hängen die Services auf Rocky Linux: NTP (chrony), Web (nginx), DHCP (ISC dhcpd), DNS (BIND9), File (Samba), Syslog (rsyslog) und SNMP-Manager (Net-SNMP). Die FortiGate sichert den Standort ab und bildet den Übergang zu ISP1 (PE-CUST01-ISP1).'),
 'site2': dict(title='Standort 2', count=cnt('site2'),
   text='Fabric mit zwei Border-Leafs, drei Spines und sieben Leafs. An den Leafs hängen die Services – Splunk (Licensing Manager, Cluster Manager, Indexer, Search Heads), TACACS+ und der Ansible Control Node – sowie eine CML-Umgebung mit vBond, vManage und vSync. Alle Server laufen auf ESXi. Die FortiGate verbindet die Fabric mit ISP1 (PE-CUST02-ISP1).'),
 'site3': dict(title='Standort 3', count=cnt('site3'),
   text='Campus-Netz mit FortiGate, zwei Edge-Routern, Distribution (DIST1/DIST2) und vier Access-Switches. Am ESXi-Host laufen zwei Linux-Clients, ein Windows-Client und ein Linux-Server. Die Anbindung erfolgt über ISP2 (PE-CUST02-ISP2).'),
 'isp': dict(title='ISP · ISP1 & ISP2', count=cnt('isp'),
   text='Zwei Provider-Netze mit P-Routern, je zwei Route Reflectors und PE-Routern für die Kundenanbindung. ISP1 und ISP2 sind über zwei PE-IAS-Paare miteinander verbunden, der Internet-Breakout erfolgt über ISP2.'),
}
for k in ('site1', 'site2', 'site3', 'isp'): areas[k]['bounds'] = B[k]
areas['all']['bounds'] = dict(minX=canvas['minX'], minY=canvas['minY'], width=canvas['width'], height=canvas['height'])

tx = [a['x'] + len(a['text']) * a['size'] * 2.2 * 0.62 for a in ann if a['type'] == 'text']
maxx = max(max(allx) + M, max(tx) + 80); minx = min(min(allx) - M, min(a['x'] for a in ann if a['type'] == 'text') - 80)
canvas.update(minX=round(minx), width=round(maxx - minx))
areas['all']['bounds'] = dict(minX=canvas['minX'], minY=canvas['minY'], width=canvas['width'], height=canvas['height'])
data = dict(canvas=canvas, nodes=out_nodes, links=out_links, annotations=ann, areas=areas)
json.dump(data, open(sys.argv[1], 'w'), ensure_ascii=False, separators=(',', ':'))
print('nodes', len(out_nodes), 'links', len(out_links), {k: v['count'] for k, v in areas.items()})
print('canvas', canvas); print(B)
