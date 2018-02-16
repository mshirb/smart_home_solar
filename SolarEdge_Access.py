import requests

url_head = 'https://monitoringapi.solaredge.com/'

# test_data = '{siteCurrentPowerFlow: {updateRefreshRate: 3, unit: kW, connections: [{from: LOAD, to: Grid}, {from: PV, to: Load}], GRID: {status: Active, currentPower: 0.66}, LOAD: {status: Active, currentPower: 1.96}, PV: {status: Active, currentPower: 2.62}}}'


def url_builder(classSE, location, param):
    url = url_head + location + '.json?api_key=' + classSE.getapikey()
    for para in param:
        url += '&' + para
    return url


class SolarEdge:

    def __init__(self, APIKEY):
        self.api_key = APIKEY

    def getapikey(self):
        return self.api_key


    def getcurrentpowerflow(self, Site_Id):
        """
        Get the current Power Flow from Solar Edge Monitoring of system at Site ID
        Is an instaneous read
        :param Site_Id: the id of site supplied by SolarEdge
        :return: Tuple: Direction (Boolean), Unit (String), PV Power, Load Power, Grid Power
        """
        # build url and get json reply
        location = 'site/' + Site_Id + '/currentPowerFlow'
        url = url_builder(self, location, [])
        print(url)
        r = requests.get(url)
        if(r.status_code != 200):
            raise Exception('Web Request Failed')
        jreply = r.json()['siteCurrentPowerFlow']
        print(jreply)

        # seperate data
        connections = jreply['connections'][1]
        grid = jreply['GRID']
        load = jreply['LOAD']
        pv = jreply['PV']
        direction = False
        if(str(connections['from']).lower() == 'load'):
            direction = True
        # print(str(connections['from']) + '->' + str(connections['to']))
        units = jreply['unit']
        PVPower = pv['currentPower']
        LoadPower = load['currentPower']
        GridPower = grid['currentPower']
        returnval = direction, units, PVPower, LoadPower, GridPower
        print(returnval)
        return returnval


