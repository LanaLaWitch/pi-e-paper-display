def SetupWiFi():

    from network_connect import TestConnectToWiFi
    from wifi_config_handler import SaveWiFiConfig

    print('Beginning Wi-Fi setup')

    network_ssid = _GetNetworkSSID()
    if network_ssid == None:
        return

    psswrd = _GetPassword()

    print(f'Network name: {network_ssid}')
    print(f'Password: {psswrd}')

    connection_attempt_result = TestConnectToWiFi(network_ssid, psswrd)

    if not connection_attempt_result:
        print('Could not connect to network. Exiting...')
        return
    
    print('Tested connection successfully. Saving credentials for future use')
    SaveWiFiConfig(network_ssid, psswrd)
    print('Credentials Saved')

def _GetNetworkSSID():

    from network_connect import ScanForNetworks

    print('Scanning for possible networks...')

    found_networks = ScanForNetworks()
    if len(found_networks) <= 0:
        print('Could not find any networks to connect to. Exiting...')
        return

    valid_ssid_input = False

    while not valid_ssid_input:
        ssid = input('Enter network name or index: ')

        try:
            ssid_as_int = int(ssid)
            if ssid_as_int >= 0 and ssid_as_int < len(found_networks):
                network_name = found_networks[ssid_as_int][0].decode('utf-8')
                valid_ssid_input = True # As redundancy
                break
        except:
            pass

        for found_network in found_networks:
            if found_network[0].decode('utf-8') == ssid:
                network_name = found_networks[ssid_as_int][0].decode('utf-8')
                valid_ssid_input = True # As redundancy
                break

        if not valid_ssid_input:
            print('Invalid network selection, please try again.')

    return network_name


def _GetPassword():
    
    psswrd = input('Enter network password: ')

    return psswrd

SetupWiFi()