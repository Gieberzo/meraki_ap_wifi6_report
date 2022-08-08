import meraki
import json

capabilities = {}
dashboard = meraki.DashboardAPI()

for org in dashboard.organizations.getOrganizations():
    capabilities[org['name']] = {}
    try:
        for network in dashboard.organizations.getOrganizationNetworks(org['id']):
            capabilities[org['name']][network['name']] = {}
            capabilities[org['name']][network['name']]['wirelessClients'] = 0
            capabilities[org['name']][network['name']]['802.11axClients'] = 0
            for client in dashboard.networks.getNetworkClients(network['id']):
                if "Wireless" in client['recentDeviceConnection']:
                    capabilities[org['name']][network['name']]['wirelessClients'] += 1
                    if '802.11ax' in dashboard.networks.getNetworkClient(network['id'], client['id'])['wirelessCapabilities']:
                        capabilities[org['name']][network['name']]['802.11axClients'] += 1
            if capabilities[org['name']][network['name']]['wirelessClients'] > 0:
                capabilities[org['name']][network['name']]['percentage'] = (capabilities[org['name']][network['name']]['802.11axClients']/capabilities[org['name']][network['name']]['wirelessClients']*100)
    except Exception as e: 
        print(e)
        pass

json_object = json.dumps(capabilities, indent = 4)
print(json_object)