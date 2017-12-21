DB name: soapapp
TABLES: vsats (
                t_id INT(15) PRIMARY KEY,   --> Terminal ID
                t_name VARCHAR(20),         --> Terminal name
                bh_vlan INT(4),             --> Backhauling VLAN
                bh_name VARCHAR(30),        --> Backhaul name
                bh_src VARCHAR (20),        --> Backhaul source (PROFILE or VR)
                bh_src_ip VARCHAR(20),      --> Backhaul source IP
                is_route VARCHAR(3)         --> Is there static route?
                t_rt_ip VARCHAR(20),        --> Route
                t_rt_msk VARCHAR(20),       --> Route mask
                t_rt_gw VARCHAR(20)         --> Route GW
                is_service VARCHAR(3)       --> Currently service is enabled?

              );


CREATE TABLE vsats (
                t_id INT(15) PRIMARY KEY,
                t_name VARCHAR(20),
                bh_vlan INT(4),
                bh_name VARCHAR(30),
                bh_src VARCHAR (20),
                bh_src_ip VARCHAR(20),
                is_route VARCHAR(3),
                t_rt_ip VARCHAR(20),
                t_rt_msk VARCHAR(20),
                t_rt_gw VARCHAR(20),
                is_service VARCHAR(3)

              );
