    import pymysql
    conn = pymysql.connect("localhost","root","$SatCom$","soapapp")
    cur = conn.cursor(pymysql.cursors.DictCursor)
    for i in range(1,500):
        t_name = str(i)+'VSAT'
        bh_vlan = '24'
        bh_name = str(i)+'BH'
        bh_src = 'PROFILE'
        bh_src_ip = '0.0.0.0'
        is_route = 'YES'
        t_rt_ip = '8.8.8.8'
        t_rt_msk = '255.255.255.255'
        t_rt_gw = '10.0.0.1'
        is_service = 'YES'
        result = cur.execute("INSERT INTO vsats(t_id, t_name, bh_vlan, bh_name, bh_src, bh_src_ip, is_route, t_rt_ip, t_rt_msk, t_rt_gw, is_service) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i, t_name, bh_vlan, bh_name, bh_src, bh_src_ip, is_route, t_rt_ip, t_rt_msk, t_rt_gw, is_service))
    conn.commit()
    cur.close()
