import sys
sys.path.append('/home/laboratorio/Programs/Odoo')

import odoo

from rich.tree import Tree
from rich import print as rprint
from rich.console import Console
console = Console()

#Input manual del ID del sistema para el que se va a crear el arbol
#id = int(console.input("[bold][[cyan]+[/cyan]] Introduce el ID de sistema: [/bold]"))

id = "IN10145"
id_sys = 4462

elements = odoo.installation(id)

cam_ptree = Tree("[bold][cyan]Camaras[/cyan][/bold]")
nvr_ptree = Tree("[bold][cyan]NVR[/cyan][/bold]")
caa_ptree = Tree("[bold][cyan]CCAA[/cyan][/bold]")
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

def cacp_tree(elements):
    cacp_qty = int(elements['CACP'][1])
    cacp_ip_final = cacp_qty +125 -1
    cacp_ip_inicio = 125
    cam_ip_final = cacp_ip_final + 40
    cam_ip_inicio = 165

    cacp_list = [125]
    cam_list = [165]

    if cacp_ip_final == 125:
        return(cacp_list)
    elif cacp_ip_final > 125 and cacp_ip_final < 164:
        while cacp_ip_inicio < cacp_ip_final: 
            cacp_ip_inicio += 1
            cacp_list.append(cacp_ip_inicio)
        return(cacp_list)
    elif cacp_ip_final == 164:
        while cacp_ip_inicio < cacp_ip_final: 
            cacp_ip_inicio += 1
            cacp_list.append(cacp_ip_inicio)
        return(cacp_list)
    else:
        return("Cantidad no soportada")

def cacv_tree(elements):
    cacv_qty = int(elements['CACV'][1])
    cacv_ip_final = cacv_qty +125 -1
    cacv_ip_inicio = 125

    cacv_list = [125]

    if cacv_ip_final == 125:
        return(cacv_list)
    elif cacv_ip_final > 125 and cacv_ip_final < 164:
        while cacv_ip_inicio < cacv_ip_final: 
            cacv_ip_inicio += 1
            cacv_list.append(cacv_ip_inicio)
        return(cacv_list)
    elif cacv_ip_final == 164:
        while cacv_ip_inicio < cacv_ip_final: 
            cacv_ip_inicio += 1
            cacv_list.append(cacv_ip_inicio)
        return(cacv_list)
    else:
        return("Cantidad no soportada")

def cavp_tree(cacp_qty, cacv_qty):
    cacp_qty = int(elements['CACP'][1])
    cacv_qty = int(elements['CACV'][1])
    cacp_ip_final = cacp_qty +125 -1
    cacv_ip_final = cacp_ip_final + cacv_qty 

    cacp_list = cacp_tree(cacp_qty)
    cacv_list = []

    cacv_ip_start = int(cacp_list[-1])
    while cacv_ip_start < cacv_ip_final:
        cacv_ip_start += 1
        cacv_list.append(cacv_ip_start)
    return(cacp_list, cacv_list)

def ccaa_type(elements):
    cacp_qty = int(elements['CACP'][1])
    cacv_qty = int(elements['CACV'][1])

    if cacp_qty >= 1 and cacv_qty == 0:
        return('CACP')
        #return(cacp_tree(cacp_qty))
    elif cacv_qty >= 1 and cacp_qty == 0:
        return('CACV')
        #return(cacv_tree(cacv_qty))
    elif cacp_qty >= 1 and cacv_qty >= 1:
        return('CCAA')
        #return(cavp_tree(cacp_qty, cacv_qty))
    else:
        return('ERROR CCAA')
        #return(f"CACP:{cacp_qty}, CACV:{cacv_qty}")


def print_tree():

    ip = odoo.network(id_sys)
    net_1 = ip[0]
    net_2 = ip[1]
    net_3 = ip[2]

    nvr = nvr_tree(elements)
    nvr_qty = len(nvr)

    cam = camera_tree(elements)
    cam_qty = len(cam)
    
    ccaa = ccaa_type(elements)
    cacp_qty = int(elements['CACP'][1])
    cacv_qty = int(elements['CACV'][1])
    
    #---
    #NVR
    #---
    for n in range(nvr_qty):
        nvr_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(nvr[n]))

    #-------
    #Cámaras
    #-------
    for c in range(cam_qty):
        cam_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(cam[c]))
    
    #----
    #CCAA
    #----
    if ccaa == 'CACP':
        cacp = cacp_tree(elements)
        cacp_qty = len(cacp)
        for cp in range(cacp_qty):
            cacp_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(cacp[cp]))
    elif ccaa == 'CACV':
        cacv = cacv_tree(elements)
        cacv_qty = len(cacv)
        for cv in range(cacv_qty):
            cacv_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(cacv[cv]))
    elif ccaa == 'CCAA':
        ca = cavp_tree(cacp_qty, cacv_qty)
        cacp = ca[0]
        cacp_qty = len(ca[0])
        cacv = ca[1]
        cacv_qty = len(ca[1])
        for cp in range(cacp_qty):
            cacp_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(cacp[cp]))
        for cv in range(cacv_qty):
            cacv_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(cacv[cv]))
    else:
        return('No hay controladoras')


print_tree()
rprint(nvr_ptree)
rprint(cam_ptree)
rprint(cacp_ptree)
rprint(cacv_ptree)