def setup_wifi():

    from network.wifi_connection_handler import test_connect_to_wifi
    from network.wifi_config_handler import save_wifi_config

    print('Beginning Wi-Fi setup')

    network_ssid = _get_network_ssid()
    if network_ssid == None:
        return

    psswrd = _get_password()

    print(f'Network name: {network_ssid}')
    print(f'Password: {psswrd}')

    connection_attempt_result = test_connect_to_wifi(network_ssid, psswrd)

    if not connection_attempt_result:
        print('Could not connect to network. Exiting...')
        return
    
    print('Tested connection successfully. Saving credentials for future use')
    save_wifi_config(network_ssid, psswrd)
    print('Credentials Saved')

def _get_network_ssid():

    from network.wifi_connection_handler import scan_for_networks

    print('Scanning for possible networks...')

    found_networks = scan_for_networks()
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
                network_name = ssid
                valid_ssid_input = True # As redundancy
                break

        if not valid_ssid_input:
            print('Invalid network selection, please try again.')

    return network_name


def _get_password():
    
    psswrd = input('Enter network password: ')

    return psswrd

setup_wifi()