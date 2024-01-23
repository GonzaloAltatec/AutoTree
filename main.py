import sys
sys.path.append('/home/laboratorio/Programs/Odoo')
import odoo
from tree import OdooTree
from rich.tree import Tree as PTree
from rich import print as rprint
from rich.console import Console
from elements import CA
console = Console()

#Input manual del ID del sistema para el que se va a crear el arbol
#id = console.input("[bold][[cyan]+[/cyan]] Introduce el ID de sistema: [/bold]")

id = "IN10203"
tree = OdooTree(id)

#Arboles para outputs de consola
cctv_ptree = PTree("[bold][cyan]CCTV[/cyan][/bold]")
cacp_ptree = PTree("[bold][cyan]CACP[/cyan][/bold]")
cacv_ptree = PTree("[bold][cyan]CACV[/cyan][/bold]")

#Función que gestiona como se muestra el arbol
def print_tree():

    ip = odoo.network(id)
    net = str(ip[0] + "." + ip[1] + "." + ip[2] + ".")

    nvr = tree.nvr_tree()
    nvr_qty = len(nvr)

    cam = tree.camera_tree()
    cam_qty = len(cam)
    
    elements = odoo.installation(id)
    cacp_qty = int(elements['CACP'][1])
    cacv_qty = int(elements['CACV'][1])
    total_ca = cacp_qty + cacv_qty

    ccaa = tree.ccaa_dictionary()
    
    #----
    #CCTV
    #----
    cam_count = 0
    cam_num = 1
    nvr_num = 1
    cctv_tree = cctv_ptree.add(f"[bold][green]+[/green]NVR{nvr_num}:[/bold] {net}{str(nvr[0])}")
    while cam_count < cam_qty:
        cctv_tree.add(f'C{cam_num}N{nvr_num}: {net}{str(cam[cam_count])}')
        cam_count += 1
        cam_num += 1
        if cam_count == 20:
            cam_num = 1
            nvr_num += 1
            cctv_tree = cctv_ptree.add(f"[bold][green]+[/green]NVR{nvr_num}:[/bold] {net}{str(nvr[1])}")
        if cam_count == 40:
            cam_num = 1
            nvr_num += 1
            cctv_tree = cctv_ptree.add(f'[bold][green]+[/green]NVR{nvr_num}:[/bold] {net}{str(nvr[2])}')
        if cam_count == 60:
            cam_num = 1
            nvr_num += 1
            cctv_tree = cctv_ptree.add(f'[bold][green]+[/green]NVR{nvr_num}:[/bold] {net}{str(nvr[3])}')

    #----
    #CCAA
    #----

    for ca in range(total_ca):
        name = ccaa[f'CA{ca+1}']['Nombre']
        position = name.find('- PEATONAL')
        if position != -1:
            cacp_tree = cacp_ptree.add("[bold][green]+[/green][/bold] " + str(ccaa[f'CA{ca+1}']['Nombre']))
            cacp_tree.add("IP: " + net + str(ccaa[f'CA{ca+1}']['IP']))
            cacp_tree.add("VCA IP: " + net + str(ccaa[f'CA{ca+1}']['VCA IP']))
            cacp_tree.add("ESP IP: " + net + str(ccaa[f'CA{ca+1}']['ESP IP']))
        else:
            cacv_tree = cacv_ptree.add("[bold][green]+[/green][/bold] " + str(ccaa[f'CA{ca+1}']['Nombre']))
            cacv_tree.add("IP: " + net + str(ccaa[f'CA{ca+1}']['IP']))
            cacv_tree.add("VCA IP: " + net + str(ccaa[f'CA{ca+1}']['VCA IP']))
            cacv_tree.add("ESP IP: " + net + str(ccaa[f'CA{ca+1}']['ESP IP']))

#Outputs
print('')
print_tree()
rprint(cctv_ptree)
rprint(cacp_ptree)
rprint(cacv_ptree)