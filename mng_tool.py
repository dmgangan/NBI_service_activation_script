import json
import copy
BH_mod_data = {
    'cpeId': {
        'managedGroupId': '2',
        'subscriberId': '',
    },
	'vlanIdToUpdate':'',
    'backhauling': {
        'name': '',
        'cpeSideIPAddressSource': 'PROFILE',
    },}
term_data=json.load(open('terminals.json'))

changes={'activate':[],'deactivate':[]}
while 1:
	chose=input(' a:Add/modify\n d:Delete\n v:View\n s:Commit\n q:Exit\n:')
	if chose=='a':
		while 1: 
			t_id=input("Enter Termial ID: ")
			term_data[t_id]={}
			sla_name=input("Enter SLA name: ")
			term_data[t_id]['sla']=sla_name
			rtn_name=input("Enter RNT-Classidier name: ")
			term_data[t_id]['rtn']=rtn_name
			bh_name=input("Enter BH name: ")
			term_data[t_id]['bh_name']=bh_name
			bh_src=input("Enter BH source(VR,PROFILE): ")
			term_data[t_id]['bh_src']=bh_src
			v_id=input("Enter VLAN ID: ")
			term_data[t_id]['vlan_id']=v_id
			ip_route=input("Enter route for VLAN {}:".format(v_id))
			term_data[t_id]['ip_route']=ip_route
			ip_r_mask=input("Enter mask for route {}:".format(ip_route))
			term_data[t_id]['ip_mask']=ip_r_mask
			ip_r_gw=input("Enter DG for route {}:".format(ip_route))
			term_data[t_id]['ip_gw']=ip_r_gw
			term_data[t_id]['service']='1'
			print('-------------')
			if input('more (y/n)')==('y' or 'Y'):
				continue
			else: break
		with open('terminals.json', 'w') as outfile:
			json.dump(term_data, outfile)
			
	elif chose=='v':
		while 1:
			vmode=input('\n1:short 2:detail: ')
			if vmode=='1':
				print('{}|{:9}|{:10}\n------------+---------+------------'.format('Terminal ID ',' Service', ' BH Profile '))
				for key in term_data.keys():
					print ('   {:9}|   {}     |  {}'.format(key, term_data[key]['service'],term_data[key]['bh_name']))
			elif vmode=='2':
				term_id=input('Enter Terminal ID:')
				for i in term_data[term_id].items():
					print ('{:10}{}'.format(i[0],i[1]))
			elif vmode=='q': break
			
	elif chose=='s':
		print ('Not available for now')
		input('...')

	elif chose=='q':
		break
