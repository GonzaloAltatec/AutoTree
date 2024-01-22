import sys
sys.path.append('/home/laboratorio/Programs/Odoo')

import odoo

from rich.tree import Tree
from rich import print as rprint
from rich.console import Console
from elements import CA
console = Console()

#Input manual del ID del sistema para el que se va a crear el arbol
#id = int(console.input("[bold][[cyan]+[/cyan]] Introduce el ID de sistema: [/bold]"))

#-----------------
#ID's para Testing
#-----------------

id = "IN10203"
#id_sys = 4492

# x3CP x1CV
#id = "IN10145"
#id_sys = 4462

# x2CP
#id = "IN10158"
#id_sys = 4470

# x1CP
#id = "IN10133"
#id_sys = 4456

elements = odoo.installation(id)
cacp_qty = int(elements['CACP'][1])
cacv_qty = int(elements['CACV'][1])

cam_ptree = Tree("[bold][cyan]Camaras[/cyan][/bold]")
nvr_ptree = Tree("[bold][cyan]NVR[/cyan][/bold]")
cacp_ptree = Tree("[bold][cyan]CACP[/cyan][/bold]")
cacv_ptree = Tree("[bold][cyan]CACV[/cyan][/bold]")


def nvr_tree(elements):
    nvr_qty = int(elements["Nvr"][1])
    nvr_ip_final = nvr_qty + 10

    nvr_list = [11]
    nvr_ip_inicio = 11

    if nvr_ip_final == 11:
        return(nvr_list)
    elif nvr_ip_final > 11 and nvr_ip_final < 15:
        while nvr_ip_inicio < nvr_ip_final: 
            nvr_ip_inicio += 1
            nvr_list.append(nvr_ip_inicio)
        return(nvr_list)
    elif nvr_ip_final == 15:
        while nvr_ip_inicio < nvr_ip_final: 
            nvr_ip_inicio += 1
            nvr_list.append(nvr_ip_inicio)
        return(nvr_list)
    else:
        return("Cantidad no soportada")

def camera_tree(elements):
    cam_qty = int(elements["Cameras"][1])
    cam_ip_final = cam_qty + 16 -1

    cam_list = [16]
    cam_ip_inicio = 16

    if cam_ip_final == 16:
        return(cam_list)
    elif cam_ip_final > 16 and cam_ip_final < 120:
        while cam_ip_inicio < cam_ip_final: 
            cam_ip_inicio += 1
            cam_list.append(cam_ip_inicio)
        return(cam_list)
    elif cam_ip_final == 120:
        while cam_ip_inicio < cam_ip_final: 
            cam_ip_inicio += 1
            cam_list.append(cam_ip_inicio)
        return(cam_list)
    else:
        return("Cantidad no soportada")

def ccaa_type(elements):
    cacp_qty = int(elements['CACP'][1])
    cacv_qty = int(elements['CACV'][1])

    if cacp_qty >= 1 and cacv_qty == 0:
        return('CACP')
    elif cacv_qty >= 1 and cacp_qty == 0:
        return('CACV')
    elif cacp_qty >= 1 and cacv_qty >= 1:
        return('CCAA')
    else:
        return('ERROR CCAA')
        
def ccaa_names(cacp_qty, cacv_qty):
    ccaa = ccaa_type(elements)
    start_count = 1
    name_list = []

    if ccaa == 'CACP':
        cacp_qty += 1
        for name in range(1, cacp_qty):
            name_list.append(f"CA{name} - PEATONAL")
        return(name_list)
    elif ccaa == 'CACV':
        cacv_qty += 1
        for name in range(1, cacv_qty):
            name_list.append(f"CA{name} - VEHICULOS")
        return(name_list)
    elif ccaa == 'CCAA':
        ccaa_final = cacp_qty + cacv_qty +1
        while start_count <= cacp_qty:
            name_list.append(f"CA{start_count} - PEATONAL")
            start_count += 1
        while start_count < ccaa_final:
            name_list.append(f"CA{start_count} - VEHICULOS")
            start_count += 1
        return(name_list)

def ccaa_ip(cacp_qty, cacv_qty):    
    ccaa_total = cacp_qty + cacv_qty    
    ip_start = 125
    ip_final = ccaa_total +125 -1
    ip_list = [125]

    while ip_final > ip_list[-1]:
        ip_start += 1
        ip_list.append(ip_start)
    return(ip_list)

def vca_ip(cacp_qty, cacv_qty):    
    ccaa_total = cacp_qty + cacv_qty    
    ip_start = 165
    ip_final = ccaa_total +165 -1
    ip_list = [165]

    while ip_final > ip_list[-1]:
        ip_start += 1
        ip_list.append(ip_start)
    return(ip_list)

def esp_ip(cacp_qty, cacv_qty):    
    ccaa_total = cacp_qty + cacv_qty    
    ip_start = 205
    ip_final = ccaa_total +205 -1
    ip_list = [205]

    while ip_final > ip_list[-1]:
        ip_start += 1
        ip_list.append(ip_start)
    return(ip_list)

def dictionaries(cacp_qty, cacv_qty):
    total = cacp_qty + cacv_qty
    name = ccaa_names(cacp_qty, cacv_qty)
    ip = ccaa_ip(cacp_qty, cacv_qty)
    vca = vca_ip(cacp_qty, cacv_qty)
    esp = esp_ip(cacp_qty, cacv_qty)

    ca_dict = {}

    for x in range(total):
        ca = CA(name[x], ip[x], vca[x], esp[x])
        ca_values = ca.dic()
        ca_dict[f'CA{x+1}'] = ca_values
    return(ca_dict)

def print_tree():

    ip = odoo.network(id)
    net_1 = ip[0]
    net_2 = ip[1]
    net_3 = ip[2]

    nvr = nvr_tree(elements)
    nvr_qty = len(nvr)

    cam = camera_tree(elements)
    cam_qty = len(cam)
    
    ccaa = dictionaries(cacp_qty, cacv_qty)
    total_ca = cacp_qty + cacv_qty

    #---
    #NVR
    #---
    for n in range(nvr_qty):
        nvr_ptree.add(f"[bold][green]+[/green][/bold] NVR{n+1}: " + net_1 + "." + net_2 + "." + net_3 + "." + str(nvr[n]))

    #-------
    #Cámaras
    #-------
    cam_count = 0
    cam_num = 1
    nvr_num = 1
    while cam_count < cam_qty:
    #for c in range(cam_qty):
        cam_ptree.add(f"[bold][green]+[/green][/bold] C{cam_num}N{nvr_num}: " + net_1 + "." + net_2 + "." + net_3 + "." + str(cam[cam_count]))
        cam_num += 1
        cam_count += 1
        if cam_count == 20:
            cam_num = 1
            nvr_num += 1
        if cam_count == 40:
            nvr_num += 1
        if cam_count == 60:
            nvr_num += 1
    #----
    #CCAA
    #----
 
    type_list = []
    ca_count = 0

    for ca in range(total_ca):
        name = ccaa[f'CA{ca+1}']['Nombre']
        position = name.find('- PEATONAL')
        type_list.append(position)
        if position != -1:
            cacp_tree = cacp_ptree.add("[bold][green]+[/green][/bold] " + str(ccaa[f'CA{ca+1}']['Nombre']))
            cacp_tree.add("IP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(ccaa[f'CA{ca+1}']['IP']))
            cacp_tree.add("VCA IP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(ccaa[f'CA{ca+1}']['VCA IP']))
            cacp_tree.add("ESP IP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(ccaa[f'CA{ca+1}']['ESP IP']))
            ca_count += 1
        else:
            cacv_tree = cacv_ptree.add("[bold][green]+[/green][/bold] " + str(ccaa[f'CA{ca_count+1}']['Nombre']))
            cacv_tree.add("IP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(ccaa[f'CA{ca_count+1}']['IP']))
            cacv_tree.add("VCA IP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(ccaa[f'CA{ca_count+1}']['VCA IP']))
            cacv_tree.add("ESP IP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(ccaa[f'CA{ca_count+1}']['ESP IP']))

    
print(print_tree())
rprint(nvr_ptree)
rprint(cam_ptree)
rprint(cacp_ptree)
rprint(cacv_ptree)