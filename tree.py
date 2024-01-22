def ccaa_names(elements):
    cacp_qty = int(elements['CACP'][1])
    cacv_qty = int(elements['CACV'][1])
    ccaa = ccaa_type(elements)

    if ccaa == 'CACP':
        for name in range(cacp_qty):
            print(f"CA{name} - PEATONAL")
    elif ccaa == 'CACV':
        for name in range(cacv_qty):
            print(f"CA{name} - VEHICULOS")
    elif ccaa == 'CCAA':
        pass
