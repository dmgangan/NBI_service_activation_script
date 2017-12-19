DB name: soapapp
TABLES: vsats (
                t_id INT(15) PRIMARY KEY,   --> Terminal ID
                t_name VARCHAR(20),         --> Terminal name
                bh_vlan INT(4),             --> Backhauling VLAN
                bh_name VARCHAR(30),        --> Backhaul name
                bh_src VARCHAR (20),        --> Backhaul source (PROFILE or VR)
                bh_src_ip VARCHAR(20),      --> Backhaul source IP
                t_rt_ip VARCHAR(20),        --> Route
                t_rt_msk VARCHAR(20),       --> Route mask
                t_rt_gw VARCHAR(20)         --> Route GW
              );
