#Backup printeo de arbol
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
        ca = cacp_tree(elements)
        cacp = ca[0]
        cacp_qty = len(cacp)
        cam = ca[1]
        esp = ca[2]
        for cp in range(cacp_qty):
            cacp_ptree.add("[+]CA: " + net_1 + "." + net_2 + "." + net_3 + "." + str(cacp[cp]))
            cacp_ptree.add("  -VCA: " + net_1 + "." + net_2 + "." + net_3 + "." + str(cam[cp]))
            cacp_ptree.add("  -ESP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(esp[cp]))
    elif ccaa == 'CACV':
        ca = cacv_tree(elements)
        cacv = ca[0]
        cacv_qty = len(cacv)
        cam = ca[1]
        esp = ca[2]
        for cv in range(cacv_qty):
            cacv_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(cacv[cv]))
            cacv_ptree.add("  -VCA: " + net_1 + "." + net_2 + "." + net_3 + "." + str(cam[cv]))
            cacv_ptree.add("  -ESP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(esp[cv]))

    elif ccaa == 'CCAA':
        ca = cavp_tree(cacp_qty, cacv_qty)
        cacp = ca[0][0]
        cacp_cam = ca[0][1]
        cacp_esp = ca[0][2]
        cacp_qty = len(cacp)
        cacv = ca[1][0]
        cacv_qty = len(cacv[0])
        for cp in range(cacp_qty):
            cacp_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(cacp[cp]))
            cacp_ptree.add("  -VCA: " + net_1 + "." + net_2 + "." + net_3 + "." + str(cacp_cam[cp]))
            cacp_ptree.add("  -ESP: " + net_1 + "." + net_2 + "." + net_3 + "." + str(cacp_esp[cp]))

        for cv in range(cacv_qty):
            cacv_ptree.add(net_1 + "." + net_2 + "." + net_3 + "." + str(cacv[cv]))
    else:
        return('No hay controladoras')

#Backup  creación de arboles CCAA
def cacp_tree(elements):
    cacp_qty = int(elements['CACP'][1])
    cacp_ip_final = cacp_qty +125 -1
    cacp_ip_inicio = 125
    cam_ip_inicio = 165
    esp_ip_inicio = 205

    cacp_list = [125]
    cam_list = [165]
    esp_list = [205]

    if cacp_ip_final == 125:
        return(cacp_list, cam_list, esp_list)
    elif cacp_ip_final > 125 and cacp_ip_final < 164:
        while cacp_ip_inicio < cacp_ip_final: 
            cacp_ip_inicio += 1
            cam_ip_inicio += 1
            esp_ip_inicio += 1
            esp_list.append(esp_ip_inicio)
            cam_list.append(cam_ip_inicio)
            cacp_list.append(cacp_ip_inicio)
        return(cacp_list, cam_list, esp_list)
    elif cacp_ip_final == 164:
        while cacp_ip_inicio < cacp_ip_final: 
            cacp_ip_inicio += 1
            cam_ip_inicio += 1
            esp_ip_inicio += 1
            cam_list.append(cam_ip_inicio)
            cacp_list.append(cacp_ip_inicio)
            esp_list.append(esp_ip_inicio)
        return(cacp_list, cam_list, esp_list)
    else:
        return("Cantidad no soportada")

def cacv_tree(elements):
    cacv_qty = int(elements['CACV'][1])
    cacv_ip_final = cacv_qty +125 -1
    cacv_ip_inicio = 125
    cam_ip_inicio = 165
    esp_ip_inicio = 205

    cacv_list = [125]
    cam_list = [165]
    esp_list = [205]

    if cacv_ip_final == 125:
        return(cacv_list, cam_list, esp_list)
    elif cacv_ip_final > 125 and cacv_ip_final < 164:
        while cacv_ip_inicio < cacv_ip_final: 
            cacv_ip_inicio += 1
            cam_ip_inicio += 1
            esp_ip_inicio += 1
            cacv_list.append(cacv_ip_inicio)
            cam_list.append(cam_ip_inicio)
            esp_list.append(esp_ip_inicio)
        return(cacv_list, cam_list, esp_list)
    elif cacv_ip_final == 164:
        while cacv_ip_inicio < cacv_ip_final: 
            cacv_ip_inicio += 1
            cam_ip_inicio += 1
            esp_ip_inicio += 1
            cacv_list.append(cacv_ip_inicio)
            cam_list.append(cam_ip_inicio)
            esp_list.append(esp_ip_inicio)
        return(cacv_list, cam_list, esp_list)
    else:
        return("Cantidad no soportada")

def cavp_tree(cacp_qty, cacv_qty):
    cacp_qty = int(elements['CACP'][1])
    cacv_qty = int(elements['CACV'][1])
    cacp_ip_final = cacp_qty +125 -1
    cacv_ip_final = cacp_ip_final + cacv_qty 


    cacp_list = cacp_tree(elements)
    cacp = cacp_list[0]
    cacp_cam = cacp_list[1]
    cacp_esp = cacp_list[2]
    cacv_list = []
    cacv_cam_list = cacv_list + []

    cacv_ip_start = int(cacp[-1])
    cacv_ip_start_list = []
    cacv_cam_ip_start = int(cacp_cam[-1])
    cacv_cam_list = []
    cacv_esp_ip_start = int(cacp_esp[-1])

    while cacv_ip_start < cacv_ip_final:
        cacv_ip_start += 1
        cacv_cam_ip_start += 1
        cacv_ip_start_list.append(cacv_ip_start)
        cacv_cam_list.append(cacv_cam_ip_start)
    cacv_list.append(cacv_ip_start_list)
    cacv_list.append(cacv_cam_list)
    return(cacp_list, cacv_list)

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
